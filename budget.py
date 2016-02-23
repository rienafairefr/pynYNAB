from Entity import Entity, ListofEntities, EntityField, Fields, undef


class Transaction(Entity):
    def __init__(self):
        self.accepted = None
        self.amount = None
        self.cash_amount = None
        self.check_number = None
        self.cleared = None
        self.credit_amount = None
        self.date = None
        self.date_entered_from_schedule = None
        self.entities_account_id = None
        self.entities_payee_id = None
        self.entities_scheduled_transaction_id = None
        self.entities_subcategory_id = None
        self.flag = None
        self.id = None
        self.imported_date = None
        self.imported_payee = None
        self.is_tombstone = None
        self.matched_transaction_id = None
        self.memo = None
        self.source = None
        self.transfer_account_id = None
        self.transfer_subtransaction_id = None
        self.transfer_transaction_id = None
        self.ynab_id = None
        Fields.register(self)

        super(Transaction, self).__init__()




class MasterCategory(Entity):
    def __init__(self):
        self.deletable = None
        self.id = None
        self.internal_name = None
        self.is_hidden = None
        self.is_tombstone = None
        self.name = None
        self.note = None
        self.sortable_index = None

        Fields.register(self)
        super(MasterCategory, self).__init__()


class Setting(Entity):
    def __init__(self):
        self.id = None
        self.setting_name = None
        self.setting_value = None

        Fields.register(self)
        super(Setting, self).__init__()


class MonthlyBudgetCalculation(Entity):
    def __init__(self):
        self.additional_to_be_budgeted = None
        self.age_of_money = None
        self.available_to_budget = None
        self.balance = None
        self.budgeted = None
        self.calculation_notes = None
        self.cash_outflows = None
        self.credit_outflows = None
        self.deferred_income = None
        self.entities_monthly_budget_id = None
        self.hidden_balance = None
        self.hidden_budgeted = None
        self.hidden_cash_outflows = None
        self.hidden_credit_outflows = None
        self.id = None
        self.immediate_income = None
        self.is_tombstone = None
        self.over_spent = None
        self.previous_income = None
        self.uncategorized_balance = None
        self.uncategorized_cash_outflows = None
        self.uncategorized_credit_outflows = None

        Fields.register(self)
        super(MonthlyBudgetCalculation, self).__init__()


class AccountMapping(Entity):
    def __init__(self):
        self.date_sequence = None
        self.entities_account_id = None
        self.fid = None
        self.hash = None
        self.id = None
        self.is_tombstone = None
        self.salt = None
        self.shortened_account_id = None
        self.should_flip_payees_memos = None
        self.should_import_memos = None
        self.skip_import = None

        Fields.register(self)
        super(AccountMapping, self).__init__()


class Subtransaction(Entity):
    def __init__(self):
        self.amount = None
        self.cash_amount = None
        self.check_number = None
        self.credit_amount = None
        self.entities_payee_id = None
        self.entities_subcategory_id = None
        self.entities_transaction_id = None
        self.id = None
        self.is_tombstone = None
        self.memo = None
        self.sortable_index = None
        self.transfer_account_id = None
        self.transfer_transaction_id = None

        Fields.register(self)
        super(Subtransaction, self).__init__()


class ScheduledSubtransaction(Entity):
    def __init__(self):
        self.amount = None
        self.entities_payee_id = None
        self.entities_scheduled_transaction_id = None
        self.entities_subcategory_id = None
        self.id = None
        self.is_tombstone = None
        self.memo = None
        self.sortable_index = None
        self.transfer_account_id = None

        Fields.register(self)
        super(ScheduledSubtransaction, self).__init__()


class MonthlyBudget(Entity):
    def __init__(self):
        self.id = None
        self.is_tombstone = None
        self.month = None
        self.note = None

        Fields.register(self)
        super(MonthlyBudget, self).__init__()


class Subcategory(Entity):
    def __init__(self):
        self.entities_account_id = None
        self.entities_master_category_id = None
        self.goal_creation_month = None
        self.goal_type = None
        self.id = None
        self.internal_name = None
        self.is_hidden = None
        self.is_tombstone = None
        self.monthly_funding = None
        self.name = None
        self.note = None
        self.sortable_index = None
        self.target_balance = None
        self.target_balance_month = None
        self.type = None

        Fields.register(self)
        super(Subcategory, self).__init__()


