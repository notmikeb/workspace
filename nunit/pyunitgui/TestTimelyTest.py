"Timely running test"
import unittest,time

class TestTimelyTest(unittest.TestCase):
	"Test Python properties"
	def setUp(self):	pass
	
	def testWait1SecNFail(self):
		time.sleep(1.)
		self.assert_(0)
		#fail("expected AttributeError")

	def testWait1p3SecNSuccess(self):
		time.sleep(1.3)
		self.assert_(1)
	def testWait1p5SecNFail(self):
		time.sleep(1.5)
		self.assert_(0)
	
if __name__=='__main__':
	unittest.main()
	