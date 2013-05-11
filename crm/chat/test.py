import os, sys
sys.path.append('/root/django_crm')
os.environ['DJANGO_SETTINGS_MODULE'] = 'django_crm.settings'
from crm.models import ChatMessage
from tornado.options import options, define, parse_command_line
import django.conf
import django.contrib.auth
import django.core.handlers.wsgi
import django.db
import django.utils.importlib

import tornado.httpserver
import tornado.ioloop
import tornado.web
import tornado.websocket
import tornado.wsgi
import datetime

import httplib
import json
import logging

from tornado.options import options, define

define('port', type=int, default=8080)


class BaseWebSocketHandler(tornado.websocket.WebSocketHandler):
    def prepare(self):
        super(BaseWebSocketHandler, self).prepare()
        # Prepare ORM connections
        django.db.connection.queries = []

    def finish(self, chunk = None):
        super(BaseWebSocketHandler, self).finish(chunk = chunk)
        # Clean up django ORM connections
        django.db.connection.close()
        if False:
            logging.info('%d sql queries' % len(django.db.connection.queries))
            for query in django.db.connection.queries:
                logging.debug('%s [%s seconds]' % (query['sql'], query['time']))

        # Clean up after python-memcached
        from django.core.cache import cache
        if hasattr(cache, 'close'):
            cache.close()

    def get_django_session(self):
        if not hasattr(self, '_session'):
            engine = django.utils.importlib.import_module(
                django.conf.settings.SESSION_ENGINE)
            session_key = self.get_cookie(django.conf.settings.SESSION_COOKIE_NAME)
            self._session = engine.SessionStore(session_key)
        return self._session

    def get_user_locale(self):
        # locale.get will use the first non-empty argument that matches a
        # supported language.
        return tornado.locale.get(
            self.get_argument('lang', None),
            self.get_django_session().get('django_language', None),
            self.get_cookie('django_language', None))

    def get_current_user(self):
        # get_user needs a django request object, but only looks at the session
        class Dummy(object): pass
        django_request = Dummy()
        django_request.session = self.get_django_session()
        user = django.contrib.auth.get_user(django_request)
        if user.is_authenticated():
            return user
        else:
            # try basic auth
            if not self.request.headers.has_key('Authorization'):
                return None
            kind, data = self.request.headers['Authorization'].split(' ')
            if kind != 'Basic':
                return None
            (username, _, password) = data.decode('base64').partition(':')
            user = django.contrib.auth.authenticate(username=username, password=password)
            if user is not None and user.is_authenticated():
                return user
            return None

    def get_django_request(self):
        request = django.core.handlers.wsgi.WSGIRequest(
            tornado.wsgi.WSGIContainer.environ(self.request))
        request.session = self.get_django_session()

        if self.current_user:
            request.user = self.current_user
        else:
            request.user = django.contrib.auth.models.AnonymousUser()
        return request

class HelloHandler(tornado.web.RequestHandler):
    def get(self):
        self.write('Hello from tornado')

class WebSocketHandler(BaseWebSocketHandler):
    def open(self):
        print 'Websocket opened'
        print 'Current user: ' + str(self.get_current_user())

    def on_message(self, message):
        print 'Websocket got a message: ' + str(message)

    def on_close(self):
        print 'Websocket closed'


class NoCacheStaticHandler(tornado.web.StaticFileHandler):
    """ Request static file handlers for development and debug only.
    It disables any caching for static file.
    """
    def set_extra_headers(self, path):
        self.set_header('Cache-Control', 'no-cache, must-revalidate')
        self.set_header('Expires', '0')
        now = datetime.datetime.now()
        expiration = datetime.datetime(now.year-1, now.month, now.day)
        self.set_header('Last-Modified', expiration)


def main():
    wsgi_app = tornado.wsgi.WSGIContainer(
            django.core.handlers.wsgi.WSGIHandler())
    tornado_app = tornado.web.Application(
        [
            (r'/static/(.*)', NoCacheStaticHandler, {'path': 'fe/static'}),
            ('/hello-tornado', HelloHandler),
            ('/chat', WebSocketHandler),
            ('.*', tornado.web.FallbackHandler, dict(fallback=wsgi_app)),
            ])
    server = tornado.httpserver.HTTPServer(tornado_app)
    server.listen(7070)
    tornado.ioloop.IOLoop.instance().start()

if __name__ == '__main__':
    main()