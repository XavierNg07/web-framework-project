from api import API

app = API()


# The route method is a decorator that accepts a path and wraps the methods.
@app.route('/home')
def home(request, response):
    response.text = 'Hello from the HOME page'


@app.route('/about')
def about(request, response):
    response.text = 'Hello from the ABOUT page'
