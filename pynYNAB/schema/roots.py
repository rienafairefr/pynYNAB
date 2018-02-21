from sqlalchemy import Column
from sqlalchemy import Date
from sqlalchemy import String, Integer
from sqlalchemy.orm import relationship

from pynYNAB import KeyGenerator
from pynYNAB.schema.Entity import Base
from pynYNAB.schema.RootEntity import RootEntity
from pynYNAB.schema.budget import TransactionGroup


class Catalog(Base, RootEntity):
    user_budgets = relationship('UserBudget')
    user_settings = relationship('UserSetting')
    budget_versions = relationship('BudgetVersion')
    users = relationship('User')
    budgets = relationship('CatalogBudget')


class Budget(Base, RootEntity):
    transactions = relationship('Transaction')
    master_categories = relationship('MasterCategory')
    settings = relationship('Setting')
    monthly_budget_calculations = relationship('MonthlyBudgetCalculation')
    account_mappings = relationship('AccountMapping')
    subtransactions = relationship('Subtransaction')
    scheduled_subtransactions = relationship('ScheduledSubtransaction')
    monthly_budgets = relationship('MonthlyBudget')
    subcategories = relationship('SubCategory')
    payee_locations = relationship('PayeeLocation')
    account_calculations = relationship('AccountCalculation')
    monthly_account_calculations = relationship('MonthlyAccountCalculation')
    monthly_subcategory_budget_calculations = relationship('MonthlySubcategoryBudgetCalculation')
    scheduled_transactions = relationship('ScheduledTransaction')
    payees = relationship('Payee')
    monthly_subcategory_budgets = relationship('MonthlySubcategoryBudget')
    payee_rename_conditions = relationship('PayeeRenameCondition')
    accounts = relationship('Account')
    last_month = Column(Date)
    first_month = Column(Date)

    knowledge = relationship('Knowledge')

    def get_changed_entities(self):
        changed_entities = super(Budget, self).get_changed_entities()
        if 'transactions' in changed_entities:
            changed_entities['transaction_groups'] = []
            for tr in changed_entities.pop('transactions'):
                subtransactions = []
                if 'subtransactions' in changed_entities:
                    for subtransaction in changed_entities['subtransactions']:
                        if subtransaction.entities_transaction_id == tr.id:
                            subtransactions.append(subtransaction)
                    for subtransaction in subtransactions:
                        changed_entities['subtransactions'].remove(subtransaction)
                if not subtransactions:
                    subtransactions = None
                group = TransactionGroup(
                    id=tr.id,
                    transaction=tr,
                    subtransactions=subtransactions,
                    matched_transaction=None)
                changed_entities['transaction_groups'].append(group)
        if changed_entities.get('subtransactions') is not None:
            del changed_entities['subtransactions']
        return changed_entities


class Knowledge(Base):
    __tablename__ = 'knowledge'

    obj_id = Column(String,primary_key=True,default=KeyGenerator.generateuuid)
    current_device_knowledge = Column(Integer,default=0)
    device_knowledge_of_server = Column(Integer,default=0)