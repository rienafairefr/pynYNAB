from pynYNAB.Entity import Entity, ListofEntities, obj_from_dict
from pynYNAB.budget import MasterCategory, Setting, MonthlyBudgetCalculation, AccountMapping, Subtransaction, \
    ScheduledSubtransaction, Subcategory, PayeeLocation, AccountCalculation, MonthlyAccountCalculation, \
    MonthlySubcategoryBudgetCalculation, ScheduledTransaction, Payee, MonthlySubcategoryBudget, PayeeRenameCondition, \
    Account, MonthlyBudget, TransactionGroup, DateField
from pynYNAB.budget import Transaction
from pynYNAB.catalog import UserBudget, UserSetting, BudgetVersion, User, CatalogBudget
from pynYNAB.schema.Fields import EntityListField


def knowledge_change(changed_entities):
    return sum(map(lambda v: len(v), [changed_entitity for dictkey, changed_entitity in changed_entities.items()]))


class Root(Entity):
    def __init__(self):

        self.knowledge = 0
        self.current_knowledge = 0
        self.device_knowledge_of_server = 0
        self.server_knowledge_of_device = 0
        super(Root, self).__init__()

    def sync(self, connection, opname):
        change, request_data = self.get_request_data()
        syncData = connection.dorequest(request_data, opname)
        for namefield in self.ListFields:
            getattr(self, namefield).changed = []
        self.knowledge += change
        changed_entities = {}
        for name, value in syncData['changed_entities'].items():
            if isinstance(value, list):
                for entityDict in value:
                    obj = obj_from_dict(self.ListFields[name].type, entityDict)
                    try:
                        changed_entities[name].append(obj)
                    except KeyError:
                        changed_entities[name] = [obj]
            else:
                changed_entities[name] = self.AllFields[name].posttreat(value)

        self.update_from_changed_entities(changed_entities)
        self.server_knowledge_of_device = syncData['server_knowledge_of_device']
        # To handle cases where the local knwoledge got out of sync
        if self.server_knowledge_of_device > self.knowledge:
            self.knowledge = self.server_knowledge_of_device
        self.device_knowledge_of_server = syncData['current_server_knowledge']

    def get_request_data(self):
        changed_entities = self.get_changed_entities()
        change = knowledge_change(changed_entities)
        return (change, {"starting_device_knowledge": self.knowledge,
                         "ending_device_knowledge": self.knowledge + change,
                         "device_knowledge_of_server": self.device_knowledge_of_server,
                         "changed_entities": changed_entities})


class Budget(Root):
    def __init__(self):
        super(Budget, self).__init__()
        self.budget_version_id = None

    Fields = dict(
        be_transactions=EntityListField(Transaction),
        be_master_categories=EntityListField(MasterCategory),
        be_settings=EntityListField(Setting),
        be_monthly_budget_calculations=EntityListField(MonthlyBudgetCalculation),
        be_account_mappings=EntityListField(AccountMapping),
        be_subtransactions=EntityListField(Subtransaction),
        be_scheduled_subtransactions=EntityListField(ScheduledSubtransaction),
        be_monthly_budgets=EntityListField(MonthlyBudget),
        be_subcategories=EntityListField(Subcategory),
        be_payee_locations=EntityListField(PayeeLocation),
        be_account_calculations=EntityListField(AccountCalculation),
        be_monthly_account_calculations=EntityListField(MonthlyAccountCalculation),
        be_monthly_subcategory_budget_calculations=EntityListField(MonthlySubcategoryBudgetCalculation),
        be_scheduled_transactions=EntityListField(ScheduledTransaction),
        be_payees=EntityListField(Payee),
        be_monthly_subcategory_budgets=EntityListField(MonthlySubcategoryBudget),
        be_payee_rename_conditions=EntityListField(PayeeRenameCondition),
        be_accounts=EntityListField(Account),
        last_month=DateField(None),
        first_month=DateField(None)
    )

    def get_request_data(self):
        k, request_data = super(Budget, self).get_request_data()
        request_data['budget_version_id'] = self.budget_version_id
        request_data['calculated_entities_included'] = False
        return k, request_data

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
    Fields = dict(
        ce_user_budgets=EntityListField(UserBudget),
        ce_user_settings=EntityListField(UserSetting),
        ce_budget_versions=EntityListField(BudgetVersion),
        ce_users=EntityListField(User),
        ce_budgets=EntityListField(CatalogBudget)
    )
