import itertools
import logging
from abc import abstractproperty, ABCMeta

from sqlalchemy import event, inspect

from pynYNAB.schema import fromapi_conversion_functions_table, listfields, scalarfields

LOG = logging.getLogger(__name__)


def split_seq(iterable, size):
    it = iter(iterable)
    item = list(itertools.islice(it, size))
    while item:
        yield item
        item = list(itertools.islice(it, size))


class RootObjClient():

    def extra(self):
        return {}

    def opname(self):
        return ''

    def __init__(self, obj, client, cls):
        self.obj = obj
        self.cls = cls
        self.changed = cls()
        self.client = client
        self.connection = client.connection
        self.session = client.session
        self.server_entities = {}
        self.synced = False

        self.listfields = listfields(cls)
        self.scalarfields = scalarfields(cls)
        self.rev_listfields = {v: k for k, v in self.listfields.items()}

        mapper_obj = inspect(cls)
        for rel_attr in mapper_obj.relationships:
            if rel_attr.key in self.listfields:
                self.collection_listener(rel_attr)

        for container,cls in self.listfields.items():
            for col_attr in inspect(cls).column_attrs:
                self.attribute_track_listener(col_attr)

    def get_changed_entities(self):
        returnvalue = {}
        for k in self.obj.listfields:
            v = getattr(self.changed,k)
            if v:
                returnvalue[k] = {el.id:el for el in v}
        return returnvalue

    def get_changed_apidict(self):
        returnvalue = {}
        changed = self.get_changed_entities()
        for key, values in changed.items():
            for k, v in values.items():
                returnvalue.setdefault(key, []).append(v.dict_to_apidict(v.get_dict()))

        return returnvalue

    def clear_changed_entities(self):
        self.changed = self.cls()

    def collection_listener(self, rel_attr):
        @event.listens_for(rel_attr, 'append')
        def append(target, value, initiator):
            if target == self.obj:
                print('c append %s' % value.id)
                container = getattr(self.changed, rel_attr.key)
                if value in container:
                    if value.is_tombstone:
                        container.remove(value)
                else:
                    container.append(value)

        @event.listens_for(rel_attr, 'remove')
        def remove(target, value, initiator):
            if target == self.obj:
                print('c remove %s' % value.id)
                container = getattr(self.changed, rel_attr.key)
                if value in container:
                    container.remove(value)
                else:
                    value.is_tombstone = True
                    if value not in container:
                        container.append(value)

    def attribute_track_listener(self, col_attr):
        @event.listens_for(col_attr, "set")
        def receive_set(target, value, oldvalue, initiator):
            if hasattr(target, 'parent') and target.parent  is not None and target.parent == self.obj:
                print('c attr set %s %s' % (target.id, initiator.key))
                getattr(self.changed, self.rev_listfields[target.__class__]).append(target)

    def update_from_api_changed_entitydicts(self, changed_entitydicts, update_keys=None):
        if update_keys is None:
            update_keys = list(self.obj.listfields.keys())
        else:
            update_keys = [k for k in update_keys if k in self.obj.listfields]
        modified_entitydicts = {}
        for listfield_name in update_keys:
            newlist = []
            if changed_entitydicts[listfield_name] is not None:
                for entitydict in changed_entitydicts[listfield_name]:
                    entitydict['parent_id'] = self.obj.id
                    newlist.append(self.obj.listfields[listfield_name].from_apidict(entitydict))
            modified_entitydicts[listfield_name] = newlist
        for scalarfield_name in self.obj.scalarfields:
            if scalarfield_name in changed_entitydicts:
                typ = self.scalarfields[scalarfield_name]
                conversion_function = fromapi_conversion_functions_table.get(typ, lambda t, x: x)
                modified_entitydicts[scalarfield_name] = conversion_function(typ, changed_entitydicts[scalarfield_name])
        self.update_from_changed_entities(modified_entitydicts)

    def update_from_changed_entities(self, changed_entities):
       # to_add =[]
        for name in changed_entities:
            value = changed_entities[name]
            if not isinstance(value, list) or not value:
                continue

            for obj in [v for v in value if v.parent_id is None]:
                obj.parent = self.obj

            value = {obj.id: obj for obj in value}

            cls = self.obj.listfields[name]

            for seq in split_seq(value.keys(),999):
                for each in self.session.query(cls).filter(cls.id.in_(seq)).all():
                    v = value.pop(each.id)
                    if v.is_tombstone:
                        # delete is_tombstone entities
                        self.session.query(cls).filter_by(id=each.id).delete()
                    else:
                        # Only merge entities that already exist in the db
                        self.session.merge(v)



            self.session.add_all(value.values())

            getattr(self.obj,name).dirty=True
        self.session.commit()

    def update_from_sync_data(self, sync_data, update_keys=None):
        self.update_from_api_changed_entitydicts(sync_data['changed_entities'],update_keys)

    def sync(self, update_keys=None):
        if self.connection is None:
            return
        sync_data = self.get_sync_data_obj()

        self.server_entities[self.opname] = sync_data['changed_entities']
        LOG.debug('server_knowledge_of_device ' + str(sync_data['server_knowledge_of_device']))
        LOG.debug('current_server_knowledge ' + str(sync_data['current_server_knowledge']))
        self.update_from_sync_data(sync_data,update_keys)
        self.session.commit()
        self.clear_changed_entities()

        server_knowledge_of_device = sync_data['server_knowledge_of_device']
        current_server_knowledge = sync_data['current_server_knowledge']

        change = current_server_knowledge - self.obj.knowledge.device_knowledge_of_server
        if change > 0:
            LOG.debug('Server knowledge has gone up by ' + str(
                change) + '. We should be getting back some entities from the server')
        if  self.obj.knowledge.current_device_knowledge < server_knowledge_of_device:
            if  self.obj.knowledge.current_device_knowledge != 0:
                LOG.error('The server knows more about this device than we know about ourselves')
            self.obj.knowledge.current_device_knowledge = server_knowledge_of_device
        self.obj.knowledge.device_knowledge_of_server = current_server_knowledge

        LOG.debug('current_device_knowledge %s' %  self.obj.knowledge.current_device_knowledge)
        LOG.debug('device_knowledge_of_server %s' % self.obj.knowledge.device_knowledge_of_server)
        self.synced = True

    def push(self, update_from_sync_data=True, update_keys=None):
        changed_entities = self.get_changed_apidict()
        request_data = dict(starting_device_knowledge=self.client.starting_device_knowledge,
                            ending_device_knowledge=self.client.ending_device_knowledge,
                            device_knowledge_of_server=self.obj.knowledge.device_knowledge_of_server,
                            changed_entities=changed_entities)
        request_data.update(self.extra)

        def validate():
            self.session.commit()
            self.clear_changed_entities()
        if self.connection is not None:
            sync_data = self.connection.dorequest(request_data, self.opname)
            LOG.debug('server_knowledge_of_device ' + str(sync_data['server_knowledge_of_device']))
            LOG.debug('current_server_knowledge ' + str(sync_data['current_server_knowledge']))
            if update_from_sync_data:
                self.update_from_sync_data(sync_data, update_keys)
                validate()

                server_knowledge_of_device = sync_data['server_knowledge_of_device']
                current_server_knowledge = sync_data['current_server_knowledge']

                change = current_server_knowledge - self.obj.knowledge.device_knowledge_of_server
                if change > 0:
                    LOG.debug('Server knowledge has gone up by ' + str(
                        change) + '. We should be getting back some entities from the server')
                if  self.obj.knowledge.current_device_knowledge < server_knowledge_of_device:
                    if  self.obj.knowledge.current_device_knowledge != 0:
                        LOG.error('The server knows more about this device than we know about ourselves')
                    self.obj.knowledge.current_device_knowledge = server_knowledge_of_device
                self.obj.knowledge.device_knowledge_of_server = current_server_knowledge

                LOG.debug('current_device_knowledge %s' %  self.obj.knowledge.current_device_knowledge)
                LOG.debug('device_knowledge_of_server %s' % self.obj.knowledge.device_knowledge_of_server)
        else:
            validate()

    def get_sync_data_obj(self):
        if self.connection is None:
            return

            # sync with disregard for knowledge, start from 0
        request_data = dict(starting_device_knowledge=self.client.starting_device_knowledge,
                            ending_device_knowledge=self.client.ending_device_knowledge,
                            device_knowledge_of_server=self.obj.knowledge.device_knowledge_of_server,
                            changed_entities={})

        request_data.update(self.extra)

        return self.connection.dorequest(request_data, self.opname)