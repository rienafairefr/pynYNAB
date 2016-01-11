# coding=utf-8
import urllib2
import configparser
import mechanize
import json
import uuid
import requests
from requests.cookies import RequestsCookieJar

class Urls:
    url='https://app.youneedabudget.com/users/login'
    urlCatalog='https://app.youneedabudget.com/api/v1/catalog'

class nYNABConnectionError(Exception):
    pass

class nYNAB(object):
    def __init__(self,email,password):
        jar=RequestsCookieJar()

        self.session=requests.Session()
        self.session.cookies=jar
        self.browser=mechanize.Browser()
        self.browser.set_handle_robots(False)
        self.browser.open(Urls.url)
        self.id=str(uuid.uuid3(uuid.NAMESPACE_DNS,"rienafairefr"))

        firstlogin=self.dorequest({"email":email,"password":password,"remember_me":True,"device_info":{"id":self.id}},'loginUser')
        if firstlogin['error'] is not None:
            raise(nYNABConnectionError)
        self.sessionToken=firstlogin["session_token"]

        self.session.headers['X-Session-Token']=self.sessionToken
        self.session.headers['User-Agent']='python nYNAB API bot - rienafairefr rienafairefr@gmail.com'
        self.session.headers['X-YNAB-Client-App-Version']='build/staging/v0.6.8597'

        self.catalog=self.dorequest({"starting_device_knowledge":0,"ending_device_knowledge":0,"device_knowledge_of_server":0,"changed_entities":{}},'syncCatalogData')

    def dorequest(self,request_dic,opname):
        params = {'request_data': json.dumps(request_dic), u'operation_name':opname}
        headers={'X-YNAB-Device-Id':id}
        r=self.session.post(Urls.urlCatalog,params,headers=headers, verify=False)
        js=r.json()
        if js['error'] is None:
            return js

class Transaction(object):
    pass
class Budget(object):
    pass


cp=configparser.ConfigParser()
cp.read("ynab.conf")
email=cp.get('AUTHENTICATION','email')
password=cp.get('AUTHENTICATION','password')

YNABobject=nYNAB(email,password)

#budget_version_id=sync['changed_entities']['ce_budget_versions'][0]['id']

#syncB=dorequest({"budget_version_id":budget_version_id,"starting_device_knowledge":0,"ending_device_knowledge":0,"device_knowledge_of_server":0,"calculated_entities_included":False,"changed_entities":{}},'syncBudgetData')

print(YNABobject.catalog)









