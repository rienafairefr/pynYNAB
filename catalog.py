from Entity import Entity, ListofEntities, EntityField, undef, EntityListField


class CatalogBudget(Entity):
    @property
    def Fields(self):
        return dict(
            budget_name=EntityField(None),
            id=EntityField(None),
            is_tombstone=EntityField(None)
        )


class UserBudget(Entity):
    @property
    def Fields(self):
        return dict(
            budget_id=EntityField(undef),
            user_id=EntityField(None),
            id=EntityField(None),
            is_tombstone=EntityField(None),
            permissions=EntityField(None)
        )


class UserSetting(Entity):
    @property
    def Fields(self):
        return dict(
            setting_name=EntityField(None),
            user_id=EntityField(None),
            id=EntityField(None),
            setting_value=EntityField(None)
        )


class User(Entity):
    @property
    def Fields(self):
        return dict(
            username=EntityField(None),
            trial_expires_on=EntityField(None),
            is_tombstone=EntityField(None),
            email=EntityField(None)
        )


class BudgetVersion(Entity):
    @property
    def Fields(self):
        return dict(
            date_format=EntityField(None),
            last_accessed_on=EntityField(None),
            currency_format=EntityField(None),
            budget_id=EntityField(None),
            is_tombstone=EntityField(None),
            version_name=EntityField(None),
        )


class Catalog(Entity):
    @property
    def Fields(self):
        return dict(
            ce_user_budgets=EntityListField(UserBudget),
            ce_user_settings=EntityListField(UserSetting),
            ce_budget_versions=EntityListField(BudgetVersion),
            ce_users=EntityListField(User),
            ce_budgets=EntityListField(CatalogBudget)
        )

    def __init__(self):
        self.knowledge = 0
        self.current_knowledge = 0
        self.device_knowledge_of_server = 0
        self.server_knowledge_of_device = 0
        super(Catalog, self).__init__()
