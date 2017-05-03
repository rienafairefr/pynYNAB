import logging
from abc import abstractproperty,ABCMeta

from pynYNAB.schema import fromapi_conversion_functions_table

LOG = logging.getLogger(__name__)



class RootObjClient():
    __metaclass__ = ABCMeta

    @abstractproperty
    def extra(self):
        return {}

    @abstractproperty
    def opname(self):
        return ''

    def __init__(self, obj, client):
        self.obj = obj
        self.client = client
        self.connection = client.connection
        self.session = client.session
        self.server_entities = {}
        self.synced = False

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
                    newlist.append(self.obj.listfields[listfield_name].from_apidict(entitydict))
            modified_entitydicts[listfield_name] = newlist
        for scalarfield_name in self.obj.scalarfields:
            if scalarfield_name in changed_entitydicts:
                typ = self.obj.scalarfields[scalarfield_name]
                conversion_function = fromapi_conversion_functions_table.get(typ, lambda t, x: x)
                modified_entitydicts[scalarfield_name] = conversion_function(typ, changed_entitydicts[scalarfield_name])
        self.update_from_changed_entities(modified_entitydicts)

    def update_from_changed_entitydict(self, changed_entitiydicts):
        for name in changed_entitiydicts:
            value = changed_entitiydicts[name]
            if not isinstance(value, list):
                continue

            for incoming_obj_dict in value:
                incoming_obj_dict['parent_id'] = self.obj.id
                current_obj = self.session.query(self.obj.listfields[name]).get(incoming_obj_dict['id'])
                if current_obj is not None:
                    if incoming_obj_dict['is_tombstone']:
                        self.session.delete(current_obj)
                        continue
                else:
                    incoming_obj = self.obj.listfields[name].from_dict(incoming_obj_dict)
                    self.session.merge(incoming_obj)
        self.session.commit()
        self.session.expire(self.obj)
        pass

    def update_from_changed_entities(self, changed_entities):
        for name in changed_entities:
            value = changed_entities[name]
            if not isinstance(value, list):
                continue
            list_of_entities = getattr(self.obj, name)
            for incoming_obj in value:
                current_obj = self.session.query(self.obj.listfields[name]).get(incoming_obj.id)
                if current_obj is not None:
                    if incoming_obj.is_tombstone:
                        self.session.delete(current_obj)
                    else:
                        if current_obj not in list_of_entities:
                            current_obj.parent = self.obj
                        else:
                            for field in current_obj.scalarfields:
                                incoming = getattr(incoming_obj, field)
                                present = getattr(current_obj, field)
                                if present != incoming:
                                    setattr(current_obj, field, incoming)
                                    pass
                            pass
                else:
                    if not incoming_obj.is_tombstone:
                        self.session.add(incoming_obj)
                        incoming_obj.parent = self.obj
        self.session.commit()
        pass

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
        self.obj.clear_changed_entities()

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
        changed_entities = self.obj.get_changed_apidict()
        request_data = dict(starting_device_knowledge=self.client.starting_device_knowledge,
                            ending_device_knowledge=self.client.ending_device_knowledge,
                            device_knowledge_of_server=self.obj.knowledge.device_knowledge_of_server,
                            changed_entities=changed_entities)
        request_data.update(self.extra)

        def validate():
            self.session.commit()
            self.obj.clear_changed_entities()
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