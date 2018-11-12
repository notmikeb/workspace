import logging

logger = logging.getLogger(__main__)

def sayHello(name):
  logger.error("sayHello - this is {} by error api".format(name))
  logger.info("sayHello - tthis is {} by info api".format(name))
  logger.debug("sayHello - tthis is {} by debug api".format(name))
