import re
import numpy as np
from sklearn import svm
from sklearn import linear_model
from sklearn.kernel_approximation import RBFSampler
from sklearn.naive_bayes import GaussianNB
from sklearn.neural_network import MLPClassifier
from sklearn.model_selection import cross_val_score

class Parser:
	
	data_path = "../data/"
	movie_file = data_path + "movies.csv"
	rating_file = data_path + "ratings.csv"
	tag_file = data_path + "genome-scores.csv"
	link_file = data_path + "links.csv"
	tag_file_list = ['scores/scores_2036.csv', 'scores/scores_4010.csv', 'scores/scores_6214.csv', 'scores/scores_27073.csv', 'scores/scores_71926.csv', 'scores/scores_rest.csv']
	tag_file_list = map(lambda x : "../data/" + x, tag_file_list)
	genreList = ['Adventure', 'Animation', 'Children', 'Comedy', 'Fantasy', 'Romance', 'Drama', 'Action', 'Crime', 'Thriller', 'Horror', 'Mystery', 'Sci-Fi', 'IMAX', 'Documentary', 'War', 'Musical', 'Western', 'Film-Noir', '(no genres listed)']

	def __init__(self, _data_path = data_path):
		self.data_path = _data_path
	
	def pre_process_line(self, line):
		line = line.replace("\r\n", "")
		line = line.replace("\n", "")
		return line

	def parse_history_entry(self, line):
		line = self.pre_process_line(line)
		lineGroup = line.split(",")
		return [lineGroup[0], lineGroup[1], lineGroup[2], lineGroup[3]]
	
	def get_user_history(self, u_id):
		count = 0
		fp = open(self.rating_file, 'r')
		foundFlag = False
		ret_movie = list()
		ret_rating = list()
		for line in fp:
			count = count + 1
			if (count == 1):
				continue
			[c_u_id, m_id, rating, timeStamp] = self.parse_history_entry(line)
			if (u_id == int(c_u_id)):
				foundFlag = True
				ret_movie.append(m_id)
				ret_rating.append(rating)
			if (foundFlag and u_id != int(c_u_id)):
				break
		fp.close()
		if (len(ret_movie) != len(ret_rating)):
			print "[Error]: movie does not correspond a rating"
			return (list(), list())
		else:
			return (ret_movie, ret_rating)
	
	def parse_movie_entry(self, line):
		line = self.pre_process_line(line)
		featureList = []
		if (line.find("\"") != -1):
			featureList = line.split('"')
			featureList[0] = featureList[0].replace(",", "")
			featureList[2] = featureList[2].replace(",", "")
		else:
			featureList = line.split(',')
		m_id = featureList[0]
		name = featureList[1]
		year = featureList[1]
		genre = featureList[2]
		name = name[0:name.find("(") - 1]
		pattern = re.compile(r'\((\d\d\d\d)\)', flags=re.DOTALL)
		year = pattern.findall(year)
		if (len(year) > 0):
			year = year[0]
		else:
			year = ""
		return [m_id, name, genre, year]
	
	def genre2vec(self, genre):
		gl = genre.split("|")
		ret = list()
		for g in self.genreList:
			if g in gl:
				ret.append(1.0)
			else:
				ret.append(0.0)
		return ret
	
	def get_movie_genre_vector(self, m_id):
		count = 0
		fp = open(self.movie_file, 'r')
		for line in fp:
			count = count + 1
			if (count == 1):
				continue
			[c_m_id, name, genre, year] = self.parse_movie_entry(line)
			if (m_id == int(c_m_id)):
				return self.genre2vec(genre)
		fp.close()
		return list()
	
	def parse_tag_entry(self, line):
		line = self.pre_process_line(line)
		group = line.split(",")
		return [group[0], group[1], group[2]]

	def tag2vec(self, tags):
		if (len(tags) != 1128):
			print "Invalid tag file"
		ret = list()
		for (t,s) in tags:
			ret.append(s)
		if (len(tags) == 0):
			for i in range (0, 1128):
				ret.append(0.0)
		if (len(ret) != 1128):
			print "Cast to valid vector failed"
		return ret

	def get_movie_tag_vector(self, m_id):
		count = 0
		fp = open(self.tag_file, 'r')
		tags = list()
		foundFlag = False
		for line in fp:
			count = count + 1
			if (count == 1):
				continue
			[c_m_id, t_id, score] = self.parse_tag_entry(line)
			if (m_id == int(c_m_id)):
				foundFlag = True
				tags.append((t_id, score))
			if (m_id != int(c_m_id) and foundFlag):
				foundFlag = True
				break
		fp.close()
		return self.tag2vec(tags)

	def get_movie_tag_vector_fast(self, m_id):
		m_id = int(m_id)
		f = ''
		if m_id <= 2036:
			f = self.tag_file_list[0]
		else:
			if m_id <= 4010:
				f = self.tag_file_list[1]
			else:
				if m_id <= 6214:
					f = self.tag_file_list[2]
				else:
					if m_id <= 27073:
						f = self.tag_file_list[3]
					else:
						if m_id <= 71926:
							f = self.tag_file_list[4]
						else:
							f = self.tag_file_list[5]
		fp = open(f, 'r')
		tags = list()
		foundFlag = False
		for line in fp:
			[c_m_id, t_id, score] = self.parse_tag_entry(line)
			if (m_id == int(c_m_id)):
				foundFlag = True
				tags.append((t_id, score))
			if (int(c_m_id) > m_id and foundFlag == False):
				break
			if (m_id != int(c_m_id) and foundFlag):
				foundFlag = True
				break
		fp.close()
		return self.tag2vec(tags)
	
	def parse_link_entry(self, line):
		line = self.pre_process_line(line)
		group = line.split(',')
		return [group[0], group[1], group[2]]
	
	def get_movie_imdb_id(self, m_id):
		count = 0
		fp = open(self.link_file, 'r')
		ret = 0
		for line in fp:
			count = count + 1
			if (count == 1):
				continue
			[c_m_id, imdb_id, tmdb_id] = self.parse_link_entry(line)
			if (m_id == int(c_m_id)):
				ret = imdb_id
				break
		fp.close()
		return int(ret)

			

