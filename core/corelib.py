import sys
from sklearn import svm
from sklearn import linear_model
from sklearn.kernel_approximation import RBFSampler
from sklearn.naive_bayes import GaussianNB
from sklearn.neural_network import MLPClassifier
from sklearn.model_selection import cross_val_score
import pickle
import base64
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
		# Temp solution: check condition in training and saving
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
	
	def onlyOneClass(self):
		classTag = self.classes[0]
		for i in range (1, len(self.classes)):
			if (self.classes[i] != classTag):
				return False
		return True

	def train(self):
		if (self.onlyOneClass()):
			return
		self.train_genre()
		self.train_tag()
	
	def save_model(self):
		genre_model = pickle.dumps(self.genre_learner)
		tag_model = pickle.dumps(self.tag_learner)
		if (self.onlyOneClass()):
			genre_model = "[ONECLASS]:" + str(self.classes[0])
			tag_model = genre_model

		#genre_model = base64.b64encode(genre_model)
		#tag_model = base64.b64encode(tag_model)
		self.db.add_user_model(self.u_id, genre_model, tag_model)
		


# Predictor is in charge of retriving models and predict on movies based on models
class Predictor:
	u_id = 0
	db = object()
	parser = object()
	genre_model = ''
	tag_model = ''
	genre_learner = object()
	tag_learner = object()
	movies = list()
	movie_score = list()

	def __init__(self, _u_id):
		self.u_id = _u_id
		self.db = database_util.database()
		self.parser = mrlib.Parser()
		self.getModels()
		if (self.onlyOneClass() == False):
			self.loadModels()
	
	def getModels(self):
		fromDB = self.db.get_user_model(self.u_id)
		g_model_64 = fromDB[0][1]
		t_model_64 = fromDB[0][2]
		assert(g_model_64 != t_model_64)
		#self.genre_model = base64.b64decode(g_model_64)
		#self.tag_model = base64.b64decode(t_model_64)
		self.genre_model = g_model_64
		self.tag_model = t_model_64
	
	def loadModels(self):
		self.genre_learner = pickle.loads(self.genre_model)
		self.tag_learner = pickle.loads(self.tag_model)
	
	def getMovies(self, _movies):
		if (len(_movies) == 0):
			self.processError(0)
		self.movies = _movies

	def processError(self, error_code):
		if (error_code == 0):
			print "[ERROR]: Candidate movie list is empty"
		if (error_code == 1):
			print "[ERROR]: Only one class has been speicified by user"
	
	# return a score of a movie
	def score(self, m_id):
		# TODO: gives the same score now
		# Might be buggy
		print "Scoring: " + str(m_id)
		info = self.db.get_movie_info(m_id)
		t_feature = self.db.s2a(info[5])
		g_feature = self.parser.genre2vec(info[2])
		
		t_matrix = self.tag_learner.predict_proba([t_feature])
		g_matrix = self.genre_learner.predict_proba([g_feature])

		print t_matrix
		print g_matrix

		return 0
	
	def sort(self):
		for m in self.movies:
			s = self.score(m)
			self.movie_score.append((m, s))
		self.movie_score.sort(key = lambda x : x[1])
	
	def onlyOneClass(self):
		group = self.genre_model.split(":")
		if (group[0] == "[ONECLASS]"):
			return True
		return False
	
	def getRecommendations(self, num):
		if (self.onlyOneClass()):
			self.processError(1)
			return
		ret = list()
		self.sort()
		if (num > len(self.movies)):
			num = len(self.movies)
		for i in range(0, num):
			(mid, score) = self.movie_score[i]
			ret.append(mid)
		return ret
			
		
		
		

		
