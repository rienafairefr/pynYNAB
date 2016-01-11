# coding=utf-8
import mechanize
import json
import uuid
import pickle
import requests
from requests.cookies import RequestsCookieJar
from appdirs import AppDirs
import os
from budget import BudgetBudget
from catalog import Catalog

appdir=AppDirs('nYNABpyClient')
try:
    os.makedirs(appdir.user_data_dir)
except:
    pass

class Urls:
    url='https://app.youneedabudget.com/users/login'
    urlCatalog='https://app.youneedabudget.com/api/v1/catalog'

class nYNABConnectionError(Exception):
    pass

class nYNAB(object):
    sessionpath=os.path.join(appdir.user_data_dir,'session')

    def getsession(self):
        self.session.cookies=RequestsCookieJar()
        self.browser.open(Urls.url)
        self.id=str(uuid.uuid3(uuid.NAMESPACE_DNS,"rienafairefr"))
        self.session.headers['X-YNAB-Device-Id']=self.id
        self.session.headers['User-Agent']='python nYNAB API bot - rienafairefr rienafairefr@gmail.com'

        firstlogin=self.dorequest({"email":self.email,"password":self.password,"remember_me":True,"device_info":{"id":self.id}},'loginUser')
        self.sessionToken=firstlogin["session_token"]
        self.session.headers['X-Session-Token']=self.sessionToken

    def loadsession(self):
        with open(self.sessionpath,'r') as file:
            self.session=pickle.load(file)
            self.sessionToken=self.session.headers['X-Session-Token']
            self.id=self.session.headers['X-YNAB-Device-Id']

    def savesession(self):
        with open(self.sessionpath,'w') as file:
            pickle.dump(self.session,file)

    catalogpath=os.path.join(appdir.user_data_dir,'catalog')

    def getcatalog(self):
        syncCatalogData=self.dorequest({"starting_device_knowledge":0,"ending_device_knowledge":0,"device_knowledge_of_server":0,"changed_entities":{}},'syncCatalogData')
        self.catalog.update_from_changed_entities(syncCatalogData['changed_entities'])
        self.catalog.current_server_knowledge=syncCatalogData['current_server_knowledge']
        self.catalog.server_knowledge_of_device=syncCatalogData['server_knowledge_of_device']

    def loadcatalog(self):
        with open(self.catalogpath,'r') as file:
            self.catalog=pickle.load(file)

    def savecatalog(self):
        with open(self.catalogpath,'w') as file:
            pickle.dump(self.catalog,file)

    def __init__(self,email,password,reload=False):
        self.email=email
        self.password=password
        self.session=requests.Session()
        self.browser=mechanize.Browser()
        self.browser.set_handle_robots(False)
        self.catalog=Catalog()

        if reload:
            self.getsession()
            self.getcatalog()
        else:
            try:
                self.loadsession()
            except:
                self.getsession()
            try:
                self.loadcatalog()
            except:
                self.getcatalog()
        self.savecatalog()
        self.savesession()

        budgetpath=os.path.join(appdir.user_data_dir,'budget')
        try:
            # we have a budget file that should hold already some data with some knowledge
            with open(budgetpath,'r') as file:
                self.budget=pickle.load(file)
        except:
            self.budgets=[]
            for budget_version in self.catalog.ce_budget_versions:
                budget=BudgetBudget()
                syncBudget=self.dorequest({"budget_version_id":budget_version.id,"starting_device_knowledge":0,"ending_device_knowledge":0,"device_knowledge_of_server":0,"calculated_entities_included":True,"changed_entities":{}},'syncBudgetData')
                budget.update_from_changed_entities(syncBudget['changed_entities'])
                budget.current_server_knowledge=syncBudget['current_server_knowledge']
                budget.server_knowledge_of_device=syncBudget['server_knowledge_of_device']
                self.budgets.append(budget)

    def dorequest(self,request_dic,opname):
        # Available operations : loginUser,getInitialUserData,logoutUser,createNewBudget,freshStartABudget,cloneBudget,deleteTombstonedBudgets,syncCatalogData,syncBudgetData,getInstitutionList
        #                        getInstitutionLoginFields,getInstitutionAccountList,registerAccountForDirectConnect,updateDirectConnectCredentials,poll,createFeedback,runSqlStatement

        params = {'request_data': json.dumps(request_dic), u'operation_name':opname}
        r=self.session.post(Urls.urlCatalog,params,verify=False)
        js=r.json()
        if r.status_code!=200:
            raise nYNABConnectionError('non-200 HTTP code returned from the API')
        if js['error'] is None:
            return js
        else:
            raise nYNABConnectionError('Error was returned from the API')













