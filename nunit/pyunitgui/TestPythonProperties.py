"Test Python 'property' language feature"
import unittest

class C(object):
	def __init__(self, val): 
		self.__x=val
	def getx(self): return self.__x
	#def setx(self, value): self.__x = value #commented out
	def delx(self): del self.__x
	x = property(getx, None, delx, "test property")

class TestPythonProperties(unittest.TestCase):
	"Test Python properties"
	def setUp(self):	pass
	
	def testCheckReadonlyProperty(self):
		o=C(1)
		self.assertEqual(o.x, 1)
		try:
			o.x=2 # AttributeError: can't set attribute
		except AttributeError:
			pass  #self.assertEqual(str(e),"can't set attribute")
		else:
			fail("expected AttributeError")
		
	def testConstatntlyFailing(self):
		self.assert_(0, "Fails for testing")

def test():
	import sys
	suite = unittest.makeSuite(TestPythonProperties)
	tr=unittest._TextTestResult(unittest._WritelnDecorator(sys.stderr),'DESCs',2)
	try:
		suite(tr)
	except Exception,e:
		print "eee",e
	print 'Test results=',tr
	
if __name__=='__main__':
	#unittest.main()
	test()