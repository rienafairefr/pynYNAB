import logging

LOG = logging.getLogger(__name__)

class RootObjClient(object):
    def __init__(self, obj, client, opname):
        self.obj = obj
        self.client = client
        self.connection = client.connection
        self.session = client.session
        self.opname = opname

    def update_from_api_changed_entities(self, changed_entities):
        for name in self.obj.listfields:
            if changed_entities[name] is None:
                continue
            newlist = []
            for entitydict in changed_entities[name]:
                newlist.append(self.obj.listfields[name].from_apidict(entitydict))
            changed_entities[name] = newlist
        self.update_from_changed_entities(changed_entities)

    def update_from_changed_entities(self, changed_entities):
        for name, value in changed_entities.items():
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

    def update_from_sync_data(self, sync_data):
        self.update_from_api_changed_entities(sync_data['changed_entities'])

    def sync(self, extra=None):
        sync_data = self.get_sync_data_obj(extra)

        self.client.server_entities[self.opname] = sync_data['changed_entities']
        LOG.debug('server_knowledge_of_device ' + str(sync_data['server_knowledge_of_device']))
        LOG.debug('current_server_knowledge ' + str(sync_data['current_server_knowledge']))
        self.update_from_sync_data(sync_data)
        self.session.commit()
        self.obj.clear_changed_entities()

        server_knowledge_of_device = sync_data['server_knowledge_of_device']
        current_server_knowledge = sync_data['current_server_knowledge']

        change = current_server_knowledge - self.client.device_knowledge_of_server[self.opname]
        if change > 0:
            LOG.debug('Server knowledge has gone up by ' + str(
                change) + '. We should be getting back some entities from the server')
        if self.client.current_device_knowledge[self.opname] < server_knowledge_of_device:
            if self.client.current_device_knowledge[self.opname] != 0:
                LOG.error('The server knows more about this device than we know about ourselves')
            self.client.current_device_knowledge[self.opname] = server_knowledge_of_device
        self.client.device_knowledge_of_server[self.opname] = current_server_knowledge

        LOG.debug('current_device_knowledge %s' % self.client.current_device_knowledge[self.opname])
        LOG.debug('device_knowledge_of_server %s' % self.client.device_knowledge_of_server[self.opname])

    def push(self, extra=None):
        if self.connection is None:
            return
        if extra is None:
            extra = {}

        changed_entities = self.obj.get_changed_apidict()
        request_data = dict(starting_device_knowledge=self.client.starting_device_knowledge,
                            ending_device_knowledge=self.client.ending_device_knowledge,
                            device_knowledge_of_server=self.client.device_knowledge_of_server[self.opname],
                            changed_entities=changed_entities)
        request_data.update(extra)
        sync_data = self.connection.dorequest(request_data, self.opname)
        LOG.debug('server_knowledge_of_device ' + str(sync_data['server_knowledge_of_device']))
        LOG.debug('current_server_knowledge ' + str(sync_data['current_server_knowledge']))
        self.update_from_sync_data(sync_data)
        self.session.commit()
        self.obj.clear_changed_entities()

        server_knowledge_of_device = sync_data['server_knowledge_of_device']
        current_server_knowledge = sync_data['current_server_knowledge']

        change = current_server_knowledge - self.client.device_knowledge_of_server[self.opname]
        if change > 0:
            LOG.debug('Server knowledge has gone up by ' + str(
                change) + '. We should be getting back some entities from the server')
        if self.client.current_device_knowledge[self.opname] < server_knowledge_of_device:
            if self.client.current_device_knowledge[self.opname] != 0:
                LOG.error('The server knows more about this device than we know about ourselves')
            self.client.current_device_knowledge[self.opname] = server_knowledge_of_device
        self.client.device_knowledge_of_server[self.opname] = current_server_knowledge

        LOG.debug('current_device_knowledge %s' % self.client.current_device_knowledge[self.opname])
        LOG.debug('device_knowledge_of_server %s' % self.client.device_knowledge_of_server[self.opname])

    def get_sync_data_obj(self, extra=None):
        if self.connection is None:
            return
        if extra is None:
            extra = {}
        if self.opname not in self.client.current_device_knowledge:
            self.client.current_device_knowledge[self.opname] = 0
        if self.opname not in self.client.device_knowledge_of_server:
            self.client.device_knowledge_of_server[self.opname] = 0
            # sync with disregard for knowledge, start from 0
        request_data = dict(starting_device_knowledge=self.client.starting_device_knowledge,
                            ending_device_knowledge=self.client.ending_device_knowledge,
                            device_knowledge_of_server=self.client.device_knowledge_of_server[self.opname],
                            changed_entities={})

        request_data.update(extra)

        return self.connection.dorequest(request_data, self.opname)