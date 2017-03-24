#!/bin/python
''' Tasks:
Initially: all FIXMEs, after that:
 If pyfile.timestamp changed after prev - reload it automatically

Output TestResult info into specific panels
  Replace current error-at-run-time-accounting approach with errors registering delegates
Remained output is only related with tests output
Window positions remembering and recall

Rule of thumb: To mark quick-and-dirty fixes (hacks) - (If any!) with:
 print >>self.stdout, "FIXME-date-time hack_description"
 example: "FIXME-061206-0508 temp file loading hack..."
'''
import sys, os, os.path, time
import wx
import string 
import unittest,ututil,traceback
import Config
from   ColorGauge import ColorGauge

progname = 'PyUnitGui'
projfile = 'Newtest'

debug_mode = True  # to print additional info
			
"Tree item type"
TestNone, TestSuite, TestCase, TestFunction = range(4)

class SbId:
	"StatusBar Section Id"
	Message, CasesCount, RunCount, FailuresCount, TimeRan = range(5)
		
def MsgBox (window, string, caption=progname):
	dlg=wx.MessageDialog(window, string, caption, wx.OK)
	dlg.ShowModal()
	dlg.Destroy()


class MainWindow(wx.Frame):
	def __init__(self, parent, id, title):
		wx.Frame.__init__(self, parent, -1, title, size = (600, 450),
		          style=wx.DEFAULT_FRAME_STYLE|wx.NO_FULL_REPAINT_ON_RESIZE)
		self.config=Config.Config('pyunitgui.config')
		wx.EVT_CLOSE(self, self.OnTestExit)
		self.recents={}
		self.testname2treeitem={}
		# ...
		self.CreateStatusBar()
		# (Ready|Reloaded|'Running '+TestName |Completed  .width=long, 
		# TestCases: %d, Tests Run: %d, Failures : %d, Time : %f s)
		self.sb=self.GetStatusBar()
		self.sb.SetFieldsCount(5)
		self.sb.SetStatusWidths([-1,90,90,90,90])
		self.sb.SetStatusText("Ready", SbId.Message)
		self.sb.SetStatusText('', SbId.CasesCount)
		self.sb.SetStatusText('', SbId.RunCount)
		self.sb.SetStatusText('', SbId.FailuresCount)
		self.sb.SetStatusText('', SbId.TimeRan)
		
		'''font=self.GetFont()
		sz=font.GetPointSize()
		print sz
		font.SetPointSize(sz+1)
		print font.GetPointSize(), "medi_1"
		self.SetFont(font)
		font=self.GetFont().GetPointSize()
		print sz, "after"'''

		self.CreateMenu() 
		# Create Windows program icon; don't sweat it if it doesn't load
		try:            
			self.SetIcon(wx.Icon("tb/PULogoIcon.ico", wx.BITMAP_TYPE_ICO))
		finally: pass

		# ------------------------------------------------------------------------------------
		# Create the splitter window.
		splitter = wx.SplitterWindow(self, -1, style=wx.SP_3D|wx.SP_LIVE_UPDATE )
		splitter.SetMinimumPaneSize(20)

		# Left panel
		tID = wx.NewId()
		self.tree = wx.TreeCtrl (splitter, tID, style=wx.TR_HAS_BUTTONS |
									wx.TR_EDIT_LABELS )
		self.loadTreeImagelist()
		wx.EVT_TREE_ITEM_ACTIVATED(self.tree, tID, self.OnTreeItemActivated)
		wx.EVT_TREE_SEL_CHANGED(self.tree, tID, self.OnTreeSelChanged)

		# Right panel
		self.rightPanel= wx.Panel(splitter, -1)
		box = wx.BoxSizer(wx.VERTICAL)
		
		dlgFrame= wx.Panel(self.rightPanel, -1, wx.DefaultPosition, wx.Size(100,100))

		self.btnRun = wx.Button(dlgFrame, 401, "Run", wx.DLG_PNT(dlgFrame, 15, 10)).SetDefault()
		wx.EVT_BUTTON(dlgFrame, 401, self.OnBtnRun)
		self.btnStop = wx.Button(dlgFrame, 402, "Stop", wx.DLG_PNT(dlgFrame, 82, 10))
		wx.EVT_BUTTON(dlgFrame, 402, self.OnBtnStop)
		
		self.gauge = ColorGauge(dlgFrame, -1, (12, 50), wx.Size(250, 25))
		self.gauge.setColor("GREEN")
		self.gauge.setPercent(0.0)
		'''box1 = wx.BoxSizer(wx.VERTICAL)
		box3 = wx.BoxSizer(wx.HORIZONTAL)
		#box3.Add(self.btnRun, 0, wx.EXPAND)
		btn1=wx.Button(dlgFrame, 1010, "four")
		box3.Add(btn1, 0, wx.EXPAND, 10)
		#box3.Add(self.btnRun, 0, wx.EXPAND)
		#box3.Add(self.btnStop, 0, wx.EXPAND)

		box2 = wx.BoxSizer(wx.HORIZONTAL)
		box2.Add(self.gauge, 1, wx.EXPAND,10)
		
		box1.Add(box3, 0, wx.ALIGN_TOP)
		box1.Add(box2, 1, wx.ALIGN_BOTTOM)
		box1.Fit(dlgFrame)
		dlgFrame.SetAutoLayout(True)
		dlgFrame.SetSizer(box1)'''
	
		dlgFrame.SetAutoLayout(True)
		lc = wx.LayoutConstraints()
		lc.top.   SameAs(dlgFrame, wx.Top, 55) #AsIs()
		lc.left.  AsIs()
		lc.height.AsIs()
		lc.right. SameAs(dlgFrame, wx.Right, 10)
		self.gauge.SetConstraints(lc)
		
		box.Add(dlgFrame, 0, wx.EXPAND)
		
		bottomPanel= wx.Notebook(self.rightPanel, -1, style=wx.NB_BOTTOM)
		bottomPanel.AddPage(self.makeErrorsPanel(bottomPanel), " Errors && Failures ")

		# stdout and err panel
		self.consoleText= wx.TextCtrl(bottomPanel, -1, "", wx.DefaultPosition, wx.DefaultSize, 
			wx.TE_MULTILINE|wx.TE_READONLY)
		#redirect console to window
		from ConsoleRedirector import ConsoleRedirector,StreamOnTextCtrl
		self.stdout = StreamOnTextCtrl(self.consoleText)
		#stderr = StreamOnTextCtrl(self.stderrText)
		redirector = ConsoleRedirector(self.stdout,self.stdout) 
		#redirector = ConsoleRedirector(self.stdout,self.stdout)    #FIXME-061606-0716: where is output to stderr??!
		bottomPanel.AddPage(self.consoleText, " sys.stdout && stderr ")

		bottomPanel.AddPage(self.makeIgnoredPanel(bottomPanel), "Ignored Tests")
		# notebook is complete
		#bottomPanel.SetSelection(1)

		box.Add(bottomPanel, 1, wx.EXPAND)

		box.Fit(self.rightPanel)
		self.rightPanel.SetAutoLayout(True)
		self.rightPanel.SetSizer(box)
		# Set splitter windows
		splitter.SplitVertically(self.tree, self.rightPanel, 150)
		splitter.SetSashPosition(250, True)

		self.Show(True)

		# Load window options 
		x,y,w,h = self.config.getints("MainWin",['x','y','w','h'])
		self.SetDimensions(x,y,w,h)

		# Some global state variables.
		self.projectdirty = False
		self.activeitem = None
		self.OnStart()
		self.__importreloader= RollbackImporter()
			
	def loadTreeImagelist(self):
		from BitmapsLoader import BitmapsLoader

		self.il = wx.ImageList(16,15)
		bmlist = BitmapsLoader().load("tb/iconTree%s.bmp",4)
		self.TiNeutralId = self.il.Add(bmlist[0]) # id tree icon white
		self.TiYellowId= self.il.Add(bmlist[1])
		self.TiRedId   = self.il.Add(bmlist[2])
		self.TiGreenId = self.il.Add(bmlist[3])
		self.tree.SetImageList(self.il)
		self.tree.SetStateImageList(self.il)
		
	def makeNotebookPanel(self, parentNotebook):
		return wx.TextCtrl(parentNotebook, -1, "", wx.DefaultPosition, wx.Size(400,100), 
			wx.TE_MULTILINE|wx.TE_READONLY) # ID_TEXTCTRL_QR, 

	def makeErrorsPanel(self, parentNotebook):
		splitter = wx.SplitterWindow(parentNotebook, -1, style= wx.NO_3D | wx.SP_3D 
		 | wx.SP_LIVE_UPDATE)
		splitter.SetMinimumPaneSize(20)
		tID = wx.NewId()
		self.errlist = wx.ListBox(splitter,tID)
		self.errtext = wx.TextCtrl(splitter, -1, "", wx.DefaultPosition, wx.Size(400,100), 
			wx.TE_MULTILINE|wx.TE_READONLY)
		splitter.SplitHorizontally(self.errlist,self.errtext, 80)
		wx.EVT_LISTBOX(self,tID, self.OnErrorListSelChanged)
		return splitter

	def makeIgnoredPanel(self, parentNotebook):
		ignoreTree = wx.TreeCtrl(parentNotebook,-1,style=wx.TR_HAS_BUTTONS | wx.TR_LINES_AT_ROOT)
		ig_root = ignoreTree.AddRoot("Ignored Tests")
		ignoreTree.AppendItem(ig_root,"Test1 Ignored: reason 1")
		ignoreTree.AppendItem(ig_root,"Test2 Ignored: reason other")
		return ignoreTree
	
	def AddMenuItem(self,menu,itemStr,helpStr,func):
		menuID=wx.NewId()
		menu.Append(menuID, itemStr, helpStr)
		wx.EVT_MENU(self, menuID, func)
		return menuID
					
	def CreateMenu(self):
		# Set up menu bar for the program
		self.mainmenu = wx.MenuBar()   # Create menu bar.
		
		# File menu "Project" part
		menu=wx.Menu()
		self.AddMenuItem(menu,'Open Py &file...', 'Open Python file with test(s) in it', self.OnTestOpenFile)
		menu.AppendSeparator()

		self.AddMenuItem(menu,'&Reload', 'Reload currently load project or file', self.OnFileReload)

		menuSubID=wx.NewId()
		self.menuSub =wx.Menu()
		self.loadRecentsSubmenu()
		menu.AppendMenu(menuSubID, 'Re&cent files', self.menuSub, 'Recently open test projects or files')
		menu.AppendSeparator()
		
		self.AddMenuItem(menu,'E&xit', 'Exit program', self.OnTestExit)
		self.mainmenu.Append(menu,  '&Test')
		
		menu=wx.Menu()
		self.AddMenuItem(menu, '&Open test project...', 'Test project is a python files list with unit tests; open it',
			self.OnTestProjectOpen)
		menu.AppendSeparator()
		# File menu Project creation part
		self.AddMenuItem(menu,'&New empty project', 'Create and open new empty project', self.OnTestProjectNew)
		self.AddMenuItem(menu,'&Create from directory...', 'Create new project with all test python files in specified directory',
			self.OnTestProjectDirOpen)
		self.AddMenuItem(menu,'&Add file...', 'Add file to project', self.OnFileAdd)
		self.AddMenuItem(menu,'Remo&ve file...', 'Remove file from project',self.OnFileRemove)
		menu.AppendSeparator()
		self.AddMenuItem(menu,'&Options...', 'Set PyUnit options',lambda self:0)

		self.mainmenu.Append(menu,  '&Project')
		
		#  Help menu
		menu=wx.Menu()                                 
		self.AddMenuItem(menu,'&Help...', 'Read this help and write review', self.OnHelp)
		menu.AppendSeparator()
		
		self.AddMenuItem(menu, '&About '+progname +'...', 'Read about author; click on site', self.OnHelpAbout)
		
		self.mainmenu.Append(menu,  '&Help')		    
		
		self.SetMenuBar (self.mainmenu)    #  Attach the menu bar to the window.

	#-----------------------------------------------------------------------------
	def OnStart(self):
		if self.config.getint("Generic", "ReloadLastAtStartup"):
			print 'Autoloading at startup project "%s"' % self.config.lastROFvalue()
			self.OpenRecentFile_helper(self.config.lastROFvalue())

		#"development" test:
		#self.test_getChildrenList()
		self.lastDir = "."
	
	def OnBtnRun(self, event):
		item=self.tree.GetSelection()
		if not item:
			return
		self.runTestOnItem(item)

	def OnBtnStop(self, event):
		print "OnBtnStop()"

	def OnFileReload(self,event): 
		print "ToBeImplemented: OnFileReload"
		self.consoleText.SetValue("")
		self.__importreloader.rollbackImports()
		self.__importreloader= RollbackImporter()
		self.OpenPyFile(self.path)

	def OnOpenRecentFile(self,event): 
		#print 'OnOpenRecentFile()', event.GetId(),self.recents[event.GetId()]
		file=self.recents[event.GetId()]
		self.OpenRecentFile_helper(file)
	def OpenRecentFile_helper(self,file): 
		try:
			self.OpenPyFile(file)
			self.config.addNewROF(file)
		except Exception,e:
			print "Can't load project '%s', because %s"% (file,e)
			if debug_mode:
				#print details of error separately for safeness...
				tracebackLines = apply(traceback.format_exception, sys.exc_info())
				#tracebackText
				dbg=' dbg> ' # note for debug mode
				print '\n'+dbg+string.join(tracebackLines,dbg)
				self.config.removeROF(file)
		self.config.save()
		self.loadRecentsSubmenu()
		
	def loadRecentsSubmenu(self):
		if self.recents:
			for id in self.recents:
				self.menuSub.Delete(id)
		rof, rof_paths = self.config.loadROFList()
		self.recents={}
		if not rof_paths:
			self.menuSub .AppendSeparator()
		else:
			for f in rof_paths:
				menuId=self.AddMenuItem(self.menuSub,f,'',self.OnOpenRecentFile)
				self.recents[menuId]=f

	# Some nice little helpers.
	def project_open(self, project_file):
		try:
			input = open (project_file, 'r')
			self.tree.DeleteAllItems()
			self.project_file = project_file
			name = string.replace(input.readline(), "\n", "")
			self.SetTitle (name+" - "+progname)
			self.root = self.tree.AddRoot(name)
			self.activeitem = self.root
			for line in input.readlines():
				self.tree.AppendItem (self.root, string.replace(line, "\n", ""))
			input.close
			self.tree.Expand (self.root)
			
			self.projectdirty = False
		except IOError:
			pass

	def project_save(self):
		try:
			output = open (self.project_file, 'w+')
			output.write (self.tree.GetItemText (self.root) + "\n")

			count = self.tree.GetChildrenCount (self.root)
			iter = 0
			child = ''
			for i in range(count):
				if i == 0:
					(child,iter) = self.tree.GetFirstChild(self.root,iter)
				else:
					(child,iter) = self.tree.GetNextChild(self.root,iter)
				output.write (self.tree.GetItemText(child) + "\n")
			output.close()
			self.projectdirty = False
		except IOError:
			dlg_m = wx.MessageDialog (self, 'There was an error saving the project file.',
										'Error!', wx.OK)
			dlg_m.ShowModal()
			dlg_m.Destroy()
			
	# Tree Helper -----------------------------------------------------------------------------
	def getChildrenList(self,item):
		"return tree subitems of item list"
		list=[]
		count = self.tree.GetChildrenCount(item,False)
		child,iter = None,0
		for i in range(count):
			if i == 0:
				(child,iter) = self.tree.GetFirstChild(item)
			else:
				(child,iter) = self.tree.GetNextChild(item,iter)
			list.append(child)
		return list
	def test_getChildrenList(self):
		l=self.getChildrenList(self.root)
		print "Tree.root len=",len(l), 
		for c in l: print self.tree.GetItemText(c),
		
		l2= self.getChildrenList(l[0])
		print "\nTree.1.1 len=",len(l2), 
		for c in l2: print self.tree.GetItemText(c),

	# ----------------------------------------------------------------------------------------
	# Event handlers from here on out.
	# ----------------------------------------------------------------------------------------
	def OnTestProjectOpen(self, event):
		open_it = True
		if self.projectdirty:
			dlg=wx.MessageDialog(self, 'The project has been changed.  Save?', progname,
								wx.YES_NO | wx.CANCEL)
			result = dlg.ShowModal()
			if result == wx.ID_YES:
				self.project_save()
			if result == wx.ID_CANCEL:
				open_it = False
			dlg.Destroy()
		if open_it:
			dlg = wx.FileDialog(self, "Choose a project to open", ".", "", "*.pytest", wx.OPEN)
			if dlg.ShowModal() == wx.ID_OK:
				self.project_open(dlg.GetPath())
			dlg.Destroy()
	
	def OnTestProjectDirOpen(self, event):
		dlg=wx.DirDialog(self)
		btn=dlg.ShowModal()
		dlg.Destroy()
		if btn!= wx.ID_OK: return
		
		from fnmatch import fnmatch
		lspy=os.listdir(dlg.GetPath())
		lspy=filter(lambda f: fnmatch(f,"*.py") or fnmatch(f,"*.pyw"), lspy)
		print "ToBeImplemented: load", lspy

	def OnTestProjectNew(self, event):
		open_it = True
		if self.projectdirty:
			dlg=wx.MessageDialog(self, 'The project has been changed.  Save?', progname,
								wx.YES_NO | wx.CANCEL)
			result = dlg.ShowModal()
			if result == wx.ID_YES:
				self.project_save()
			if result == wx.ID_CANCEL:
				open_it = False
			dlg.Destroy()

		if open_it:
			dlg = wx.TextEntryDialog (self, "Name for new project:", "New Project",
									'MyCool', wx.OK | wx.CANCEL)
			if dlg.ShowModal() == wx.ID_OK:
				newproj = dlg.GetValue()
				dlg.Destroy()
				dlg = wx.FileDialog (self, "Place to store new project", ".", "", "*.pytest",
									wx.SAVE)
				if dlg.ShowModal() == wx.ID_OK:
					try:
						proj = open (dlg.GetPath(), 'w')
						proj.write (newproj + "\n")
						proj.close()
						self.project_open (dlg.GetPath())
					except IOError:
						dlg_m = wx.MessageDialog (self,
												'There was an error saving the new project file.',
												'Error!', wx.OK)
						dlg_m.ShowModal()
						dlg_m.Destroy()
		dlg.Destroy()

	def saveWindowOptions(self):
		"Save options (window position)"
		x,y,w,h = self.GetScreenRect()
		self.config.set_list("MainWin", ["x","y","w","h"], [x,y,w,h])
		self.config.save()
		
	def OnTestExit(self, event):
		close = True
		self.saveWindowOptions()
		# save project
		if self.projectdirty:
			dlg=wx.MessageDialog(self, 'The project has been changed.  Save?', progname,
								wx.YES_NO | wx.CANCEL)
			result = dlg.ShowModal()
			if result == wx.ID_YES:
				self.project_save()
			if result == wx.ID_CANCEL:
				close = False
			dlg.Destroy()
		if close:
			self.Destroy()

	def OnFileAdd(self, event):
		dlg = wx.FileDialog(self, "Choose a file to add", ".", "", "*.*", wx.OPEN)
		if dlg.ShowModal() == wx.ID_OK:
			path = os.path.split(dlg.GetPath())
			self.tree.AppendItem (self.root, path[1])
			self.tree.Expand (self.root)
			self.project_save()

	def OnFileRemove(self, event):
		item = self.tree.GetSelection()
		if not item:
			return
		filename=self.tree.GetItemText(item)
		dlg=wx.MessageDialog(self, 'Are you sure you want to remove %s from this project?' %filename,
			progname, wx.YES_NO|wx.ICON_QUESTION)
		result = dlg.ShowModal()
		dlg.Destroy()
		if result != wx.ID_OK:
			return
		
		if item != self.root:
			self.tree.Delete (item)
			self.project_save()
		dlg.Destroy()

	def OnHelp(self, event):
		MsgBox(self, "Althouth, there is no help for this program, but it has pretty intuitive GUI (I hope).\r\n"+
			"\r\n"+
			"PyUnitGui is a GUI framework and utility for unit tests of Python, similar to unittestgui.py\r\n"+
			" of Steve Purcell, but made much more user-friendly.\r\n"+
			"\r\n"+
			"See Python unittest module help to get more about UnitTests in Python.\r\n"+
			"Read TDD or XP* books to learn how to use unit tests in everyday programming.\r\n"+
			"\r\n"+
			"Simplest usage is - open python unittest file by \"Test\"->\"Open Py file\" menu \r\n"+
			"\r\n"+
			"_____\r\n"+			
			"*) Test-Driven Development and eXtreme Programming"
		)
	
	def OnHelpAbout(self, event):
		version="v0.3"
		MsgBox(self, "PyUnitGui "+version+": Now, this becames useful tool.\r\n"
		  "At least it is much nearer to this than any time before!\r\n\r\n"+
			"Copyright(C) 2005-2007 by Minas Abrahamyan.  All rights reserved.\r\n"+
			"\r\n"+
			"Excited by: NUnit-gui - \"GUI-fied\" unit testing for .NET\r\n"+
			"\r\n"+
			"Author: Minas Abrahamyan.  E-mail: a_minas<at>web.am\r\n"+
			"Credits: Creators of Nunit-GUI and Steve Purcel, creator of PyUnit.",
				"About PyUnitGui (%s)" %version)
	
	def OnTestOpenFile(self, event):
		dlg = wx.FileDialog(self, "Choose python file to test", self.lastDir, "", "*.py", wx.OPEN)
		#self.lastDir,tmp = os.path.split( dlg.GetPath())
		if dlg.ShowModal() != wx.ID_OK:
			dlg.Destroy()
			return
		self.config.addNewROF(dlg.GetPath())
		self.OpenPyFile(dlg.GetPath())
		self.loadRecentsSubmenu()
		
	def OpenPyFile(self,path):
		self.errlist.Clear()
		self.errtext.SetValue("")
		self.gauge.setPercent(0)
		self.gauge.Refresh()
		self.gauge.Update()
		
		pydir,pyfilename = os.path.split(path)
		self.lastDir = pydir
		#os.chdir(self.lastDir) #pydir
		if pydir not in sys.path:
			sys.path.append(pydir)

		tc_list = ututil.load_tests(files=[path])
		self.loadTreeTests(pyfilename,tc_list)
		self.path=path
		if not tc_list:
			print >>sys.stderr, "Can't load any test from file '%s'"%path
			self.SetTitle(progname)
			return
		self.SetTitle(pyfilename+" - "+progname)
		
		tc_count = self.__countTestCasesList(tc_list)
		self.sb.SetStatusText('Ready', SbId.Message)
		self.sb.SetStatusText('TestCases: %d' %tc_count, SbId.CasesCount)
		self.sb.SetStatusText('', SbId.RunCount)
		self.sb.SetStatusText('', SbId.FailuresCount)
		self.sb.SetStatusText('', SbId.TimeRan)

	def __countTestCasesList(self,tc_list):
		n=0
		for tc in tc_list: 
			n+=len(tc[2])
		return n
	
	def loadTreeTests(self, pyfilename, tc_list):
		self.tree.DeleteAllItems()
		self.root = self.tree.AddRoot(pyfilename, self.TiNeutralId)
		modulename = pyfilename.split('.')[0]
		self.tree.SetPyData(self.root, (TestSuite,modulename))
		self.activeitem = self.root
		
		for tc in tc_list:
			it=self.tree.AppendItem(self.root, tc[1],self.TiNeutralId) #tc[1] is TestCase class name
			self.tree.SetPyData(it, (TestCase,tc[0])) #tc[0] is modulename
			for func in tc[2]:
				tfItem=self.tree.AppendItem(it,func,self.TiNeutralId)
				self.tree.SetPyData(tfItem,(TestFunction,tc[0]))
				self.testname2treeitem[self.testname_format(tc[0],tc[1],func)]=tfItem
			self.tree.Expand(it)
		self.tree.Expand(self.root)
		
	def testname_format(self,module,class_,func):
		"format is in form 'testX (testPyProperty.Tu1)' "
		return "%s (%s.%s)" %(func,module,class_)
													
	# Handle "clicking"
	def tree_item_type(self,item):
		return self.tree.GetPyData(item)[0]

	def OnTreeSelChanged(self, event):
		item=self.tree.GetSelection()
		self.testcases_count=0
		self.__countTestCasesSubTree(item)
		self.sb.SetStatusText('TestCases: %d' %self.testcases_count, SbId.CasesCount)
		
	def __countTestCasesSubTree(self,item):
		if self.tree_item_type(item)==TestFunction:
			self.testcases_count +=1
			return
		l=self.getChildrenList(item)
		for i in l:
			self.__countTestCasesSubTree(i)
	
	def OnTreeItemActivated(self, event):
		item=event.GetItem()
		self.activeitem = item
		#run the test:
		self.verbosity =2
		self.runTestOnItem(item)
		
	def runTestOnItem(self,item):
		self.setTestsColorsToNeutral()
		self.errlist.Clear()
		self.errtext.SetValue("")
		self.gauge.setPercent(0)
		self.verbosity =2
		item_type = self.tree_item_type(item)
		modulename= self.tree.GetPyData(item)[1]
		name=self.tree.GetItemText(item)
		if   item_type==TestFunction:
			# get testcase item, it is parent
			tcItem=self.tree.GetItemParent(item)
			class_=self.tree.GetItemText(tcItem)
			self.prepareTest()
			self.runMethodTest(item,modulename,class_,name)
			self.finishTest()
		elif item_type==TestCase:
			self.prepareTest()
			self.runClassTest(item,modulename)
			self.finishTest()
		elif item_type==TestSuite:
			self.prepareTest()
			self.runSuiteTest(item,modulename)
			self.finishTest()

	def writeStatus(self,timeTaken):
		self.sb.SetStatusText("Ready", SbId.Message)
		self.sb.SetStatusText('Tests Run: %d' %self.result.testsRun, SbId.RunCount)
		self.sb.SetStatusText('Failures : %d' %len(self.result.failures), SbId.FailuresCount)
		self.sb.SetStatusText('Time : %.3fs'  %timeTaken, SbId.TimeRan)

	def runTest(self):
		#self.testRunner = unittest.TextTestRunner(stream=self.stdout,verbosity=self.verbosity)
		#result = self.testRunner.run(self.test)
		self.test(self.result)
		return self.result.wasSuccessful()
		
	def runMethodTest(self,item,module,class_,method):
		self.test = unittest.TestLoader().loadTestsFromName(module+'.'+class_+'.'+method)
		ok = self.runTest()
		return ok

	def runClassTest(self,item,module):
		class_=self.tree.GetItemText(item)
		id_list = self.getChildrenList(item)
		if not id_list: return
		ok=True
		for child in id_list:
			name=self.tree.GetItemText(child)
			self.runMethodTest(child,module,class_,name)
			subitem = self.getTestItemByName(self.testname_format(module,class_,name))
			res= self.tree.GetItemImage(subitem,wx.TreeItemIcon_Normal) == self.TiGreenId
			ok= ok and res
		color= ok and self.TiGreenId or self.TiRedId #ignore? YellowId
		self.setTreeItemColor(item,color)
		return ok

	def runSuiteTest(self,item,module):
		id_list = self.getChildrenList(item)
		if not id_list: return
		ok=True
		for child in id_list:
			name=self.tree.GetItemText(child)
			#self.currentTestText= name # at right of buttons
			res = self.runClassTest(child,module)
			ok= ok and res
		color= ok and self.TiGreenId or self.TiRedId #ignore? YellowId
		self.setTreeItemColor(item,color)
		return ok

	def setTreeItemColor(self,item,color):
		self.tree.SetItemImage(item,color, wx.TreeItemIcon_Normal)
		self.tree.SetItemImage(item,color, wx.TreeItemIcon_Selected)
		self.tree.Refresh()
		self.tree.Update()
		
	def setTestsColorsToNeutral(self,item=None):
		if not item: 
			item = self.root
			self.setTreeItemColor(item,self.TiNeutralId)
		for child in self.getChildrenList(item):
			self.setTreeItemColor(child,self.TiNeutralId)
			self.setTestsColorsToNeutral(child)
			
	def OnErrorListSelChanged(self,event):
		selected=self.errlist.GetSelection()
		test, error = self.errorInfo[selected]
		tracebackLines = apply(traceback.format_exception, error + (10,))
		tracebackText = string.join(tracebackLines,'')
		self.errtext.SetValue(tracebackText)

	def getTestItemByName(self, testname):
		if self.testname2treeitem.has_key(testname):
			return self.testname2treeitem[testname]
		else:
			print "Error, can't find testname '%s'"%testname
			return None
	
	def prepareTest(self):
		self.result = GUITestResult(self) #unittest.TestResult() # self._makeResult()
		self.errorInfo=[]
		
		item=self.tree.GetSelection()
		self.testcases_count=0
		self.__countTestCasesSubTree(item)
		
		self.gauge.setColor("GREEN")
		self.gauge.setPercent(0)
		self.gauge.setStep(1./self.testcases_count)

		self.startTime=time.time()
	def finishTest(self):
		#self.setGaugeColorHelper()
		# FIXME/Enhance_me
		#doSomethingUseful():
		#	 zip(backup)_sources()
		pass
	def setGaugeColorHelper(self):
		isok = self.result.wasSuccessful()
		#len(self.result.failures)==0
		color= isok and "GREEN" or "RED" #ignore? YellowId
		self.gauge.setColor(color)
		self.gauge.Refresh()
		#self.gauge.Update()

	def notifyTestStarted(self,test):
		"Called back at every test start"
		pass
	def notifyTestFinished(self,test):
		"Report test results"
		stopTime = time.time()
		self.timeTaken = float(stopTime - self.startTime)
		self.writeStatus(self.timeTaken)

	def notifyTestSucceded(self,test):
		item = self.getTestItemByName(str(test))
		self.setTreeItemColor(item,self.TiGreenId)
		self.setGaugeColorHelper()
		self.gauge.makeStep()
	def notifyTestErrored(self, test, err):
		self.errlist.Append("Error: %s" % test)
		self.errorInfo.append((test,err))
		item = self.getTestItemByName(str(test))
		self.setTreeItemColor(item,self.TiRedId)
		self.setGaugeColorHelper()
		self.gauge.makeStep()
	def notifyTestFailed(self, test, err):
		self.errlist.Append("Failure: %s" % test)
		self.errorInfo.append((test,err))
		item = self.getTestItemByName(str(test))
		self.setTreeItemColor(item,self.TiRedId)
		self.setGaugeColorHelper()
		self.gauge.makeStep()

