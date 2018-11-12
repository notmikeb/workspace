import logging
import logging.config
logger = logging.getLogger(__name__)

def show(message):
  logger.error("show - '{}' by error api ".format(message))
  logger.debug("show - '{}' by debug api ".format(message))
  logger.info("show - '{}' by info api ".format(message))
  

if __name__ == "__main__":
  import os
  print("this is main by print " + __name__ )
  logging.config.fileConfig(os.path.join(os.path.dirname(__file__), 'logging2.conf'))
  show("this is main inside pylib2")
