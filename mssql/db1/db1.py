import pyodbc
cstring = '(localdb)\MSSQLLocalDB;Initial Catalog=master;Integrated Security=True;Connect Timeout=30;Encrypt=False;TrustServerCertificate=False;ApplicationIntent=ReadWrite;MultiSubnetFailover=False'
#cnxn = pyodbc.connect('DRIVER={SQL Server};SERVER=(localdb)\MSSQLLocalDB;DATABASE=database1;UID=dalong;PWD=dalong')
cnxn = pyodbc.connect('DRIVER={SQL Server Native Client 11.0};SERVER=(localdb)\MSSQLLocalDB;DATABASE=database1;UID=vs;PWD=')

cursor = cnxn.cursor()

cursor.execute("SELECT * FROM dbo.phonebook")
row = cursor.fetchone()
#cursor.execute("SELECT WORK_ORDER.TYPE,WORK_ORDER.STATUS, WORK_ORDER.BASE_ID, WORK_ORDER.LOT_ID FROM WORK_ORDER")

while row:
    print repr(row)
    [ field for field in row]
    row = cursor.fetchone()