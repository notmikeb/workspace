import logging
import logging.config
from tracetool import *  #IGNORE:W0401
from tracetool import _Internals

class CustomTraceLogger(logging.StreamHandler):
    def __init__(self):
	    logging.StreamHandler.__init__(self)

    def emit(self, record):
		msg = self.format(record)
		print record
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
logging.debug('This message should go to the log file')
logging.info('So should this')
logging.warning('And this, too')
logging.error("this is a error msg")