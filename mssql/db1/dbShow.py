from os import getenv
import pymssql

server = getenv("PYMSSQL_TEST_SERVER")
user = getenv("PYMSSQL_TEST_USERNAME")
password = getenv("PYMSSQL_TEST_PASSWORD")
server = '192.168.0.15'
user = 'sa'
password = 'goto1234'

conn = pymssql.connect(server, user, password, "database111")
cursor = conn.cursor()

cursor.execute('SELECT * FROM persons WHERE Status=%s', 'Waiting')
row = cursor.fetchone()
while row:
    print("ID=%d, Name=%s, Platform=%s " % (row[0], row[1], row[2]))
    row = cursor.fetchone()

conn.close()
