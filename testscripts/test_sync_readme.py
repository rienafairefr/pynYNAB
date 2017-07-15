from dotenv import load_dotenv,find_dotenv

from pynYNAB.Client import nYnabClient
from pynYNAB.scripts.__main__ import parser
load_dotenv(find_dotenv())

args = parser.parse_known_args()[0]

client = nYnabClient(email=args.email,password=args.password,budgetname='TestBudget')
client.sync()