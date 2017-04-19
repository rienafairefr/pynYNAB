from abc import abstractproperty

from sqlalchemy import Column
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy.orm import relationship

from pynYNAB import KeyGenerator
from pynYNAB.schema.Entity import Base
from pynYNAB.schema.roots import Catalog, Budget


class Knowledge(Base):
    __tablename__ = 'knowledge'

    obj_id = Column(String,primary_key=True,default=KeyGenerator.generateuuid)
    current_device_knowledge = Column(Integer)
    device_knowledge_of_server = Column(Integer)

class nYnabClientData(Base):
    __tablename__ = "nynabclientsdata"
    id = Column(String, primary_key=True)
    catalog_id = Column(ForeignKey('catalog.id'))
    catalog = relationship(Catalog)
    budget_id = Column(ForeignKey('budget.id'))
    budget = relationship(Budget)
    budget_version_id = Column(String)
    budget_name = Column(String)
    starting_device_knowledge = Column(Integer,default=0)
    ending_device_knowledge = Column(Integer,default=0)

    @property
    def online(self):
        return self.connection is not None
