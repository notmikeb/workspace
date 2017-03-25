"Timely running test"
import unittest,time
import logging

class TestTimelyTest(unittest.TestCase):
	"Test Python properties"
	def setUp(self):	pass
	
	def testWait1SecNFail(self):
		time.sleep(1.)
		#self.assert_(True)
		#fail("expected AttributeError")
		logging.info("use logging to show testWait1SecNFail")

	def testWait1p3SecNSuccess(self):
		time.sleep(1.3)
		self.assert_(0)
	def testWait1p5SecNFail(self):
		time.sleep(1.5)
		self.assert_(1)

class TestTimelyTest2(unittest.TestCase):
	"Test Python properties"
	def setUp(self):	pass
	
	def testWait1SecNFail(self):
		time.sleep(1.)
		#self.assert_(True)
		#fail("expected AttributeError")

	def testWait1p3SecNSuccess(self):
		time.sleep(1.3)
		self.assert_(0)
	def testWait1p5SecNFail(self):
		time.sleep(1.5)
		self.assert_(1)		
	
if __name__=='__main__':
	unittest.main()
	