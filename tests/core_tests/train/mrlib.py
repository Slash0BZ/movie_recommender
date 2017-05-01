import re
import numpy as np
from sklearn import svm
from sklearn import linear_model
from sklearn.kernel_approximation import RBFSampler
from sklearn.naive_bayes import GaussianNB
from sklearn.neural_network import MLPClassifier
from sklearn.model_selection import cross_val_score

class Parser:
	
	genreList = ['Adventure', 'Animation', 'Children', 'Comedy', 'Fantasy', 'Romance', 'Drama', 'Action', 'Crime', 'Thriller', 'Horror', 'Mystery', 'Sci-Fi', 'IMAX', 'Documentary', 'War', 'Musical', 'Western', 'Film-Noir', '(no genres listed)']

	def __init__(self):
		return
	
	def genre2vec(self, genre):
		gl = genre.split("|")
		ret = np.zeros(len(self.genreList))
		for i,g in enumerate(self.genreList):
			if g in gl:
				ret[i] = 1.0

		return ret
