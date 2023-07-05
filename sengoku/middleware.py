"""
Middleware class that can modify an HTTP request and/or response and is designed to be chained together
to form a pipeline of behavioral changes during request processing.
The middleware is not fully responsible for responding to a client. Instead, it changes the behavior
in some way as part of the pipeline, leaving the actual response to come from something later in the pipeline.
"""
from webob import Request


class Middleware:
    def __init__(self, app):
        """
        Wrap around a WSGI app that have the ability to modify requests and responses.
        --FirstMiddleware(SecondMiddleware(our_wsgi_app))--

        :param app:
        """
        self.app = app

    def __call__(self, environ, start_response):
        """
        Middleware is the first entrypoint to the app, it is now called by a web server (e.g., Gunicorn).
        Thus, the middleware should implement the WSGI entrypoint interface.

        :param environ:
        :param start_response:
        :return:
        """
        request = Request(environ)
        response = self.app.handle_request(request)
        return response(environ, start_response)

    def add(self, middleware_cls):
        self.app = middleware_cls(self.app)

    def process_request(self, req):
        pass

    def process_response(self, req, res):
        pass

    def handle_request(self, request):
        """
        Call self.process_request to do something with the request. Then it delegates the response creation to the app
        that it is wrapping. Finally, it calls the process_response to do something with the response object.
        Then it simply returns the response upward.

        :param request:
        :return:
        """
        self.process_request(request)
        response = self.app.handle_request(request)
        self.process_response(request, response)

        return response
