# coding=utf-8
import urllib2
import configparser
import mechanize
import json
import uuid
import requests
from requests.cookies import RequestsCookieJar

id=str(uuid.uuid3(uuid.NAMESPACE_DNS,"rienafairefr"))

cp=configparser.ConfigParser()
cp.read("ynab.conf")

email=cp.get('AUTHENTICATION','email')
password=cp.get('AUTHENTICATION','password')

url='https://app.youneedabudget.com/users/login'
urlCatalog='https://app.youneedabudget.com/api/v1/catalog'

jar=RequestsCookieJar()
session=requests.Session()
session.cookies=jar

def dorequest(request_dic,opname):
    params = {'request_data': json.dumps(request_dic), u'operation_name':opname}
    headers={'X-YNAB-Device-Id':id}
    r=session.post(urlCatalog,params,headers=headers, verify=False)
    js=r.json()
    if js['error'] is None:
        return js

br=mechanize.Browser()

br.set_handle_robots(False)
br.open(url)

firstlogin=dorequest({"email":email,"password":password,"remember_me":True,"device_info":{"id":id}},'loginUser')
sessionToken=firstlogin["session_token"]
session.headers['X-Session-Token']=sessionToken
session.headers['User-Agent']='python nYNAB API bot - rienafairefr rienafairefr@gmail.com'
session.headers['X-YNAB-Client-App-Version']='build/staging/v0.6.8597'

with open('ynab.conf','w') as fp:
    cp.write(fp)


sync=dorequest({"starting_device_knowledge":0,"ending_device_knowledge":0,"device_knowledge_of_server":0,"changed_entities":{}},'syncCatalogData')

budget_version_id=sync['changed_entities']['ce_budget_versions'][0]['id']

syncB=dorequest({"budget_version_id":budget_version_id,"starting_device_knowledge":0,"ending_device_knowledge":0,"device_knowledge_of_server":0,"calculated_entities_included":False,"changed_entities":{}},'syncBudgetData')

pass









