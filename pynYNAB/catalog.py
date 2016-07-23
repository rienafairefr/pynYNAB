from pynYNAB.Entity import Entity, undef
from pynYNAB.schema.Fields import EntityField


class CatalogBudget(Entity):
    budget_name=EntityField(None)
    is_tombstone=EntityField(None)


class UserBudget(Entity):
    budget_id=EntityField(undef)
    user_id=EntityField(None)
    is_tombstone=EntityField(False)
    permissions=EntityField(None)


class UserSetting(Entity):
    setting_name=EntityField(None)
    user_id=EntityField(None)
    setting_value=EntityField(None)


class User(Entity):
    username=EntityField(None)
    trial_expires_on=EntityField(None)
    is_tombstone=EntityField(False)
    email=EntityField(None)
    feature_flags=EntityField(None)
    is_subscribed=EntityField(None)


class BudgetVersion(Entity):
    date_format=EntityField(None)
    last_accessed_on=EntityField(None)
    currency_format=EntityField(None)
    budget_id=EntityField(None)
    is_tombstone=EntityField(False)
    version_name=EntityField(None)
    source=EntityField(None)



