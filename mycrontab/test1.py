# -*- coding: utf-8 -*-
import sys
#sys.path = ["c:\\python27\\lib", "c:\\python27\\lib\\site-packages"]

from datetime import datetime
import time

import sqlite3
conn = sqlite3.connect('testdb.db')
DATETIME_FORMAT = "%Y%m%d %H:%M:%S"

def getCronTable(c):
    sqlstring = "select * from crontable order by id desc"
    r = c.execute(sqlstring)
    items = [ i for i in r ]
    print "items are {}".format(items)
    #id, cronstring, count, action, param, resonse, comment, lastrun
    for i in items:
        print "{} {}".format(i[0], i[1])
    return items

def RunCommand(a,b):
    msg = "RunCommand '{}' '{}'".format(a, b)
    print msg
    global c1
    c1.sendMsg(msg)

from crontab import CronTab
ct1 = CronTab(tab="""
""", handler = RunCommand)


#j1 = c1.new(command='j:\\testlog.bat item2haha', comment='SomeID')
#j1.minute.every(2)

#j1 = c1.new(command='j:\\testlog.bat item5 ', comment='SomeID')
#j1.minute.every(5)

items = getCronTable(conn)
for item in items:
    id = item[0]
    cronstring = item[1]
    action = item[3]
    param = item[4]
    comment = item[6]
    lastrun = item[7]
    print "action {} id {} cronstring {}".format(action, id, cronstring)
    job1 = ct1.new(line = "{} {} {} #{}".format(cronstring, action, param,comment) , command = action, comment=comment, id = id)
    print ("job1 type{} ".format( type(job1) ))
    #job1.parse(cronstring)
    print "job render '{}' id:{}".format(job1.render(), job1.id)
    
print ct1.render()

#for result in ct1.run_scheduler(timeout = 1, wrap = True):
#    print "This was printed to stdout by the process."
#ct1.run_sleeper(timeout = 3, loop = 20, test = True)

###################################################################
import telepot
import time
import urllib3
#from lxml import html
import requests

searchKeywords = ["mtk", "asus", "acer", "csr", "qualcomm", "bluetooth"]
#searchData = [u"聯發科", "華碩", "acer", "csr", "qualcomm", u"藍牙"]
searchData = [u"mediatek", "asus", "acer", "csr", "qualcomm", u"bluetooth"]


def getItems(url = ''):
  URL = 'https://news.google.com/news/story?ncl=d9fvvLVMNYA0pVM38XCeibLFYUucM&q=%E8%81%AF%E7%99%BC%E7%A7%91&lr=Chinese&hl=zh-TW&sa=X'
  response = requests.get(URL)
  pagehtml = html.fromstring(response.text)
  news = pagehtml.xpath('//a/span[@class="titletext"]')

  items = []
  for a in news:
    u1 = a.getparent().get('href')
    t1 = "".join(list(a.itertext()))
    items.append( [u1, t1] )
  return items

# You can leave this bit out if you're using a paid PythonAnywhere account
proxy_url = "http://proxy.server:3128"
"""
telepot.api._pools = {
    'default': urllib3.ProxyManager(proxy_url=proxy_url, num_pools=3, maxsize=10, retries=False, timeout=30),
}
telepot.api._onetime_pool_spec = (urllib3.ProxyManager, dict(proxy_url=proxy_url, num_pools=1, maxsize=1, retries=False, timeout=30))
# end of the stuff that's only needed for free accounts
"""
bot = telepot.Bot('384930197:AAGeEfV7A-1n9RA-syHx573KfZ7IocD7vm0')
#bot.deleteWebhook()

import threading
import time

class cronThread(threading.Thread):
  def __init__(self):
    super(cronThread, self).__init__()
    self.chatid = -1
    self.bot = None
    self.started = False
  def setChatId(self, chatid):
    if self.chatid != chatid:
      self.chatid = chatid
      self.sendMsg("initial the cron runner~~~")
    else:
      pass
      ## ignore the setting
  def isStart(self):
    return self.started
  def setBot(self, bot):
    self.bot = bot
  def parseCommand(self, cmd):
    if cmd.lower() == 'start':
      if self.chatid >0:
        self.started = True
        self.sendMsg("bot:start the runner loop")
      else:
        print("error to start cmd loop~~~")
    elif cmd.lower() == 'stop':
      if self.chatid >0:
        self.sendMsg("bot: stop the runner loop")
        self.started = False
      else:
        print("error to start cmd loop~~~")
    elif cmd.lower() == 'id':
      self.sendMsg('id is {}'.format(self.chatid))
    else:
      print("no handle '{}'".format(cmd.lower()))

  def sendMsg(self, txt):
    if self.bot != None and self.chatid > 0:
      #print ("telebot:{} {}".format(self.chatid, txt))
      self.bot.sendMessage(self.chatid, txt, parse_mode = "HTML")
  def run(self):
    self.sendMsg("run_sleeper start")
    ct1.run_sleeper(timeout = 3, loop = 20, test = False)
    self.sendMsg("run_sleeper end")
    
  def run2xxx(self):
    self.sendMsg("run start")
    count = 1
    while 1:
      if self.chatid > 0 and self.bot != None and self.started == True:
        self.sendMsg("run count:{}".format(count))
        count += 1
      else:
        time.sleep(60)
      time.sleep(10)
    self.sendMsg("run done")

c1 = cronThread()
c1.setBot(bot)
c1.start()

def handle(msg):
    content_type, chat_type, chat_id = telepot.glance(msg)
    print(content_type, chat_type, chat_id)

    if content_type == 'text':
        if msg["text"].lower() in searchKeywords:
            itext = ""
            for k in getItems(msg["text"].lower())[:5]:
                u1, t1 = k
                itext += "<a href='{}'>{}</a>".format(u1, t1)
            bot.sendMessage(chat_id, "MTKer!\n{}".format(itext), parse_mode = "HTML")
        ret = "You said '{}'".format(msg["text"])
        #ret = "<a href='www.kimo.tw'>{}</a>".format(msg["text"])
        c1.parseCommand(msg["text"])
        bot.sendMessage(chat_id, ret, parse_mode = "HTML")
        c1.setChatId(chat_id)
        print("chat_id {}".format(chat_id))
    else:
        print("content_type {}".format(content_type))

bot.message_loop(handle)

print ('Listening ...')

# Keep the program running.
while 1:
    time.sleep(1000)
print "end"	