from wsgiref.simple_server import make_server
from reverseware import Reverseware


def application(environ, start_response):
    """
    According to PEP 333, the document which specifies the details of WSGI,
     the application interface is implemented as a callable object such as a function.
     This object should accept two positional arguments and return the response body as strings in an iterable.

    :param environ: a dictionary with environment variables
    :param start_response: a callback function that will be used to send HTTP statuses and HTTP headers to the server
    :return: the response body as strings in an iterable
    """
    response_body = [
        f'{key}: {value}' for key, value in sorted(environ.items())
    ]
    response_body = '\n'.join(response_body)

    status = '200 OK'

    response_headers = [
        ('Content-type', 'text/plain'),
    ]

    start_response(status, response_headers)

    return iter([response_body.encode('utf-8')])


def start():
    server = make_server('localhost', 8000, app=Reverseware(application))
    server.serve_forever()
