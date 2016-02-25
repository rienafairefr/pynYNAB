from Entity import EntityListField, Entity, EntityField, ListofEntities
from budget import MasterCategory, Setting, MonthlyBudgetCalculation, AccountMapping, Subtransaction, \
    ScheduledSubtransaction, Subcategory, PayeeLocation, AccountCalculation, MonthlyAccountCalculation, \
    MonthlySubcategoryBudgetCalculation, ScheduledTransaction, Payee, MonthlySubcategoryBudget, PayeeRenameCondition, \
    Account, MonthlyBudget, TransactionGroup
from budget import Transaction
from catalog import UserBudget, UserSetting, BudgetVersion, User, CatalogBudget


def knowledge_change(changed_entities):
    return sum(map(lambda v: len(v),[v for k,v in changed_entities.iteritems()]))


class Root(Entity):
    def __init__(self):

        self.knowledge = 0
        self.current_knowledge = 0
        self.device_knowledge_of_server = 0
        self.server_knowledge_of_device = 0
        super(Root,self).__init__()

    def sync(self,connection,opname):
        change, request_data=self.get_request_data()
        syncData=connection.dorequest(request_data,opname)
        self.knowledge+=change
        self.update_from_changed_entities(syncData['changed_entities'])
        self.server_knowledge_of_device=syncData['server_knowledge_of_device']
        self.device_knowledge_of_server=syncData['current_server_knowledge']

    def get_request_data(self):
        changed_entities=self.get_changed_entities()
        change= knowledge_change(changed_entities)
        return (change,{"starting_device_knowledge":self.knowledge,
                                     "ending_device_knowledge":self.knowledge+change,
                                     "device_knowledge_of_server":self.device_knowledge_of_server,
                                     "changed_entities":changed_entities})

class Budget(Root):
    def __init__(self):
        super(Budget, self).__init__()
        self.budget_version_id = None

    Fields= dict(
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
            last_month=EntityField(None),
            first_month=EntityField(None)
        )

    def get_request_data(self):
        k,request_data=super(Budget,self).get_request_data()
        request_data['budget_version_id']=self.budget_version_id
        request_data['calculated_entities_included']=False
        return k,request_data

    def get_changed_entities(self):
        changed_entities=super(Budget,self).get_changed_entities()
        if 'be_transactions' in changed_entities:
            changed_entities['be_transaction_groups']=ListofEntities(TransactionGroup)
            for tr in changed_entities.pop('be_transactions'):
                changed_entities['be_transaction_groups'].append(TransactionGroup(
                    id=tr.id,
                    be_transaction=tr,
                ))
        return changed_entities

class Catalog(Root):
    Fields= dict(
            ce_user_budgets=EntityListField(UserBudget),
            ce_user_settings=EntityListField(UserSetting),
            ce_budget_versions=EntityListField(BudgetVersion),
            ce_users=EntityListField(User),
            ce_budgets=EntityListField(CatalogBudget)
        )

