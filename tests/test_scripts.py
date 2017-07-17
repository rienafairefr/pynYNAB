import unittest

import sys
try:
    import unittest.mock as mock
except ImportError:
    import mock

from pynYNAB.ClientFactory import nYnabClientFactory
from pynYNAB.scripts.__main__ import verify_common_args, MainCommands


class TestScripts(unittest.TestCase):
    class Args(object):
        def __init__(self, email, password, budgetname):
            self.email = email
            self.password = password
            self.budgetname = budgetname

    def test_verify_common_noemail(self):
        self.assertRaises(SystemExit, lambda: verify_common_args(self.Args('', None, '')))

    def test_verify_common_nopassword(self):
        self.assertRaises(SystemExit, lambda: verify_common_args(self.Args(None, '', '')))

    def test_verify_common_nobudgetname(self):
        self.assertRaises(SystemExit, lambda: verify_common_args(self.Args('', '', None)))

    @mock.patch.object(sys, 'argv', ["prog", 'csvimport'])
    @mock.patch.object(MainCommands, 'csvimport')
    def test_command_selection_csvimport(self, mock_csvimport):
        MainCommands()
        self.assertTrue(mock_csvimport.called)

    @mock.patch.object(sys, 'argv', ["prog", 'ofximport'])
    @mock.patch.object(MainCommands, 'ofximport')
    def test_command_selection_ofximport(self, mock_ofximport):
        MainCommands()
        self.assertTrue(mock_ofximport.called)

    @mock.patch.object(sys, 'argv',
                          ["prog", 'csvimport', '--email', 'email', '--password', 'password', '--budgetname',
                           'budgetname', 'csvfile',
                           'csvschema'])
    @mock.patch.object(nYnabClientFactory, 'create_client')
    @mock.patch('pynYNAB.scripts.__main__.verify_csvimport')
    @mock.patch('pynYNAB.scripts.__main__.do_csvimport')
    def test_command_do_csvimport(self, mock_do_csvimport, mock_verify_csvimport, mock_create_client):
        MainCommands()

        self.assertTrue(mock_verify_csvimport.called)
        call_args_verify = mock_verify_csvimport.call_args[0][0]

        self.assertEqual('email', call_args_verify.email)
        self.assertEqual('password', call_args_verify.password)
        self.assertEqual('budgetname', call_args_verify.budgetname)
        self.assertEqual('csvfile', call_args_verify.csvfile)
        self.assertEqual('csvschema', call_args_verify.schema)

        self.assertTrue(mock_do_csvimport.called)
        call_args_do = mock_do_csvimport.call_args[0]
        self.assertEqual(mock_create_client(), call_args_do[2])
        call_args_do = call_args_do[0]
        self.assertEqual('email', call_args_do.email)
        self.assertEqual('password', call_args_do.password)
        self.assertEqual('budgetname', call_args_do.budgetname)
        self.assertEqual('csvfile', call_args_do.csvfile)
        self.assertEqual('csvschema', call_args_do.schema)

    @mock.patch.object(sys, 'argv',
                          ["prog", 'ofximport', '--email', 'email', '--password', 'password', '--budgetname',
                           'budgetname', 'ofxfile'])
    @mock.patch.object(nYnabClientFactory, 'create_client')
    @mock.patch('pynYNAB.scripts.__main__.verify_ofximport')
    @mock.patch('pynYNAB.scripts.__main__.do_ofximport')
    def test_command_do_ofximport(self, mock_do_ofximport, mock_verify_ofximport, mock_create_client):
        MainCommands()

        self.assertTrue(mock_verify_ofximport.called)
        call_args_verify = mock_verify_ofximport.call_args[0][0]

        self.assertEqual('email', call_args_verify.email)
        self.assertEqual('password', call_args_verify.password)
        self.assertEqual('budgetname', call_args_verify.budgetname)
        self.assertEqual('ofxfile', call_args_verify.ofxfile)

        self.assertTrue(mock_do_ofximport.called)
        call_args_do = mock_do_ofximport.call_args[0]
        self.assertEqual(mock_create_client(), call_args_do[2])
        call_args_do = call_args_do[0]
        self.assertEqual('email', call_args_do.email)
        self.assertEqual('password', call_args_do.password)
        self.assertEqual('budgetname', call_args_do.budgetname)
        self.assertEqual('ofxfile', call_args_do.ofxfile)
