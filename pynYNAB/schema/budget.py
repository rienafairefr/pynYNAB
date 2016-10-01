from pynYNAB.Entity import Entity, undef, on_budget_dict, AccountTypes
from pynYNAB.schema.Fields import EntityField, AmountField, DateField, AccountTypeField, EntityListField, DatesField, \
    PropertyField


class Transaction(Entity):
    accepted=EntityField(True)
    amount=AmountField()
    cash_amount=AmountField()
    check_number=EntityField(None)
    cleared=EntityField('Uncleared')
    credit_amount=AmountField()
    date=DateField(None)
    date_entered_from_schedule=DateField(None)
    entities_account_id=EntityField(None)
    entities_payee_id=EntityField(None)
    entities_scheduled_transaction_id=EntityField(None)
    entities_subcategory_id=EntityField(None)
    flag=EntityField("")
    imported_date=DateField(None)
    imported_payee=EntityField(None)
    is_tombstone=EntityField(False)
    matched_transaction_id=EntityField(None)
    memo=EntityField(None)
    source=EntityField(None)
    subcategory_credit_amount_preceding=EntityField(0)
    transfer_account_id=EntityField(None)
    transfer_subtransaction_id=EntityField(None)
    transfer_transaction_id=EntityField(None)
    ynab_id=EntityField(None)


class MasterCategory(Entity):
    deletable=EntityField(True)
    internal_name=EntityField(None)
    is_hidden=EntityField(False)
    is_tombstone=EntityField(False)
    name=EntityField(None)
    note=EntityField(None)
    sortable_index=EntityField(None)


class Setting(Entity):
    setting_name=EntityField(None)
    setting_value=EntityField(None)


class MonthlyBudgetCalculation(Entity):
    additional_to_be_budgeted=AmountField()
    age_of_money=EntityField(None)
    available_to_budget=EntityField(None)
    balance=EntityField(None)
    budgeted=EntityField(None)
    calculation_notes=EntityField(None)
    cash_outflows=AmountField()
    credit_outflows=AmountField()
    deferred_income=AmountField()
    entities_monthly_budget_id=EntityField(None)
    hidden_balance=AmountField()
    hidden_budgeted=AmountField()
    hidden_cash_outflows=AmountField()
    hidden_credit_outflows=AmountField()
    immediate_income=AmountField()
    is_tombstone=EntityField(False)
    over_spent=AmountField()
    previous_income=AmountField()
    uncategorized_balance=AmountField()
    uncategorized_cash_outflows=AmountField()
    uncategorized_credit_outflows=AmountField()


class AccountMapping(Entity):
    date_sequence=DateField(None)
    entities_account_id=EntityField(None)
    hash=EntityField(None)
    fid=EntityField(None)
    is_tombstone=EntityField(False)
    salt=EntityField(None)
    shortened_account_id=EntityField(None)
    should_flip_payees_memos=EntityField(None)
    should_import_memos=EntityField(None)
    skip_import=EntityField(None)


class Subtransaction(Entity):
    amount=AmountField()
    cash_amount=AmountField()
    check_number=EntityField(None)
    credit_amount=AmountField()
    entities_payee_id=EntityField(None)
    entities_subcategory_id=EntityField(None)
    entities_transaction_id=EntityField(None)
    is_tombstone=EntityField(False)
    memo=EntityField(None)
    sortable_index=EntityField(0)
    subcategory_credit_amount_preceding=EntityField(0)
    transfer_account_id=EntityField(None)
    transfer_transaction_id=EntityField(None)


class ScheduledSubtransaction(Entity):
    amount=AmountField()
    entities_payee_id=EntityField(None)
    entities_scheduled_transaction_id=EntityField(None)
    entities_subcategory_id=EntityField(None)
    is_tombstone=EntityField(False)
    memo=EntityField(None)
    sortable_index=EntityField(0)
    transfer_account_id=EntityField(None)


class MonthlyBudget(Entity):
    is_tombstone=EntityField(False)
    month=EntityField(None)
    note=EntityField(None)


class Subcategory(Entity):
    entities_account_id=EntityField(None)
    entities_master_category_id=EntityField(None)
    goal_creation_month=EntityField(None)
    goal_type=EntityField(None)
    internal_name=EntityField(None)
    is_hidden=EntityField(False)
    is_tombstone=EntityField(False)
    monthly_funding=EntityField(None)
    name=EntityField(None)
    note=EntityField(None)
    sortable_index=EntityField(0)
    target_balance=AmountField()
    target_balance_month=EntityField(None)
    type=EntityField(None)


