# The test script that is going to be run be unit testers
from os import path
import sys
sys.path.insert(0, path.abspath(path.dirname(__file__)) + "/core_tests/core")
sys.path.insert(1, path.abspath(path.dirname(__file__)) + "/core_tests/database")
import unittest
import corelib
import database_util

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
	
	def test_pseudo_db(self):
		db = database_util.database()
		self.assertEqual(len(db.get_movie_info(12)), 0)
		self.assertEqual(db.get_mid_from_imdbid(100), 0)
		self.assertEqual(db.get_mid_from_imdbid(113189), str(10))
		self.assertEqual(db.get_imdbid_from_mid(10), str(113189))
		self.assertEqual(db.get_imdbid_from_mid(12), 0)
		self.assertEqual(db.get_uid(12), 12)
		self.assertEqual(db.get_identifier(12), 12)

	def test_corelib_process_err(self):
		learner = corelib.Learner(3)
		learner.train()
		learner.save_model()
		self.assertEqual(learner.processError(0), 0)
		learner.processError(1)
		learner.processError(2)
		learner = corelib.Learner(1)
		learner.train()
		learner.save_model()
		predictor = corelib.Predictor(3)
		predictor.processError(1)
		predictor.processError(2)
		predictor.processError(3)
		predictor.processError(4)
		predictor.getRecommendations(1)


if __name__ == '__main__':
    unittest.main()
