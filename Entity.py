import collections


class Entity(object):
    def __getstate__(self):
        return {'__dict__':self.__dict__.copy(),'values':self.values}

    def __setstate__(self, dict):
        self.__dict__ = dict['__dict__']
        self.values = dict['values']

    def __getattr__(self, item):
        if item=='values':
            raise AttributeError()
        if item in self.values:
            return self.values[item]
        else:
            return object.__getattribute__(self, item)

    def __str__(self):
        return self.values.__str__()

    def __unicode__(self):
        return self.__str__()

    def __repr__(self):
        return self.__str__()

    def __init__(self):
        self.values={}
        self.fields = self.fields if hasattr(self,'fields') else {}
        self.listfields = self.listfields if hasattr(self,'listfields') else {}
        for field in self.fields:
            self.values[field]=Entity()
        for listfield in self.listfields.iterkeys():
            self.values[listfield]=ListofEntities(self.listfields[listfield])

    def update_from_changed_entities(self,changed_entities):
        for listfield in self.listfields:
            self.values[listfield].update_from_changed_entities(changed_entities[listfield])

    def update_from_dict(self,d):
        self.values=d.copy()


class ListofEntities(object):
    def __init__(self, typ):
        self.dict_entities={}
        self.typeItems=typ

    def __str__(self):
        return self.dict_entities.values().__str__()

    def __unicode__(self):
        return self.__str__()

    def __repr__(self):
        return self.__str__()

    def update_from_changed_entities(self,changed_entities):
        for entity in changed_entities:
            entity_id=entity['id']
            try:
                self.dict_entities[entity_id].update_from_changed_entities(entity)
            except KeyError:
                self.dict_entities[entity_id]=self.typeItems()
                self.dict_entities[entity_id].update_from_dict(entity)

    def __iter__(self):
        return self.dict_entities.itervalues()

    def __len__(self):
        return len(self.dict_entities)

    def __getitem__(self, item):
        return self.dict_entities.values().__getitem__(item)