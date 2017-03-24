import ConfigParser

class Config(ConfigParser.ConfigParser):
	"ROF - Recently Opened File(s)"
	default_keepLastROFcount = 15
	default_ReloadLastAtStartup = 0
	def __init__(self,filename):
		ConfigParser.ConfigParser.__init__(self)
		self.load(filename)
	def load(self,filename):
		self.filename=filename
		self.read([filename])

		sections= ["Generic","MainWin","ROF","LastROF"]
		for sect in sections:
			if not self.has_section(sect):
				self.add_section(sect)
		self.set_default("Generic","ReloadLastAtStartup", Config.default_ReloadLastAtStartup)
		self.set_default("LastROF","keepLastROFcount", Config.default_keepLastROFcount)
		self.save()
		
	def set_default(self,section,option,default):
		if not self.has_option(section,option):
			self.set(section,option,default)
		
	def save(self,filename=''):
		if filename=='':
			filename=self.filename
		self.write(file(filename,"w"))

	def getints(self, section, optnames):
		l=[]
		for opt in optnames:
			l.append( self.getint(section,opt) )
		return l
	def getstrings(self, section, optnames):
		l=[]
		for opt in optnames:
			l.append( self.get(section,opt) )
		return l

	def set_list(self, section, optnames, vals):
		"Set options by one list"
		assert(len(optnames)==len(vals))
		for i in range(0,len(optnames)):
			self.set(section,optnames[i],vals[i])
	
	def loadROFList(self):
		rof=[]
		rof= self.options("ROF")
		rofi=map(int,rof)
		rofi.sort()
		rofi.reverse()
		rof=map(str,rofi)
		rof_paths = self.getstrings("ROF",rof)
		return rof,rof_paths
	def addNewROF(self, path):
		"Write into config new (last) entry"
		rof= self.options("ROF")
		if self.has_option("LastROF","last"):
			lastRof= self.getint("LastROF","last")
			lastRof+= 1
		else:
			lastRof=0
		self.set("LastROF","last",str(lastRof))
		# find copy of this addend item and remove if found:
		self.removeROF(path)
		#/
		self.set("ROF",str(lastRof),path)
		self.cleanupOldROFentries()
		self.save()
		
	def removeROF(self,path):
		rof= self.options("ROF")
		for si in rof:
			if path==self.get("ROF",si):
				self.remove_option("ROF",si)
		
	def lastROFvalue(self):
		rof= self.options("ROF")
		if len(rof)==0:
			return "<empty>"
		lastrof=max(map(int,rof))
		return self.get("ROF",str(lastrof))
	def cleanupOldROFentries(self):
		self.keepLastROFcount=self.getint("LastROF","keepLastROFcount")		
		rof = self.options("ROF")

		if len(rof)<=self.keepLastROFcount:
			return
		lastRof= self.getint("LastROF","last")
		LowerBound= lastRof-self.keepLastROFcount+1
		for si in rof:
			if int(si)<LowerBound:
				self.remove_option("ROF",si)
		self.canonizeROF()
	def canonizeROF(self):
		lastRof= self.getint("LastROF","last")
		if lastRof <= self.keepLastROFcount-1:
			return #nothing to do
		if lastRof <= 100: # not to call it every time
			return
		delta= lastRof +1 - self.keepLastROFcount
		rof = self.options("ROF")
		for si in rof:
			newi= int(si) - delta
			path=self.get("ROF",si)
			self.set("ROF", str(newi),path)
			self.remove_option("ROF",si)
		lastRof = self.getint("LastROF","last")
		lastRof-= delta
		self.set("LastROF","last",str(lastRof))

import unittest

class TestConfig(unittest.TestCase,Config):
	"Test Config file. ROF - Recently Opened File(s)"
	def __init__(self,tests):
		unittest.TestCase.__init__(self,tests)
		self.config = Config("testConfig.config")
	def setUp(self):
		pass
	def test1ConfigWrite(self):
		# test ReadWindowCoords
		x,y,w,h=150,200,150,100
		self.config.set("MainWin", "x", x)
		self.config.set("MainWin", "y", y)
		#self.config.set("MainWin", "w", w)
		#self.config.set("MainWin", "h", h)
		self.config.set_list("MainWin", ["w","h"], [w,h])
		self.config.save()
		self.config.load(self.config.filename)
		rect = self.config.getints("MainWin",['x','y','w','h'])
		self.assertEqual([x,y,w,h], rect, "Read after write is not equal")
		
		self.config.set("Generic", "ReloadLastAtStartup", 1)

	def test3loadROF(self):
		"test OnProgramStart: populate menu with ROFList; autoload last project"
		rof, rof_paths = self.config.loadROFList()
		#print "ROF= ", rof, rof_paths
		if self.config.getint("Generic", "ReloadLastAtStartup"):
			print 'Autoloading at startup project "%s"' % self.config.lastROFvalue()
	def test2AddNewROF(self):
		"test OnOpenProject: add new entry to ROF"
		path="D:\\Source\\PyUnitGui\\TestPythonProperties.py" # "/path/project"
		self.config.addNewROF(path)
		rof, rof_paths = self.config.loadROFList()
		#print "now ROF= ", rof,rof_paths

if __name__=='__main__':
	unittest.main()
	