import sys
from sklearn import svm
from sklearn import linear_model
from sklearn.kernel_approximation import RBFSampler
from sklearn.naive_bayes import GaussianNB
from sklearn.neural_network import MLPClassifier
from sklearn.model_selection import cross_val_score
import pickle
sys.path.insert(0, '../database')
sys.path.insert(1, '../train')
import database_util
import mrlib

# Learner is in charge of building models and saving models to database
class Learner:
	u_id = 0
	db = object()
	parser = object()
	movies = list()
	ratings = list()
	classes = list()
	genre_features = list()
	tag_features = list()
	genre_learner = svm.SVC(probability=True)
	tag_learner = svm.SVC(probability=True)

	def __init__(self, _u_id):
		self.u_id = _u_id
		self.db = database_util.database()
		self.parser = mrlib.Parser()
		self.getFeatures()
		if (self.validateFeature() == False):
			self.processError(0)
		self.genClasses()

	def getFeatures(self):
		history = self.db.get_user_history(self.u_id)

		for h in history:
			self.movies.append(h[1])
			self.ratings.append(h[2])

		for m in self.movies:
			info = self.db.get_movie_info(m)
			t = self.db.s2a(info[5])
			g = self.parser.genre2vec(info[2])
			self.genre_features.append(g)
			self.tag_features.append(t)
	
	def genClasses(self):
		# TODO: solve the case that only one class is seen
		# This causes learner to raise an error
		for r in self.ratings:
			if (float(r) > 3):
				self.classes.append(1.0)
			else:
				self.classes.append(0.0)
	
	def validateFeature(self):
		if (len(self.ratings) != len(self.genre_features)):
			return False
		if (len(self.ratings) != len(self.tag_features)):
			return False
		for t in self.tag_features:
			if len(t) != 1128:
				return False
		for g in self.genre_features:
			if len(g) != 20:
				return False
		return True
	
	def processError(self, error_code):
		# 0: Feature is not valid
		if (error_code == 0):
			print "[ERROR]: Feature set is not valid"
	
	def train_genre(self):
		self.genre_learner.fit(self.genre_features, self.classes)				
	
	def train_tag(self):
		self.tag_learner.fit(self.tag_features, self.classes)

	def train(self):
		self.train_genre()
		self.train_tag()
	
	def save_model(self):
		genre_model = pickle.dumps(self.genre_learner)
		tag_model = pickle.dumps(self.tag_learner)
		


			
			
		

# Predictor is in charge of retriving models and predict on movies based on models
class Predictor:
	u_id = 0
	db = object()
	def __init__(self, _u_id):
		self.u_id = _u_id
		db = database_util.database()

		
