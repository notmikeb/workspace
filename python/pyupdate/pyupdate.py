import sys
import logging
import os

logger = logging.getLogger(__name__)
logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)

chkfile = "version.txt"
exefile = "testapp.exe"
filelist = [exefile, chkfile]
remotedir = r"\\localhost\d\temp\testapp"

# check local 'checkfile' with remote dir
new_version = None
old_version = -1
try:
  with open( os.path.join( remotedir, chkfile ), 'r') as f1:
    new_version = "".join(f1.readlines()).strip()
    logger.info("new_version: {}".format(new_version))
    new_version.strip()
except:
  import traceback
  traceback.print_exc()
  logger.error("ignore it")

try:
  with open(chkfile, 'r') as f2:
    old_version = "".join(f2.readlines()).strip()
    old_version.strip()
    logger.info("old_version: {}".format(new_version))
except:
  import traceback
  traceback.print_exc()
  logger.error("ignore old_version")

if new_version != old_version and new_version:
  logger.info("Download .... {} to {}".format(old_version, new_version) )
  import time
  for i in range(1):
    time.sleep(0.5)
    print("."*i, end = '', flush = True)
  import shutil
  check_all = True
  for fname in filelist:
      filepath = os.path.join( remotedir, fname)
      if not os.path.exists(filepath):
          check_all = False
          logger.error("no file at remote {}".format(filepath))
      else:
          logger.info("has {}".format(filepath))
  if check_all:
      for fname in filelist:
          src = os.path.join(remotedir, fname)
          dst = fname
          logger.info("copy {} to {}".format(src, dst))
          shutil.copyfile( src, dst )
      logger.info("copy all done")
  else:
      logger.warn("abort download new veresion")
  logger.info("end")
else:
  logger.info("no new-version update")

args = sys.argv[:]
logger.debug('Re-spawning %s' % ' '.join(args))

#args.insert(0, sys.executable)
if sys.platform == 'win32':
    args = ['"%s"' % arg for arg in args]
    logger.info("origin args is '{}'".format( " ".join(args)))
    if 'python' in sys.executable.lower():
        args.remove(args[0])

if os.path.exists( exefile ):
    logger.info("run {}".format(exefile) + " " + " ".join(args))
else:
    logger.error("Error ! no file '{}'".format(exefile))
os.execv(exefile, args)