import copy
import json
import uuid

def undef():
    pass

class ComplexEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Entity):
            return obj.__dict__
        if isinstance(obj, ListofEntities):
            return obj._dict_entities.values()
        return json.JSONEncoder.default(self, obj)

class EntityField(object):
    pass

class Fields(dict):
    fields={}
    @classmethod
    def register(self, obj):
        if not obj.__class__ in self.fields:
            self.fields[obj.__class__] = {k:v for k,v in obj.__dict__.iteritems()}
        for k,v in copy.deepcopy(obj.__dict__).iteritems():
            if isinstance(v,ListofEntities):
                pass
            else:
                if v==undef:
                    delattr(obj,k)
                else:
                    setattr(obj,k,None)
        #obj.id=str(uuid.uuid4())


class Entity(object):
    def __init__(self):
        self.id=str(uuid.uuid4())
        super(Entity,self).__init__()

    def __str__(self):
        return self.__dict__.__str__()

    @classmethod
    def create(cls, **kwargs):
        obj=cls()
        obj.__dict__.update(kwargs)
        return obj

    def __unicode__(self):
        return self.__str__()

    def getdict(self):
        return {k:getattr(self,k) for k in self.__dict__ if k!='fields' and k!='listfields'}

    def get_changed_entities(self,previous):
        firstrun={}
        for namefield,field in Fields.fields[self.__class__].iteritems():
            if isinstance(field,ListofEntities):
                firstrun[namefield]=getattr(self,namefield).get_changed_entities(getattr(previous,namefield))
        return {k:v for k,v in firstrun.iteritems() if v!=[]}

    def update_from_changed_entities(self,changed_entities):
        for namefield,field in Fields.fields[self.__class__].iteritems():
            if isinstance(field,ListofEntities):
                getattr(self,namefield).update_from_changed_entities(changed_entities[namefield])

    def update_from_dict(self,d):
        self.__dict__.update(d)

class ListofEntities(object):
    def __init__(self, typ):
        super(ListofEntities, self).__init__()
        self._dict_entities={}
        self.typeItems=typ

    def __str__(self):
        return self._dict_entities.values().__str__()

    def __unicode__(self):
        return self.__str__()

    def update_from_changed_entities(self,changed_entities):
        if changed_entities is None:
            return
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

    def get_changed_entities(self,previous):
        if not isinstance(previous,ListofEntities):
            return
        changed=[]
        for current_id,current_entity in self._dict_entities.iteritems():
            if current_id not in previous._dict_entities:
                # entity is added
                changed.append(current_entity)
        for previous_id,previous_entity in previous._dict_entities.iteritems():
            if previous_id not in self._dict_entities:
                # entity is deleted
                previous_entity.is_tombstone=True
                changed.append(previous_entity)

        for current_id,current_entity in self._dict_entities.iteritems():
            if current_id in previous._dict_entities:
                previous_entity=previous._dict_entities[current_id]
                if not previous_entity.getdict()==current_entity.getdict():
                    # something changed for that entity, we add the current version
                    changed.append(current_entity)

        return changed
