from wxPython.wx import *
import sys,os
from ConsoleRedirector import *

class TestFrame(wxFrame):
	def __init__(self, parent):
		wxFrame.__init__(self, parent, -1, 'Test Redirecting', size=(500, 300))
		EVT_CLOSE(self, self.OnCloseWindow)
		#wxWindow(self,-1).SetBackgroundColour(wxNamedColour("WHITE"))
		self.CreateStatusBar()

		ID_TEXTCTRL_QR = wxNewId()
		self.textResults = wxTextCtrl(self, ID_TEXTCTRL_QR, "", wxDefaultPosition, wxSize(400,100), 
			wxTE_MULTILINE|wxTE_READONLY )
		self.textCtrl2 = wxTextCtrl(self, ID_TEXTCTRL_QR, "", wxDefaultPosition, wxSize(400,100), 
			wxTE_MULTILINE )
		self.textResults.WriteText("TextCtrl\r\n")
		self.listTables = wxListCtrl(self, -1, wxDefaultPosition, wxSize(400,100), 
			wxLC_REPORT|wxSUNKEN_BORDER)
		self.listTables.InsertColumn(0, "heading")
		self.listTables.InsertStringItem(0, "ListCtrl")
		
		box1 = wxBoxSizer(wxVERTICAL)
		box1.Add(self.textResults,1, wxEXPAND)
		box1.Add(self.textCtrl2,  1, wxEXPAND)
		box1.Add(self.listTables, 1, wxEXPAND)
		box1.Fit(self)
		self.SetAutoLayout(True)
		self.SetSizer(box1)
		
		self.Show(True)
		
		self.test_redirection()

	def OnCloseWindow(self, event):
		self.Destroy()
	def test_redirection(self):
		#self.stderr = sys.stderr #self.stdout

		stdout = StreamOnTextCtrl(self.textResults)
		#stderr = TextCtrlToStream(self.textCtrl2)
		redirector = ConsoleRedirector(stdout,stdout)
		
		print >>sys.stderr, " stderr< Haile!"
		print " stdout< Hello!"
		#try:
		#os.system("ls")
		import TestPythonProperties
		TestPythonProperties.test()
		#except Exception,e:
		#print >>sys.stderr, e, "|", sys.exc_info()[0], "byl zdes'"
				
class App(wxApp):
	def OnInit(self):
		frame = TestFrame(None)
		self.SetTopWindow(frame)
		return True
def main(argv):
	app = App(0)
	app.MainLoop()
if __name__=='__main__':
	main(sys.argv)