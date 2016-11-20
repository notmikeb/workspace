import PyQt4.pyqtconfig, subprocess

config = PyQt4.pyqtconfig.Configuration()

command = [config.sip_bin,
               config.pyqt_sip_flags,
               "-I", config.pyqt_sip_dir,
               "hello.sip"]
print " ".join(command)
#subprocess.call(command)
line = " ".join(command)
subprocess.call(line, shell=True)
