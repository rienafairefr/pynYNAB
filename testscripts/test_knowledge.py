from test_live.test_live import liveTests

test_fixture = liveTests()
test_fixture.setUp()

test_fixture.test_add_delete_account()
test_fixture.test_add_delete_budget()
test_fixture.test_add_deletetransaction()