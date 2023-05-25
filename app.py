from api import API

app = API()


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


@app.route('/book')
class BookResource:
    def get(self, request, response):
        response.text = 'Book Page'

    def post(self, request, response):
        response.text = 'Endpoint to create a book'


@app.route('/sum/{num_1:d}/{num_2:d}')
def sum(request, response, num_1, num_2):
    """
    Testing route whose params are given the type.
    If you pass in a non-digit, it will not be able to parse it and our default_response will do its job.

    :param request:
    :param response:
    :param num_1:
    :param num_2:
    :return:

    """
    total = int(num_1) + int(num_2)
    response.text = f'{num_1} + {num_2} = {total}'
