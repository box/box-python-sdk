# coding: utf-8

from bottle import HTTPError, ServerAdapter
from functools import partial, wraps
from threading import Thread


RETRY_AFTER_HEADER = str('Retry-After')


def abort(code, message=None, headers=None):
    """
    Abort a request and send a response with the given code, and optional message and headers.
    :raises:
        :class:`HTTPError`
    """
    raise HTTPError(code, {'message': message}, headers=headers)


def retry_after(delay, code=429):
    """
    Abort a request and send a response, including a Retry-After header informing the client when a retry of
    the request will be accepted.
    """
    abort(code, headers={RETRY_AFTER_HEADER: delay})


def authorize(method):
    """Decorator for a method that requires authorization. Unauthorized requests will be aborted with a 401."""
    @wraps(method)
    def authorized_method(self, *args, **kwargs):
        skip_auth = kwargs.pop('skip_auth', False)
        if not skip_auth:
            self.check_authorization_header()
        return method(self, *args, **kwargs)
    return authorized_method


def rate_limit(method):
    """Decorator for a method that requires rate limiting. Too many requests will be aborted with a 429."""
    @wraps(method)
    def limited_method(self, *args, **kwargs):
        skip_limit = kwargs.pop('skip_limit', False)
        if not skip_limit:
            self.check_rate_limits()
        return method(self, *args, **kwargs)
    return limited_method


def _route(verb, app, route):
    """Helper decorator to apply methods to routes."""
    def routed_method(method):
        setattr(method, 'verb', verb)
        setattr(method, 'app', app)
        setattr(method, 'route', route)
        return method
    return routed_method


def log_request(method):
    """Decorator for a method to add its request to the request log."""
    @wraps(method)
    def logged_method(self, *args, **kwargs):
        skip_log = kwargs.pop('skip_log', False)
        if not skip_log:
            self.append_to_request_log()
        return method(self, *args, **kwargs)
    return logged_method


GET = partial(_route, 'GET')
POST = partial(_route, 'POST')
PUT = partial(_route, 'PUT')
DELETE = partial(_route, 'DELETE')
OPTIONS = partial(_route, 'OPTIONS')


class StoppableWSGIRefServer(ServerAdapter):
    """
    Subclass of built-in Bottle server adapter that allows the server to be stopped.
    This is important for testing, since we don't want to "serve forever".
    """
    def __init__(self, host='127.0.0.1', port=8080, **options):
        super().__init__(host, port, **options)
        self.srv = None
        self._thread = None

    def run(self, app):
        from wsgiref.simple_server import WSGIRequestHandler, WSGIServer
        from wsgiref.simple_server import make_server

        class FixedHandler(WSGIRequestHandler):
            def address_string(self):
                return self.client_address[0]

            parent = self

            def log_request(self, *args, **kw):
                if not self.parent.quiet:
                    return WSGIRequestHandler.log_request(self, *args, **kw)

        handler_cls = self.options.get('handler_class', FixedHandler)
        server_cls = self.options.get('server_class', WSGIServer)

        self.srv = make_server(self.host, self.port, app, server_cls, handler_cls)
        thread = Thread(target=self.srv.serve_forever)
        thread.daemon = True
        thread.start()
        self._thread = thread
        self.srv.wait = self.wait
        return self.srv

    def wait(self):
        self.srv.server_close()
        self._thread.join()
