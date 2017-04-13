# The test script that is going to be run be unit testers
import unittest
import corelib

class TestMethods(unittest.TestCase):
    def test_add(self):
        self.assertEqual(1, 1)
	def test_learner(self):
		learner = corelib.Learner(12)
		learner.train()


if __name__ == '__main__':
    unittest.main()
