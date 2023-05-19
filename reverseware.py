class Reverseware:
    """
    A middleware that reverses the response from our application.
    Since web servers will talk to this middleware first, and thus it must adhere to the same WSGI standards.
    That is, it should be a callable object that receives two params (environ and start_response) and then returns
    the response as an iterable.
    """
    def __init__(self, app):
        """
        This middleware is getting the response from the app that it wraps.

        :param app:
        """
        self.wrapped_app = app

    def __call__(self, environ, start_response):
        """
        This middleware is tweaking (reversing the response) from the app.
        This is generally what middlewares are used for: tweaking the request and the response.

        :param environ:
        :param start_response:
        :return:
        """
        wrapped_app_response = self.wrapped_app(environ, start_response)
        return [data[::-1] for data in wrapped_app_response]
