import pytest
from sengoku.api import API


@pytest.fixture
def api():
    return API()


@pytest.fixture
def client(api):
    """
    The HTTPAdapter is designed to handle HTTP requests efficiently and supports features like
    connection pooling, persistent connections, and session-level configuration.
    ---
    However, when it comes to unit testing, the HTTPAdapter can present challenges. Since it relies
    on an actual web server, such as Gunicorn, to handle the requests, it introduces external dependencies
    into your tests. This can make your unit tests less isolated and potentially slower, as you need to start and stop
    the web server for each test run. Unit tests are ideally self-contained and should not rely on external resources.
    ---
    To overcome this limitation, the WSGI Transport Adapter can be used. It allows you to create a test client
    that interacts directly with a WSGI application, simulating the behavior of a web server. This eliminates the need
    for an actual web server during unit testing, making your tests more self-sustained and independent.
    ---
    The client uses the api fixture to return the test_session that written earlier.
    This client fixture can be used in unit tests.

    :param api:
    :return:
    """
    return api.test_session()
