from pynYNAB.ClientFactory import nYnabClientFactory
from pynYNAB.scripts.helpers import get_config_from_yaml

config = get_config_from_yaml()

engine_url = 'sqlite:////tmp/persist.db'

factory1 = nYnabClientFactory(engine_url=engine_url)

client1 = factory1.create_client(**config)

factory2 = nYnabClientFactory(engine_url=engine_url)

client2 = factory2.create_client(sync=False, **config)

# client1 and client2 contain the same data
assert client1.budget == client2.budget
assert client1.catalog == client2.catalog
