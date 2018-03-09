import signal
import sys

import asyncio
import aiohttp
import json

loop = asyncio.get_event_loop()
client = aiohttp.ClientSession(loop = loop)

def signal_handle(*kw):
  loop.stop()
  client.close()
  print("signal handled") 
  sys.exit(0)
  
signal.signal(signal.SIGINT, signal_handle)

async def get_json(client, url):
  async with client.get(url) as response:
    assert response.status == 200
    return await response.read()

async def get_reddit_top(subreddit, client):
  data1 = await get_json(client, 'https://www.reddit.com/r/' + subreddit + '/top.json?sort=top&t=day&limit=5')

  j = json.loads(data1.decode('utf8'))
  for i in j['data']['children']:
    score = i['data']['score']
    title = i['data']['title']
    link = i['data']['url']
    print('{} : {} ({})'.format(score , title , link ))
  print("Done ", subreddit, '\n')

q = asyncio.Queue()
async def produce( title, client):
  print("put to queue ", title)
  await q.put(title)

async def consumer():
  while True:
    value = await q.get()
    print("value got is :", value)
    await get_reddit_top(value, client)

print("before run_forever")
#asyncio.ensure_future( get_reddit_top('python', client) )
b = get_reddit_top('programming', client)
print(type(b), b)
#asyncio.ensure_future(b)  
asyncio.ensure_future( produce('linux', client ))
asyncio.ensure_future( produce('javascript', client ))

#asyncio.ensure_future( get_reddit_top('linux', client))
loop.create_task(consumer())
loop.run_until_complete(consumer())
print("after run_forever")
