from Entity import Entity


class Transaction(Entity):
    def __init__(self):
        self.fields = [
            'accepted',
            'amount',
            'cash_amount',
            'check_number',
            'cleared',
            'credit_amount',
            'date',
            'date_entered_from_schedule',
            'entities_account_id',
            'entities_payee_id',
            'entities_scheduled_transaction_id',
            'entities_subcategory_id',
            'flag',
            'id',
            'imported_date',
            'imported_payee',
            'is_tombstone',
            'matched_transaction_id',
            'memo',
            'source',
            'transfer_account_id',
            'transfer_subtransaction_id',
            'transfer_transaction_id',
            'ynab_id'
        ]
        Entity.__init__(self)


class MasterCategory(Entity):
    def __init__(self):
        self.fields = [
            'deletable',
            'id',
            'internal_name',
            'is_hidden',
            'is_tombstone',
            'name',
            'note'
            'sortable_index'
        ]
        Entity.__init__(self)


class Setting(Entity):
    def __init__(self):
        self.fields = [
            'id',
            'setting_name',
            'setting_value'
        ]
        Entity.__init__(self)


class MonthlyBudgetCalculation(Entity):
    def __init__(self):
        self.fields = [
            'additional_to_be_budgeted',
            'age_of_money',
            'available_to_budget',
            'balance',
            'budgeted',
            'calculation_notes',
            'cash_outflows',
            'credit_outflows',
            'deferred_income',
            'entities_monthly_budget_id',
            'hidden_balance',
            'hidden_budgeted',
            'hidden_cash_outflows',
            'hidden_credit_outflows',
            'id',
            'immediate_income',
            'is_tombstone',
            'over_spent',
            'previous_income',
            'uncategorized_balance',
            'uncategorized_cash_outflows',
            'uncategorized_credit_outflows'
        ]
        Entity.__init__(self)


class AccountMapping(Entity):
    def __init__(self):
        self.fields = [
            'date_sequence',
            'entities_account_id',
            'fid',
            'hash',
            'id',
            'is_tombstone',
            'salt',
            'shortened_account_id',
            'should_flip_payees_memos',
            'should_import_memos',
            'skip_import'
        ]
        Entity.__init__(self)


class Subtransaction(Entity):
    def __init__(self):
        self.fields = [
            'amount',
            'cash_amount',
            'check_number',
            'credit_amount',
            'entities_payee_id',
            'entities_subcategory_id',
            'entities_transaction_id',
            'id',
            'is_tombstone',
            'memo',
            'sortable_index',
            'transfer_account_id',
            'transfer_transaction_id'
        ]
        Entity.__init__(self)


class ScheduledSubtransaction(Entity):
    def __init__(self):
        self.fields = [
            'amount',
            'entities_payee_id',
            'entities_scheduled_transaction_id',
            'entities_subcategory_id',
            'id',
            'is_tombstone',
            'memo',
            'sortable_index',
            'transfer_account_id'
        ]
        Entity.__init__(self)


class MonthlyBudget(Entity):
    def __init__(self):
        self.fields = [
            'id',
            'is_tombstone'
            'month'
            'note'
        ]
        Entity.__init__(self)


class Subcategory(Entity):
    def __init__(self):
        self.fields = [
            'entities_account_id',
            'entities_master_category_id',
            'goal_creation_month',
            'goal_type',
            'id',
            'internal_name',
            'is_hidden',
            'is_tombstone',
            'monthly_funding',
            'name',
            'note',
            'sortable_index',
            'target_balance',
            'target_balance_month',
            'type'
        ]
        Entity.__init__(self)


class PayeeLocation(Entity):
    def __init__(self):
        self.fields = [
            'entities_payee_id'
            'id',
            'is_tombstone',
            'latitude'
            'longitude'
        ]
        Entity.__init__(self)


class AccountCalculation(Entity):
    def __init__(self):
        self.fields = [
            'cleared_balance',
            'entities_account_id',
            'error_count'
            'id',
            'info_count',
            'is_tombstone',
            'month',
            'transaction_count',
            'uncleared_balance',
            'warning_count'
        ]
        Entity.__init__(self)


