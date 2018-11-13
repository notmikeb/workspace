import logging
import logging.config

logger = logging.getLogger(__name__)

def sayHello(name):
  logger.error("sayHello - this is {} by error api".format(name))
  logger.info("sayHello - tthis is {} by info api".format(name))
  logger.debug("sayHello - tthis is {} by debug api".format(name))


if __name__ == "__main__":
  import os
  print("this is pylib1 main by print " + __name__ )
  logging.config.fileConfig(os.path.join(os.path.dirname(__file__), 'logging1.conf'))
  sayHello("this is main inside pylib1")