class Genre2BinaryLearner:
	
	u_id = 0
	GenreList = []
	ClassList = []
	Train_GenreList = []
	Train_ClassList = []
	Test_GenreList = []
	Test_ClassList = []
	learner = MLPClassifier(solver='lbfgs', alpha=1e-5, hidden_layer_sizes=(5, 2), random_state=1)

	def __init__(self, u_id):
		self.u_id = u_id
		self.fillParameters()
		self.splitTrainTest()

	def fillParameters(self):
		parser = Parser()
		(ml, rl) = parser.get_user_history(self.u_id)
		
		for m in ml:
			self.GenreList.append(parser.get_movie_genre_vector(int(m)))

		d_rl = [float(i) for i in rl]
		averageRating = sum(d_rl) / len(d_rl)
		for r in d_rl:
			Output = 0.0
			if (r >= averageRating):
				Output = 1.0
			self.ClassList.append(Output)
	
	def splitTrainTest(self):
		trainNum = int(len(self.ClassList) * 0.9)
		testNum = len(self.ClassList) - trainNum
		#rbf_feature = RBFSampler(gamma=1, random_state=1)
		#self.GenreList = rbf_feature.fit_transform(self.GenreList)
		self.Train_GenreList = self.GenreList[0:trainNum]
		self.Train_ClassList = self.ClassList[0:trainNum]
		self.Test_GenreList = self.GenreList[trainNum:]
		self.Test_ClassList = self.ClassList[trainNum:]

	def train(self):
		self.learner.fit(self.Train_GenreList, self.Train_ClassList)

	def test(self):
		output = self.learner.predict(self.Test_GenreList)
		total = len(output)
		correct = 0.0
		for i in range (0, len(output)):
			if (output[i] == self.Test_ClassList[i]):
				correct = correct + 1.0

		print "Test on uid " + str(self.u_id)
		print "correctness: " + str(correct / total)
	
	def crossValidation(self):
		print cross_val_score(self.learner, self.GenreList, self.ClassList, scoring='accuracy')
			

	
