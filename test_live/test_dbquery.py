from sqlalchemy import extract

from pynYNAB.Client import clientfromargs
from pynYNAB.__main__ import parser
from pynYNAB.schema.budget import Transaction

args = parser.parse_known_args()[0]
client = clientfromargs(args)
client.sync()


session = client.session
march_payees = session.query(Transaction).filter(extract('month',Transaction.date.month)==3).all()
pass


