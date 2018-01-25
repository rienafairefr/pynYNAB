import unittest

import sys

import os

try:
    import mock
except ImportError:
    import unittest.mock as mock

from pynYNAB.ClientFactory import nYnabClientFactory
from pynYNAB.scripts.__main__ import verify_common_args, MainCommands, CsvImport, OfxImport


def expect_exception(exception):
    """Marks test to expect the specified exception. Call assertRaises internally"""

    def test_decorator(fn):
        def test_decorated(self, *args, **kwargs):
            self.assertRaises(exception, fn, self, *args, **kwargs)

        return test_decorated

    return test_decorator


class TestScripts(unittest.TestCase):
    class Args(object):
        def __init__(self, email, password, budget_name):
            self.email = email
            self.password = password
            self.budget_name = budget_name

    @expect_exception(SystemExit)
    def test_verify_common_noemail(self):
        verify_common_args(self.Args('', None, ''))

    @expect_exception(SystemExit)
    def test_verify_common_nopassword(self):
        verify_common_args(self.Args(None, '', ''))

    @expect_exception(SystemExit)
    def test_verify_common_nobudgetname(self):
        verify_common_args(self.Args('', '', None))

    @mock.patch.object(sys, 'argv', ["prog", 'csvimport'])
    @mock.patch.object(CsvImport, 'command')
    def test_command_selection_csvimport(self, mock_csvimport):
        MainCommands()
        self.assertTrue(mock_csvimport.called)

    @mock.patch.object(sys, 'argv', ["prog", 'ofximport'])
    @mock.patch.object(OfxImport, 'command')
    def test_command_selection_ofximport(self, mock_ofximport):
        MainCommands()
        self.assertTrue(mock_ofximport.called)

    @mock.patch.object(sys, 'argv',
                          ["prog", 'csvimport', '--email', 'email', '--password', 'password', '--budget_name',
                           'budgetname', 'csvfile',
                           'csvschema'])
    @mock.patch.object(nYnabClientFactory, 'create_client')
    @mock.patch('pynYNAB.scripts.__main__.verify_csvimport')
    @mock.patch('pynYNAB.scripts.__main__.do_csvimport')
    def test_command_do_csvimport(self, mock_do_csvimport, mock_verify_csvimport, mock_create_client):
        with mock.patch('os.path.exists') as ospathexists:
            def side_effect(input):
                return True
            ospathexists.side_effect = side_effect
            MainCommands()

        self.assertTrue(mock_verify_csvimport.called)
        call_args_verify = mock_verify_csvimport.call_args[0]

        self.assertEqual('csvschema', call_args_verify[0])
        self.assertEqual(None, call_args_verify[1])

        self.assertTrue(mock_do_csvimport.called)
        call_args_do = mock_do_csvimport.call_args[0]
        self.assertEqual(mock_create_client(), call_args_do[1])
        call_args_do = call_args_do[0]
        self.assertEqual('email', call_args_do.email)
        self.assertEqual('password', call_args_do.password)
        self.assertEqual('budgetname', call_args_do.budget_name)
        self.assertEqual('csvfile', call_args_do.csvfile)
        self.assertEqual('csvschema', call_args_do.schema)

    @mock.patch.object(sys, 'argv',
                          ["prog", 'ofximport', '--email', 'email', '--password', 'password', '--budget_name',
                           'budgetname', 'ofxfile'])
    @mock.patch.object(nYnabClientFactory, 'create_client')
    @mock.patch('pynYNAB.scripts.__main__.do_ofximport')
    def test_command_do_ofximport(self, mock_do_ofximport, mock_create_client):
        with mock.patch('os.path.exists') as ospathexists:
            def side_effect(input):
                return True
            ospathexists.side_effect = side_effect
            MainCommands()

        self.assertTrue(mock_do_ofximport.called)
        call_args_do = mock_do_ofximport.call_args[0]
        self.assertEqual(mock_create_client(), call_args_do[1])
        self.assertEqual('ofxfile', call_args_do[0])
