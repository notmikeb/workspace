
#from socket import socket, AF_INET, SOCK_STREAM  #, error
import socket
import threading
from time import clock #, sleep
from datetime import datetime
import random



#host = TTrace.options.socketHost
#port = TTrace.options.socketPort

#create an INET, STREAMing socket
serversocket = socket.socket(
    socket.AF_INET, socket.SOCK_STREAM)
#bind the socket to a public host,
# and a well-known port
serversocket.bind(("127.0.0.1", 8090))
#become a server socket
serversocket.listen(5)

print ("listing")

while 1:
    #accept connections from outside
    (clientsocket, address) = serversocket.accept()
    print clientsocket, address
    a = clientsocket.recv(10)
    while a != None:
        for i in range(len(a)):  
            print ord(a[i])
        a = clientsocket.recv(10)