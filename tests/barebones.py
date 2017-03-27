from pynYNAB.Client import nYnabClient
from pynYNAB.connection import nYnabConnection

email = "############"
password = "######"

connection = nYnabConnection(email, password)
client = nYnabClient(nynabconnection=connection,budgetname='TestBudget')
client.sync()