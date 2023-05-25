import pytest
from api import API


@pytest.fixture
def api():
    return API()


@pytest.fixture
def client(api):
    """
    The client uses the api fixture to return the test_session that written earlier.
    This client fixture can be used in unit tests.

    :param api:
    :return:
    """
    return api.test_session()
