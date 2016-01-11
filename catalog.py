from Entity import Entity, ListofEntities


class CatalogBudget(Entity):
    def __init__(self):
        self.fields = [
            'budget_name',
            'id',
            'is_tombstone'
        ]
        Entity.__init__(self)


class UserBudget(Entity):
    def __init__(self):
        self.fields = [
            'budget_id',
            'user_id',
            'id',
            'is_tombstone',
            'permissions']
        Entity.__init__(self)


class UserSetting(Entity):
    def __init__(self):
        self.fields = [
            'setting_name',
            'user_id',
            'id',
            'setting_value'
        ]
        Entity.__init__(self)


class User(Entity):
    def __init__(self):
        self.fields = [
            'username',
            'trial_expires_on',
            'id',
            'is_tombstone',
            'email'
        ]
        Entity.__init__(self)


class BudgetVersion(Entity):
    def __init__(self):
        self.fields = [
            'date_format',
            'last_accessed_on',
            'currency_format',
            'budget_id',
            'is_tombstone',
            'version_name',
            'id'
        ]
        Entity.__init__(self)


class Catalog(Entity):
    def __init__(self):
        self.listfields = {
            'ce_user_budgets': UserBudget,
            'ce_user_settings': UserSetting,
            'ce_budget_versions': BudgetVersion,
            'ce_users': User,
            'ce_budgets': CatalogBudget
        }
        Entity.__init__(self)
        self.knowledge = 0
        self.current_knowledge=0
        self.server_knowledge_of_device = 0
