# -*- coding: utf-8 -*-
import sys
#sys.path = ["c:\\python27\\lib", "c:\\python27\\lib\\site-packages"]

from datetime import datetime
import time

import sqlite3
#conn = sqlite3.connect('testdb.db')
DATETIME_FORMAT = "%Y%m%d %H:%M:%S"
g_chatid = 0

def openDb():
    conn = sqlite3.connect('testdb.db')
    return conn
def closeDb(c):
    c.close()
    
def updateRecordLastrun(id, date1):
    c = openDb()
    datestring = date1.strftime(DATETIME_FORMAT)
    sqlstring = "update crontable set lastrun= '{}' where id={}".format(datestring, id)
    r = c.execute(sqlstring)
    c.commit()
    print ("result r:{}".format(r))
    closeDb(c)
    return r

def getRecordLastrun(id):
    c = openDb()
    sqlstring = "select lastrun from crontable where id={}".format(id)
    r = c.execute(sqlstring)
    c.commit()
    print ("result r:{}".format(r))
    ret = r.fetchone()
    closeDb(c)
    return ret
    
def getCronTable(c):
    sqlstring = "select * from crontable order by id desc"
    r = c.execute(sqlstring)
    items = [ i for i in r ]
    print "items are {}".format(items)
    #id, cronstring, count, action, param, resonse, comment, lastrun
    for i in items:
        print "{} {}".format(i[0], i[1])
    return items
    
def getNoackRecords():
    c = openDb()
    sqlstring = "select id from crontable where ack <> 1 and action not like '%/checknoack%'"
    r = c.execute(sqlstring)
    c.commit()
    all = r.fetchall()
    noacklist = [i[0] for i in all]
    print ("result r:{}".format(noacklist))
    closeDb(c)
    return noacklist

def setNoackRecord(id, b):
    c = openDb()
    if b:
        ack_value = 1
    else:
        ack_value = 0
    sqlstring = "update crontable set ack={} where id={}".format(ack_value, id )
    r = c.execute(sqlstring)
    c.commit()
    print ("result r:{}".format(r))
    closeDb(c)
    return r

    
def getChatId(c):
    sqlstring = "select chatid, comment from chattable"
    r = c.execute(sqlstring)
    a = r.fetchone()
    return a

def sendMsg(msg):
    if g_chatid > 0:
        bot.sendMessage(g_chatid, msg )

def HandleCron(cmdstring, job = None, trigger = None):
    ret = True;
    try:
        cmds = cmdstring.split(' ')
        cmd = cmds[0]
        print("cmd is {}".format(cmd))
        if job != None:
            markup = ReplyKeyboardMarkup(
                                    keyboard=[
                                        [KeyboardButton(text="/cronack id:{}".format(job.id)), KeyboardButton(text="/cron id:{}".format(job.id))]
                                    ]
                                )
            if job.id >= 0 and trigger == 'cron':                    
                setNoackRecord(job.id, 0)
        else:
            markup = None

        if cmd.lower() in ["cron" , "/cron"]:
            # show all 
            msgs = []
            for i, item in enumerate(ct1):
                a = getRecordLastrun(item.id)
                msgs.append( "id:{} DB-last_run:'{}' next:'{}' last_run:'{}'\n".format(item.id, a[0], item.get_next_time(), item.last_run ))
            if len(ct1)>0:
                bot.sendMessage(g_chatid, "".join(msgs) )
            else:
                bot.sendMessage("No record !")
        elif cmd.lower() in ["/echo", "/show", "/type"]:
            global g_chatid
            msg = " ".join(cmds[1:])
            if job != None:
                msg = "[id:{}]".format(job.id) + msg
            print "my msg is ", msg
            bot.sendMessage(g_chatid, msg,
                               reply_markup = markup, parse_mode = "HTML")
        elif cmd.lower() == '/checknoack':
            if job != None:
                ignoreid = job.id
                setNoackRecord(job.id, True)        
            noacks = getNoackRecords()
            print ("noacks '{}'".format(noacks))
            bot.sendMessage(g_chatid, "checknoack----start");
            ignoreid = -1
            for i, id in enumerate(noacks):
                print ("get the index:'{}'".format(i))
                for job in ct1:
                    if job.id == id and ignoreid != id:
                        # do the command again
                        HandleCron(job.command, job)
                time.sleep(1)
            bot.sendMessage(g_chatid, "checknoack----end");
        elif cmd.lower() in ["/cronack" ,"cron:ack"] :
            id = -1
            try:
                id = int(cmds[1].split(':')[1])
                print("ack id:{}".format(id))
            except:
                print("Has exception")
            if id > 0:
                updateRecordLastrun(id, datetime.now())
                ret = getRecordLastrun(id)
                print "ret ", ret
                ret = True
            setNoackRecord(id, True)
            sendMsg('ack to id:{} done'.format(id))
        else:
            print("cron cmd:'{}'".format(cmd))
            ret = False
    except:
        exc_type, exc_value, exc_traceback = sys.exc_info()
        print exc_type, exc_value, exc_traceback
        
    return ret
        
