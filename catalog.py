from Entity import Entity, ListofEntities, EntityField, Fields


class CatalogBudget(Entity):
    def __init__(self):
        self.budget_name=EntityField()
        self.id=EntityField()
        self.is_tombstone=EntityField()

        Fields.register(self)
        super(CatalogBudget, self).__init__()


class UserBudget(Entity):
    def __init__(self):
        self.budget_id=EntityField()
        self.user_id=EntityField()
        self.id=EntityField()
        self.is_tombstone=EntityField()
        self.permissions=EntityField()

        Fields.register(self)
        super(UserBudget, self).__init__()


class UserSetting(Entity):
    def __init__(self):
        self.setting_name=EntityField()
        self.user_id=EntityField()
        self.id=EntityField()
        self.setting_value=EntityField()

        Fields.register(self)
        super(UserSetting, self).__init__()


class User(Entity):
    def __init__(self):
        self.username=EntityField()
        self.trial_expires_on=EntityField()
        self.is_tombstone=EntityField()
        self.email=EntityField()

        Fields.register(self)
        super(User, self).__init__()


class BudgetVersion(Entity):
    def __init__(self):
        self.date_format=EntityField()
        self.last_accessed_on=EntityField()
        self.currency_format=EntityField()
        self.budget_id=EntityField()
        self.is_tombstone=EntityField()
        self.version_name=EntityField()

        Fields.register(self)
        super(BudgetVersion, self).__init__()


class Catalog(Entity):
    def __init__(self):
        self.ce_user_budgets=ListofEntities(UserBudget)
        self.ce_user_settings=ListofEntities(UserSetting)
        self.ce_budget_versions=ListofEntities( BudgetVersion)
        self.ce_users=ListofEntities(User)
        self.ce_budgets=ListofEntities(CatalogBudget)

        Fields.register(self)
        super(Catalog, self).__init__()

        self.knowledge = 0
        self.current_knowledge = 0
        self.device_knowledge_of_server = 0
        self.server_knowledge_of_device = 0
