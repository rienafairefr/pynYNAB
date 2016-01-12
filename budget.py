from Entity import Entity, ListofEntities, EntityField


class Transaction(Entity):
    def __init__(self):
        self.accepted = EntityField()
        self.amount = EntityField()
        self.cash_amount = EntityField()
        self.check_number = EntityField()
        self.cleared = EntityField()
        self.credit_amount = EntityField()
        self.date = EntityField()
        self.date_entered_from_schedule = EntityField()
        self.entities_account_id = EntityField()
        self.entities_payee_id = EntityField()
        self.entities_scheduled_transaction_id = EntityField()
        self.entities_subcategory_id = EntityField()
        self.flag = EntityField()
        self.id = EntityField()
        self.imported_date = EntityField()
        self.imported_payee = EntityField()
        self.is_tombstone = EntityField()
        self.matched_transaction_id = EntityField()
        self.memo = EntityField()
        self.source = EntityField()
        self.transfer_account_id = EntityField()
        self.transfer_subtransaction_id = EntityField()
        self.transfer_transaction_id = EntityField()
        self.ynab_id = EntityField()
        Entity.__init__(self)


class MasterCategory(Entity):
    def __init__(self):
        self.deletable = EntityField()
        self.id = EntityField()
        self.internal_name = EntityField()
        self.is_hidden = EntityField()
        self.is_tombstone = EntityField()
        self.name = EntityField()
        self.note = EntityField()
        self.sortable_index = EntityField()
        Entity.__init__(self)


class Setting(Entity):
    def __init__(self):
        self.id = EntityField()
        self.setting_name = EntityField()
        self.setting_value = EntityField()
        Entity.__init__(self)


class MonthlyBudgetCalculation(Entity):
    def __init__(self):
        self.additional_to_be_budgeted = EntityField()
        self.age_of_money = EntityField()
        self.available_to_budget = EntityField()
        self.balance = EntityField()
        self.budgeted = EntityField()
        self.calculation_notes = EntityField()
        self.cash_outflows = EntityField()
        self.credit_outflows = EntityField()
        self.deferred_income = EntityField()
        self.entities_monthly_budget_id = EntityField()
        self.hidden_balance = EntityField()
        self.hidden_budgeted = EntityField()
        self.hidden_cash_outflows = EntityField()
        self.hidden_credit_outflows = EntityField()
        self.id = EntityField()
        self.immediate_income = EntityField()
        self.is_tombstone = EntityField()
        self.over_spent = EntityField()
        self.previous_income = EntityField()
        self.uncategorized_balance = EntityField()
        self.uncategorized_cash_outflows = EntityField()
        self.uncategorized_credit_outflows = EntityField()
        Entity.__init__(self)


class AccountMapping(Entity):
    def __init__(self):
        self.date_sequence = EntityField()
        self.entities_account_id = EntityField()
        self.fid = EntityField()
        self.hash = EntityField()
        self.id = EntityField()
        self.is_tombstone = EntityField()
        self.salt = EntityField()
        self.shortened_account_id = EntityField()
        self.should_flip_payees_memos = EntityField()
        self.should_import_memos = EntityField()
        self.skip_import = EntityField()
        Entity.__init__(self)


class Subtransaction(Entity):
    def __init__(self):
        self.amount = EntityField()
        self.cash_amount = EntityField()
        self.check_number = EntityField()
        self.credit_amount = EntityField()
        self.entities_payee_id = EntityField()
        self.entities_subcategory_id = EntityField()
        self.entities_transaction_id = EntityField()
        self.id = EntityField()
        self.is_tombstone = EntityField()
        self.memo = EntityField()
        self.sortable_index = EntityField()
        self.transfer_account_id = EntityField()
        self.transfer_transaction_id = EntityField()
        Entity.__init__(self)


