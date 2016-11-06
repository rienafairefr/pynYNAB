from sqlalchemy import Column
from sqlalchemy import Date
from sqlalchemy.orm import relationship

from pynYNAB.Entity import Entity, ListofEntities, obj_from_dict, Base
from pynYNAB.schema.Fields import EntityListField
from pynYNAB.schema.budget import MasterCategory, Setting, MonthlyBudgetCalculation, AccountMapping, Subtransaction, \
    ScheduledSubtransaction, Subcategory, PayeeLocation, AccountCalculation, MonthlyAccountCalculation, \
    MonthlySubcategoryBudgetCalculation, ScheduledTransaction, Payee, MonthlySubcategoryBudget, PayeeRenameCondition, \
    Account, MonthlyBudget, TransactionGroup, DateField
from pynYNAB.schema.budget import Transaction
from pynYNAB.schema.catalog import UserBudget, UserSetting, BudgetVersion, User, CatalogBudget
from pynYNAB.scripts.config import get_logger


def knowledge_change(changed_entities):
    return sum(map(lambda v: len(v), [changed_entitity for dictkey, changed_entitity in changed_entities.items()]))


class Root(Entity):
    pass


class Budget(Base,Root):
    def __init__(self):
        super(Budget, self).__init__()
        self.budget_version_id = None

    be_transactions=relationship('Transaction')
    be_master_categories=relationship('MasterCategory')
    be_settings=relationship('Setting')
    be_monthly_budget_calculations=relationship('MonthlyBudgetCalculation')
    be_account_mappings=relationship('AccountMapping')
    be_subtransactions=relationship('Subtransaction')
    be_scheduled_subtransactions=relationship('ScheduledSubtransaction')
    be_monthly_budgets=relationship('MonthlyBudget')
    be_subcategories=relationship('Subcategory')
    be_payee_locations=relationship('PayeeLocation')
    be_account_calculations=relationship('AccountCalculation')
    be_monthly_account_calculations=relationship('MonthlyAccountCalculation')
    be_monthly_subcategory_budget_calculations=relationship('MonthlySubcategoryBudgetCalculation')
    be_scheduled_transactions=relationship('ScheduledTransaction')
    be_payees=relationship('Payee')
    be_monthly_subcategory_budgets=relationship('MonthlySubcategoryBudget')
    be_payee_rename_conditions=relationship('PayeeRenameCondition')
    be_accounts=relationship('Account')
    last_month=Column(Date)
    first_month=Column(Date)

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


class Catalog(Base,Root):
    ce_user_budgets=relationship('UserBudget')
    ce_user_settings=relationship('UserSetting')
    ce_budget_versions=relationship('BudgetVersion')
    ce_users=relationship('User')
    ce_budgets=relationship('CatalogBudget')
