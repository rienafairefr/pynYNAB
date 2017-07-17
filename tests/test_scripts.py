import unittest

import sys
from mock import patch, mock

from pynYNAB.ClientFactory import nYnabClientFactory
from pynYNAB.scripts.__main__ import verify_common_args, MainCommands


def expect_exception(exception):
    """Marks test to expect the specified exception. Call assertRaises internally"""

    def test_decorator(fn):
        def test_decorated(self, *args, **kwargs):
            self.assertRaises(exception, fn, self, *args, **kwargs)

        return test_decorated

    return test_decorator


class TestScripts(unittest.TestCase):
    class Args(object):
        def __init__(self, email, password, budgetname):
            self.email = email
            self.password = password
            self.budgetname = budgetname

    @expect_exception(SystemExit)
    def test_verify_common_noemail(self):
        verify_common_args(self.Args('', None, ''))

    @expect_exception(SystemExit)
    def test_verify_common_nopassword(self):
        verify_common_args(self.Args(None, '', ''))

    @expect_exception(SystemExit)
    def test_verify_common_nobudgetname(self):
        verify_common_args(self.Args('', '', None))

    @patch.object(sys, 'argv', ["prog", 'csvimport'])
    @patch.object(MainCommands, 'csvimport')
    def test_command_selection_csvimport(self, new_m):
        MainCommands()
        self.assertTrue(new_m.called)

    @patch.object(sys, 'argv', ["prog", 'ofximport'])
    @patch.object(MainCommands, 'ofximport')
    def test_command_selection_ofximport(self, new_m):
        MainCommands()
        self.assertTrue(new_m.called)

    @patch.object(sys, 'argv',
                          ["prog", 'csvimport', '--email', 'email', '--password', 'password', '--budgetname',
                           'budgetname', 'csvfile',
                           'csvschema'])
    @patch.object(nYnabClientFactory, 'create_client')
    @mock.patch('pynYNAB.scripts.__main__.verify_csvimport')
    @mock.patch('pynYNAB.scripts.__main__.do_csvimport')
    def test_command_do_csvimport(self, new_m, new_m2, new_c):
        MainCommands()

        self.assertTrue(new_m2.called)
        call_args_verify = new_m2.call_args[0][0]

        self.assertEqual('email', call_args_verify.email)
        self.assertEqual('password', call_args_verify.password)
        self.assertEqual('budgetname', call_args_verify.budgetname)
        self.assertEqual('csvfile', call_args_verify.csvfile)
        self.assertEqual('csvschema', call_args_verify.schema)

        self.assertTrue(new_m.called)
        call_args = new_m.call_args[0]
        self.assertEqual(new_c(), call_args[2])
        call_args = call_args[0]
        self.assertEqual('email', call_args.email)
        self.assertEqual('password', call_args.password)
        self.assertEqual('budgetname', call_args.budgetname)
        self.assertEqual('csvfile', call_args.csvfile)
        self.assertEqual('csvschema', call_args.schema)

    @patch.object(sys, 'argv',
                          ["prog", 'ofximport', '--email', 'email', '--password', 'password', '--budgetname',
                           'budgetname', 'ofxfile'])
    @patch.object(nYnabClientFactory, 'create_client')
    @mock.patch('pynYNAB.scripts.__main__.verify_ofximport')
    @mock.patch('pynYNAB.scripts.__main__.do_ofximport')
    def test_command_do_ofximport(self, new_m, new_m2, new_c):
        MainCommands()

        self.assertTrue(new_m2.called)
        call_args_verify = new_m2.call_args[0][0]

        self.assertEqual('email', call_args_verify.email)
        self.assertEqual('password', call_args_verify.password)
        self.assertEqual('budgetname', call_args_verify.budgetname)
        self.assertEqual('ofxfile', call_args_verify.ofxfile)

        self.assertTrue(new_m.called)
        call_args = new_m.call_args[0]
        self.assertEqual(new_c(), call_args[2])
        call_args = call_args[0]
        self.assertEqual('email', call_args.email)
        self.assertEqual('password', call_args.password)
        self.assertEqual('budgetname', call_args.budgetname)
        self.assertEqual('ofxfile', call_args.ofxfile)