class ScheduledSubtransaction(Entity):
    def __init__(self):
        self.amount = EntityField()
        self.entities_payee_id = EntityField()
        self.entities_scheduled_transaction_id = EntityField()
        self.entities_subcategory_id = EntityField()
        self.id = EntityField()
        self.is_tombstone = EntityField()
        self.memo = EntityField()
        self.sortable_index = EntityField()
        self.transfer_account_id = EntityField()
        Entity.__init__(self)


class MonthlyBudget(Entity):
    def __init__(self):
        self.id = EntityField()
        self.is_tombstone = EntityField()
        self.month = EntityField()
        self.note = EntityField()
        Entity.__init__(self)


class Subcategory(Entity):
    def __init__(self):
        self.entities_account_id = EntityField()
        self.entities_master_category_id = EntityField()
        self.goal_creation_month = EntityField()
        self.goal_type = EntityField()
        self.id = EntityField()
        self.internal_name = EntityField()
        self.is_hidden = EntityField()
        self.is_tombstone = EntityField()
        self.monthly_funding = EntityField()
        self.name = EntityField()
        self.note = EntityField()
        self.sortable_index = EntityField()
        self.target_balance = EntityField()
        self.target_balance_month = EntityField()
        self.type = EntityField()
        Entity.__init__(self)


class PayeeLocation(Entity):
    def __init__(self):
        self.entities_payee_id = EntityField()
        self.id = EntityField()
        self.is_tombstone = EntityField()
        self.latitude = EntityField()
        self.longitude = EntityField()
        Entity.__init__(self)


class AccountCalculation(Entity):
    def __init__(self):
        self.cleared_balance = EntityField()
        self.entities_account_id = EntityField()
        self.error_count = EntityField()
        self.id = EntityField()
        self.info_count = EntityField()
        self.is_tombstone = EntityField()
        self.month = EntityField()
        self.transaction_count = EntityField()
        self.uncleared_balance = EntityField()
        self.warning_count = EntityField()
        Entity.__init__(self)


class MonthlyAccountCalculation(Entity):
    def __init__(self):
        self.cleared_balance = EntityField()
        self.entities_account_id = EntityField()
        self.error_count = EntityField()
        self.id = EntityField()
        self.info_count = EntityField()
        self.is_tombstone = EntityField()
        self.month = EntityField()
        self.transaction_count = EntityField()
        self.uncleared_balance = EntityField()
        self.warning_count = EntityField()
        Entity.__init__(self)


class MonthlySubcategoryBudgetCalculation(Entity):
    def __init__(self):
        self.all_spending = EntityField()
        self.all_spending_since_last_payment = EntityField()
        self.balance = EntityField()
        self.balance_previous_month = EntityField()
        self.budgeted_average = EntityField()
        self.budgeted_cash_outflows = EntityField()
        self.budgeted_credit_outflows = EntityField()
        self.budgeted_previous_month = EntityField()
        self.budgeted_spending = EntityField()
        self.cash_outflows = EntityField()
        self.credit_outflows = EntityField()
        self.entities_monthly_subcategory_budget_id = EntityField()
        self.goal_expected_completion = EntityField()
        self.goal_overall_funded = EntityField()
        self.goal_overall_left = EntityField()
        self.goal_target = EntityField()
        self.goal_under_funded = EntityField()
        self.id = EntityField()
        self.is_tombstone = EntityField()
        self.overspending_affects_buffer = EntityField()
        self.payment_average = EntityField()
        self.payment_previous_month = EntityField()
        self.spent_average = EntityField()
        self.spent_previous_month = EntityField()
        self.unbudgeted_cash_outflows = EntityField()
        self.unbudgeted_credit_outflows = EntityField()
        self.upcoming_transactions = EntityField()
        Entity.__init__(self)


