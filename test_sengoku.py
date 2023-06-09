import pytest
from sengoku.api import API
from sengoku.middleware import Middleware

FILE_DIR = 'css'
FILE_NAME = 'main.css'
FILE_CONTENTS = 'body {background-color: blue}'


# helpers

def _create_static(static_dir):
    asset = static_dir.mkdir(FILE_DIR).join(FILE_NAME)
    asset.write(FILE_CONTENTS)

    return asset


# tests


def test_basic_route_adding(api):
    @api.route('/home')
    def home(req, res):
        res.text = 'the HOME page'


def test_route_overlap_throws_exception(api):
    @api.route('/home')
    def home(req, res):
        res.text = 'the HOME page'

    with pytest.raises(AssertionError):
        @api.route('/home')
        def home2(req, res):
            res.text = 'the HOME2 page'


def test_client_can_send_requests(api, client):
    res_text = "this is a response text"

    @api.route("/hey")
    def greeting(req, res):
        res.text = res_text

    assert client.get('http://testserver/hey').text == res_text


def test_parameterized_route(api, client):
    @api.route('/{name}')
    def hello(req, res, name):
        res.text = f'hey {name}'

    assert client.get('http://testserver/xavier').text == 'hey xavier'
    assert client.get('http://testserver/nguyen').text == 'hey nguyen'


def test_default_404_response(client):
    res = client.get('http://testserver/doesnotexist')

    assert res.status_code == 404
    assert res.text == 'Not found.'


def test_class_based_handler_get(api, client):
    response_text = 'this is a get request'

    @api.route('/book')
    class BookResource:
        def get(self, req, res):
            res.text = response_text

    assert client.get('http://testserver/book').text == response_text


def test_class_based_handler_post(api, client):
    response_text = 'this is a post request'

    @api.route('/book')
    class BookResource:
        def post(self, req, res):
            res.text = response_text

    assert client.post('http://testserver/book').text == response_text


def test_class_based_handler_not_allowed_method(api, client):
    @api.route('/book')
    class BookResource:
        def post(self, req, res):
            res.text = 'only post request allowed'

    with pytest.raises(AttributeError):
        client.get('http://testserver/book')


def test_alternative_route(api, client):
    response_text = 'Alternative way to add a route'

    def home(req, res):
        res.text = response_text

    api.add_route('/alternative', home)

    assert client.get('http://testserver/alternative').text == response_text


def test_template(api, client):
    @api.route('/html')
    def html_handler(req, res):
        res.body = api.template('index.html', context={'title': 'Some Title', 'name': 'Some Name'}).encode()

    response = client.get('http://testserver/html')

    assert 'text/html' in response.headers['Content-Type']
    assert 'Some Title' in response.text
    assert 'Some Name' in response.text


def test_custom_exception_handler(api, client):
    def on_exception(req, res, exc):
        res.text = 'AttributeErrorHappened'

    api.add_exception_handler(on_exception)

    @api.route('/')
    def index(req, res):
        raise AttributeError()

    response = client.get('http://testserver/')

    assert response.text == 'AttributeErrorHappened'


def test_404_is_returned_for_nonexistent_static_file(client):
    assert client.get('http://testserver/static/main.css').status_code == 404


def test_assets_are_served(tmpdir_factory):
    static_dir = tmpdir_factory.mktemp('static')
    _create_static(static_dir)
    api = API(static_dir=str(static_dir))
    client = api.test_session()

    response = client.get(f'http://testserver/static/{FILE_DIR}/{FILE_NAME}')

    assert response.status_code == 200
    assert response.text == FILE_CONTENTS


def test_middleware_methods_are_called(api, client):
    process_request_called = False
    process_response_called = False

    class CallMiddlewareMethods(Middleware):
        def __init__(self, app):
            super().__init__(app)

        def process_request(self, req):
            nonlocal process_request_called
            process_request_called = True

        def process_response(self, req, res):
            nonlocal process_response_called
            process_response_called = True

    api.add_middleware(CallMiddlewareMethods)

    @api.route('/')
    def index(req, res):
        res.text = 'index'

    client.get('http://testserver/')

    assert process_request_called is True
    assert process_response_called is True


def test_allowed_methods_for_function_based_handlers(api, client):
    @api.route('/home', allowed_methods=['post'])
    def home(req, res):
        res.text = 'Hello from the HOME page'

    with pytest.raises(AttributeError):
        client.get('http://testserver/home')

    assert client.post('http://testserver/home').text == 'Hello from the HOME page'


def test_json_response_helper(api, client):
    @api.route('/json')
    def json_handler(req, res):
        res.json = {'name': 'sengoku'}

    response = client.get('http://testserver/json')
    json_body = response.json()

    assert response.headers['Content-Type'] == 'application/json'
    assert json_body['name'] == 'sengoku'


def test_html_response_helper(api, client):
    @api.route('/html')
    def html_handler(req, res):
        res.html = api.template('index.html', context={'title': 'Best Title', 'name': 'Best Name'})

    response = client.get('http://testserver/html')

    assert 'text/html' in response.headers['Content-Type']
    assert 'Best Title' in response.text
    assert 'Best Name' in response.text


def test_text_response_helper(api, client):
    response_text = 'Just Plain Text'

    @api.route('/text')
    def text_handler(req, res):
        res.text = response_text

    response = client.get('http://testserver/text')

    assert 'text/plain' in response.headers['Content-Type']
    assert response.text == response_text


def test_manually_setting_body(api, client):
    @api.route('/body')
    def text_handler(req, res):
        res.body = b'Byte Body'
        res.content_type = 'text/plain'

    response = client.get('http://testserver/body')

    assert 'text/plain' in response.headers['Content-Type']
    assert response.text == 'Byte Body'
