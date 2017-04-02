from ctypes import *

myd = cdll.LoadLibrary("Debug\\libusbbt1.dll")
print (myd)

myd.myrun1()
myd.bt1_init()
myd.bt1_deinit()