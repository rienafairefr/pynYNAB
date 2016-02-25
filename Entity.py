import json
import uuid

def undef():
    pass

class AccountTypes(object):
    Checking = 'Checking'
    Savings = 'Savings'
    CreditCard = 'CreditCard'
    Cash = 'Cash'
    InvestmentAccount = 'InvestmentAccount'
    Mortgage = 'Mortgage'
    OtherAsset = 'OtherAsset'
    OtherLiability = 'OtherLiability'
    LineofCredit = 'LineOfCredit'
    PayPal = 'PayPal'
    MerchantAccount = 'MerchantAccount'


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
            setattr(self,namefield,kwargs.get(namefield) if kwargs.get(namefield) is not None else self.AllFields[namefield]())
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

    def get_changed_entities(self):
        firstrun={namefield:getattr(self,namefield).get_changed_entities() for namefield in self.ListFields}
        return {namefield:value for namefield,value in firstrun.iteritems() if value != []}

    def update_from_changed_entities(self,changed_entities):
        for namefield in self.ListFields:
            getattr(self,namefield).update_from_changed_entities(changed_entities.get(namefield))

    def update_from_dict(self,d):
        self.__dict__.update(d)

    def __eq__(self, other):
        if isinstance(other,Entity):
            return self.getdict()==other.getdict()
        else:
            return False

class ListofEntities(object):
    def __init__(self, typ):
        super(ListofEntities, self).__init__()
        from collections import OrderedDict
        self._dict_entities=OrderedDict()
        self.typeItems=typ
        self.changed=[]

    def __str__(self):
        return self._dict_entities.values().__str__()

    def __unicode__(self):
        return self.__str__()

    def __getitem__(self, item):
        return self._dict_entities.values().__getitem__(item)

    def update_from_changed_entities(self,changed_entities):
        if changed_entities is None:
            return
        for entityDict in changed_entities:
            try:
                self._dict_entities[entityDict['id']].update_from_changed_entities(entityDict)
            except KeyError:
                self._dict_entities[entityDict['id']]=self.typeItems(**entityDict)

    def get(self,id):
        return self._dict_entities.get(id)

    def append(self,o,track=True):
        if not isinstance(o,self.typeItems):
            raise ValueError('this ListofEntities can only contain %s' % self.typeItems.__name__)
        self._dict_entities[o.id]=o
        if track:
            self.changed.append(o)

    def delete(self,o,track=True):
        if not isinstance(o,self.typeItems):
            raise ValueError('this ListofEntities can only contain %s' % self.typeItems.__name__)
        if o.id in self._dict_entities:
            del self._dict_entities[o.id]
        if track:
            o.is_tombstone=True
            self.changed.append(o)

    def modify(self,o,track=True):
        if not isinstance(o,self.typeItems):
            raise ValueError('this ListofEntities can only contain %s' % self.typeItems.__name__)
        if o.id in self._dict_entities:
            self._dict_entities[o.id]=o
            if track:
                self.changed.append(o)

    def __iter__(self):
        return self._dict_entities.itervalues()

    def __len__(self):
        return len(self._dict_entities)

    def __contains__(self, item):
        if not isinstance(item,self.typeItems):
            return False
        else:
            return item.id in self._dict_entities


    def get_changed_entities(self):
        return self.changed

    def query(self,searched):
        for k,entity in self._dict_entities.iteritems():
            if searched(entity):
                return entity

