import sys
import time
import os
import subprocess

cwd = os.getcwd()
print "Author: daylong {}".format(os.getcwd())
#print sys.argv[0]
#print sys.argv[1]

time.sleep(3)

def unzip_folder( zipfile, extract_folder):
    # uncompress zip and put it to extract_folder
    print("output folder is {}".format(extract_folder))
    try:
        os.mkdir(extract_folder)
    except:
        pass
    # invoke ../lib/7z/7z.exe 
    args = ['cmd.exe', '/c', os.path.join( cwd, r'.\..\lib\7z\7z.exe')  , 'e', '-y', '-o{}'.format(extract_folder), zipfile]
    print " ".join(args)
    try:
        subprocess.call(args)
    except:
        print sys.exc_info()[0]
    return extract_folder

def analyze_folder(folder):
    content = os.listdir(folder)
    return " ".join(content)
    
def open_window( folder ):
    # open folder by 'start <folder>'
    subprocess.call(['cmd.exe', '/c', 'start' , folder])

try:
  if len(sys.argv) > 1:
   target = sys.argv[1]
   if os.path.isfile(target):
      print "this is a file"
      d = os.path.dirname(target)
      name_ext = os.path.basename(target)
      name, ext = os.path.splitext(name_ext)
      if ext.lower() in ['.zip', 'rar', 'tar.gz', 'tar']:
           print("unzip it {} {} {}".format(d, name, ext))
           out = unzip_folder(target, os.path.join(d, name))
           print "invoke python analyze to the unzip folder {}".format(d)
           analyze_folder(d)
           print "open the target folder !"
           open_window(out)
      elif ext.lower() in ['.log', '.cfa']:
           print "invoke python analyze to the unzip folder"
           analyze_folder(d)
           print "open the target folder !"
           open_window(d)
      else:
           print "unknown file {}".format(target)
   elif os.path.isdir(target):
      print "invoke python analyze to it directly !"
      analyze_folder(target)
      print "open the target folder !"
      open_window(target)
except:
  print sys.exc_info()
print "sleep 10 seconds"
time.sleep(10)