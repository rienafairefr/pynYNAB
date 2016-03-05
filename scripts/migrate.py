import argparse
import random
import re
from _csv import QUOTE_NONE
from collections import namedtuple
from datetime import datetime

import dateparser

from pynYNAB.Client import nYnabClient, BudgetNotFound
from pynYNAB.Entity import AccountTypes
from pynYNAB.budget import MasterCategory, Subcategory, Account, Payee, Transaction, Subtransaction
from pynYNAB.config import email, password
from pynYNAB.connection import nYnabConnection

parser = argparse.ArgumentParser(description='Migrate a YNAB4 budget transaction history to nYNAB')
parser.add_argument('budgetname', metavar='BudgetName', type=str,
                    help='The budget to create')
parser.add_argument('budget', metavar='BudgetPath', type=str,
                    help='The budget.csv file, e.g. MyBudget as of YYYY-HH-LL HSS-Budget.csv')
parser.add_argument('register', metavar='RegisterPath', type=str,
                    help='The register.csv file , e.g. MyBudget as of YYYY-HH-LL HSS-Budget.csv')
parser.add_argument('-accounttypes', metavar='accounttypesCSV', type=str,
                    help='The migrate.csv file which defines account types', required=False)
parser.add_argument('--full-migrate', dest='fullMigrate', action='store_true', default=False,
                    help='Migrate also the accounts and categories, in case this budget is not'
                         + ' already migrated through YNAB4 interface, EXPERIMENTAL')
args = parser.parse_args()

dateformat = '%d/%m/%Y'
decimal_separator = ','
currency_symbol = u'\u20ac'

fullMigrate = args.fullMigrate

connection = nYnabConnection(email, password, reload=True)


def unquote(string):
    if string.startswith('"') and string.endswith('"'):
        string = string[1:-1]
    return string


def float_from_formatedcurrencyvalue(s):
    s = s.replace(decimal_separator, '.')
    s = s.replace(currency_symbol, '')
    return float(s)


def date_from_localeformatteddate(s):
    parsed = dateparser.parse(s)
    return datetime(year=parsed.year, month=parsed.month, day=1)


