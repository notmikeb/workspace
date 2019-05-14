import sys
import random
import time

print("sys is '{}'".format( " ".join(sys.argv)))
print(time.strftime("%Y%m%d %H%M%S"))

ms = random.random()*5
if len(sys.argv) > 0:
   ms = int(sys.argv[-1])%10
else:
   print("use random value ")
print("sleep %d" % (ms))
time.sleep(ms)
print(time.strftime("%Y%m%d %H%M%S"))