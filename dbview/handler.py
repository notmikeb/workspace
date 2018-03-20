import pymssql
from datetime import datetime


def dump_date(thing):
    if isinstance(thing, datetime):
        return thing.isoformat()
    return str(thing)

    
def getMs():
    g_ms = MSSQL(host="", user="web", pwd="preflight", db="MSPDB")
    return g_ms

class MSSQL(object):
  def __init__(self,host,user,pwd,db):
    self.host=host
    self.user=user
    self.pwd=pwd
    self.db=db

  def GetConnect(self):
    if not self.db:
        raise (NameError,"no databsae ")
    self.connect=pymssql.connect(host=self.host,user=self.user,password=self.pwd,database=self.db,charset="utf8")
    cur=self.connect.cursor()
    if not cur:
        raise (NameError,"connect failed")
    else:
        return cur

  def ExecQuery(self,sql):
    self.cur=self.GetConnect()
    self.cur.execute(sql)
    resList = self.cur.fetchall()

    self.connect.close()
    return resList

  def query_db(self, query, args=(), one=False):
    cur = self.GetConnect()
    cur.execute(query, args)
    r = [dict((cur.description[i][0], value) \
               for i, value in enumerate(row)) for row in cur.fetchall()]
    cur.connection.close()
    return (r[0] if r else None) if one else r

  def db(self):
    return self.db
    return self.db

  def ExecNonQuery(self, sql):
        cur = self.__GetConnect()
        cur.execute(sql)
        self.connect.commit()
        self.connect.close()

def query_sqlstring(sqlstring):
        ms = getMs()
        print(sqlstring)
        a = ms.query_db( sqlstring )
        import json
        data= json.dumps( a, default = dump_date, indent = 2)
        return data        

def test( max = 3, cl = None): ## ms = MSSQL(host="localhost",user="msp",pwd="123456",db="MSPDB_Debugging")
        ## ms.ExecNonQuery("insert into WeiBoUser values('2','3')")
        ms = getMs()
        try: 
            max = int(max)
        except:
            max = 3
        if cl != None:
            sqlstring = "select top {} * from dbo.Task where P4Label like '%{cl}%' order by TaskID desc".format(max, cl = cl)
        else:
            sqlstring = "select top {} * from dbo.Task order by TaskID desc".format(max)
        print(sqlstring)
        a = ms.query_db( sqlstring )
        import json
        data= json.dumps( a, default = dump_date, indent = 2)
        return data        
        

if __name__ == '__main__':
    test()
