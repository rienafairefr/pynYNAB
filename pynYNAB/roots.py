from pynYNAB.Entity import Entity, ListofEntities, obj_from_dict
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


class Budget(Root):
    def __init__(self):
        super(Budget, self).__init__()
        self.budget_version_id = None

    be_transactions=EntityListField(Transaction)
    be_master_categories=EntityListField(MasterCategory)
    be_settings=EntityListField(Setting)
    be_monthly_budget_calculations=EntityListField(MonthlyBudgetCalculation)
    be_account_mappings=EntityListField(AccountMapping)
    be_subtransactions=EntityListField(Subtransaction)
    be_scheduled_subtransactions=EntityListField(ScheduledSubtransaction)
    be_monthly_budgets=EntityListField(MonthlyBudget)
    be_subcategories=EntityListField(Subcategory)
    be_payee_locations=EntityListField(PayeeLocation)
    be_account_calculations=EntityListField(AccountCalculation)
    be_monthly_account_calculations=EntityListField(MonthlyAccountCalculation)
    be_monthly_subcategory_budget_calculations=EntityListField(MonthlySubcategoryBudgetCalculation)
    be_scheduled_transactions=EntityListField(ScheduledTransaction)
    be_payees=EntityListField(Payee)
    be_monthly_subcategory_budgets=EntityListField(MonthlySubcategoryBudget)
    be_payee_rename_conditions=EntityListField(PayeeRenameCondition)
    be_accounts=EntityListField(Account)
    last_month=DateField(None)
    first_month=DateField(None)

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


class Catalog(Root):
    ce_user_budgets=EntityListField(UserBudget)
    ce_user_settings=EntityListField(UserSetting)
    ce_budget_versions=EntityListField(BudgetVersion)
    ce_users=EntityListField(User)
    ce_budgets=EntityListField(CatalogBudget)
