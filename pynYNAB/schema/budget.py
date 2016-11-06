from sqlalchemy import Boolean, types
from sqlalchemy import Column
from sqlalchemy import Date
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.orm import relationship

from pynYNAB.Entity import Entity, undef, on_budget_dict, AccountTypes, Base
from pynYNAB.schema.Fields import EntityField, AmountField, DateField, AccountTypeField, EntityListField, DatesField, \
    PropertyField


class AmountType(types.TypeDecorator):
    impl = types.Integer

    def load_dialect_impl(self, dialect):
        return dialect.type_descriptor(types.Integer)

    def process_bind_param(self, value, dialect):
        return int(value * 100) if value is not None else None

    def process_result_value(self, value, dialect):
        return float(value) / 100 if value is not None else None


class BudgetEntity(Entity):
    @declared_attr
    def parent_id(self):
        return Column(ForeignKey('budget.id'))

    @declared_attr
    def parent(self):
        return relationship('Budget')


class Transaction(Base, BudgetEntity):
    accepted = Column(Boolean, default=True)
    amount = Column(AmountType)
    cash_amount = Column(AmountType)
    check_number = Column(String)
    cleared = Column(String, default='Uncleared')
    credit_amount = Column(AmountType)
    date = Column(Date)
    date_entered_from_schedule = Column(Date)
    entities_account_id = Column(ForeignKey('account.id'))
    entities_account = relationship('Account',foreign_keys=entities_account_id)
    entities_payee_id = Column(ForeignKey('payee.id'))
    entities_payee = relationship('Payee')
    entities_scheduled_transaction_id = Column(ForeignKey('scheduledtransaction.id'))
    entities_subcategory_id = Column(ForeignKey('subcategory.id'))
    flag = Column(String, default="")
    imported_date = Column(Date)
    imported_payee = Column(String)
    is_tombstone = Column(Boolean, default=False)
    matched_transaction_id = Column(String)
    memo = Column(String)
    source = Column(String)
    subcategory_credit_amount_preceding = Column(AmountType, default=0)
    transfer_account_id = Column(ForeignKey('account.id'))
    transfer_account=relationship('Account',foreign_keys=transfer_account_id)
    transfer_subtransaction_id = Column(ForeignKey('subtransaction.id'))
    transfer_transaction_id = Column(ForeignKey('transaction.id'))
    transfer_transaction = relationship('Transaction')
    ynab_id = Column(String)


class MasterCategory(Base, BudgetEntity):
    deletable = Column(Boolean, default=True)
    internal_name = Column(String)
    is_hidden = Column(Boolean, default=False)
    is_tombstone = Column(Boolean, default=False)
    name = Column(String)
    note = Column(String)
    sortable_index = Column(String)


class Setting(Base, BudgetEntity):
    setting_name = Column(String)
    setting_value = Column(String)


class MonthlyBudgetCalculation(Base, BudgetEntity):
    additional_to_be_budgeted = Column(AmountType)
    age_of_money = Column(String)
    available_to_budget = Column(String)
    balance = Column(String)
    budgeted = Column(String)
    calculation_notes = Column(String)
    cash_outflows = Column(AmountType)
    credit_outflows = Column(AmountType)
    deferred_income = Column(AmountType)
    entities_monthly_budget_id = Column(ForeignKey('monthlybudget.id'))
    entities_monthly_budget = relationship('MonthlyBudget')
    hidden_balance = Column(AmountType)
    hidden_budgeted = Column(AmountType)
    hidden_cash_outflows = Column(AmountType)
    hidden_credit_outflows = Column(AmountType)
    immediate_income = Column(AmountType)
    is_tombstone = EntityField(False)
    over_spent = Column(AmountType)
    previous_income = Column(AmountType)
    uncategorized_balance = Column(AmountType)
    uncategorized_cash_outflows = Column(AmountType)
    uncategorized_credit_outflows = Column(AmountType)


class AccountMapping(Base, BudgetEntity):
    date_sequence = DateField(None)
    entities_account_id = Column(String)
    hash = Column(String)
    fid = Column(String)
    is_tombstone = EntityField(False)
    salt = Column(String)
    shortened_account_id = Column(String)
    should_flip_payees_memos = Column(String)
    should_import_memos = Column(String)
    skip_import = Column(String)


