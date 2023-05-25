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
