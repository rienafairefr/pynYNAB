from sqlalchemy import Column
from sqlalchemy import ForeignKey
from sqlalchemy import String
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.orm import relationship

from pynYNAB.schema.Entity import Entity, undef, Base, Root
from pynYNAB.schema.Fields import EntityField
from pynYNAB.schema.types import ArrayType


class CatalogEntity(Entity):
    @declared_attr
    def parent_id(self):
        return Column(ForeignKey('catalog.id'))

    @declared_attr
    def parent(self):
        return relationship('Catalog')


class Catalog(Base, Root):
    ce_user_budgets = relationship('UserBudget')
    ce_user_settings = relationship('UserSetting')
    ce_budget_versions = relationship('BudgetVersion')
    ce_users = relationship('User')
    ce_budgets = relationship('CatalogBudget')


class CatalogBudget(Base, CatalogEntity):
    budget_name = Column(String)
    is_tombstone = Column(String)


class User(Base, CatalogEntity):
    username = Column(String)
    trial_expires_on = Column(String)
    is_tombstone = EntityField(False)
    email = Column(String)
    feature_flags = Column(ArrayType)
    is_subscribed = Column(String)


class UserSetting(Base, CatalogEntity):
    setting_name = Column(String)
    user_id = Column(ForeignKey('user.id'))
    setting_value = Column(String)

    user = relationship('User', backref='settings')


class UserBudget(Base, CatalogEntity):
    budget_id = EntityField(undef)
    user_id = Column(ForeignKey('user.id'))
    is_tombstone = EntityField(False)
    permissions = Column(String)

    user = relationship('User', backref='budgets')


class BudgetVersion(Base, CatalogEntity):
    date_format = Column(String)
    last_accessed_on = Column(String)
    currency_format = Column(String)
    budget_id = Column(ForeignKey('catalogbudget.id'))
    is_tombstone = EntityField(False)
    version_name = Column(String)
    source = Column(String)

    budget = relationship('CatalogBudget')



