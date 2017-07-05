# -*- coding: utf-8 -*-
import sys
#sys.path = ["c:\\python27\\lib", "c:\\python27\\lib\\site-packages"]

from datetime import datetime
import time

import sqlite3
conn = sqlite3.connect('testdb.db')
DATETIME_FORMAT = "%Y%m%d %H:%M:%S"

def updateRecordLastrun(c, id, date1):
    datestring = date1.strftime(DATETIME_FORMAT)
    sqlstring = "update crontable set lastrun= '{}' where id={}".format(datestring, id)
    r = c.execute(sqlstring)
    c.commit()
    print ("result r:{}".format(r))
    return r

def getRecordLastrun(c, id):
    sqlstring = "select lastrun from crontable where id={}".format(id)
    print (sqlstring)
    r = c.execute(sqlstring).fetchone()
    c.commit()
    print ("result r:{}".format(r))
    return r