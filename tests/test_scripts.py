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

    def test_command_selection_csvimport(self):
        testargs = ["prog", 'csvimport']
        with patch.object(sys, 'argv', testargs):
            with patch.object(MainCommands, 'csvimport') as new_m:
                MainCommands()
                self.assertTrue(new_m.called)

    def test_command_selection_ofximport(self):
        testargs = ["prog", 'ofximport']
        with patch.object(sys, 'argv', testargs):
            with patch.object(MainCommands, 'ofximport') as new_m:
                MainCommands()
                self.assertTrue(new_m.called)

    def test_command_do_csvimport(self):
        with patch.object(sys, 'argv',
                          ["prog", 'csvimport', '--email', 'email', '--password', 'password', '--budgetname',
                           'budgetname', 'csvfile',
                           'csvschema']):
            with mock.patch('pynYNAB.scripts.__main__.do_csvimport') as new_m:
                with mock.patch('pynYNAB.scripts.__main__.verify_csvimport') as new_m2:
                    with patch.object(nYnabClientFactory, 'create_client') as new_c:
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

    def test_command_do_ofximport(self):
        with patch.object(sys, 'argv',
                          ["prog", 'ofximport', '--email', 'email', '--password', 'password', '--budgetname',
                           'budgetname', 'ofxfile']):
            with mock.patch('pynYNAB.scripts.__main__.do_ofximport') as new_m:
                with patch.object(nYnabClientFactory, 'create_client') as new_c:
                    MainCommands()
                    self.assertTrue(new_m.called)
                    call_args = new_m.call_args[0]
                    self.assertEqual(new_c(), call_args[1])
                    call_args = call_args[0]
                    self.assertEqual('email', call_args.email)
                    self.assertEqual('password', call_args.password)
                    self.assertEqual('budgetname', call_args.budgetname)
                    self.assertEqual('ofxfile', call_args.ofxfile)
