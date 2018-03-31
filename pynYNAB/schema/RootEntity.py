from sqlalchemy import orm, Column, ForeignKey
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.orm import relationship

from pynYNAB.schema import BaseModel, Entity


class RootEntity(BaseModel):
    previous_map = {}

    def _get_changed(self, fn):
        changed_entities = self.get_changed_entities()
        changed_dict = {}
        for key in changed_entities:
            changed_dict[key] = list(map(fn, changed_entities[key]))

        return changed_dict

    def _get_changed_dict(self, fn):
        changed_entities = self.get_changed_entities_dict()
        changed_dict = {}
        for key in changed_entities:
            changed_dict[key] = list(map(fn, changed_entities[key]))

        return changed_dict

    def get_changed_apidict(self):
        returnvalue = {}
        changed = self.get_changed_entities()
        for key, values in changed.items():
            for k, v in values.items():
                returnvalue.setdefault(key, []).append(v.dict_to_apidict(v.get_dict()))

        return returnvalue

    def get_changed_entities(self):
        return self._changed_entities

    def get_changed_entities_dict(self):
        return self._changed_entities_dict

    def _sort_ce_values(self, input_dict, cmp_key):
        returnvalue = {}
        for key, value in input_dict.items():
            sorted_values = sorted(list(value.values()), key=cmp_key)
            returnvalue[key] = sorted_values

        return returnvalue

    def __init__(self):
        super(RootEntity, self).__init__()
        self.clear_changed_entities()

    @orm.reconstructor
    def clear_changed_entities(self):
        self._changed_entities_dict = {}
        self._changed_entities = {}

    @declared_attr
    def knowledge_id(self):
        return Column(ForeignKey('knowledge.id'))

    @declared_attr
    def knowledge(self):
        return relationship('Knowledge')
