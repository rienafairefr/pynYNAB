import random
import time
from datetime import datetime

from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm.exc import NoResultFound

from pynYNAB.schema.Entity import AccountTypes
from pynYNAB.schema.budget import Account, Payee


def rate_limited(maxpersecond):
    minInterval = 1.0 / float(maxpersecond)

    def decorate(func):
        lastTimeCalled = [None]

        def rateLimitedFunction(*args, **kargs):
            if lastTimeCalled[0] is not None:
                elapsed = time.clock() - lastTimeCalled[0]
                leftToWait = minInterval - elapsed
                if leftToWait > 0:
                    time.sleep(leftToWait)
            ret = func(*args, **kargs)
            lastTimeCalled[0] = time.clock()
            return ret

        return rateLimitedFunction

    return decorate


def get_or_create_account(client, name):
    accounts = {a.account_name: a for a in client.budget.be_accounts if
                a.account_name == name}
    if name in accounts:
        account = accounts[name]
        client.delete_account(account)

    account = Account(
        account_type=AccountTypes.Checking,
        account_name=name
    )

    client.add_account(account, balance=random.randint(-10, 10), balance_date=datetime.now())
    return account


def get_or_create_payee(client, name):
    payees = {p.name: p for p in client.budget.be_payees if
              p.name == name}
    if name in payees:
        return payees[name]
    payee = Payee(
        name=name
    )

    client.budget.be_payees.append(payee)
    client.push(1)
    return payee

def get_one_or_create(session,
                      model,
                      create_method='',
                      create_method_kwargs=None,
                      **kwargs):
    try:
        return session.query(model).filter_by(**kwargs).one(), False
    except NoResultFound:
        kwargs.update(create_method_kwargs or {})
        created = getattr(model, create_method, model)(**kwargs)
        try:
            session.add(created)
            session.flush()
            return created, True
        except IntegrityError:
            session.rollback()
            return session.query(model).filter_by(**kwargs).one(), True