import json
import uuid

def undef():
    pass


class ComplexEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Entity):
            return {f:getattr(obj,f) for f in obj.AllFields}
        elif isinstance(obj, ListofEntities):
            return obj._dict_entities.values()
        elif obj==undef:
            return
        else:
            return json.JSONEncoder.default(self, obj)

class EntityField(object):
    def __init__(self,default):
        self.default=default

    def __call__(self, *args, **kwargs):
        return self.default


class EntityListField(object):
    def __init__(self,type):
        self.type=type

    def __call__(self, *args, **kwargs):
        return ListofEntities(self.type)


class Entity(object):
    def __init__(self,*args,**kwargs):
        for namefield in self.AllFields:
            setattr(self,namefield,kwargs.get(namefield) if kwargs.get(namefield) else self.AllFields[namefield]())
        if self.id is None:
            self.id=str(uuid.uuid4())
        super(Entity,self).__init__()

    def __str__(self):
        return str(self.getdict())

    @property
    def AllFields(self):
        return dict(self.Fields.items()+self.CommonFields.items())

    @property
    def CommonFields(self):
        return dict(
            id=EntityField(None)
        )

    @property
    def Fields(self):
        return {}

    @property
    def ListFields(self):
        return {namefield:value for namefield,value in self.AllFields.iteritems() if isinstance(value,EntityListField)}

    def __unicode__(self):
        return self.__str__()

    def getdict(self):
        return {namefield:getattr(self,namefield) for namefield in self.AllFields}

    def get_changed_entities(self,previous):
        firstrun={namefield:getattr(self,namefield).get_changed_entities(getattr(previous,namefield)) for namefield in self.ListFields}
        return {namefield:value for namefield,value in firstrun.iteritems() if value != []}

    def update_from_changed_entities(self,changed_entities):
        for namefield in self.ListFields:
            getattr(self,namefield).update_from_changed_entities(changed_entities.get(namefield))

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
            try:
                self._dict_entities[entity.id].update_from_changed_entities(entity)
            except KeyError:
                self._dict_entities[entity.id]=self.typeItems()
                self._dict_entities[entity.id].update_from_dict(entity.getdict())

    def append(self,o):
        if not isinstance(o,self.typeItems):
            raise ValueError('this ListofEntities can only contain %s' % self.typeItems.__name__)
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
