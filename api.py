import inspect
import os
import requests
from parse import parse
from webob import Request, Response
from wsgiadapter import WSGIAdapter
from jinja2 import Environment, FileSystemLoader
from whitenoise import WhiteNoise
from middleware import Middleware


def default_response(response):
    response.status_code = 404
    response.text = 'Not found.'


class API:
    def __init__(self, templates_dir='templates', static_dir='static'):
        """
        Define a dict called self. routes where the framework will store paths as keys and handlers as value.
        Values of that dict will look something like this
        {
            '/home': <function home at 0x1100a70c8>,
            '/about': <function about at 0x1101a80c3>
        }
        ---
        Jinja2 uses a central object called the template Environment. This environment can be configured
        upon application initialization and templates can be loaded with the help of this environment.
        FileSystemLoader loads templates from the file system. This loader can find templates in folders
        on the file system and is the preferred way to load them. It takes the path t the templates directory
        as a parameter
        ---
        To configure WhiteNoise, wrap the WSGI app and give WhiteNoise the static folder path as a parameter.
        """
        self.routes = {}
        self.templates_env = Environment(loader=FileSystemLoader(os.path.abspath(templates_dir)))
        self.exception_handler = None
        self.whitenoise = WhiteNoise(self.wsgi_app, root=static_dir)
        self.middleware = Middleware(self)

    def __call__(self, environ, start_response):
        """
        Treat requests for static files differently from all other requests.
        When a request is coming in for a static file -> call WhiteNoise.
        For others -> call the middleware.

        :param environ:
        :param start_response:
        :return:
        """
        path_info = environ['PATH_INFO']

        if path_info.startswith('/static'):
            # remove /static from the path; otherwise, WhiteNoise won't find the files
            environ['PATH_INFO'] = path_info[len('/static'):]
            return self.whitenoise(environ, start_response)

        return self.middleware(environ, start_response)

    def wsgi_app(self, environ, start_response):
        request = Request(environ)

        response = self.handle_request(request)

        return response(environ, start_response)

    def add_route(self, path, handler):
        assert path not in self.routes, 'Such route already exists.'

        self.routes[path] = handler

    def route(self, path):
        """
        Take a path as an argument and in the wrapper method added this path in the self. routes dictionary
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

        try:
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
        except Exception as e:
            if self.exception_handler is None:
                raise e
            else:
                self.exception_handler(request, response, e)

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

    def template(self, template_name, context=None):
        if context is None:
            context = {}

        return self.templates_env.get_template(template_name).render(**context)

    def add_exception_handler(self, exception_handler):
        self.exception_handler = exception_handler

    def add_middleware(self, middleware_cls):
        self.middleware.add(middleware_cls)
