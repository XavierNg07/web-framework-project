import inspect
import requests
from parse import parse
from webob import Request, Response
from wsgiadapter import WSGIAdapter


def default_response(response):
    response.status_code = 404
    response.text = 'Not found.'


class API:
    def __init__(self):
        """
        Define a dict called self.routes where the framework will store paths as keys and handlers as value.
        Values of that dict will look something like this
        {
            '/home': <function home at 0x1100a70c8>,
            '/about': <function about at 0x1101a80c3>
        }
        """
        self.routes = {}

    def __call__(self, environ, start_response):
        request = Request(environ)

        response = self.handle_request(request)

        return response(environ, start_response)

    def add_route(self, path, handler):
        assert path not in self.routes, 'Such route already exists.'

        self.routes[path] = handler

    def route(self, path):
        """
        Take a path as an argument and in the wrapper method added this path in the self.routes dictionary
         as a key and the handler as a value.

        :param path:
        :return:
        """
        def wrapper(handler):
            self.add_route(path, handler)
            return handler

        return wrapper

    def find_handler(self, request_path):
        """
        Compare the path to the request path, the method tries to parse it and if there is a result,
        it returns both the handler and keyword params as a dictionary.

        :param request_path:
        :return:
        """
        for path, handler in self.routes.items():
            parse_result = parse(path, request_path)
            if parse_result is not None:
                return handler, parse_result.named
        return None, None

    def handle_request(self, request):
        """
        Check if the handler is a function or if it is a class.
        If it's a class, depending on the request method, it should call the appropriate method of the class.
        That is, if the request method is GET it should call the get() method of the class...
        if it is POST it should call the post() method... and so on

        :param request:
        :return:
        """
        response = Response()

        handler, kwargs = self.find_handler(request_path=request.path)

        if handler is not None:
            if inspect.isclass(handler):
                handler = getattr(handler(), request.method.lower(), None)
                # if the handler is None, it means that such function was not implemented in the class
                # and the request method is not allowed
                if handler is None:
                    raise AttributeError('Method not allowed', request.method)

            handler(request, response, **kwargs)
        else:
            default_response(response)

        return response

    def test_session(self, base_url='http://testserver'):
        """
        To use the Requests WSGI Adapter, you need to mount it to a Session object.
        That way, any request made using this test_session whose URL starts with the given prefix,
        will use the given RequestsWSGIAdapter.

        :param base_url:
        :return:
        """
        session = requests.Session()
        session.mount(prefix=base_url, adapter=WSGIAdapter(self))
        return session
