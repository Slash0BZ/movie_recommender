# The test script that is going to be run be unit testers
from os import path
import sys
sys.path.insert(0, path.abspath(path.dirname(__file__)) + "/core_tests/core")
import unittest
import corelib

class TestMethods(unittest.TestCase):

	def test_basic_learner_predictor(self):
		learner = corelib.Learner(1)
		learner.train()
		learner.save_model()
		arr = [9, 10]
		predictor = corelib.Predictor(1)
		predictor.getMovies(arr)
		result = predictor.getRecommendations(4)
		self.assertEqual(result, [[10.0, 0.5], [9.0, 0.5]])

	def test_corner_learner_predictor(self):
		learner = corelib.Learner(2)
		learner.train()
		learner.save_model()
		arr = []
		predictor = corelib.Predictor(2)
		predictor.getMovies(arr)
		result = predictor.getRecommendations(4)
		self.assertEqual(result, [])


if __name__ == '__main__':
    unittest.main()
