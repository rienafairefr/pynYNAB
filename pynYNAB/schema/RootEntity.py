from sqlalchemy import orm, Column, ForeignKey
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.orm import relationship

from pynYNAB.schema import BaseModel, DictDiffer, EVENTS, Entity


class RootEntity(BaseModel):
    previous_map = {}

    def _get_changed(self, fn):
        changed_entities = self.get_changed_entities()
        changed_dict = {}
        for key in changed_entities:
            changed_dict[key] = list(map(fn, changed_entities[key]))
        return changed_dict

    def get_changed_apidict(self):
        return self._get_changed(lambda entity: entity.get_apidict())

    def get_changed_dict(self):
        return self._get_changed(lambda entity: entity.get_dict())

    def get_tracked_modifications(self):
        returnvalue = {}
        for key in self.listfields:
            returnvalue[key] = []

            appended = self._track_modifications['append'][key]
            removed = self._track_modifications['remove'][key]
            changed = self._track_modifications['change'][key]

            returnvalue[key] = appended
            returnvalue[key].update(changed)

            for k,v in removed.items():
                v['is_tombstone'] = True

            returnvalue[key].update(removed)
        return self.filter_empty(returnvalue, lambda k: Entity.key_from_dict(k))

    def get_changed_entities_dict(self):
        return self._sort_ce_values(self._changed_entities_dict, lambda k: Entity.key_from_dict(k))

    def get_changed_entities(self):
        current_map = self.getmaps()
        diff_map = {}

        for key in current_map:
            if key not in diff_map:
                diff_map[key] = {}
            if isinstance(current_map[key], dict):
                if key in self.previous_map:
                    diff = DictDiffer(current_map[key], self.previous_map[key])
                    for obj_id in diff.added() | diff.changed():
                        obj = current_map[key][obj_id]
                        objc = obj.copy()
                        diff_map[key][obj_id] = objc
                    for obj_id in diff.removed():
                        obj = self.previous_map[key][obj_id]
                        objc = obj.copy()
                        objc.is_tombstone = True
                        diff_map[key][obj.id] = objc

                else:
                    diff_map[key] = current_map[key]
        return self._sort_ce_values(self.filter_empty(diff_map), lambda k: k.key())

    def filter_empty(self, input_dict):
        returnvalue = {}
        for key, value in input_dict.items():
            if isinstance(value, dict):
                if value:
                    returnvalue[key] = value

        return returnvalue

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
        self.previous_map = self.getmaps()

        self._changed_entities_dict = {}

    def getmap(self, key):
        objs_dict = {}
        if getattr(self, key) is not None:
            for instance in getattr(self, key):
                objc = instance.copy()
                objs_dict[str(instance.id)] = objc
        return objs_dict

    def getmaps(self):
        objs_dict = {}
        for key in self.listfields:
            objs_dict[key] = self.getmap(key)
        for key in self.scalarfields:
            objs_dict[key] = getattr(self, key)
        return objs_dict

    @declared_attr
    def knowledge_id(self):
        return Column(ForeignKey('knowledge.id'))

    @declared_attr
    def knowledge(self):
        return relationship('Knowledge')