class PayeeLocation(Entity):
    def __init__(self):
        self.entities_payee_id = None
        self.id = None
        self.is_tombstone = None
        self.latitude = None
        self.longitude = None

        Fields.register(self)
        super(PayeeLocation, self).__init__()


class AccountCalculation(Entity):
    def __init__(self):
        self.cleared_balance = None
        self.entities_account_id = None
        self.error_count = None
        self.id = None
        self.info_count = None
        self.is_tombstone = None
        self.transaction_count = None
        self.uncleared_balance = None
        self.warning_count = None
        Fields.register(self)
        super(AccountCalculation, self).__init__()


class MonthlyAccountCalculation(Entity):
    def __init__(self):
        self.cleared_balance = None
        self.entities_account_id = None
        self.error_count = None
        self.id = None
        self.info_count = None
        self.is_tombstone = None
        self.month = None
        self.transaction_count = None
        self.uncleared_balance = None
        self.warning_count = None

        Fields.register(self)
        super(MonthlyAccountCalculation, self).__init__()


class MonthlySubcategoryBudgetCalculation(Entity):
    def __init__(self):
        self.all_spending = None
        self.all_spending_since_last_payment = None
        self.balance = None
        self.balance_previous_month = None
        self.budgeted_average = None
        self.budgeted_cash_outflows = None
        self.budgeted_credit_outflows = None
        self.budgeted_previous_month = None
        self.budgeted_spending = None
        self.cash_outflows = None
        self.credit_outflows = None
        self.entities_monthly_subcategory_budget_id = None
        self.goal_expected_completion = None
        self.goal_overall_funded = None
        self.goal_overall_left = None
        self.goal_target = None
        self.goal_under_funded = None
        self.id = None
        self.is_tombstone = None
        self.overspending_affects_buffer = None
        self.payment_average = None
        self.payment_previous_month = None
        self.spent_average = None
        self.spent_previous_month = None
        self.unbudgeted_cash_outflows = None
        self.unbudgeted_credit_outflows = None
        self.upcoming_transactions = None

        Fields.register(self)
        super(MonthlySubcategoryBudgetCalculation, self).__init__()


class ScheduledTransaction(Entity):
    def __init__(self):
        self.amount = None
        self.date = None
        self.entities_account_id = None
        self.entities_payee_id = None
        self.entities_subcategory_id = None
        self.flag = None
        self.frequency = None
        self.id = None
        self.is_tombstone = None
        self.memo = None
        self.transfer_account_id = None
        self.upcoming_instances = None

        Fields.register(self)
        super(ScheduledTransaction, self).__init__()


class Payee(Entity):
    def __init__(self):
        self.auto_fill_amount = None
        self.auto_fill_amount_enabled = None
        self.auto_fill_memo = None
        self.auto_fill_memo_enabled = None
        self.auto_fill_subcategory_enabled = None
        self.auto_fill_subcategory_id = None
        self.enabled = None
        self.entities_account_id = None
        self.id = None
        self.internal_name = None
        self.is_tombstone = None
        self.name = None
        self.rename_on_import_enabled = None

        Fields.register(self)
        super(Payee, self).__init__()


class MonthlySubcategoryBudget(Entity):
    def __init__(self):
        self.budgeted = None
        self.entities_monthly_budget_id = None
        self.entities_subcategory_id = None
        self.id = None
        self.is_tombstone = None
        self.note = None
        self.overspending_handling = None

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
        self.entities_payee_id = None
        self.id = None
        self.is_tombstone = None
        self.operand = None
        self.operator = None

        Fields.register(self)
        super(PayeeRenameCondition, self).__init__()


class Account(Entity):
    def __init__(self):
        self.account_name = None
        self.account_type = None
        self.direct_connect_account_id = undef
        self.direct_connect_enabled = None
        self.direct_connect_institution_id = undef
        self.hidden = None
        self.id = None
        self.is_tombstone = None
        self.last_entered_check_number = None
        self.last_imported_at = undef
        self.last_imported_error_code = undef
        self.last_reconciled_balance = None
        self.last_reconciled_date = None
        self.note = None
        self.on_budget = None
        self.sortable_index = None

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

        self.last_month = None
        self.first_month = None

        Fields.register(self)
        super(BudgetBudget, self).__init__()

        self.knowledge = 0
        self.current_knowledge = 0
        self.server_knowledge_of_device = 0
        self.device_knowledge_of_server = 0


