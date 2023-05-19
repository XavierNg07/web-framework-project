from webob import Request, Response


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

    def route(self, path):
        """
        Take a path as an argument and in the wrapper method added this path in the self.routes dictionary
         as a key and the handler as a value.

        :param path:
        :return:
        """
        def wrapper(handler):
            self.routes[path] = handler
            return handler
        return wrapper

    def find_handler(self, request_path):
        for path, handler in self.routes.items():
            if path == request_path:
                return handler

    def default_response(self, response):
        response.status_code = 404
        response.text = 'Not found.'

    def handle_request(self, request):
        response = Response()

        handler = self.find_handler(request_path=request.path)

        if handler is not None:
            handler(request, response)
        else:
            self.default_response(response)

        return response