with open(args.budget, 'rb') as budget, open(args.register, 'rb') as register , open(args.accounttypes, 'rb') as account_types:
    from unicodecsv.py2 import UnicodeReader, Dialect


    class MyDialect(Dialect):
        delimiter = '\t'
        quotechar = '"'
        escapechar = '\''
        doublequote = False
        skipinitialspace = True
        lineterminator = '\n'
        quoting = QUOTE_NONE


    # RowBudget class for the data inside the table
    RowBudget = namedtuple('RowBudget',
                           ['Month', 'MasterCategoryName', 'SubCategoryName', 'Budgeted', 'Outflows',
                            'CategoryBalance'])
    # Read the Budget file into a list of  of RowBudget
    budget_lines = budget.readlines()
    budget_reader = UnicodeReader(budget_lines, dialect=MyDialect, encoding='utf-8-sig')
    budget_headers = map(unquote, budget_reader.next())

    BudgetRows = [RowBudget(
        Month=date_from_localeformatteddate(unquote(budget_row[0])),
        MasterCategoryName=unquote(budget_row[2]),
        SubCategoryName=unquote(budget_row[3]),
        Budgeted=float_from_formatedcurrencyvalue(budget_row[4]),
        Outflows=float_from_formatedcurrencyvalue(budget_row[5]),
        CategoryBalance=float_from_formatedcurrencyvalue(budget_row[6])
    ) for budget_row in budget_reader if len(budget_row) == 7]

    # RowRegister class for the data inside the table
    RowRegister = namedtuple('RowRegister',
                             ['AccountName', 'Flag', 'CheckNumber', 'Date', 'PayeeName', 'Category',
                              'MasterCategoryName', 'SubcategoryName', 'Memo', 'Outflow', 'Inflow',
                              'Cleared', 'RunningBalance'])
    # Read the Budget file into a list of  of RowBudget
    register_lines = register.readlines()
    register_reader = UnicodeReader(register_lines, dialect=MyDialect, encoding='utf-8-sig')
    register_headers = map(unquote, register_reader.next())

    RegisterRows = [RowRegister(
        AccountName=unquote(register_row[0]),
        Flag=register_row[1],  # Color, like Red, Green, etc,
        CheckNumber=register_row[2],
        Date=datetime.strptime(register_row[3], dateformat),
        PayeeName=unquote(register_row[4]),
        Category=unquote(register_row[5]),
        MasterCategoryName=unquote(register_row[6]),
        SubcategoryName=unquote(register_row[7]),
        Memo=unquote(register_row[8]),
        Outflow=float_from_formatedcurrencyvalue(register_row[9]),
        Inflow=float_from_formatedcurrencyvalue(register_row[10]),
        Cleared=register_row[11],  # R for locked ? C for Cleared, Nothing for unclered ?
        RunningBalance=float_from_formatedcurrencyvalue(register_row[12])
    ) for register_row in register_reader if len(register_row) == 13]

    try:
        nYNABobject = nYnabClient(connection, budget_name=args.budgetname, reload=True)
    except BudgetNotFound:
        # Do the full migration obviously...
        fullMigrate = True
        nYNABobject = nYnabClient(connection, reload=True)
        nYNABobject.createbudget(args.budgetname)
    nYNABobject.clean_transactions()
    if fullMigrate:

        nYNABobject.clean_budget()
        MasterCategoryNames = set(map(lambda x: x.MasterCategoryName, BudgetRows))
        SubcategoryNames = {}
        for MasterCategoryName in MasterCategoryNames:
            SubcategoryNames[MasterCategoryName] = set(
                [Row.SubCategoryName for Row in BudgetRows if Row.MasterCategoryName == MasterCategoryName])
        for MasterCategoryName in MasterCategoryNames:
            master_entity = MasterCategory(
                name=MasterCategoryName,
                sortable_index=random.randint(-50000, 50000)
            )
            nYNABobject.budget.be_master_categories.append(master_entity)
            subcategorynames = SubcategoryNames[MasterCategoryName]
            for subcategoryname in subcategorynames:
                entity = Subcategory(
                    name=subcategoryname,
                    entities_master_category_id=master_entity.id,
                    sortable_index=random.randint(-50000, 50000)
                )
                nYNABobject.budget.be_subcategories.append(entity)

        nYNABobject.sync()

        account_types_lines = filter(lambda x:not x.startswith('#'),account_types.readlines())
        account_types_reader = UnicodeReader(account_types_lines, encoding='utf-8')
        account_types_headers = account_types_reader.next()

        account_types_rows=[account_types_row for account_types_row in account_types_reader if len(account_types_row) == 3]

        account_types_dict={account_types_row[0]: getattr(AccountTypes,account_types_row[1]) for account_types_row in account_types_rows if hasattr(AccountTypes,account_types_row[1])}

        def str2bool(v):
            return v.lower() in ("yes", "true", "t", "1")
        account_onbudget_dict={account_types_row[0]: str2bool(account_types_row[2]) for account_types_row in account_types_rows}

        for account_name in set([register_row.AccountName for register_row in RegisterRows]):
            mindate = min(
                [register_row.Date for register_row in RegisterRows if register_row.AccountName == account_name])
            # Can't know the type of account from the register or budget file, workaround is using a manual migrate.csv
            try:
                account_type=account_types_dict[account_name]
            except KeyError:
                account_type=AccountTypes.Checking
            try:
                on_budget=account_onbudget_dict[account_name]
            except KeyError:
                on_budget=True
            account = Account(
                account_name=account_name,
                account_type=account_type,
                on_budget=on_budget,
                sortable_index=random.randint(-50000, 50000)
            )
            nYNABobject.add_account(account, 0, mindate)

        for payee_name in set([Row.PayeeName for Row in RegisterRows]):
            if 'Transfer : ' in payee_name: continue  # This payee should already exist, created by the add_account

            payee = Payee(name=payee_name)
            nYNABobject.budget.be_payees.append(payee)
        nYNABobject.sync()

    # At this  point, we should have identical accounts, payees, categories between YNAB4 and nYNAB,
    # either  through migration above or through the YNAB4 builtin migration

    accountmapping = {account.account_name: account.id for account in nYNABobject.budget.be_accounts}
    payeemapping = {payee.name: payee.id for payee in nYNABobject.budget.be_payees}
    mastercategorymapping = {mastercategory.name: mastercategory.id for mastercategory in
                             nYNABobject.budget.be_master_categories}
    submapping = {
    mastercategory.name: {subcategory.name: subcategory.id for subcategory in nYNABobject.budget.be_subcategories if
                          subcategory.entities_master_category_id == mastercategory.id} for mastercategory in
    nYNABobject.budget.be_master_categories}

    if not u'Pre-YNAB Debt' in mastercategorymapping and u'Credit Card Payments' in mastercategorymapping:
        mastercategorymapping[u'Pre-YNAB Debt'] = mastercategorymapping[u'Credit Card Payments']
        submapping[u'Pre-YNAB Debt'] = submapping[u'Credit Card Payments']

    if not u'Income' in mastercategorymapping and u'Credit Card Payments' in mastercategorymapping:
        mastercategoryinternal_id = next(
            mastercategory.id for mastercategory in nYNABobject.budget.be_master_categories if
            mastercategory.internal_name == 'MasterCategory/__Internal__')
        mastercategorymapping[u'Income'] = mastercategoryinternal_id

        subcategoryincome_id = next(subcategory.id for subcategory in nYNABobject.budget.be_subcategories if
                                    subcategory.internal_name == 'Category/__ImmediateIncome__')
        submapping[u'Income'] = {'Available this month': subcategoryincome_id,
                                 'Available next month': subcategoryincome_id}

    transactions = []
    subtransactions = []
    accumulatedSplits = []
    transfers = []
    reTransfer = re.compile('.*?Transfer : (?P<account>.*)')
    reSplit = re.compile('\(Split (?P<num1>\d+)/(?P<num2>\d+)\)')

    split_id = next(x.id for x in nYNABobject.budget.be_subcategories if x.internal_name == 'Category/__Split__')

    for register_row in RegisterRows:
        try:
            payee_id = payeemapping[register_row.PayeeName]
        except KeyError:
            payee_id = None
        resultSplit = reSplit.match(register_row.Memo)
        if resultSplit:
            accumulatedSplits.append(register_row)

            if resultSplit.group('num1') == resultSplit.group('num2'):
                total = sum(map(lambda x: x.Inflow - x.Outflow, accumulatedSplits))
                try:
                    payee_id = payeemapping[next(x.PayeeName for x in accumulatedSplits if x.PayeeName in payeemapping)]
                except StopIteration:
                    payee_id = None
                transaction = Transaction(
                    amount=total,
                    date=register_row.Date,
                    entities_payee_id=payee_id,
                    entities_account_id=accountmapping[register_row.AccountName],
                    entities_subcategory_id=split_id,
                    flag=register_row.Flag
                )
                transactions.append(transaction)
                for split in accumulatedSplits:
                    result = reTransfer.match(split.PayeeName)
                    if result is not None:
                        otheraccount = result.group('account')
                        payee_id = payeemapping['Transfer : ' + otheraccount]

                        # this => other
                        subtransaction = Subtransaction(
                            amount=split.Inflow - split.Outflow,
                            date=split.Date,
                            entities_payee_id=payee_id,
                            entities_account_id=accountmapping[split.AccountName],
                            transfer_account_id=accountmapping[otheraccount],
                            flag=split.Flag,
                            entities_transaction_id=transaction.id
                        )
                        subtransactions.append(subtransaction)
                        transfers.append(subtransaction)
                    else:
                        if split.MasterCategoryName == '':
                            # an out of budget transaction most probably
                            entities_subcategory_id = None
                        else:
                            entities_subcategory_id = submapping[split.MasterCategoryName][split.SubcategoryName]
                        subtransactions.append(Subtransaction(
                            amount=split.Inflow - split.Outflow,
                            date=split.Date,
                            entities_account_id=accountmapping[split.AccountName],
                            entities_payee_id=payee_id,
                            entities_subcategory_id=entities_subcategory_id,
                            flag=split.Flag,
                            entities_transaction_id=transaction.id
                        ))
                accumulatedSplits = []
        else:
            result = reTransfer.match(register_row.PayeeName)
            if result is not None:
                payee_id = payeemapping[register_row.PayeeName]
                otheraccount = result.group('account')
                # this => other
                transaction = Transaction(
                    amount=register_row.Inflow - register_row.Outflow,
                    date=register_row.Date,
                    entities_payee_id=payee_id,
                    entities_account_id=accountmapping[register_row.AccountName],
                    transfer_account_id=accountmapping[otheraccount],
                    flag=register_row.Flag
                )
                transfers.append(transaction)
            else:
                if register_row.MasterCategoryName == '':
                    # an out of budget transaction most probably
                    entities_subcategory_id = None
                else:
                    entities_subcategory_id = submapping[register_row.MasterCategoryName][register_row.SubcategoryName]
                transactions.append(Transaction(
                    amount=register_row.Inflow - register_row.Outflow,
                    date=register_row.Date,
                    entities_account_id=accountmapping[register_row.AccountName],
                    entities_payee_id=payee_id,
                    entities_subcategory_id=entities_subcategory_id,
                    flag=register_row.Flag
                ))

    unsplittransactions=[transaction for transaction in transactions if transaction.entities_subcategory_id != split_id]
    splittransactions=[transaction for transaction in transactions if transaction.entities_subcategory_id == split_id]

    transactions_dict={transaction.id:transaction for transaction in transactions}
    subtransactions_dict={subtransaction.id:subtransaction for subtransaction in subtransactions}

    transfers_dict = {tr.id: tr for tr in transfers}
    random.shuffle(transfers)

    for i1 in range(len(transfers)):
        tr1 = transfers[i1]
        for i2 in range(len(transfers)):
            if i2 > i1:
                tr2 = transfers[i2]
                if isinstance(tr1, Transaction) and isinstance(tr2, Transaction):
                    if tr1.entities_account_id == tr2.transfer_account_id \
                            and tr1.date == tr2.date \
                            and tr1.amount == -tr2.amount:

                        tr1.transfer_transaction_id = tr2.id
                        tr2.transfer_transaction_id = tr1.id

                        transactions.append(tr1)
                        transactions.append(tr2)
                elif isinstance(tr1, Transaction) and isinstance(tr2, Subtransaction):
                    tr2parent = next(x for x in transactions if x.id == tr2.entities_transaction_id)
                    if tr1.entities_account_id == tr2.transfer_account_id \
                            and tr1.date == tr2parent.date \
                            and tr1.amount == -tr2.amount:
                        siblings = [subtransaction for subtransaction in subtransactions if subtransaction.entities_transaction_id == tr2parent.id]

                        tr1.transfer_subtransaction_id = tr2.id
                        tr2.transfer_transaction_id = tr1.id

                        transactions.append(tr1)
                        subtransactions.append(tr2)
                elif isinstance(tr1, Subtransaction) and isinstance(tr2, Transaction):
                    tr1parent = next(x for x in transactions if x.id == tr1.entities_transaction_id)
                    if tr1parent.entities_account_id == tr2.transfer_account_id \
                            and tr1parent.date == tr2.date \
                            and tr1.amount == -tr2.amount:
                        siblings = [subtransaction for subtransaction in subtransactions if subtransaction.entities_transaction_id == tr1parent.id]

                        tr1.transfer_transaction_id = tr2.id
                        tr2.transfer_subtransaction_id = tr1.id

                        subtransactions.append(tr1)
                        transactions.append(tr2)



    nYNABobject.budget.be_transactions.extend(transactions)
    nYNABobject.budget.be_subtransactions.extend(subtransactions)

    nYNABobject.sync()



    pass
