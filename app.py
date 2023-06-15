from api import API
from middleware import Middleware

app = API()


# function-based handlers

# The route method is a decorator that accepts a path and wraps the methods.
@app.route('/home')
def home(request, response):
    response.text = 'Hello from the HOME page'


@app.route('/about')
def about(request, response):
    response.text = 'Hello from the ABOUT page'


@app.route('/hello/{name}')
def greeting(request, response, name):
    response.text = f'Hello, {name}'


@app.route('/sub/{num_1:d}/{num_2:d}')
def sub(request, response, num_1, num_2):
    """
    Testing route whose params are given the type.
    If you pass in a non-digit, it will not be able to parse it and our default_response will do its job.

    :param request:
    :param response:
    :param num_1:
    :param num_2:
    :return:

    """
    diff = int(num_1) - int(num_2)
    response.text = f'{num_1} - {num_2} = {diff}'


# @app.route('/template')
# def template_handler(request, response):
#     response.body = app.template('index.html', context={'name': 'Bumbo', 'title': 'Best Framework'}).encode()

# @app.route('/json')
# def json_handler(req, res):
#     response_data = {'name': 'data', 'type': 'JSON'}
#     res.body = json.dumps(response_data).encode()
#     res.content_type = 'application/json'

@app.route('/exception')
def exception_throwing_handler(request, response):
    raise AssertionError('This handler should not be used.')


# class-based handlers

@app.route('/book')
class BooksHandler:
    def get(self, request, response):
        response.text = 'Book Page'

    def post(self, request, response):
        response.text = 'Endpoint to create a book'


# django-like handlers
def handler(request, response):
    response.text = 'sample'


app.add_route('/sample', handler)


# exception handler
def custom_exception_handler(request, response, exception_cls):
    response.text = str(exception_cls)


app.add_exception_handler(custom_exception_handler)


# custom middleware
class SimpleCustomMiddleware(Middleware):
    def process_request(self, req):
        print('Processing request', req.url)

    def process_response(self, req, res):
        print('Processing response', req.url)


app.add_middleware(SimpleCustomMiddleware)