class PayeeLocation(Entity):
    entities_payee_id=EntityField(None)
    is_tombstone=EntityField(False)
    latitude=EntityField(None)
    longitude=EntityField(None)


class AccountCalculation(Entity):
    cleared_balance=AmountField()
    entities_account_id=EntityField(None)
    error_count=EntityField(None)
    info_count=EntityField(None)
    is_tombstone=EntityField(False)
    transaction_count=EntityField(None)
    uncleared_balance=AmountField()
    warning_count=EntityField(None)


class MonthlyAccountCalculation(Entity):
    cleared_balance=AmountField()
    entities_account_id=EntityField(None)
    error_count=EntityField(None)
    info_count=EntityField(None)
    is_tombstone=EntityField(False)
    month=EntityField(None)
    transaction_count=EntityField(None)
    uncleared_balance=AmountField()
    warning_count=EntityField(None)
    rolling_balance=AmountField()


class MonthlySubcategoryBudgetCalculation(Entity):
    additional_to_be_budgeted=EntityField(None)
    all_spending=AmountField()
    all_spending_since_last_payment=AmountField()
    balance=AmountField()
    balance_previous_month=AmountField()
    budgeted_average=AmountField()
    budgeted_cash_outflows=AmountField()
    budgeted_credit_outflows=AmountField()
    budgeted_previous_month=AmountField()
    budgeted_spending=AmountField()
    cash_outflows=AmountField()
    credit_outflows=AmountField()
    entities_monthly_subcategory_budget_id=EntityField(None)
    goal_expected_completion=EntityField(None)
    goal_overall_funded=AmountField()
    goal_overall_left=AmountField()
    goal_percentage_complete=EntityField(None)
    goal_target=EntityField(None)
    goal_under_funded=EntityField(None)
    is_tombstone=EntityField(False)
    overspending_affects_buffer=EntityField(None)
    payment_average=AmountField()
    payment_previous_month=AmountField()
    spent_average=AmountField()
    spent_previous_month=AmountField()
    unbudgeted_cash_outflows=AmountField()
    unbudgeted_credit_outflows=AmountField()
    upcoming_transactions=AmountField()
    upcoming_transactions_count=EntityField(None)
    positive_cash_outflows=AmountField()


class ScheduledTransaction(Entity):
    amount=AmountField()
    date=DateField(None)
    entities_account_id=EntityField(None)
    entities_payee_id=EntityField(None)
    entities_subcategory_id=EntityField(None)
    flag=EntityField(None)
    frequency=EntityField(None)
    is_tombstone=EntityField(False)
    memo=EntityField(None)
    transfer_account_id=EntityField(None)
    upcoming_instances=DatesField([])


class Payee(Entity):
    auto_fill_amount=AmountField()
    auto_fill_amount_enabled=EntityField(None)
    auto_fill_memo=EntityField(None)
    auto_fill_memo_enabled=EntityField(None)
    auto_fill_subcategory_enabled=EntityField(None)
    auto_fill_subcategory_id=EntityField(None)
    enabled=EntityField(True)
    entities_account_id=EntityField(None)
    internal_name=EntityField(None)
    is_tombstone=EntityField(False)
    name=EntityField(None)
    rename_on_import_enabled=EntityField(None)


class MonthlySubcategoryBudget(Entity):
    budgeted=AmountField()
    entities_monthly_budget_id=EntityField(None)
    entities_subcategory_id=EntityField(None)
    is_tombstone=EntityField(False)
    note=EntityField(None)
    overspending_handling=EntityField(None)


class TransactionGroup(Entity):
    be_transaction=EntityField(None)
    be_subtransactions=EntityField(None)
    be_matched_transaction=EntityField(None)


class PayeeRenameCondition(Entity):
    entities_payee_id=EntityField(None)
    is_tombstone=EntityField(False)
    operand=EntityField(None)
    operator=EntityField(None)


def on_budget_default(self):
    return on_budget_dict[self.account_type.value]


class Account(Entity):
    account_name=EntityField(None)
    account_type=AccountTypeField(AccountTypes.undef)
    direct_connect_account_id=EntityField(undef)
    direct_connect_enabled=EntityField(False)
    direct_connect_institution_id=EntityField(undef)
    hidden=EntityField(False)
    is_tombstone=EntityField(False)
    last_entered_check_number=EntityField(None)
    last_imported_at=EntityField(undef)
    last_imported_error_code=EntityField(undef)
    last_reconciled_balance=EntityField(None)
    last_reconciled_date=DateField(None)
    direct_connect_last_error_code=EntityField(None)
    direct_connect_last_imported_at=DateField(None)
    note=EntityField(None)
    sortable_index=EntityField(0)
    on_budget=PropertyField(on_budget_default)
