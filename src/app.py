#!/usr/bin/env python
# -*- coding: UTF-8 -*-
#
# The MIT License (MIT)
# Copyright © 2013 Lex Tang, http://LexTang.com
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the “Software”), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
#
"""
lexr.us app

"""

__author__ = 'lex'

import os
import pwd
from tornado import web, ioloop, httpserver
from tornado.options import options, define
from LTShort import handlers
import tornadoredis


define('port', default=1983, type=int, help='server port')
define('host', default='lexr.us', type=str, help='server host name')
define('listen', default='0.0.0.0', type=str, help='listen interface')
define('num_processes', default=1, type=int, help='number of subprocesses(0 - auto)')
define('template_path', default='tpl', type=str, help='template path')
define('redis_host', default='127.0.0.1', type=str, help='Redis server host')
define('redis_port', default=6379, type=int, help='Redis server port')
define('user', default='', type=str, help='user')
define('group', default='', type=str, help='group')
define('allowed_hosts', default='*', type=str, help='allowed hosts, comma-separated values', multiple=True)


class LTShort(web.Application):
    def __init__(self):
        connection_pool = tornadoredis.ConnectionPool(max_connections=500, wait_for_available=True, host=options.redis_host, port=options.redis_port)
        settings = {
            'gzip': True,
            'autoescape': 'xhtml_escape',
            'connection_pool': connection_pool,
            'template_path': options.template_path,
            'host': options.host,
            'static_path': os.path.join(os.path.dirname(__file__), "public"),
            'allowed_hosts': options.allowed_hosts,
        }
        routes = [
            (r'/(.{0})', web.StaticFileHandler, {
                'path': settings['static_path'],
                'default_filename': 'index.html'
            }),
            (r'/public/(.*)', web.StaticFileHandler, {
                'path': settings['static_path'],
            }),
            (r'/(favicon\.ico)', web.StaticFileHandler, {
                'path': settings['static_path'],
            }),
            (r'/api/url', handlers.LTShortURLHandler),
            (r'/.*', handlers.LTRedirectHandler),
        ]



        web.Application.__init__(self, routes, **settings)


def main():
    options.parse_command_line()
    if options.group:
        # define group to run as
        run_as_group = options.group
        gid = pwd.getpwnam(run_as_group)[3]
        os.setgid(gid)
    if options.user:
        # define user to run as
        run_as_user = options.user
        uid = pwd.getpwnam(run_as_user)[2]
        os.setuid(uid)

    app = LTShort()
    server = httpserver.HTTPServer(app)
    server.bind(options.port, options.listen)
    server.start(options.num_processes)

    ioloop.IOLoop.instance().start()

if __name__ == '__main__':
    main()
