import unittest

import re

from pynYNAB.connection import nYnabConnection, NYnabConnectionError
from mock import Mock

noerror = {'error':None}

new_post= Mock()

class MockResponse(object):
    elapsed=0
    text=''

    def __init__(self, returnvalue=noerror, status_code=200, headers={}):
        self.jsonreturn = returnvalue
        self.status_code = status_code
        self.headers = headers

    def json(self):
        return self.jsonreturn

connection = nYnabConnection(email='email', password='password')
opname = 'opname'
request_dict = {}
connection.session.post = new_post


class TestConnection(unittest.TestCase):
    def test_init_session(self):
        uuidhex = re.compile('[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}', re.I)
        user_id = '123456'
        session_token = 'abcdef'

        # mock response
        def new_do_request( request_dic, opname):
            self.assertEqual(opname,'loginUser')
            self.assertTrue(uuidhex.match(request_dic['device_info']['id']))
            del request_dic['device_info']
            self.assertEqual(request_dic,{'email': 'email',
                                          'password': 'password',
                                          'remember_me': True})
            return {'session_token':session_token,'user':{'id':user_id}}

        connection.dorequest = new_do_request
        connection.init_session()
        self.assertEqual(connection.user_id,user_id)
        self.assertEqual(connection.sessionToken, session_token)

    def test_dorequest(self):
        new_post.side_effect = [MockResponse()]
        returnvalue_request = connection.dorequest(request_dict,opname)
        self.assertEqual(returnvalue_request,noerror)

    def test_dorequest_fail(self):
        new_post.side_effect=[MockResponse(status_code=500)]
        self.assertRaises(NYnabConnectionError, lambda:connection.dorequest(request_dict,opname))

    def test_connect_error_no_id(self):
        new_post.side_effect=[MockResponse({'error':{'message':'meh'}})]
        self.assertRaises(NYnabConnectionError, lambda:connection.dorequest(request_dict,opname))

    def test_connect_error_user_password_invalid(self):
        new_post.side_effect=[MockResponse({'error':{'id':'user_password_invalid'}})]
        self.assertRaises(NYnabConnectionError, lambda:connection.dorequest(request_dict,opname))

    def test_connect_error_user_not_found(self):
        new_post.side_effect=[MockResponse({'error':{'id':'user_not_found'}})]
        self.assertRaises(NYnabConnectionError, lambda:connection.dorequest(request_dict,opname))
