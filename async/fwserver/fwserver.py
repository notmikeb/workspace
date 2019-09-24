#!/bin/python3

"""
asycio server
https://stackoverflow.com/questions/48506460/python-simple-socket-client-server-using-asyncio
"""

import asyncio
import socket

async def handle_client(client):
    request = None
    while request != 'quit' and request != '9':
        request = (await loop.sock_recv(client, 255))
        try:
            request = request.decode('utf8')
            response = str(eval(request)) + '\n'
        except:
            import traceback
            traceback.print_exc()
            response = 'error '  
        await loop.sock_sendall(client, response.encode('utf8'))
        request = request.strip()
        print("client1 '{}'".format(request))
    print("prepare close")
    client.close()

async def handle_client2(client):
    request = None
    while request != 'quit' and request != '9':
        request = (await loop.sock_recv(client, 255))
        try:
            request = request.decode('utf8')
            response = str(eval(request)) + '\n'
        except:
            pass
            response = 'error '  
        await loop.sock_sendall(client, response.encode('utf8'))
        request = request.strip()
        print("client2 '{}'".format(request))
    print("prepare close")
    client.close()


async def run_server():
    while True:
        client, _ = await loop.sock_accept(server)
        loop.create_task(handle_client(client))

async def run_server2():
    while True:
        client, _ = await loop.sock_accept(server2)
        loop.create_task(handle_client2(client))


server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(('localhost', 15555))
server.listen(8)
server.setblocking(False)

server2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server2.bind(('localhost', 15556))
server2.listen(2)
server2.setblocking(False)

import signal
import os
import time
import functools

def handler(signum, frame):
    print('Signal handler called with signal', signum)
    import sys
    print("before sys.exit(-1)")
    sys.exit(-1)
    print("after sys.exit(-1)")

#signal.signal(signal.SIGINT, handler) # windows 
# TBD https://stackoverflow.com/questions/7085604/sending-c-to-python-subprocess-objects-on-windows
# TBD https://stackoverflow.com/questions/37417595/graceful-shutdown-of-asyncio-coroutines

loop = asyncio.get_event_loop()
try:
    loop.run_until_complete( asyncio.gather(run_server(), run_server2()) )
except KeyboardInterrupt:
    print("Received exit, exiting")
finally:
    print("finally")