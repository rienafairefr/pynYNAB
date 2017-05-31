from sqlalchemy import Boolean
from sqlalchemy import Column
from sqlalchemy import Date
from sqlalchemy import Enum
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.orm import relationship

from pynYNAB.schema.Entity import Entity, AccountTypes, Base
from pynYNAB.schema.types import AmountType


class BudgetEntity(Entity):
    @declared_attr
    def parent_id(self):
        return Column(ForeignKey('budget.id'))

    @declared_attr
    def parent(self):
        return relationship('Budget', lazy=False)


class Transaction(Base, BudgetEntity):
    accepted = Column(Boolean, default=True)
    amount = Column(AmountType)
    cash_amount = Column(AmountType)
    check_number = Column(String)
    cleared = Column(String, default='Uncleared')
    credit_amount = Column(AmountType)
    credit_amount_adjusted = Column(AmountType)
    date = Column(Date)
    date_entered_from_schedule = Column(Date)
    entities_account_id = Column(ForeignKey('account.id'))
    entities_account = relationship('Account', foreign_keys=entities_account_id)
    entities_payee_id = Column(ForeignKey('payee.id'))
    entities_payee = relationship('Payee')
    entities_scheduled_transaction_id = Column(ForeignKey('scheduledtransaction.id'))
    entities_subcategory_id = Column(ForeignKey('subcategory.id'))
    entities_subcategory = relationship('SubCategory')
    flag = Column(String, default=None)
    imported_date = Column(Date)
    imported_payee = Column(String)
    matched_transaction_id = Column(ForeignKey('transaction.id'))
    matched_transaction = relationship('Transaction', foreign_keys=matched_transaction_id)
    memo = Column(String)
    source = Column(String)
    subcategory_credit_amount_preceding = Column(AmountType, default=0)
    transfer_account_id = Column(ForeignKey('account.id'))
    transfer_account = relationship('Account', foreign_keys=transfer_account_id)
    transfer_subtransaction_id = Column(ForeignKey('subtransaction.id'))
    transfer_transaction_id = Column(ForeignKey('transaction.id'))
    transfer_transaction = relationship('Transaction', foreign_keys=transfer_transaction_id)
    ynab_id = Column(String)


class MasterCategory(Base, BudgetEntity):
    deletable = Column(Boolean, default=True)
    internal_name = Column(String)
    is_hidden = Column(Boolean, default=False)
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
    over_spent = Column(AmountType)
    previous_income = Column(AmountType)
    uncategorized_balance = Column(AmountType)
    uncategorized_cash_outflows = Column(AmountType)
    uncategorized_credit_outflows = Column(AmountType)


class AccountMapping(Base, BudgetEntity):
    date_sequence = Column(Date)
    entities_account_id = Column(ForeignKey('account.id'))
    entities_account = relationship('Account', foreign_keys=entities_account_id)
    hash = Column(String)
    fid = Column(String)
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
    entities_subcategory = relationship('SubCategory', foreign_keys=entities_subcategory_id)
    entities_transaction_id = Column(ForeignKey('transaction.id'))
    entities_transaction = relationship('Transaction', foreign_keys=entities_transaction_id)
    memo = Column(String)
    sortable_index = Column(Integer, default=0)
    subcategory_credit_amount_preceding = Column(Integer, default=0)
    transfer_account_id = Column(ForeignKey('account.id'))
    transfer_account = relationship('Account')
    transfer_transaction_id = Column(ForeignKey('transaction.id'))
    transfer_transaction = relationship('Transaction', backref='transfer_subtransaction',
                                        foreign_keys=transfer_transaction_id)


class ScheduledSubtransaction(Base, BudgetEntity):
    amount = Column(AmountType)
    entities_payee_id = Column(ForeignKey('payee.id'))
    entities_payee = relationship('Payee', foreign_keys=entities_payee_id)
    entities_scheduled_transaction_id = Column(ForeignKey('scheduledtransaction.id'))
    entities_scheduled_transaction = relationship('ScheduledTransaction',
                                                  foreign_keys=entities_scheduled_transaction_id)
    entities_subcategory_id = Column(ForeignKey('subcategory.id'))
    entities_subcategory = relationship('SubCategory', foreign_keys=entities_subcategory_id)
    memo = Column(String)
    sortable_index = Column(Integer, default=0)
    transfer_account_id = Column(ForeignKey('account.id'))
    transfer_account = relationship('Account', foreign_keys=transfer_account_id)


class MonthlyBudget(Base, BudgetEntity):
    month = Column(Date)
    note = Column(String)


class SubCategory(Base, BudgetEntity):
    entities_account_id = Column(ForeignKey('account.id'))
    entities_account = relationship('Account', foreign_keys=entities_account_id)
    entities_master_category_id = Column(ForeignKey('mastercategory.id'))
    entities_master_category = relationship('MasterCategory', foreign_keys=entities_master_category_id)
    goal_creation_month = Column(String)
    goal_type = Column(String)
    internal_name = Column(String)
    is_hidden = Column(Boolean, default=False)
    monthly_funding = Column(String)
    name = Column(String)
    note = Column(String)
    sortable_index = Column(Integer, default=0)
    target_balance = Column(AmountType)
    target_balance_month = Column(String)
    type = Column(String)


