from os import getenv
import time
import pymssql
import datetime
import sys


import jenkinsapi

def triggerBuildComplete(jobname):
    result = ""
    j = jenkinsapi.jenkins.Jenkins("http://192.168.74.129:8080/", username="oielq", password="goto123")
    import time
    #jobname = 'iphone5'
    job = j[jobname]
    q5 = job.invoke(build_params={})
    time.sleep(10)
    if q5:
        print "wait q5 to complete"
        p = None
        try:
            p = q5.block_until_building(delay=10)
        except:
            print("cancel before start building ! error !")		
        bn = 0
        if p:
            bn = p.get_number()
            print ("p is :{} {}".format(type(p), repr(p)))
        #b5 = job.get_build() # after building state, we has a build object
        print("build number bn {}".format( bn))
        try:
            q5.block_until_complete()
            b5 = job.get_last_build()
            result = "status {} number {} params {}".format(b5.get_status(), b5.get_number(), repr(b5.get_params()))
        except:
            result = "error ! cancel !"
        print (result)
    else:
        print ("fail to get queue ! error !")
    return result

def myopen():
    server = getenv("PYMSSQL_TEST_SERVER")
    user = getenv("PYMSSQL_TEST_USERNAME")
    password = getenv("PYMSSQL_TEST_PASSWORD")
    server = '192.168.0.15'
    user = 'sa'
    password = 'goto1234'

    conn = pymssql.connect(server, user, password, "database111")
    return conn

def queryOne(where_param):
    conn = myopen()
    if conn == None:
        return None
    cursor = conn.cursor()

    sqlstring = "SELECT * FROM persons WHERE Status='{}' and {}".format('Waiting', where_param)
    print ("sqlstirng {}".format(sqlstring))
    cursor.execute(sqlstring)
    row = cursor.fetchone()
    #while row:
    #    print("ID=%d, Name=%s, Platform=%s " % (row[0], row[1], row[2]))
    #    row = cursor.fetchone()

    conn.close()
    if row:
        print ("Get a valid record: {}".format(row[0]))
    return row
    
def occupyOne(id):
    conn = myopen()
    cursor = conn.cursor()
    sqlstring = "update dbo.persons set Status='{}' WHERE id='{}'".format("IN_PROGRESS", id)
    #sqlstring = "UPDATE dbo.persons SET [Status] = 'IN_PROGRESS' WHERE id = 1"
    p = cursor.execute(sqlstring)
    conn.commit()
    print ( "occupyOne {} - {}".format(p, sqlstring))
    conn.close()
    return True
    
def finishOne(id, result):    
    conn = myopen()
    cursor = conn.cursor()

    p1 = cursor.execute("update persons set Status='{}' WHERE id='{}'".format("Done", id))
    conn.commit()
    print ( "finishOne p1:{}".format(p1))
    result = repr(datetime.datetime.now().strftime(r"%h%m%s")).replace("'", '')+repr(result)
    result = result.replace('"', "#")
    result = result.replace("'", "-")
    sqlstring = "update persons set Result='{}' WHERE id='{}'".format( result, id)
    print sqlstring
    p2 = cursor.execute(sqlstring)
    conn.commit()
    print ( "finishOne p2:{}".format(p2))
    conn.close()
    return p2
    
while True:
    data = queryOne(" platform like 'iphone%' ")
    a = None
    if data:
        a = data[0]
    if a:
        print("Get a record id:{}".format(a))
        time.sleep(5)
        r = occupyOne(a)
        z = triggerBuildComplete(data[2])
        print(z)
        if r:
            print ("occupyed One id:{}".format(a))
            time.sleep(5)
            s = finishOne(a, z)
            print ("result is {}".format(s))
        else:
            print ("error ! cannot occupty it")
    else:
        time.sleep(10)
    sys.stdout.flush()