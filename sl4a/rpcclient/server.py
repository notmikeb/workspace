import socket, sys

import time
import signal
import sys

import thread

def interuppt_handler(signum, frame):
    print "Signal handler!!!"
    sys.exit(-2) #Terminate process here as catching the signal removes the close process behaviour of Ctrl-C

signal.signal(signal.SIGINT, interuppt_handler)
print "registered"

def server_thread_tcp(*arg):
 try:
  try:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  except socket.error, msg:
    sys.stderr.write("[ERROR] %s\n" % msg[1])
    sys.exit(1)

  sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) #reuse tcp
  sock.bind(('', 54321))
  sock.listen(5)
#sock.settimeout(10)


  while True:
    (csock, adr) = sock.accept()
    print "Client Info: ", csock, adr
    msg = csock.recv(1024)
    if not msg:
        pass
    else:
        print "Client send: " + msg
        csock.send("Hello I'm Server.\r\n")
    csock.close()
 except e:
  print repr(e)

if __name__ == "__main__":
  try:
    thread.start_new(server_thread_tcp, ('', 1024))
  except:
    raise
  raw_input()