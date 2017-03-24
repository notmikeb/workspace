"Test no.1 for PyUnitGui"
import random
import unittest

class TestSequenceFunctions(unittest.TestCase):
    "test three functions from the random module; Test no.1 for PyUnitGui"
    
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

    def testsample(self):
        self.assertRaises(ValueError, random.sample, self.seq, 20)
        for element in random.sample(self.seq, 5):
            self.assert_(element in self.seq)


if __name__ == '__main__':
    choice=2
    if   choice==1:
        unittest.main()
    elif choice==2:
        suite = unittest.TestSuite()
        suite.addTest(unittest.makeSuite(TestSequenceFunctions))
        unittest.TextTestRunner(verbosity=2).run(suite)
