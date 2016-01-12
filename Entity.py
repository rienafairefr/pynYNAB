import collections
import uuid

class EntityField(object):
    pass

class Entity(object):
    def __str__(self):
        return self.__dict__.__str__()

    def __unicode__(self):
        return self.__str__()

    def __repr__(self):
        return self.__str__()

    def __setattr__(self, key, value):
        try:
            if key in self.fields or key in self.listfields:
                # TODO: data validation
                pass
        except AttributeError:
            pass
        object.__setattr__(self,key,value)

    def get_changed_entities(self,other):
        firstrun= {l:getattr(self,l).get_changed_entities(getattr(other,l)) for l in self.listfields}
        return {k:v for k,v in firstrun.iteritems() if v!=[]}


    def __init__(self):
        # initialize the Entity, go through the instance fields and fetch the actual fields and listfields
        # After that __init__, self.name_attr=blabla will go into the values dictionary as well
        self.fields = {k:v for k,v in self.__dict__.iteritems() if isinstance(v,EntityField)}
        self.listfields = {k:v for k,v in self.__dict__.iteritems() if isinstance(v,ListofEntities)}
        self.id=str(uuid.uuid4())

    def update_from_changed_entities(self,changed_entities):
        for listfield in self.listfields:
            getattr(self,listfield).update_from_changed_entities(changed_entities[listfield])

    def update_from_dict(self,d):
        self.values=d.copy()


class ListofEntities(object):
    def __init__(self, typ):
        self._dict_entities={}
        self.typeItems=typ

    def __str__(self):
        return self._dict_entities.values().__str__()

    def __unicode__(self):
        return self.__str__()

    def __repr__(self):
        return self.__str__()

    def update_from_changed_entities(self,changed_entities):
        for entity in changed_entities:
            entity_id=entity['id']
            try:
                self._dict_entities[entity_id].update_from_changed_entities(entity)
            except KeyError:
                self._dict_entities[entity_id]=self.typeItems()
                self._dict_entities[entity_id].update_from_dict(entity)
    def append(self,o):
        if not isinstance(o,Entity):
            raise ValueError('this ListofEntities can only contain Entities')
        self._dict_entities[o.id]=o
    def __iter__(self):
        return self._dict_entities.itervalues()

    def __len__(self):
        return len(self._dict_entities)

    def __getitem__(self, item):
        return self._dict_entities.values().__getitem__(item)

    def get_changed_entities(self,other):
        if not isinstance(other,ListofEntities):
            return
        changed=[]
        for id,entity in other._dict_entities.iteritems():
            try:
                if self._dict_entities[id] != entity:
                    changed.append(entity)
            except KeyError:
                # entity is added in other compared to self
                changed.append(entity)
        return changed
