import configargparse
import inspect
import os
import random
import re
import sys
from pynYNAB.config import test_common_args
from ynab import YNAB

from pynYNAB.Client import nYnabClient, BudgetNotFound, clientfromargs
from pynYNAB.Entity import AccountTypes
from pynYNAB.connection import nYnabConnection
from pynYNAB.schema.budget import MasterCategory, Subcategory, Account, Payee, Transaction


def migrate_main():
    print('migrate YNAB4 to pynYNAB')
    """Migrate a YNAB4 budget transaction history to nYNAB, using pyynab"""

    parser = configargparse.getArgumentParser('pynYNAB')
    parser.description=inspect.getdoc(migrate_main)
    parser.add_argument('budget', metavar='BudgetPath', type=str,
                        help='The budget .ynab4 directory')
    args = parser.parse_args()
    test_common_args(args)

    budget_base_name=os.path.basename(args.budget)
    budget_path=os.path.dirname(args.budget)
    budget_name=re.match(r"(?P<budget_name>.*)~[A-Z0-9]{8}\.ynab4",budget_base_name).groupdict().get('budget_name')

    if args.budgetname is not None:
        budget_name=args.budgetname

    thisynab = YNAB(budget_path,budget_name)

    client = clientfromargs(args, reset=True)



    for ynab4_account in thisynab.accounts:
        account=Account(
            name=ynab4_account.name,
            account_type=ynab4_account.type.value,
            on_budget=ynab4_account.on_budget,
            sortable_index=random.randint(-50000, 50000),
        )
        mindate=min([ynab4transaction.date for ynab4transaction in thisynab.transactions if ynab4transaction.account == ynab4_account])
        client.add_account(account, 0, mindate)

    for master_category in thisynab.master_categories:
        master_entity = MasterCategory(
            name=master_category.name,
            sortable_index=random.randint(-50000, 50000)
        )
        client.budget.be_master_categories.append(master_entity)
        for category in master_category.categories:

            entity = Subcategory(
                name=category.name,
                entities_master_category_id=master_entity.id,
                sortable_index=random.randint(-50000, 50000)
            )
            client.budget.be_subcategories.append(entity)
        client.sync()

    for ynab4_payee in thisynab.payees:
        payee=Payee(
            name=ynab4_payee.name
                   )
        client.budget.be_payees.append(payee)
        client.sync()

    for ynab4transaction in thisynab.transactions:
        transaction=Transaction(

        )
        pass
    #
    #     transactions = []
    #     subtransactions = []
    #     accumulatedSplits = []
    #     transfers = []
    #     reTransfer = re.compile('.*?Transfer : (?P<account>.*)')
    #     reSplit = re.compile('\(Split\ (?P<num1>\d+)\/(?P<num2>\d+)\)')
    #
    #     split_id = next(x.id for x in nYNABobject.budget.be_subcategories if x.internal_name == 'Category/__Split__')
    #
    #     for register_row in RegisterRows:
    #         try:
    #             payee_id = payeemapping[register_row.PayeeName]
    #         except KeyError:
    #             payee_id = None
    #         resultSplit = reSplit.match(register_row.Memo)
    #         if resultSplit:
    #             accumulatedSplits.append(register_row)
    #
    #             if resultSplit.group('num1') == resultSplit.group('num2'):
    #                 total = sum(map(lambda x: x.Inflow - x.Outflow, accumulatedSplits))
    #                 try:
    #                     payee_id = payeemapping[next(x.PayeeName for x in accumulatedSplits if x.PayeeName in payeemapping)]
    #                 except StopIteration:
    #                     payee_id = None
    #                 transaction = Transaction(
    #                     amount=total,
    #                     date=register_row.Date,
    #                     entities_payee_id=payee_id,
    #                     entities_account_id=accountmapping[register_row.AccountName],
    #                     entities_subcategory_id=split_id,
    #                     flag=register_row.Flag
    #                 )
    #                 transactions.append(transaction)
    #                 for split in accumulatedSplits:
    #                     result = reTransfer.match(split.PayeeName)
    #                     if result is not None:
    #                         otheraccount = result.group('account')
    #                         payee_id = payeemapping['Transfer : ' + otheraccount]
    #
    #                         # this => other
    #                         subtransaction = Subtransaction(
    #                             amount=split.Inflow - split.Outflow,
    #                             date=split.Date,
    #                             entities_payee_id=payee_id,
    #                             entities_account_id=accountmapping[split.AccountName],
    #                             transfer_account_id=accountmapping[otheraccount],
    #                             flag=split.Flag,
    #                             entities_transaction_id=transaction.id
    #                         )
    #                         subtransactions.append(subtransaction)
    #                         transfers.append(subtransaction)
    #                     else:
    #                         if split.MasterCategoryName == '':
    #                             # an out of budget transaction most probably
    #                             entities_subcategory_id = None
    #                         else:
    #                             entities_subcategory_id = submapping[split.MasterCategoryName][split.SubcategoryName]
    #                         subtransactions.append(Subtransaction(
    #                             amount=split.Inflow - split.Outflow,
    #                             date=split.Date,
    #                             entities_account_id=accountmapping[split.AccountName],
    #                             entities_payee_id=payee_id,
    #                             entities_subcategory_id=entities_subcategory_id,
    #                             flag=split.Flag,
    #                             entities_transaction_id=transaction.id
    #                         ))
    #                 accumulatedSplits = []
    #         else:
    #             result = reTransfer.match(register_row.PayeeName)
    #             if result is not None:
    #                 payee_id = payeemapping[register_row.PayeeName]
    #                 otheraccount = result.group('account')
    #                 # this => other
    #                 transaction = Transaction(
    #                     amount=register_row.Inflow - register_row.Outflow,
    #                     date=register_row.Date,
    #                     entities_payee_id=payee_id,
    #                     entities_account_id=accountmapping[register_row.AccountName],
    #                     transfer_account_id=accountmapping[otheraccount],
    #                     flag=register_row.Flag
    #                 )
    #                 transfers.append(transaction)
    #             else:
    #                 if register_row.MasterCategoryName == '':
    #                     # an out of budget transaction most probably
    #                     entities_subcategory_id = None
    #                 else:
    #                     entities_subcategory_id = submapping[register_row.MasterCategoryName][register_row.SubcategoryName]
    #                 transactions.append(Transaction(
    #                     amount=register_row.Inflow - register_row.Outflow,
    #                     date=register_row.Date,
    #                     entities_account_id=accountmapping[register_row.AccountName],
    #                     entities_payee_id=payee_id,
    #                     entities_subcategory_id=entities_subcategory_id,
    #                     flag=register_row.Flag
    #                 ))
    #
    #     unsplittransactions=[transaction for transaction in transactions if transaction.entities_subcategory_id != split_id]
    #     splittransactions=[transaction for transaction in transactions if transaction.entities_subcategory_id == split_id]
    #
    #     transactions_dict={transaction.id:transaction for transaction in transactions}
    #     subtransactions_dict={subtransaction.id:subtransaction for subtransaction in subtransactions}
    #
    #     transfers_dict = {tr.id: tr for tr in transfers}
    #     random.shuffle(transfers)
    #
    #     for i1 in range(len(transfers)):
    #         tr1 = transfers[i1]
    #         for i2 in range(len(transfers)):
    #             if i2 > i1:
    #                 tr2 = transfers[i2]
    #                 if isinstance(tr1, Transaction) and isinstance(tr2, Transaction):
    #                     if tr1.entities_account_id == tr2.transfer_account_id \
    #                             and tr1.date == tr2.date \
    #                             and tr1.amount == -tr2.amount:
    #
    #                         tr1.transfer_transaction_id = tr2.id
    #                         tr2.transfer_transaction_id = tr1.id
    #
    #                         transactions.append(tr1)
    #                         transactions.append(tr2)
    #                 elif isinstance(tr1, Transaction) and isinstance(tr2, Subtransaction):
    #                     tr2parent = next(x for x in transactions if x.id == tr2.entities_transaction_id)
    #                     if tr1.entities_account_id == tr2.transfer_account_id \
    #                             and tr1.date == tr2parent.date \
    #                             and tr1.amount == -tr2.amount:
    #                         siblings = [subtransaction for subtransaction in subtransactions if subtransaction.entities_transaction_id == tr2parent.id]
    #
    #                         tr1.transfer_subtransaction_id = tr2.id
    #                         tr2.transfer_transaction_id = tr1.id
    #
    #                         transactions.append(tr1)
    #                         subtransactions.append(tr2)
    #                 elif isinstance(tr1, Subtransaction) and isinstance(tr2, Transaction):
    #                     tr1parent = next(x for x in transactions if x.id == tr1.entities_transaction_id)
    #                     if tr1parent.entities_account_id == tr2.transfer_account_id \
    #                             and tr1parent.date == tr2.date \
    #                             and tr1.amount == -tr2.amount:
    #                         siblings = [subtransaction for subtransaction in subtransactions if subtransaction.entities_transaction_id == tr1parent.id]
    #
    #                         tr1.transfer_transaction_id = tr2.id
    #                         tr2.transfer_subtransaction_id = tr1.id
    #
    #                         subtransactions.append(tr1)
    #                         transactions.append(tr2)
    #
    #
    #
    #     nYNABobject.budget.be_transactions.extend(transactions)
    #     nYNABobject.budget.be_subtransactions.extend(subtransactions)
    #
    #     nYNABobject.sync()
    #
    #
    #
    #     pass

if __name__ == "__main__":
    migrate_main()