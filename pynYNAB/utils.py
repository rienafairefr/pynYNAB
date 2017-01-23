import random
import time
from datetime import datetime

from pynYNAB.schema.Entity import AccountTypes
from pynYNAB.schema.budget import Account, Payee


def rate_limited(maxpersecond):
    minInterval = 1.0 / float(maxpersecond)

    def decorate(func):
        lastTimeCalled = [0.0]

        def rateLimitedFunction(*args, **kargs):
            elapsed = time.clock() - lastTimeCalled[0]
            leftToWait = minInterval - elapsed
            if leftToWait > 0:
                time.sleep(leftToWait)
            ret = func(*args, **kargs)
            lastTimeCalled[0] = time.clock()
            return ret

        return rateLimitedFunction

    return decorate


def chunk(iterable, chunk_size):
    """Generate sequences of `chunk_size` elements from `iterable`."""
    iterable = iter(iterable)
    while True:
        current_chunk = []
        try:
            for _ in range(chunk_size):
                current_chunk.append(next(iterable))
            yield current_chunk
        except StopIteration:
            if current_chunk:
                yield current_chunk
            break


# http://stackoverflow.com/q/10480806/1685379
def equal_dicts(a, b, ignore_keys):
    ka = set(a).difference(ignore_keys)
    kb = set(b).difference(ignore_keys)
    return ka == kb and all(a[k] == b[k] for k in ka)


def util_get_empty_account_by_name_if_doesnt_exist(client, name):
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
    client.reload()
    return account


def util_add_payee_by_name_if_doesnt_exist(client, name):
    payees = {p.name: p for p in client.budget.be_payees if
              p.name == name}
    if name in payees:
        return payees[name]
    payee = Payee(
        name=name
    )

    client.budget.be_payees.append(payee)
    client.sync()
    return payee