import sys
from os import path
sys.path.insert(0, path.abspath(path.dirname(__file__)) + '/../database')
sys.path.insert(1, path.abspath(path.dirname(__file__)) + '/../train')
from sklearn import svm
from sklearn import linear_model
from sklearn.kernel_approximation import RBFSampler
from sklearn.naive_bayes import GaussianNB
from sklearn.neural_network import MLPClassifier
from sklearn.model_selection import cross_val_score
import pickle
import base64

import database_util
import mrlib
import datetime

import numpy as np

import bottleneck as bn

# Learner is in charge of building models and saving models to database
class Learner:
	here = path.abspath(path.dirname(__file__))
	log_path = here + '/../log/'

	db = object()
	parser = object()
	genre_learner = svm.SVC(probability=True)
	tag_learner = svm.SVC(probability=True)
        
	def __init__(self, _u_id):
		self.u_id = _u_id
		self.db = database_util.database()
		self.parser = mrlib.Parser()
		self.movies = list()
		self.ratings = list()
		self.genre_features = list()
		self.tag_features = list()
		self.classes = list()
		self.not_enough_history = False
		self.average_rating = 0.0
		self.getFeatures()
		self.genClasses()
		if (self.validateFeature() == False):
			self.processError(0)


	# Write a msg with time to the end of the log_file
	def write_log(self, msg, log_file_name):
		log_file = self.log_path + log_file_name + ".log"
		time_string = str(datetime.datetime.now())
		prepared_string = "[%s]: %s \n" % (time_string, msg)
		f = open(log_file, 'a+')
		f.write(prepared_string)
		f.close()

	def getFeatures(self):
		history = self.db.get_user_history(self.u_id)
                
		if (len(history) < 2):
			self.processError(1)	

		for h in history:
			self.movies.append(h[1])
			self.ratings.append(h[2])

		info = self.db.get_movie_info_batch(self.movies)
		for i,m in enumerate(self.movies):
			# TODO: Figure out how to do with empty tag
                        if len(info[i]) < 6:
                                t = np.zeros(1128)
                        else:
			        t = self.db.s2a(info[i][5])
			if  (t.shape[0] != 1128):
				t = np.zeros(1128)
			g = self.parser.genre2vec(info[i][2])
			self.genre_features.append(g)
			self.tag_features.append(t)
	
	def genClasses(self):
		# TODO: solve the case that only one class is seen
		# This causes learner to raise an error
		# Temp solution: check condition in training and saving
		for r in self.ratings:
			self.average_rating = self.average_rating + float(r)
		self.average_rating = self.average_rating / float(len(self.ratings))

		for r in self.ratings:
			if (float(r) > self.average_rating):
				self.classes.append(1.0)
			else:
				self.classes.append(0.0)
	
	def validateFeature(self):
		if (len(self.ratings) != len(self.genre_features)):
			return False
		if (len(self.ratings) != len(self.tag_features)):
			return False
		for t in self.tag_features:
			if t.shape[0] != 1128:
				return False
		for g in self.genre_features:
			if g.shape[0] != 20:
				return False
		return True
	
	def processError(self, error_code):
		# 0: Feature is not valid
		if (error_code == 0):
			print("[ERROR]: Feature set is not valid")
			return 0
		# 1: history length is too short
		if (error_code == 1):
                        self.not_enough_history = True
			print("[ERROR]: Insufficient history")
			return 1
		else:
			print("[ERROR]: Unknown error")
			return 2
	
	def train_genre(self):
		self.genre_learner.fit(self.genre_features, self.classes)				
	
	def train_tag(self):
		assert(len(self.tag_features) == len(self.classes))
		for t in self.tag_features:
			assert(t.shape[0] == 1128)
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
		self.write_log("user %s genre_model updated" % (self.u_id), "learner")
		self.train_tag()
		self.write_log("user %s tag_model updated" % (self.u_id), "learner")
	
	def save_model(self):
		genre_model = pickle.dumps(self.genre_learner)
		tag_model = pickle.dumps(self.tag_learner)
		if (self.onlyOneClass()):
			genre_model = "[ONECLASS]:" + str(self.classes[0])
			print genre_model
			tag_model = genre_model
			
		#genre_model = base64.b64encode(genre_model)
		#tag_model = base64.b64encode(tag_model)
		self.db.add_user_model(self.u_id, genre_model, tag_model, self.average_rating)
		self.write_log("user %s model saved" % (self.u_id), "learner")
		


