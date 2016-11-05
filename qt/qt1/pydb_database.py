import sqlite3

result = ''
def createTable():
    global result
    connection = sqlite3.connect("login.db")
    connection.execute("CREATE TABLE USERS (USERNAME TEXT NOT NULL, EMAIL TEXT, PASSSWORD TEXT)")
    connection.execute("INSERT INTO USERS VALUES(?,?,?)", ('user', 'user@gmail.com', 'password'))

    connection.commit()

    result = connection.execute("SELECT * from USERS")

if __name__ == "__main__":
    createTable()
    for data in result:
        print("USERNAME: ", data[0])
        print("EMAIL: ", data[1])
        print("PASSWROD: ", data[2])
