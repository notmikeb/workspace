"""ututil.py - Unit Test Utility module
Changelog:
  061206-0508-bug: import_ex doesn't load from any path: changed with 
   adding import_from_path(pypath). and created test for it (test_import_from_path)
"""
import unittest,types,os,string,imp,sys
from fnmatch import fnmatch

# import_ex(name) is not used now
def import_ex(name):
	"name - module name"
	mod = None
	try:
		mod = __import__(name)
	except Exception,e:
		print "Error loading module '%s': %s"%(name,e)
	components = name.split('.')
	for comp in components[1:]:
		mod = getattr(mod, comp)
	return mod
	
def import_from_path(pypath):
	"""Import module from any python module file at pypath path
	returns tuple (pair) of loaded module object and module name"""
	pyfilename = pypath.split(os.sep)[-1]
	nameparts = pyfilename.split('.')
	modname= string.join(nameparts[0:-1],'.') # although nameparts[0:-1] would be right, 
	  # using nameparts[0] is more stable for filenames with dots in it
	suffix=nameparts[-1]
	try:
		f = file(pypath,"r")
	except IOError:
		print >>sys.stdout, "Error importing '%s': file can't be opened" %pypath
		raise
	try:
		desc = (suffix, "r", imp.PY_SOURCE)
		return (imp.load_module(modname, f, pypath, desc), modname)
	finally:		
		f.close()

def test_import_from_path():
	pypath = "C:\\temp.py"
	
	src1=""""This is test module, remove it"
print 'This is a test code from within test file'
g=file('c:\\g','w')
g.close()"""
	src2=""""Test no.1 for PyUnitGui"
import random,unittest
class TestSequenceFunctions(unittest.TestCase):
	"test function from the random module"
	def setUp(self):
		self.seq = range(10)
	def testshuffle(self):
		"testshuffle: Make sure the shuffled sequence does not lose any elements"
		random.shuffle(self.seq)
		self.seq.sort()
		self.assertEqual(self.seq, range(10))
	def testchoice(self):
		element = random.choice(self.seq)
		self.assert_(element in self.seq)"""
		
	f=file(pypath,"w")
	print >>f,src2
	f.close()
	mod,modname = import_from_path(pypath)
	tc = load_tests_from_module(mod,modname)
	print tc
	os.unlink(pypath)

def load_tests(files=[], dir=''):
	"""Load tests from file or dir; tests are: test cases and suites in .py files
	return list of tuples (modulename, class_object, list_of_test_methods)"""
	assert dir or files, "Either file list or directory should be specified"
	assert not dir and files or dir and not files, "File list and  directory can't be specified simultaneously"
	if dir!='':
		return load_tests_from_dir(dir)
	if files:
		tc=[]
		for pyfile in files:
			mod,modname = import_from_path(pyfile)
			tc.extend( load_tests_from_module(mod,modname))
		return tc
	return [] #syntax-beauty


def load_tests_from_module(mod, modulename):
	"""Loads tests from mod module loaded before this method call
	modulename is the name of the module and is used to form the tests functions list
	return list of tuples (module_name, class_name, list_of[test_method_names])"""
	if not mod: 
		return []
	test_cases = []
	for sym,cl in mod.__dict__.items():
		if isinstance(cl, (type, types.ClassType)) and issubclass(cl, unittest.TestCase):
			test_cases.append((sym,cl))
	#test_cases = loadTestsFromModule(mod)
	list_tc = []
	for cl in test_cases:
		tc = (modulename, cl[0], getTestCaseNames(cl[1]))
		list_tc.append(tc)
		#print "Test methods in %s are: %s" % tc
	return list_tc

def load_tests_from_dir(dir):
	if dir[-1]!=os.sep: 
		dir = dir +os.sep
	ls=os.listdir(dir)
	ls= filter(lambda f: fnmatch(f,"*.py") or fnmatch(f,"*.pyw"), ls)
	ls= map(lambda f: f.split('.')[0], ls)
	assert ls== ['1PyUnitGui', 'test1', 'ut_tests', 'unittest_', '_test_PyProperty'], ""
	for f in ls:
		load_tests_from_file(f)

def loadTestsFromModule(module):
	"Return a suite of all tests cases contained in the given module"
	tests = []
	for name in dir(module):
		obj = getattr(module, name)
		if (isinstance(obj, (type, types.ClassType)) and
		    issubclass(obj, unittest.TestCase)):
			tests.append(obj)
			return tests

testMethodPrefix="test"
def getTestCaseNames(testCaseClass): #self, 
	"Return a sorted sequence of method names found within testCaseClass"
	testFnNames = filter(lambda n,p=testMethodPrefix: n[:len(p)] == p,
			                 dir(testCaseClass))
	for baseclass in testCaseClass.__bases__:
		for testFnName in getTestCaseNames(baseclass): #self.
			if testFnName not in testFnNames:  # handle overridden methods
				testFnNames.append(testFnName)
	#if self.sortTestMethodsUsing:
	#	testFnNames.sort(self.sortTestMethodsUsing)
	return testFnNames

if __name__=='__main__':
	#0 t=unittest.TestProgram(mod)
	#2 load_tests()
	test_import_from_path()