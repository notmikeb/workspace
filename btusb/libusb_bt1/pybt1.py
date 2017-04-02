from ctypes import *

myd = cdll.LoadLibrary("Debug\\libusbbt1.dll")
print (myd)

myd.myrun1()
myd.bt1_init()
print ("get device list {}".format(myd.bt1_getall(0, 0)))
print ("get device list at index {} by pid vid serial number".format(myd.bt1_getDeviceIndex(0x0a12, 0x0002, 0)))
print ("get device list at index {} by pid vid serial number".format(myd.bt1_getDeviceIndex(0x0a12, 0x0001, 0)))
print ("get device list at index {} by pid vid serial number".format(myd.bt1_getDeviceIndex(0x8087, 0x8000, 0)))
myd.bt1_deinit()
print ("please check tracetool viewer")
