import pytest

from pynYNAB.schema import PayeeRenameCondition, PayeeRenameConditionOperator, Payee, Transaction
from .common_mock import setupEmptyClient


operators = [(op,) for op in PayeeRenameConditionOperator]
ids = [op.value for op in PayeeRenameConditionOperator]


@pytest.mark.parametrize(['payee_name', 'expected_equal'],[
    # valid or all operators
    ('test', lambda operator:True),
    # invalid or all operators
    ('different', lambda operator:False),
    # valid for contains only
    ('containstestcontains', lambda operator:operator == PayeeRenameConditionOperator.Contains),
    # valid for contains and endswith
    ('endswithtest',
                   lambda operator:operator in [PayeeRenameConditionOperator.EndsWith,
                                PayeeRenameConditionOperator.Contains]),
    # valid for contains and startswith
    ('teststartswith',
                   lambda operator:operator in [PayeeRenameConditionOperator.StartsWith,
                                PayeeRenameConditionOperator.Contains])
],ids=lambda arg:arg[0])
@pytest.mark.parametrize(['operator'], operators, ids=ids)
def test_payee_rename(payee_name, expected_equal, operator):
    rename_to = Payee(name='renamed')
    client = setupEmptyClient()
    payee_rename_condition = PayeeRenameCondition(operator=operator,
                                                  operand='test',
                                                  entities_payee=rename_to)

    client.budget.be_payee_rename_conditions.append(payee_rename_condition)
    client.budget.be_payees.append(rename_to)
    payee = Payee(name=payee_name)
    transaction = Transaction(entities_payee=payee)
    client.budget.be_transactions.append(transaction)

    client.run_treat_rename_payee()
    if expected_equal(operator):
        assert transaction.entities_payee == rename_to
    else:
        assert transaction.entities_payee != rename_to
    #
    # # valid or all operators
    # test_one_payee('test', True)
    # # invalid or all operators
    # test_one_payee('different', False)
    #
    # # valid for contains only
    # test_one_payee('containstestcontains',
    #                operator == PayeeRenameConditionOperator.Contains)
    #
    # # valid for contains and endswith
    # test_one_payee('endswithtest',
    #                operator in [PayeeRenameConditionOperator.EndsWith,
    #                             PayeeRenameConditionOperator.Contains])
    # # valid for contains and startswith
    # test_one_payee('teststartswith',
    #                operator in [PayeeRenameConditionOperator.StartsWith,
    #                             PayeeRenameConditionOperator.Contains])
