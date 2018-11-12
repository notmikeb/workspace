import pylib2
import pylib2.tool
import logging

import yaml

#with open('./logging.conf', 'r') as stream:
#    config = yaml.load(stream)
#logging.config.dictConfig(config)

logging.config.fileConfig('logging.conf', disable_existing_loggers = False)
pylib2.tool.show('hehe')
logging.getLogger().error("root error")
logging.getLogger().info("root info")