class ScheduledTransaction(Entity):
    def __init__(self):
        self.amount = EntityField()
        self.date = EntityField()
        self.entities_account_id = EntityField()
        self.entities_payee_id = EntityField()
        self.entities_subcategory_id = EntityField()
        self.flag = EntityField()
        self.frequency = EntityField()
        self.id = EntityField()
        self.is_tombstone = EntityField()
        self.memo = EntityField()
        self.transfer_account_id = EntityField()
        self.upcoming_instances = EntityField()
        Entity.__init__(self)


class Payee(Entity):
    def __init__(self):
        self.auto_fill_amount = EntityField()
        self.auto_fill_amount_enabled = EntityField()
        self.auto_fill_memo = EntityField()
        self.auto_fill_memo_enabled = EntityField()
        self.auto_fill_subcategory_enabled = EntityField()
        self.auto_fill_subcategory_id = EntityField()
        self.enabled = EntityField()
        self.entities_account_id = EntityField()
        self.id = EntityField()
        self.internal_name = EntityField()
        self.is_tombstone = EntityField()
        self.name = EntityField()
        self.rename_on_import_enabled = EntityField()
        Entity.__init__(self)


class MonthlySubcategoryBudget(Entity):
    def __init__(self):
        self.budgeted = EntityField()
        self.entities_monthly_budget_id = EntityField()
        self.entities_subcategory_id = EntityField()
        self.id = EntityField()
        self.is_tombstone = EntityField()
        self.note = EntityField()
        self.overspending_handling = EntityField()
        Entity.__init__(self)


class PayeeRenameCondition(Entity):
    def __init__(self):
        self.entities_payee_id = EntityField()
        self.id = EntityField()
        self.is_tombstone = EntityField()
        self.operand = EntityField()
        self.operator = EntityField()
        Entity.__init__(self)


class Account(Entity):
    def __init__(self):
        self.account_name = EntityField()
        self.account_type = EntityField()
        self.direct_connect_account_id = EntityField()
        self.direct_connect_enabled = EntityField()
        self.direct_connect_institution_id = EntityField()
        self.hidden = EntityField()
        self.id = EntityField()
        self.is_tombstone = EntityField()
        self.last_entered_check_number = EntityField()
        self.last_imported_at = EntityField()
        self.last_imported_error_code = EntityField()
        self.last_reconciled_balance = EntityField()
        self.last_reconciled_date = EntityField()
        self.note = EntityField()
        self.on_budget = EntityField()
        self.sortable_index = EntityField()
        Entity.__init__(self)


class BudgetBudget(Entity):
    def __init__(self):
        self.be_transactions = ListofEntities(Transaction)
        self.be_master_categories = ListofEntities(MasterCategory)
        self.be_settings = ListofEntities(Setting)
        self.be_monthly_budget_calculations = ListofEntities(MonthlyBudgetCalculation)
        self.be_account_mappings = ListofEntities(AccountMapping)
        self.be_subtransactions = ListofEntities(Subtransaction)
        self.be_scheduled_subtransactions = ListofEntities(ScheduledSubtransaction)
        self.be_monthly_budgets = ListofEntities(MonthlyBudget)
        self.be_subcategories = ListofEntities(Subcategory)
        self.be_payee_locations = ListofEntities(PayeeLocation)
        self.be_account_calculations = ListofEntities(AccountCalculation)
        self.be_monthly_account_calculations = ListofEntities(MonthlyAccountCalculation)
        self.be_monthly_subcategory_budget_calculations = ListofEntities(MonthlySubcategoryBudgetCalculation)
        self.be_scheduled_transactions = ListofEntities(ScheduledTransaction)
        self.be_payees = ListofEntities(Payee)
        self.be_monthly_subcategory_budgets = ListofEntities(MonthlySubcategoryBudget)
        self.be_payee_rename_conditions = ListofEntities(PayeeRenameCondition)
        self.be_accounts = ListofEntities(Account)

        self.last_month = EntityField()
        self.first_month = EntityField()
        Entity.__init__(self)

        self.knowledge = 0
        self.current_knowledge = 0
        self.server_knowledge_of_device = 0
        self.device_knowledge_of_server = 0
