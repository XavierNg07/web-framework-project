def app(environ, start_response):
    response_body = b"hello, world!"
    status = "200 OK"
    start_response(status, headers=[])
    return iter([response_body])