class PayeeLocation(Base, BudgetEntity):
    entities_payee_id = Column(ForeignKey('payee.id'))
    entities_payee = relationship('Payee', foreign_keys=entities_payee_id)
    latitude = Column(String)
    longitude = Column(String)


class AccountCalculation(Base, BudgetEntity):
    cleared_balance = Column(AmountType)
    entities_account_id = Column(ForeignKey('account.id'))
    entities_account = relationship('Account', foreign_keys=entities_account_id)
    error_count = Column(String)
    info_count = Column(String)
    transaction_count = Column(String)
    uncleared_balance = Column(AmountType)
    warning_count = Column(String)


class MonthlyAccountCalculation(Base, BudgetEntity):
    cleared_balance = Column(AmountType)
    entities_account_id = Column(ForeignKey('account.id'))
    entities_account = relationship('Account', foreign_keys=entities_account_id)
    error_count = Column(String)
    info_count = Column(String)
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
    entities_monthly_subcategory_budget_id = Column(ForeignKey('monthlysubcategorybudget.id'))
    entities_monthly_subcategory_budget = relationship('MonthlySubcategoryBudget',
                                                       foreign_keys=entities_monthly_subcategory_budget_id)
    goal_expected_completion = Column(String)
    goal_overall_funded = Column(AmountType)
    goal_overall_left = Column(AmountType)
    goal_percentage_complete = Column(String)
    goal_target = Column(String)
    goal_under_funded = Column(String)
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


class UpComingInstance(Base):
    scheduledtransaction_id = Column(ForeignKey('scheduledtransaction.id'))


class ScheduledTransaction(Base, BudgetEntity):
    amount = Column(AmountType)
    date = Column(Date)
    entities_account_id = Column(ForeignKey('account.id'))
    entities_account = relationship('Account', foreign_keys=entities_account_id)
    entities_payee_id = Column(ForeignKey('payee.id'))
    entities_payee = relationship('Payee', foreign_keys=entities_payee_id)
    entities_subcategory_id = Column(ForeignKey('subcategory.id'))
    entities_subcategory = relationship('SubCategory', foreign_keys=entities_subcategory_id)
    transaction = relationship(Transaction, backref='entities_scheduled_transaction')
    flag = Column(String, default=None)
    frequency = Column(String)
    memo = Column(String)
    transfer_account_id = Column(ForeignKey('account.id'))
    transfer_account = relationship('Account', foreign_keys=transfer_account_id)

    upcoming_instances = relationship('UpComingInstance')


class Payee(Base, BudgetEntity):
    auto_fill_amount = Column(AmountType)
    auto_fill_amount_enabled = Column(String)
    auto_fill_memo = Column(String)
    auto_fill_memo_enabled = Column(String)
    auto_fill_subcategory_enabled = Column(String)
    auto_fill_subcategory_id = Column(ForeignKey('subcategory.id'))
    auto_fill_subcategory = relationship('SubCategory', foreign_keys=auto_fill_subcategory_id)
    enabled = Column(Boolean, default=True)
    entities_account_id = Column(ForeignKey('account.id'))
    entities_account = relationship('Account', foreign_keys=entities_account_id)
    internal_name = Column(String)
    name = Column(String)
    rename_on_import_enabled = Column(String)


class MonthlySubcategoryBudget(Base, BudgetEntity):
    budgeted = Column(AmountType)
    entities_monthly_budget_id = Column(ForeignKey('monthlybudget.id'))
    entities_monthly_budget = relationship('MonthlyBudget', foreign_keys=entities_monthly_budget_id)
    entities_subcategory_id = Column(ForeignKey('subcategory.id'))
    entities_subcategory = relationship('SubCategory', foreign_keys=entities_subcategory_id)
    note = Column(String)
    overspending_handling = Column(String)


class TransactionGroup(dict):
    def get_apidict(self):
        return self

    def get_dict(self):
        return self


class PayeeRenameCondition(Base, BudgetEntity):
    entities_payee_id = Column(ForeignKey('payee.id'))
    entities_payee = relationship('Payee', foreign_keys=entities_payee_id)
    operand = Column(String)
    operator = Column(String)


class Account(Base, BudgetEntity):
    account_name = Column(String)
    account_type = Column(Enum(AccountTypes), default=AccountTypes.undef)
    hidden = Column(Boolean, default=False)
    last_entered_check_number = Column(String)
    last_reconciled_balance = Column(String)
    last_reconciled_date = Column(Date)
    note = Column(String)
    sortable_index = Column(Integer, default=0)
    on_budget = Column(Boolean, default=True)

    direct_connect_enabled = Column(Boolean, default=False)
    direct_connect_account_id = Column(String)
    direct_connect_institution_id = Column(String)
    direct_connect_last_imported_at = Column(Date)
    direct_connect_last_error_code = Column(String)

    def get_dict(self):
        super_dict = super(Account, self).get_dict()
        if not super_dict['direct_connect_enabled']:
            super_dict['direct_connect_enabled'] = False
            del super_dict['direct_connect_account_id']
            del super_dict['direct_connect_last_error_code']
            del super_dict['direct_connect_institution_id']
            del super_dict['direct_connect_last_imported_at']
        return super_dict
