import sys
sys.path.insert(0, '../database')
import database_util

# Learner is in charge of building models and saving models to database
class Learner:
	u_id = 0
	db = object()
	movie_history = list()
	genre_feature = list()
	tag_feature = list()

	def __init__(self, _u_id):
		self.u_id = _u_id
		db = database_util.database()

	def getFeatures(self):
		return

# Predictor is in charge of retriving models and predict on movies based on models
class Predictor:
	u_id = 0
	db = object()
	def __init__(self, _u_id):
		self.u_id = _u_id
		db = database_util.database()

		
