import re, time, json, logging, hashlib, base64, asyncio


from aiohttp import web
from coroweb import get, post

from flask import jsonify

@get('/api/user/{id}')
def api_get_user(*, id):
    blog = { 'id' : id }
    return web.Response(text='Forbidden', status='403')

@get('/api/data/{id}')
def api_get_blog(*, id):
    blog = { 'id' : id }
    return web.Response(text="this is a {}".format(id), status='200')