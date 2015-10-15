import ctypes 
from ctypes import *


f1 = getattr(windll.sim2, "sim1_test1@20")
f2 = getattr (windll.sim2, "hci_read@8")
# build
f1.argtypes = [ c_char, c_int, c_int, c_int, c_char_p]
f1.resptype = c_int

f2.argtypes = [c_int, c_char_p]
f2.resptype = c_int

pbuff = create_string_buffer(30);
r = f1( c_char(1), c_int(8), c_int(32), c_int(30), pbuff)
print("r ", r)
print( pbuff.raw)
# see the raw data

for i in range(10):
  r = f2( c_int(30), pbuff)
  print( r)
  print( pbuff.raw, )

  
  
