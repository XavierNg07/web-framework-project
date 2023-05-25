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
