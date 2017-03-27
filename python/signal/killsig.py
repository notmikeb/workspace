#!/usr/bin/env python
import signal
import sys
import time
def signal_handler(signal, frame):
        print('You pressed Ctrl+C!')
        sys.exit(0)
signal.signal(signal.SIGINT, signal_handler)
print('Press Ctrl+C')
#signal.pause()
# http://stackoverflow.com/questions/1112343/how-do-i-capture-sigint-in-python

while 1:
  time.sleep(10)
  print "sleep."