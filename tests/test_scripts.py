import sys

import pytest

try:
    import mock
except ImportError:
    import unittest.mock as mock

from pynYNAB.ClientFactory import nYnabClientFactory
from pynYNAB.scripts.__main__ import verify_common_args, MainCommands, CsvImport, OfxImport


class Args(object):
    def __init__(self, email, password, budget_name):
        self.email = email
        self.password = password
        self.budget_name = budget_name


def test_verify_common_noemail():
    pytest.raises(SystemExit, lambda:verify_common_args(Args('', None, '')))


def test_verify_common_nopassword():
    pytest.raises(SystemExit, lambda:verify_common_args(Args(None, '', '')))


def test_verify_common_nobudgetname():
    pytest.raises(SystemExit, lambda:verify_common_args(Args('', '', None)))


@mock.patch.object(sys, 'argv', ["prog", 'csvimport'])
@mock.patch.object(CsvImport, 'command')
def test_command_selection_csvimport(mock_csvimport):
    MainCommands()
    assert mock_csvimport.called


@mock.patch.object(sys, 'argv', ["prog", 'ofximport'])
@mock.patch.object(OfxImport, 'command')
def test_command_selection_ofximport(mock_ofximport):
    MainCommands()
    assert mock_ofximport.called


@mock.patch.object(sys, 'argv',
                   ["prog", 'csvimport', '--email', 'email', '--password', 'password', '--budget_name',
                    'budgetname', 'csvfile',
                    'csvschema'])
@mock.patch.object(nYnabClientFactory, 'create_client')
@mock.patch('pynYNAB.scripts.__main__.verify_csvimport')
@mock.patch('pynYNAB.scripts.__main__.do_csvimport')
def test_command_do_csvimport(mock_do_csvimport, mock_verify_csvimport, mock_create_client):
    with mock.patch('os.path.exists') as ospathexists:
        def side_effect(input):
            return True

        ospathexists.side_effect = side_effect
        MainCommands()

    assert mock_verify_csvimport.called
    call_args_verify = mock_verify_csvimport.call_args[0]

    assert 'csvschema' == call_args_verify[0]
    assert None == call_args_verify[1]

    assert mock_do_csvimport.called
    call_args_do = mock_do_csvimport.call_args[0]
    assert mock_create_client() == call_args_do[1]
    call_args_do = call_args_do[0]
    assert 'email' == call_args_do.email
    assert 'password' == call_args_do.password
    assert 'budgetname' == call_args_do.budget_name
    assert 'csvfile' == call_args_do.csvfile
    assert 'csvschema' == call_args_do.schema


@mock.patch.object(sys, 'argv',
                   ["prog", 'ofximport', '--email', 'email', '--password', 'password', '--budget_name',
                    'budgetname', 'ofxfile'])
@mock.patch.object(nYnabClientFactory, 'create_client')
@mock.patch('pynYNAB.scripts.__main__.do_ofximport')
def test_command_do_ofximport(mock_do_ofximport, mock_create_client):
    with mock.patch('os.path.exists') as ospathexists:
        def side_effect(input):
            return True

        ospathexists.side_effect = side_effect
        MainCommands()

    assert mock_do_ofximport.called
    call_args_do = mock_do_ofximport.call_args[0]
    assert mock_create_client() == call_args_do[1]
    assert 'ofxfile' == call_args_do[0]