class MonthlyAccountCalculation(Entity):
    def __init__(self):
        self.fields = [
            'cleared_balance',
            'entities_account_id',
            'error_count',
            'id',
            'info_count',
            'is_tombstone',
            'month',
            'transaction_count',
            'uncleared_balance',
            'warning_count'
        ]
        Entity.__init__(self)


class MonthlySubcategoryBudgetCalculation(Entity):
    def __init__(self):
        self.fields = [
            'all_spending',
            'all_spending_since_last_payment',
            'balance',
            'balance_previous_month',
            'budgeted_average',
            'budgeted_cash_outflows',
            'budgeted_credit_outflows',
            'budgeted_previous_month',
            'budgeted_spending',
            'cash_outflows',
            'credit_outflows',
            'entities_monthly_subcategory_budget_id',
            'goal_expected_completion',
            'goal_overall_funded',
            'goal_overall_left',
            'goal_target',
            'goal_under_funded',
            'id',
            'is_tombstone',
            'overspending_affects_buffer',
            'payment_average',
            'payment_previous_month',
            'spent_average',
            'spent_previous_month',
            'unbudgeted_cash_outflows',
            'unbudgeted_credit_outflows',
            'upcoming_transactions'
        ]
        Entity.__init__(self)


class ScheduledTransaction(Entity):
    def __init__(self):
        self.fields = [
            'amount',
            'date',
            'entities_account_id',
            'entities_payee_id',
            'entities_subcategory_id',
            'flag',
            'frequency',
            'id',
            'is_tombstone',
            'memo',
            'transfer_account_id',
            'upcoming_instances'
        ]
        Entity.__init__(self)


class Payee(Entity):
    def __init__(self):
        self.fields = [
            'auto_fill_amount',
            'auto_fill_amount_enabled',
            'auto_fill_memo',
            'auto_fill_memo_enabled',
            'auto_fill_subcategory_enabled',
            'auto_fill_subcategory_id',
            'enabled',
            'entities_account_id',
            'id',
            'internal_name',
            'is_tombstone',
            'name',
            'rename_on_import_enabled'
        ]
        Entity.__init__(self)


class MonthlySubcategoryBudget(Entity):
    def __init__(self):
        self.fields = [
            'budgeted',
            'entities_monthly_budget_id',
            'entities_subcategory_id',
            'id',
            'is_tombstone',
            'note',
            'overspending_handling'
        ]
        Entity.__init__(self)


class PayeeRenameCondition(Entity):
    def __init__(self):
        self.fields = [
            'entities_payee_id',
            'id',
            'is_tombstone',
            'operand',
            'operator'
        ]
        Entity.__init__(self)


class Account(Entity):
    def __init__(self):
        self.fields = [
            'account_name',
            'account_type',
            'direct_connect_account_id',
            'direct_connect_enabled',
            'direct_connect_institution_id',
            'hidden',
            'id',
            'is_tombstone',
            'last_entered_check_number',
            'last_imported_at',
            'last_imported_error_code',
            'last_reconciled_balance',
            'last_reconciled_date',
            'note',
            'on_budget',
            'sortable_index'
        ]
        Entity.__init__(self)


class BudgetBudget(Entity):
    def __init__(self):
        self.listfields = {
            'be_transactions': Transaction,
            'be_master_categories': MasterCategory,
            'be_settings': Setting,
            'be_monthly_budget_calculations': MonthlyBudgetCalculation,
            'be_account_mappings': AccountMapping,
            'be_subtransactions': Subtransaction,
            'be_scheduled_subtransactions': ScheduledSubtransaction,
            'be_monthly_budgets': MonthlyBudget,
            'be_subcategories': Subcategory,
            'be_payee_locations': PayeeLocation,
            'be_account_calculations': AccountCalculation,
            'be_monthly_account_calculations': MonthlyAccountCalculation,
            'be_monthly_subcategory_budget_calculations': MonthlySubcategoryBudgetCalculation,
            'be_scheduled_transactions': ScheduledTransaction,
            'be_payees': Payee,
            'be_monthly_subcategory_budgets': MonthlySubcategoryBudget,
            'be_payee_rename_conditions': PayeeRenameCondition,
            'be_accounts': Account
        }
        self.fields = [
            'last_month',
            'first_month'
        ]
        Entity.__init__(self)

        self.knowledge = 0
        self.current_knowledge = 0
        self.server_knowledge_of_device = 0
