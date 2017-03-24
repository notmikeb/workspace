"Test Python 'property' language feature"
import unittest, time

class C(object):
	def __init__(self, init_val=99): 
			self.__x=99
	def getx(self): return self.__x
	#def setx(self, value): self.__x = value #commented out
	def delx(self): del self.__x
	x = property(getx, None, delx, "I'm the 'x' property.")

class TestPythonProperties(unittest.TestCase):
		"Test Python properties"
		def setUp(self):
				pass
		def testCheckReadonlyProperty(self):
				o=C()
				self.assertEqual(o.x, 99)
				try:
						o.x=98 # AttributeError: can't set attribute
				except AttributeError,e:
						self.assertEqual(str(e),"can't set attribute")
		def testConstatntlyFailing(self):
			time.sleep(0.250)
			self.assert_(0, "Fails for testing")

class Tu1(unittest.TestCase):
	def testX(self):
		time.sleep(0.250)
		pass

class Tu2(unittest.TestCase):
	def testFail(self):
		time.sleep(0.250)
		self.assert_(0, "Fails for testing no.2")

if __name__=='__main__':
	unittest.main()