from crontab import CronTab
ct1 = CronTab(tab="""
""", handler = HandleCron)


#j1 = c1.new(command='j:\\testlog.bat item2haha', comment='SomeID')
#j1.minute.every(2)

#j1 = c1.new(command='j:\\testlog.bat item5 ', comment='SomeID')
#j1.minute.every(5)

conn = openDb()
items = getCronTable(conn)
closeDb(conn)
conn = None
for item in items:
    id = item[0]
    cronstring = item[1]
    action = item[3]
    param = item[4]
    comment = item[6]
    last_run = item[7]
    try:
        print ("action", action, " id ", id, " constring " , cronstring)
        print ("action {} id {} cronstring {}".format(action.encode('utf8'), id, cronstring))
    except:
        pass
    #job1 = ct1.new(line = u"{} {} {} #{}".format(cronstring, action.encode('utf8'), param, comment) , command = action, comment=comment, id = id)
    if param:
        param = param.encode('utf8')
    if comment:
        comment = comment.encode('utf8')
    line = "{} {} {} #{}".format(cronstring, action.encode('utf8'), param, comment)
    job1 = ct1.new(line = line , command = action.encode('utf8'), id = id)
    try:
        job1.last_run = datetime.strptime(last_run, DATETIME_FORMAT)
    except:
        job1.last_run = None
    #print ("job1 type{} last_run:{}".format( type(job1), job1.last_run ))
    #job1.parse(cronstring)
    #print "job render '{}' id:{} last_run:{}".format(job1.render().encode('utf8'), job1.id, job1.last_run)
    
print ct1.render()

#for result in ct1.run_scheduler(timeout = 1, wrap = True):
#    print "This was printed to stdout by the process."
#

###################################################################
import telepot
import time
import urllib3
#from lxml import html
import requests
from telepot.namedtuple import *

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
      self.sendMsg(u"initial runner by setchatid 你好")
    else:
      pass
      ## ignore the setting
  def isStart(self):
    return self.started
  def setBot(self, bot):
    self.bot = bot
  def parseCommand(self, cmd):
    ret = True
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
      ret = HandleCron(cmd)
      if ret != True:
        print("no handle '{}'".format(cmd))
    return ret

  def sendMsg(self, txt):
    if self.bot != None and self.chatid > 0:
      #print ("telebot:{} {}".format(self.chatid, txt))
      self.bot.sendMessage(self.chatid, txt, parse_mode = "HTML")
  def run(self):
    self.sendMsg("run_sleeper start")
    #ct1.run_sleeper(timeout = 3, loop = 20, test = False)
    self.sendMsg("run_sleeper end")
    
  def runRepeat(self): # test to run repeat
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
        r = c1.parseCommand(msg["text"])
        if r != True:
            bot.sendMessage(chat_id, ret, parse_mode = "HTML")
        c1.setChatId(chat_id)
        print("chat_id {}".format(chat_id))

bot.message_loop(handle)
conn = openDb()
a = getChatId(conn) # setup the chat id
closeDb(conn)
conn = None
if a and a[0] > 0:
    print("chatid {} from database".format(a[0]))
    c1.setChatId(a[0])
    g_chatid = a[0]
print ('Listening ...')

def run(loop = 20):
    ct1.run_sleeper(timeout = 3, loop = loop, test = False)
# Keep the program running.
#while 1:
#    time.sleep(1000)

if __name__ == "__main__":
    print "sys.argv '{}' len:{}".format(sys.argv, len(sys.argv))
    if len(sys.argv) < 2:
        time.sleep(1)
        run(loop = 200)
        bot.sendMessage(chat_id, "byebye", parse_mode = "HTML")
print "end"	