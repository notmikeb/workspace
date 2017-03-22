import logging
import logging.config
from tracetool import *  #IGNORE:W0401
from tracetool import _Internals
import datetime


class CustomTraceLogger(logging.StreamHandler):
    def __init__(self):
	    logging.StreamHandler.__init__(self)

    def emit(self, record):
		msg = self.format(record)
		if record.levelname == "ERROR":
			TTrace.error.send(msg)
		elif record.levelname == "INFO":
			TTrace.debug.send(msg)
		elif record.levelname == "WARNING":
			TTrace.warning.send(msg)
		else:
			TTrace.debug.send(msg)
		self.flush()

#logging.basicConfig(filename='example.log',level=logging.DEBUG)
logging.getLogger().setLevel(logging.DEBUG)
logging.getLogger().addHandler(CustomTraceLogger())
logging.info('This message should go to the log file')
while 1:
    logging.error("this is a error msg {}".format(datetime.datetime.now()))
