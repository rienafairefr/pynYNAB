import re

import pytest

from pynYNAB.connection import nYnabConnection, NYnabConnectionError
from mock import Mock

noerror = {'error': None}

new_post = Mock()


class MockResponse(object):
    elapsed = 0
    text = ''

    def __init__(self, returnvalue=noerror, status_code=200, headers={}):
        self.jsonreturn = returnvalue
        self.status_code = status_code
        self.headers = headers

    def json(self):
        return self.jsonreturn


opname = 'opname'
request_dict = {}


@pytest.fixture
def connection():
    obj = nYnabConnection(email='email', password='password')
    obj.session.post = new_post
    return obj


def test_init_session(connection):
    uuidhex = re.compile('[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}', re.I)
    user_id = '123456'
    session_token = 'abcdef'

    # mock response
    def new_do_request(request_dic, opname):
        assert opname == 'loginUser'
        assert uuidhex.match(request_dic['device_info']['id'])
        del request_dic['device_info']
        assert request_dic == {'email': 'email',
                               'password': 'password',
                               'remember_me': True}
        return {'session_token': session_token, 'user': {'id': user_id}}

    connection.dorequest = new_do_request
    connection.init_session()
    assert connection.user_id == user_id
    assert connection.sessionToken == session_token


def test_dorequest(connection):
    new_post.side_effect = [MockResponse()]
    returnvalue_request = connection.dorequest(request_dict, opname)
    assert returnvalue_request == noerror


def test_dorequest_fail(connection):
    new_post.side_effect = [MockResponse(status_code=500)]
    pytest.raises(NYnabConnectionError, lambda: connection.dorequest(request_dict, opname))


def test_connect_error_no_id(connection):
    new_post.side_effect = [MockResponse({'error': {'message': 'meh'}})]
    pytest.raises(NYnabConnectionError, lambda: connection.dorequest(request_dict, opname))


def test_connect_error_user_password_invalid(connection):
    new_post.side_effect = [MockResponse({'error': {'id': 'user_password_invalid'}})]
    pytest.raises(NYnabConnectionError, lambda: connection.dorequest(request_dict, opname))


def test_connect_error_user_not_found(connection):
    new_post.side_effect = [MockResponse({'error': {'id': 'user_not_found'}})]
    pytest.raises(NYnabConnectionError, lambda: connection.dorequest(request_dict, opname))
