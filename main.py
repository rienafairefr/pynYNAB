# coding=utf-8
from budget import Transaction, Account, Payee
from config import email, password
from nYNAB import NYnab
from NYnabConnection import NYnabConnection


connection = NYnabConnection(email, password, reload=True)
nYNABobject = NYnab(connection, reload=True)

# the catalog is where non budget specific things are stored, like users, settings, budget names
# budgets is a list of the budgets, each one contains transactions, etc

def createbudget(budget_name):
    import json
    currency_format = dict(
        iso_code='USD',
        example_format='123,456.78',
        decimal_digits=2,
        decimal_separator='.',
        symbol_first=True,
        group_separator=',',
        currency_symbol='$',
        display_symbol=True
    )
    date_format=dict(
        format='MM/DD/YYYY'
    )
    nYNABobject.connection.dorequest(opname='CreateNewBudget',
                                     request_dic={
        "budget_name": budget_name,
        "currency_format": json.dumps(currency_format),
        "date_format": json.dumps(date_format)
    })


def addaccount(budget_name,account_type,account_name,on_budget,balance):
    budget=nYNABobject.budget

    for account in budget.be_accounts:
        if account.account_name == account_name:
            return
    sortable_index=max([account.sortable_index for account in budget.be_accounts])
    account=Account(
        account_type=account_type,
        account_name=account_name,
        on_budget=True,
        hidden=False,
        sortable_index=sortable_index,
        direct_connect_enabled=False
    )

    payee=Payee(
        entities_account_id=account.id,
        enabled=True,
        auto_fill_subcategory_enabled=True,
        auto_fill_memo_enabled=False,
        auto_fill_amount_enabled=False,
        rename_on_import_enabled=False,
        name="Transfer : %s" % account_name
    )
    immediateincomeid=budget.be_subcategories.query(lambda s: s.internal_name=='Category/__ImmediateIncome__').id
    startingbalanceid=budget.be_payees.query(lambda p: p.internal_name=='StartingBalancePayee').id

    from datetime import datetime
    transaction=Transaction(
        accepted=True,
        amount=balance*1000,
        entities_subcategory_id=immediateincomeid,
        cash_amount=0,
        cleared='Cleared',
        date=datetime.now().strftime('%Y-%m-%d'),
        entities_account_id=account.id,
        credit_amount=0,
        entities_payee_id=startingbalanceid,
        is_tombstone=False
    )

    budget.be_accounts.append(account)
    budget.be_payees.append(payee)
    budget.be_transactions.append(transaction)

    nYNABobject.sync()


if __name__ == "__main__":

    addtransaction()
    #createbudget('My Budget2')
    #addaccount('My Budget',AccountTypes.Checking,'Checking1',True,10)

