# coding=utf-8
import logging
import json
import uuid
import pickle
import requests
from requests.cookies import RequestsCookieJar
import os
from Entity import ComplexEncoder
from utils import RateLimited

logger=logging.getLogger('pynYNAB')

class NYnabConnectionError(Exception):
    pass

requests.packages.urllib3.disable_warnings()

class nYnabConnection(object):
    url = 'https://app.youneedabudget.com/users/login'
    urlCatalog = 'https://app.youneedabudget.com/api/v1/catalog'

    def getsession(self):
        self.session.cookies = RequestsCookieJar()

        self.session.headers['X-YNAB-Device-Id'] = self.id
        self.session.headers['User-Agent'] = 'python nYNAB API bot - rienafairefr rienafairefr@gmail.com'

        firstlogin = self.dorequest({"email": self.email, "password": self.password, "remember_me": True,
                                     "device_info": {"id": self.id}}, 'loginUser')
        self.sessionToken = firstlogin["session_token"]
        self.session.headers['X-Session-Token'] = self.sessionToken

    def __init__(self, email, password, reload=False):
        self.email = email
        self.password = password
        self.session = requests.Session()
        self.id = str(uuid.uuid3(uuid.NAMESPACE_DNS, 'rienafairefr.pynYNAB'))
        self.lastrequest_elapsed=None

        self.getsession()

    @RateLimited(maxPerSecond=10)
    def dorequest(self, request_dic, opname):
        # Available operations : loginUser,getInitialUserData,logoutUser,createNewBudget,freshStartABudget,cloneBudget,
        # deleteTombstonedBudgets,syncCatalogData,syncBudgetData,getInstitutionList
        # getInstitutionLoginFields,getInstitutionAccountList,registerAccountForDirectConnect,
        # updateDirectConnectCredentials,poll,createFeedback,runSqlStatement

        params = { u'operation_name': opname,'request_data': json.dumps(request_dic, cls=ComplexEncoder),}
        logger.debug('POST-ing ...',params)
        r = self.session.post(self.urlCatalog, params, verify=False)
        self.lastrequest_elapsed=r.elapsed
        js = r.json()
        if r.status_code != 200:
            logger.debug(r.text)
            raise NYnabConnectionError('non-200 HTTP code returned from the API')
        if js['error'] is None:
            return js
        else:
            raise NYnabConnectionError('Error was returned from the API')