class Subtransaction(Base, BudgetEntity):
    amount = Column(AmountType)
    cash_amount = Column(AmountType)
    check_number = Column(String)
    credit_amount = Column(AmountType)
    entities_payee_id = Column(ForeignKey('payee.id'))
    entities_payee = relationship('Payee')
    entities_subcategory_id = Column(ForeignKey('subcategory.id'))
    entities_transaction_id = Column(ForeignKey('transaction.id'))
    entities_transaction = relationship('Transaction',foreign_keys=entities_transaction_id)
    is_tombstone = Column(Boolean,default=False)
    memo = Column(String)
    sortable_index = Column(Integer,default=0)
    subcategory_credit_amount_preceding = Column(Integer,default=0)
    transfer_account_id = Column(ForeignKey('account.id'))
    transfer_account = relationship('Account')
    transfer_transaction_id = Column(ForeignKey('transaction.id'))
    transfer_transaction = relationship('Transaction',backref='transfer_subtransaction',foreign_keys=transfer_transaction_id)



class ScheduledSubtransaction(Base, BudgetEntity):
    amount = Column(AmountType)
    entities_payee_id = Column(String)
    entities_scheduled_transaction_id = Column(String)
    entities_subcategory_id = Column(String)
    is_tombstone = EntityField(False)
    memo = Column(String)
    sortable_index = EntityField(0)
    transfer_account_id = Column(String)


class MonthlyBudget(Base, BudgetEntity):
    is_tombstone = EntityField(False)
    month = Column(String)
    note = Column(String)


class Subcategory(Base, BudgetEntity):
    entities_account_id = Column(String)
    entities_master_category_id = Column(String)
    goal_creation_month = Column(String)
    goal_type = Column(String)
    internal_name = Column(String)
    is_hidden = EntityField(False)
    is_tombstone = EntityField(False)
    monthly_funding = Column(String)
    name = Column(String)
    note = Column(String)
    sortable_index = EntityField(0)
    target_balance = Column(AmountType)
    target_balance_month = Column(String)
    type = Column(String)

    transaction = relationship(Transaction, backref='entities_subcategory')
    subtransaction = relationship(Subtransaction,backref='entities_subcategory')


class PayeeLocation(Base, BudgetEntity):
    entities_payee_id = Column(String)
    is_tombstone = EntityField(False)
    latitude = Column(String)
    longitude = Column(String)


class AccountCalculation(Base, BudgetEntity):
    cleared_balance = Column(AmountType)
    entities_account_id = Column(String)
    error_count = Column(String)
    info_count = Column(String)
    is_tombstone = EntityField(False)
    transaction_count = Column(String)
    uncleared_balance = Column(AmountType)
    warning_count = Column(String)


class MonthlyAccountCalculation(Base, BudgetEntity):
    cleared_balance = Column(AmountType)
    entities_account_id = Column(String)
    error_count = Column(String)
    info_count = Column(String)
    is_tombstone = EntityField(False)
    month = Column(String)
    transaction_count = Column(String)
    uncleared_balance = Column(AmountType)
    warning_count = Column(String)
    rolling_balance = Column(AmountType)


class MonthlySubcategoryBudgetCalculation(Base, BudgetEntity):
    additional_to_be_budgeted = Column(String)
    all_spending = Column(AmountType)
    all_spending_since_last_payment = Column(AmountType)
    balance = Column(AmountType)
    balance_previous_month = Column(AmountType)
    budgeted_average = Column(AmountType)
    budgeted_cash_outflows = Column(AmountType)
    budgeted_credit_outflows = Column(AmountType)
    budgeted_previous_month = Column(AmountType)
    budgeted_spending = Column(AmountType)
    cash_outflows = Column(AmountType)
    credit_outflows = Column(AmountType)
    entities_monthly_subcategory_budget_id = Column(String)
    goal_expected_completion = Column(String)
    goal_overall_funded = Column(AmountType)
    goal_overall_left = Column(AmountType)
    goal_percentage_complete = Column(String)
    goal_target = Column(String)
    goal_under_funded = Column(String)
    is_tombstone = EntityField(False)
    overspending_affects_buffer = Column(String)
    payment_average = Column(AmountType)
    payment_previous_month = Column(AmountType)
    spent_average = Column(AmountType)
    spent_previous_month = Column(AmountType)
    unbudgeted_cash_outflows = Column(AmountType)
    unbudgeted_credit_outflows = Column(AmountType)
    upcoming_transactions = Column(AmountType)
    upcoming_transactions_count = Column(String)
    positive_cash_outflows = Column(AmountType)


