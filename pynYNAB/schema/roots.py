from sqlalchemy.orm import relationship

from pynYNAB.schema.Entity import Base, RootEntity


class Catalog(Base, RootEntity):
    ce_user_budgets = relationship('UserBudget')
    ce_user_settings = relationship('UserSetting')
    ce_budget_versions = relationship('BudgetVersion')
    ce_users = relationship('User')
    ce_budgets = relationship('CatalogBudget')


class Budget(Base, RootEntity):
    def __init__(self):
        RootEntity.__init__(self)
        self.budget_version_id = None

    be_transactions = relationship('Transaction')
    be_master_categories = relationship('MasterCategory')
    be_settings = relationship('Setting')
    be_monthly_budget_calculations = relationship('MonthlyBudgetCalculation')
    be_account_mappings = relationship('AccountMapping')
    be_subtransactions = relationship('Subtransaction')
    be_scheduled_subtransactions = relationship('ScheduledSubtransaction')
    be_monthly_budgets = relationship('MonthlyBudget')
    be_subcategories = relationship('SubCategory')
    be_payee_locations = relationship('PayeeLocation')
    be_account_calculations = relationship('AccountCalculation')
    be_monthly_account_calculations = relationship('MonthlyAccountCalculation')
    be_monthly_subcategory_budget_calculations = relationship('MonthlySubcategoryBudgetCalculation')
    be_scheduled_transactions = relationship('ScheduledTransaction')
    be_payees = relationship('Payee')
    be_monthly_subcategory_budgets = relationship('MonthlySubcategoryBudget')
    be_payee_rename_conditions = relationship('PayeeRenameCondition')
    be_accounts = relationship('Account')
    last_month = Column(Date)
    first_month = Column(Date)
    budget_version_id = Column(ForeignKey('budgetversion.id'), nullable=True)
    calculated_entities_included = Column(Boolean, default=False)