class Tag2BinaryLearner:
	
	u_id = 0
	TagList = []
	ClassList = []
	Train_TagList = []
	Train_ClassList = []
	Test_TagList = []
	Test_ClassList = []
	#learner = MLPClassifier(solver='lbfgs', alpha=1e-5, hidden_layer_sizes=(5, 2), random_state=1)
	learner = svm.SVC()
	def __init__(self, u_id):
		self.u_id = u_id
		self.fillParameters()
		self.splitTrainTest()
		print "Init Completion"
	
	def fillParameters(self):
		parser = Parser()
		(ml, rl) = parser.get_user_history(self.u_id)

		count = 0
		print "Getting total " + str((len(ml))) + " vectors"
		for m in ml:
			count = count + 1
			self.TagList.append(parser.get_movie_tag_vector_fast(int(m)))
		
		for i in range (0, len(self.TagList)):
			assert(len(self.TagList[i]) == 1128)

		d_rl = [float(i) for i in rl]
		averageRating = sum(d_rl) / len(d_rl)
		for r in d_rl:
			Output = 0.0
			if (r >= averageRating):
				Output = 1.0
			self.ClassList.append(Output)

	def splitTrainTest(self):
		trainNum = int(len(self.ClassList) * 0.9)
		testNum = len(self.ClassList) - trainNum
		self.Train_TagList = self.TagList[0:trainNum]
		self.Train_ClassList = self.ClassList[0:trainNum]
		self.Test_TagList = self.TagList[trainNum:]
		self.Test_ClassList = self.ClassList[trainNum:]

	def train(self):
		assert(len(self.Train_TagList) == len(self.Train_ClassList))
		f = np.array(self.Train_TagList).astype('float32')		
		t = np.array(self.Train_ClassList).astype('float32')
		self.learner.fit(f, t)

	def test(self):
		f = np.array(self.Test_TagList).astype('float32')		
		output = self.learner.predict(f)
		total = len(output)
		correct = 0.0
		for i in range (0, len(output)):
			if (output[i] == self.Test_ClassList[i]):
				correct = correct + 1.0

		print "Test on uid " + str(self.u_id)
		print "correctness: " + str(correct / total)
	
	def scoreSet(self):
		f = np.array(self.Test_TagList).astype('float32')		
		print self.learner.classes_
		print self.learner.predict_proba(f)
		print self.Test_ClassList

	def crossValidation(self):
		print cross_val_score(self.learner, self.TagList, self.ClassList, scoring='accuracy')

class Combined2BinaryLearner:
	
	u_id = 0
	FeatureList = []
	ClassList = []
	Train_FeatureList = []
	Train_ClassList = []
	Test_FeatureList = []
	Test_ClassList = []
	#learner = MLPClassifier(solver='lbfgs', alpha=1e-5, hidden_layer_sizes=(5, 2), random_state=1)
	learner = svm.SVC()

	def __init__(self, u_id):
		self.u_id = u_id
		self.fillParameters()
		self.splitTrainTest()
		print "Init Completion"
	
	def fillParameters(self):
		parser = Parser()
		(ml, rl) = parser.get_user_history(self.u_id)

		count = 0
		for m in ml:
			count = count + 1
			featureVec = parser.get_movie_tag_vector_fast(int(m)) + parser.get_movie_genre_vector(int(m))
			assert(len(featureVec) == 1148)
			self.FeatureList.append(featureVec)

		d_rl = [float(i) for i in rl]
		averageRating = sum(d_rl) / len(d_rl)
		for r in d_rl:
			Output = 0.0
			if (r >= averageRating):
				Output = 1.0
			self.ClassList.append(Output)

	def splitTrainTest(self):
		trainNum = int(len(self.ClassList) * 0.9)
		testNum = len(self.ClassList) - trainNum
		self.Train_FeatureList = self.FeatureList[0:trainNum]
		self.Train_ClassList = self.ClassList[0:trainNum]
		self.Test_FeatureList = self.FeatureList[trainNum:]
		self.Test_ClassList = self.ClassList[trainNum:]

	def train(self):
		assert(len(self.Train_FeatureList) == len(self.Train_ClassList))
		f = np.array(self.Train_FeatureList).astype('float32')		
		t = np.array(self.Train_ClassList).astype('float32')		
		print f.dtype
		self.learner.fit(f, t)

	def test(self):
		f = np.array(self.Test_FeatureList).astype('float32')		
		output = self.learner.predict(f)
		total = len(output)
		correct = 0.0
		for i in range (0, len(output)):
			if (output[i] == self.Test_ClassList[i]):
				correct = correct + 1.0

		print "Test on uid " + str(self.u_id)
		print "correctness: " + str(correct / total)
	
	def scoreSet(self):
		f = np.array(self.Test_FeatureList).astype('float32')		
		print self.learner.classes_
		print self.learner.predict_proba(f)
		print self.Test_ClassList

	def crossValidation(self):
		print cross_val_score(self.learner, self.FeatureList, self.ClassList, scoring='accuracy')




















