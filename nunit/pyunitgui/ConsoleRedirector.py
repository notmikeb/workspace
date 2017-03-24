""" Usage: stdout = StreamOnTextCtrl(self.textCtrl)
           redirector = ConsoleRedirector(stdout,stdout) 
"""
import sys

class StreamOnTextCtrl:
	"helper class to allow redirection of stdout&/stderr to a text control widget"
	def __init__(self, widget):
		self.widget=widget
	def write(self, s):
		self.widget.AppendText(s)
	def writeln(self,s=''):
		self.widget.AppendText(s+'\r\n')
		
class ConsoleRedirector:
	def __init__(self,stdout,stderr):
		self.__saved_stdout = sys.stdout
		self.__saved_stderr = sys.stderr
		try:
			if stdout is not None:
				sys.stdout = stdout
		except:
			print >>sys.stderr,"can't redirect stdout"
		try:
			if stderr is not None:
				sys.stderr = stderr
		except:
			print >>sys.stderr,"can't redirect stderr"
	