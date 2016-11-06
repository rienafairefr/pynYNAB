from sqlalchemy import Column
from sqlalchemy import ForeignKey
from sqlalchemy import String
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.orm import relationship

from pynYNAB.Entity import Entity, undef, Base
from pynYNAB.schema.Fields import EntityField


class CatalogEntity(Entity):
    @declared_attr
    def catalog_id(self):
        return Column(ForeignKey('catalog.id'))

    @declared_attr
    def catalog(self):
        return relationship('Catalog')


class CatalogBudget(Base, CatalogEntity):
    budget_name = Column(String)
    is_tombstone = Column(String)


class UserBudget(Base, CatalogEntity):
    budget_id = EntityField(undef)
    user_id = Column(String)
    is_tombstone = EntityField(False)
    permissions = Column(String)


class UserSetting(Base, CatalogEntity):
    setting_name = Column(String)
    user_id = Column(String)
    setting_value = Column(String)


class User(Base, CatalogEntity):
    username = Column(String)
    trial_expires_on = Column(String)
    is_tombstone = EntityField(False)
    email = Column(String)
    feature_flags = Column(String)
    is_subscribed = Column(String)


class BudgetVersion(Base, CatalogEntity):
    date_format = Column(String)
    last_accessed_on = Column(String)
    currency_format = Column(String)
    budget_id = Column(String)
    is_tombstone = EntityField(False)
    version_name = Column(String)
    source = Column(String)
