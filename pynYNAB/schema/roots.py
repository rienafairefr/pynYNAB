from sqlalchemy import Column
from sqlalchemy import Date
from sqlalchemy import String, Integer
from sqlalchemy.orm import relationship

from pynYNAB import KeyGenerator
from pynYNAB.schema.Entity import Base
from pynYNAB.schema.RootEntity import RootEntity


class Catalog(Base, RootEntity):
    ce_user_budgets = relationship('UserBudget')
    ce_user_settings = relationship('UserSetting')
    ce_budget_versions = relationship('BudgetVersion')
    ce_users = relationship('User')
    ce_budgets = relationship('CatalogBudget')


class Budget(Base, RootEntity):
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

    knowledge = relationship('Knowledge')

    def get_changed_apidict(self):
        changed_api_dict = super(Budget, self).get_changed_apidict()
        if 'be_transactions' in changed_api_dict:
            changed_api_dict['be_transaction_groups'] = []
            for transaction_dict in changed_api_dict.pop('be_transactions'):
                transaction_id = transaction_dict['id']
                subtransactions = []
                if 'be_subtransactions' in changed_api_dict:
                    for subtransaction_dic in changed_api_dict['be_subtransactions'].items():
                        if subtransaction_dic['entities_transaction_id'] == transaction_id:
                            subtransactions.append(subtransaction_dic)
                    for subtransaction in subtransactions:
                        changed_api_dict['be_subtransactions'].remove(subtransaction)
                if not subtransactions:
                    subtransactions = None
                group = dict(
                    id=transaction_id,
                    be_transaction=transaction_dict,
                    be_subtransactions=subtransactions,
                    be_matched_transaction=None)
                changed_api_dict['be_transaction_groups'].append(group)
        if changed_api_dict.get('be_subtransactions') is not None:
            del changed_api_dict['be_subtransactions']
        return changed_api_dict


class Knowledge(Base):
    __tablename__ = 'knowledge'

    obj_id = Column(String,primary_key=True,default=KeyGenerator.generateuuid)
    current_device_knowledge = Column(Integer,default=0)
    device_knowledge_of_server = Column(Integer,default=0)