# Predictor is in charge of retriving models and predict on movies based on models
class Predictor:

	here = path.abspath(path.dirname(__file__))
	log_path = here + '/../log/'

	u_id = 0
	db = object()
	parser = object()

	def __init__(self, _u_id):
		self.u_id = _u_id
		self.db = database_util.database()
		self.parser = mrlib.Parser()
		self.genre_model = ''
		self.tag_model = ''
		self.movies = list()
		self.movie_score = list()
		self.invalid_user = False
		self.genre_learner = object()
		self.tag_learner = object()
		self.getModels()
		if (self.onlyOneClass() == False and self.invalid_user == False):
			self.loadModels()

	# Write a msg with time to the end of the log_file
	def write_log(self, msg, log_file_name):
		log_file = self.log_path + log_file_name + ".log"
		time_string = str(datetime.datetime.now())
		prepared_string = "[%s]: %s \n" % (time_string, msg)
		f = open(log_file, 'a+')
		f.write(prepared_string)
		f.close()
	
	def getModels(self):
		fromDB = self.db.get_user_model(self.u_id)
		if (len(fromDB) == 0):
			self.processError(3)
			return
		g_model_64 = fromDB[0][1]
		t_model_64 = fromDB[0][2]
                if "[ONECLASS]:" in g_model_64:
                        self.processError(3)
			return
                
                
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
		self.movies = np.array(_movies)

	def processError(self, error_code):
		if (error_code == 0):
			print("[ERROR]: Candidate movie list is empty")
		if (error_code == 1):
			print("[ERROR]: Only one class has been speicified by user")
		if (error_code == 2):
			print("[ERROR]: Failed to find class 1.0 in learner")
		if (error_code == 3):
			print("[ERROR]: No model exists")
			self.invalid_user = True
		else:
			print("[ERROR]: Unknown error")
	
	# return a score of a movie
	def score(self, m_id, info):
		# TODO: Improve
		t_feature = self.db.s2a(info[5])
		g_feature = self.parser.genre2vec(info[2])
		
		
		t_matrix = self.tag_learner.predict_proba([t_feature])
		g_matrix = self.genre_learner.predict_proba([g_feature])
	
		one_index = -1
		for i in range(0, 2):
			if (self.tag_learner.classes_[i] == 1.0):
				one_index = i
		if (one_index == -1):
			self.processError(2)

		tag_score = t_matrix[0][one_index]
		genre_score = g_matrix[0][one_index]

		overall_score = 0.9 * tag_score + 0.1 * genre_score

		return overall_score


	#only first Nth number is accurate (use argpartition)
	def partitionLargestKth(self, num):
		if num >= self.movies.shape[0]:
			num = self.movies.shape[0]-1

		info = self.db.get_movie_info_batch(self.movies)
		movie_score_all = np.zeros((self.movies.shape[0], 2))
		for i,m in enumerate(self.movies):
			s = self.score(m,info[i])
			movie_score_all[i] = np.array([m, s])
#			self.movie_score.append((m, s))

		#bn.argpartition make sure elements before kth position is the smallest kth. (-movie_score means we get largest kth)
		#http://berkeleyanalytics.com/bottleneck/reference.html#bottleneck.argpartition
		idxs = bn.argpartition(-movie_score_all[:,1], num)[:num+1]

		movie_score = np.zeros((num,2))
		movie_score = movie_score_all[idxs]

		#only sort largest Kth element
		movie_score[:num+1] = movie_score[np.argsort((-movie_score[:num+1, 1]))]

		self.movie_score = movie_score
#		self.movie_score.sort(key = lambda x : x[1], reverse=True)

		self.write_log("user %s movie_score %s" % (self.u_id, ' '.join(str(e) for e in self.movie_score)), "predictor")
	
	def onlyOneClass(self):
		group = self.genre_model.split(":")
		if (group[0] == "[ONECLASS]"):
			return True
		return False
	
	def getRecommendations(self, num):
		if (self.onlyOneClass()):
			self.processError(1)
			return
		if (self.invalid_user):
			return list()
		ret = list()

		if (num > self.movies.shape[0]):
			num = self.movies.shape[0]

		if (num == 0):
			return ret	

		self.partitionLargestKth(num)
                
		for i in range(0, num):
			m_score = self.movie_score[i].tolist()
			ret.append(m_score)

		self.write_log("user %s num %s recommend %s" % (self.u_id, num, ' '.join(str(e) for e in ret)), "predictor")
		return ret


	
