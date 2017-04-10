

# python run the 'test_answer2' at test_sample.py

import pytest
import logging
import tracelogging

from pytest import main

import sys

# http://stackoverflow.com/questions/11124093/redirect-python-print-output-to-logger
import logging
import sys

class StreamToLogger(object):
   """
   Fake file-like stream object that redirects writes to a logger instance.
   """
   def __init__(self, logger, log_level=logging.INFO):
      self.logger = logger
      self.log_level = log_level
      self.linebuf = ''

   def write(self, buf):
      if buf.find('assert') >= 0:
         for line in buf.rstrip().splitlines():
             self.logger.log(logging.ERROR, line.rstrip())
      else:
         for line in buf.rstrip().splitlines():
             self.logger.log(self.log_level, line.rstrip())
   def isatty(self):
      return True
   def flush(self):
      pass

logging.basicConfig(
   level=logging.INFO,
   format='%(asctime)s:%(levelname)s:%(name)s:%(message)s',
   filename="out.log",
   filemode='a'
)

stdout_logger = logging.getLogger('STDOUT')
sl = StreamToLogger(stdout_logger, logging.INFO)
sys.stdout = sl

stderr_logger = logging.getLogger('STDERR')
sl = StreamToLogger(stderr_logger, logging.ERROR)
sys.stderr = sl


def run1(*l, **d):
    print("run1")
    print("list:{}".format(repr(l)))
    print("dict:{}".format(repr(d)))

if __name__ == "__main__":
    pytest.main(sys.argv)
else:
    pytest.main([ "test_sample1.py", "-k" , "test_answer1"])
    pytest.main([ "test_sample1.py", "-k" , "test_wrong1"])
