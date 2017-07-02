## 20170702 dalongtw transfer money-records of banck.app to idb of cwmoney.app

from datetime import datetime
import time

import sqlite3
conn = sqlite3.connect('2017_07_02_CHT.iDB')


#i_kinds 'breakfast'(1) 'launch'(2) 'dinner'(3) in kinds_table
#i_kind  'food'(1) 'house'(2) 'transport'(3) 'entertainment'(5) in kind_table

def addone(c):
    i_money = 99
    i_date = (datetime.now() - datetime(1970,1,1)).total_seconds()
    r = c.execute("INSERT INTO rec_table (i_money, i_date, i_kind, i_kinds, i_account, i_item, i_create, i_invoice, i_rev1, i_gps, i_rate) VALUES ({}, {}, {},{} ,{}, {}, {}, {},{},{},{})".format(i_money, i_date, 1, 2, 1, 1, i_date, "0", 0, "0", 1))
    c.commit()
    return r

def showall(c):
    r = c.execute("select * from rec_table")
    c.commit()
    return r

r = addone(conn)