class ScheduledTransaction(Base, BudgetEntity):
    amount = Column(AmountType)
    date = DateField(None)
    entities_account_id = Column(String)
    entities_payee_id = Column(String)
    entities_subcategory_id = Column(String)
    transaction=relationship(Transaction, backref='entities_scheduled_transaction')
    flag = Column(String)
    frequency = Column(String)
    is_tombstone = EntityField(False)
    memo = Column(String)
    transfer_account_id = Column(String)
    upcoming_instances = DatesField([])


class Payee(Base, BudgetEntity):
    auto_fill_amount = Column(AmountType)
    auto_fill_amount_enabled = Column(String)
    auto_fill_memo = Column(String)
    auto_fill_memo_enabled = Column(String)
    auto_fill_subcategory_enabled = Column(String)
    auto_fill_subcategory_id = Column(String)
    enabled = EntityField(True)
    entities_account_id = Column(String)
    internal_name = Column(String)
    is_tombstone = EntityField(False)
    name = Column(String)
    rename_on_import_enabled = Column(String)


class MonthlySubcategoryBudget(Base, BudgetEntity):
    budgeted = Column(AmountType)
    entities_monthly_budget_id = Column(String)
    entities_subcategory_id = Column(String)
    is_tombstone = EntityField(False)
    note = Column(String)
    overspending_handling = Column(String)


class TransactionGroup(Base, BudgetEntity):
    be_transaction = Column(String)
    be_subtransactions = Column(String)
    be_matched_transaction = Column(String)


class PayeeRenameCondition(Base, BudgetEntity):
    entities_payee_id = Column(String)
    is_tombstone = EntityField(False)
    operand = Column(String)
    operator = Column(String)


def on_budget_default(self):
    return on_budget_dict[self.account_type.value]


class Account(Base, BudgetEntity):
    account_name = Column(String)
    account_type = AccountTypeField(AccountTypes.undef)
    direct_connect_account_id = EntityField(undef)
    direct_connect_enabled = EntityField(False)
    direct_connect_institution_id = EntityField(undef)
    hidden = EntityField(False)
    is_tombstone = EntityField(False)
    last_entered_check_number = Column(String)
    last_imported_at = EntityField(undef)
    last_imported_error_code = EntityField(undef)
    last_reconciled_balance = Column(String)
    last_reconciled_date = DateField(None)
    direct_connect_last_error_code = Column(String)
    direct_connect_last_imported_at = DateField(None)
    note = Column(String)
    sortable_index = EntityField(0)
    on_budget = PropertyField(on_budget_default)

class Budget(Base, Entity):
    def __init__(self):
        super(Budget, self).__init__()
        self.budget_version_id = None

    be_transactions = relationship('Transaction')
    be_master_categories = relationship('MasterCategory')
    be_settings = relationship('Setting')
    be_monthly_budget_calculations = relationship('MonthlyBudgetCalculation')
    be_account_mappings = relationship('AccountMapping')
    be_subtransactions = relationship('Subtransaction')
    be_scheduled_subtransactions = relationship('ScheduledSubtransaction')
    be_monthly_budgets = relationship('MonthlyBudget')
    be_subcategories = relationship('Subcategory')
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

    def get_request_data(self):
        request_data = super(Budget, self).get_request_data()
        request_data['budget_version_id'] = self.budget_version_id
        request_data['calculated_entities_included'] = False
        return request_data

    def get_changed_entities(self):
        changed_entities = super(Budget, self).get_changed_entities()
        if 'be_transactions' in changed_entities:
            changed_entities['be_transaction_groups'] = ListofEntities(TransactionGroup)
            for tr in changed_entities.pop('be_transactions'):
                subtransactions = ListofEntities(Subtransaction)
                if 'be_subtransactions' in changed_entities:
                    for subtr in [subtransaction for subtransaction in changed_entities.get('be_subtransactions') if
                                  subtransaction.entities_transaction_id == tr.id]:
                        changed_entities['be_subtransactions'].remove(subtr)
                        subtransactions.append(subtr)
                changed_entities['be_transaction_groups'].append(TransactionGroup(
                    id=tr.id,
                    be_transaction=tr,
                    be_subtransactions=subtransactions
                ))
        if changed_entities.get('be_subtransactions') is not None:
            del changed_entities['be_subtransactions']
        return changed_entities