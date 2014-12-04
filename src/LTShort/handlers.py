import fnmatch
from urlparse import urlparse
from tornado import web, gen

import tornadoredis


def base62_encode(number):
    assert number >= 0, 'positive integer required'
    base62 = []
    while number != 0:
        number, i = divmod(number, 36)
        base62.append('ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789abcdefghijklmnopqrstuvwxyz'[i])
    return ''.join(reversed(base62))


class LTAPIHandler(web.RequestHandler):
    @property
    def pool(self):
        return self.settings['connection_pool']

    @property
    def text_mode(self):
        return True if self.get_argument('text_mode', default=None) == "1" else False


class LTShortURLHandler(LTAPIHandler):
    def initialize(self):
        self.clear()
        self.set_header('Content-Type', 'application/json; charset=UTF-8')

    def _compose_short_url_by_short_id(self, short_id):
        format = '{"short_url":"%s://%s/%s"}'
        if self.text_mode:
            format = "%s://%s/%s"
        return format % (
            self.request.protocol,
            self.settings['host'],
            short_id
        )

    @web.asynchronous
    @gen.engine
    def get(self):
        self.redirect('/', permanent=True)

    @web.asynchronous
    @gen.engine
    def post(self):
        url = self.get_argument('url')

        if url is None:
            self.send_error(400)
            return

        url = url[0:2048]
        url_parts = urlparse(url)
        if not url_parts.scheme or not url_parts.netloc:
            self.send_error(400)
            return

        if url_parts.netloc == self.settings['host']:
            cp = tornadoredis.Client(connection_pool=self.pool)
            expanded = yield gen.Task(cp.get, 'url-target:' + url_parts.path[1:])
            yield gen.Task(cp.disconnect)
            if expanded:
                if self.text_mode:
                    self.finish(expanded)
                else:
                    self.finish('{"long_url":"%s"}' % expanded)
                return
            else:
                self.send_error(404)
                return

        for pattern in self.settings['allowed_hosts']:
            if fnmatch.fnmatch(url_parts.netloc, pattern):
                break
        else:
            self.send_error(400)
            return

        cp = tornadoredis.Client(connection_pool=self.pool)
        short_id = yield gen.Task(cp.get, 'reverse-url:' + url)
        yield gen.Task(cp.disconnect)
        if short_id:
            self.finish(self._compose_short_url_by_short_id(short_id))
        else:
            cp = tornadoredis.Client(connection_pool=self.pool)
            short_num = yield gen.Task(cp.incr, 'last-url-id')
            short_id = base62_encode(short_num)
            yield gen.Task(cp.set, 'url-target:' + short_id, url)
            yield gen.Task(cp.set, 'reverse-url:' + url, short_id)
            yield gen.Task(cp.disconnect)

            self.finish(self._compose_short_url_by_short_id(short_id))


class LTRedirectHandler(LTAPIHandler):
    @web.asynchronous
    @gen.engine
    def get(self):
        short_id = self.request.path[1:]
        cp = tornadoredis.Client(connection_pool=self.pool)
        url = yield gen.Task(cp.get, 'url-target:' + short_id)
        yield gen.Task(cp.disconnect)
        if url:
            self.redirect(url, permanent=True)
        else:
            self.write_error(404)
