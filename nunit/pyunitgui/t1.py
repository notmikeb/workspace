"Test no.1 for PyUnitGui"
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
		self.assert_(element in self.seq)
