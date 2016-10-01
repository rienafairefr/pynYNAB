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
    def __init__(self):

        self.logger = get_logger()
        self.current_device_knowledge = 0
        self.device_knowledge_of_server = 0
        super(Root, self).__init__()

    def sync(self, connection, opname):
        self.logger.debug('Starting sync')
        self.logger.debug('current_device_knowledge %s'%self.current_device_knowledge)
        self.logger.debug('device_knowledge_of_server %s' % self.device_knowledge_of_server)
        request_data = self.get_request_data()
        self.logger.debug('request_data starting_device_knowledge %s' % request_data['starting_device_knowledge'])
        self.logger.debug('request_data ending_device_knowledge %s' % request_data['ending_device_knowledge'])
        self.logger.debug('request_data device_knowledge_of_server %s' % request_data['device_knowledge_of_server'])
        self.logger.debug(request_data)
        syncData = connection.dorequest(request_data, opname)
        for namefield in self.ListFields:
            getattr(self, namefield).changed = []
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


        server_knowledge_of_device=syncData['server_knowledge_of_device']
        self.logger.debug('from server server_knowledge_of_device %s'%server_knowledge_of_device)
        current_server_knowledge=syncData['current_server_knowledge']
        self.logger.debug('from server current_server_knowledge %s' % current_server_knowledge)

        change = current_server_knowledge - self.device_knowledge_of_server
        if change>0:
            self.logger.debug('Server knowledge has gone up by ' + str(change) + '. We should be getting back some entities from the server')
        if self.current_device_knowledge < server_knowledge_of_device:
            if self.current_device_knowledge!=0:
                self.logger.error('The server knows more about this device than we know about ourselves')
            self.current_device_knowledge = server_knowledge_of_device
        self.update_from_changed_entities(changed_entities)

        self.device_knowledge_of_server = current_server_knowledge

        self.logger.debug('Ending sync')
        self.logger.debug('current_device_knowledge %s' % self.current_device_knowledge)
        self.logger.debug('device_knowledge_of_server %s' % self.device_knowledge_of_server)
        pass

    def get_request_data(self):
        changed_entities = self.get_changed_entities()
        dictionary = {"starting_device_knowledge": self.current_device_knowledge,
                      "device_knowledge_of_server": self.device_knowledge_of_server,
                      "changed_entities": changed_entities}
        if any(changed_entities):
            dictionary['ending_device_knowledge'] = self.current_device_knowledge + 1
        else:
            dictionary['ending_device_knowledge'] = self.current_device_knowledge
        return dictionary


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
