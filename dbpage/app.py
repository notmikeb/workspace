#!/usr/bin/python3

import logging; logging.basicConfig(level=logging.INFO)

import asyncio, os, json, time
from datetime import datetime

from aiohttp import web

from config import configs

import orm
from coroweb import add_routes, add_static
#from handlers import cookie2user, COOKIE_NAME


@asyncio.coroutine
def init(loop):
    yield from orm.create_pool(loop=loop, **configs.db)
    app = web.Application(loop=loop, middlewares=[
        #logger_factory, auth_factory, response_factory        
    ])
    #init_jinja2(app, filters=dict(datetime=datetime_filter))
    add_routes(app, 'handlers')
    add_static(app)
    srv = yield from loop.create_server(app.make_handler(), '0.0.0.0', 9000)
    logging.info('server started at http://127.0.0.1:9000...')
    return srv

loop = asyncio.get_event_loop()
loop.run_until_complete(init(loop))
loop.run_forever()
