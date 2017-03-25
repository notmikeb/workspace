# this is a file to send file and trigger the build
import logging
import logging.config
from tracetool import *  #IGNORE:W0401
from tracetool import _Internals
import datetime
from jenkinsapi.jenkins import Jenkins

class CustomTraceLogger(logging.StreamHandler):
    def __init__(self):
	    logging.StreamHandler.__init__(self)
    def emit(self, record):
		#print (dir(record), type(record))
		msg = record.name + ":" + self.format(record)
		if record.levelname == "ERROR":
			TTrace.error.send(msg)
		elif record.levelname == "INFO":
			TTrace.debug.send(msg)
		elif record.levelname == "WARNING":
			TTrace.warning.send(msg)
		else:
			TTrace.debug.send(msg)
		self.flush()
		return True

def initLogger():
    #logging.basicConfig(filename='example.log',level=logging.DEBUG)
    logging.getLogger().setLevel(logging.DEBUG)
    logging.getLogger().addHandler(CustomTraceLogger())
    logging.info('This message should go to the log file')

class BuildCS:
    def __init__(self, testplan = "", testcase = "", loop  =1 , filepath ="file.zip"):
        pass
        self.testplan = testplan
        self.testcase = testcase
        self.loop = loop
        self.filepath = filepath
        self.j = None
        self.q1 = None
        logging.info("BuildCS init {} {} {} {}".format(self.testplan, self.testcase, self.loop, self.filepath))

    """
    Create a jenkins object and trigger
    """
    def requestBuild(self):
        if self.j == None:
            pass
        else:
            logging.error( "get ride of self.j")
        self.j = Jenkins('http://localhost:8080', username ='daylong', password = 'goto1234' )
        params = {'TEST_PLAN': str(datetime.datetime.now()), 'TEST_CASE': self.testcase}
        upload_file = open(self.filepath, 'r')
        #self.qi = self.j.build_job("app3", params)
        self.qi = self.j['app3'].invoke(build_params = params, files ={"upload/file.zip": upload_file})
        """
        logging.info( "j1:" + str(self.j1) )
        logging.info( "j1:" + repr(dir(self.j1)) )
        self.qi = self.j['app3'].invoke(build_params = params)
        """
        logging.info( "qi:" + str(type(self.qi)) )
        logging.info( "qi:" + repr(dir(self.qi)) )

    def waitComplete(self):
        qi = self.qi
        if qi != None:
            logging.info(qi.is_running())
            qi.block_until_complete()

            logging.info(qi.get_build())
            logging.info(qi.get_build_number())
            build = qi.get_build()
            logging.info(build)
        else:
            logging.warning("nothoing to waitComplete")

class BuildCC:
    def __init__(self):
        logging.getLogger("uspider").info("buildcc created")


initLogger()
cs = BuildCS()
cs.requestBuild()
cs.waitComplete()
logging.info("cs.waitComplete done")
BuildCC()
import loguser
logging.getLogger("daylong").error("test done")
