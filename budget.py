from Entity import Entity, ListofEntities, EntityField, Fields


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
        Fields.register(self)

        super(Transaction, self).__init__()


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

        Fields.register(self)
        super(MasterCategory, self).__init__()


class Setting(Entity):
    def __init__(self):
        self.id = EntityField()
        self.setting_name = EntityField()
        self.setting_value = EntityField()

        Fields.register(self)
        super(Setting, self).__init__()


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

        Fields.register(self)
        super(MonthlyBudgetCalculation, self).__init__()


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

        Fields.register(self)
        super(AccountMapping, self).__init__()


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

        Fields.register(self)
        super(Subtransaction, self).__init__()


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

        Fields.register(self)
        super(ScheduledSubtransaction, self).__init__()


class MonthlyBudget(Entity):
    def __init__(self):
        self.id = EntityField()
        self.is_tombstone = EntityField()
        self.month = EntityField()
        self.note = EntityField()

        Fields.register(self)
        super(MonthlyBudget, self).__init__()


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

        Fields.register(self)
        super(Subcategory, self).__init__()


class PayeeLocation(Entity):
    def __init__(self):
        self.entities_payee_id = EntityField()
        self.id = EntityField()
        self.is_tombstone = EntityField()
        self.latitude = EntityField()
        self.longitude = EntityField()

        Fields.register(self)
        super(PayeeLocation, self).__init__()


class AccountCalculation(Entity):
    def __init__(self):
        self.cleared_balance = EntityField()
        self.entities_account_id = EntityField()
        self.error_count = EntityField()
        self.id = EntityField()
        self.info_count = EntityField()
        self.is_tombstone = EntityField()
        self.transaction_count = EntityField()
        self.uncleared_balance = EntityField()
        self.warning_count = EntityField()
        Fields.register(self)
        super(AccountCalculation, self).__init__()


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

        Fields.register(self)
        super(MonthlyAccountCalculation, self).__init__()


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

        Fields.register(self)
        super(MonthlySubcategoryBudgetCalculation, self).__init__()


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

        Fields.register(self)
        super(ScheduledTransaction, self).__init__()


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

        Fields.register(self)
        super(Payee, self).__init__()


class MonthlySubcategoryBudget(Entity):
    def __init__(self):
        self.budgeted = EntityField()
        self.entities_monthly_budget_id = EntityField()
        self.entities_subcategory_id = EntityField()
        self.id = EntityField()
        self.is_tombstone = EntityField()
        self.note = EntityField()
        self.overspending_handling = EntityField()

        Fields.register(self)
        super(MonthlySubcategoryBudget, self).__init__()


class TransactionGroup(Entity):
    def __init__(self):
        self.be_transaction=EntityField()
        self.be_subtransactions=EntityField()
        self.be_matched_transaction=EntityField()

        Fields.register(self)
        super(TransactionGroup, self).__init__()


class PayeeRenameCondition(Entity):
    def __init__(self):
        self.entities_payee_id = EntityField()
        self.id = EntityField()
        self.is_tombstone = EntityField()
        self.operand = EntityField()
        self.operator = EntityField()

        Fields.register(self)
        super(PayeeRenameCondition, self).__init__()


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

        Fields.register(self)
        super(Account, self).__init__()


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

        Fields.register(self)
        super(BudgetBudget, self).__init__()

        self.knowledge = 0
        self.current_knowledge = 0
        self.server_knowledge_of_device = 0
        self.device_knowledge_of_server = 0