class GUITestResult(unittest.TestResult):
	"""A TestResult that makes callbacks to its associated GUI TestRunner.
	Used by BaseGUITestRunner. Need not be created directly.
	"""
	def __init__(self, callback):
		unittest.TestResult.__init__(self)
		self.callback = callback

	def addSuccess(self, test):
		unittest.TestResult.addSuccess(self, test)
		self.callback.notifyTestSucceded(test)

	def addError(self, test, err):
		unittest.TestResult.addError(self, test, err)
		self.callback.notifyTestErrored(test, err)

	def addFailure(self, test, err):
		unittest.TestResult.addFailure(self, test, err)
		self.callback.notifyTestFailed(test, err)

	def stopTest(self, test):
		unittest.TestResult.stopTest(self, test)
		self.callback.notifyTestFinished(test)

	def startTest(self, test):
		unittest.TestResult.startTest(self, test)
		self.callback.notifyTestStarted(test)
		
class RollbackImporter:
	"""This tricky little class is used to make sure that modules under test
	will be reloaded the next time they are imported.
	"""
	def __init__(self):
		self.previousModules = sys.modules.copy()
		
	def rollbackImports(self):
		for modname in sys.modules.keys():
			if not self.previousModules.has_key(modname):
				# Force reload when modname next imported
				del(sys.modules[modname])

class App(wx.App):
	#from wxPython.lib.infoframe import *
	#outputWindowClass = wxPyInformationalMessagesFrame
	def OnInit(self):
		frame = MainWindow(None, -1, projfile+" - "+progname)
		self.SetTopWindow(frame)
		#if (projfile != 'Newtest'):
		#	frame.project_open (projfile)
		return True

def main(argv):
	# Process the command line. just get the name of the project file if it's given.
	projfile = 'Newtest'
	if len(argv) > 1:
		projfile = argv[1]
	app = App(0)
	app.MainLoop()

if __name__=='__main__':
	main(sys.argv)
