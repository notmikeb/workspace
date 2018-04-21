#!/bin/python3

from cryptography.fernet import Fernet
import base64

##key = Fernet.generate_key()

def enfile( pwd, infilename, outfilename):
  print("pwd ", pwd)
  pwd = pwd.encode('utf8') * 32
  pwd = pwd[0:32]
  key = base64.urlsafe_b64encode(pwd)
  okey = base64.urlsafe_b64decode(key)
  if okey != pwd: 
     print("pwd is ", pwd)
     print("okey is ", okey)
     print("key is ", key)
     raise Except("not match")
  print("key is ", key)
  if len(key) != 44:
     raise Except("length is wrong")
  f = Fernet(key)
  test(0, f, infilename, outfilename)
  test(1, f, outfilename, 'test.txt')
  return f 

def test(action, f, infilename, outfilename):
  if action == 0:
    print("encrypt")
  else: 
    print("decrypt")
  with open(outfilename, 'wb') as fout:
    with open(infilename, 'rb') as fin:
      while 1:
        if action == 0:
          bytes = fin.read(255)
        else: 
          bytes = fin.read(420)
        if not bytes:
          break
        if action == 0:
          ebytes = f.encrypt(bytes)
        else:
          ebytes = f.decrypt(bytes)
        fout.write(ebytes)
  print("enfile done ", action,  infilename, outfilename)

if __name__ == "__main__":
  import sys
  f = enfile( *sys.argv[1:] )
