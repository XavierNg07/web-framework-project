import pytest
import requests


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


def test_bumbo_test_client_can_send_requests(api, client):
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
