from sqlalchemy import orm, Column, ForeignKey
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.orm import relationship

from pynYNAB.schema import BaseModel, Entity


class RootEntity(BaseModel):
    previous_map = {}

    def __init__(self):
        super(BaseModel, self).__init__()

    @declared_attr
    def knowledge_id(self):
        return Column(ForeignKey('knowledge.id'))

    @declared_attr
    def knowledge(self):
        return relationship('Knowledge')
