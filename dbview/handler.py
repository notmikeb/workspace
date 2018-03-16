
import pymssql
from datetime import datetime


def dump_date(thing):
    if isinstance(thing, datetime):
        return thing.isoformat()
    return str(thing)


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

def test(): ## ms = MSSQL(host="localhost",user="msp",pwd="123456",db="MSPDB_Debugging")
        ## ms.ExecNonQuery("insert into WeiBoUser values('2','3')")
        ms = MSSQL(host="", user="msp", pwd="123456", db="MSPDB_Debugging")
        #resList = ms.ExecQuery("SELECT top 10 * FROM dbo.Task order by TaskID desc")
        #print(resList)
        a = ms.query_db("select top 3 * from dbo.Task")
        import json
        data= json.dumps( a, default = dump_date, indent = 2)
        return data
        

if __name__ == '__main__':
    test()