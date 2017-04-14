import corelib
from utillib import Converter
from random import shuffle
from mrelearner.database import database_util
from mrelearner.train import mrlib

def testLearn(i):
	learner = corelib.Learner(i)
	learner.train()
#	learner.save_model()

def testPredict(i,arr):
	predictor = corelib.Predictor(i)
	#arr = [151, 253, 260, 293, 296, 318, 1370]
	predictor.getMovies(arr)
	result = predictor.getRecommendations(4)
	print(result)


arr = [62, 70, 266, 480, 891,1259,1327,1548,2291,2791,2858,3565,3918]
testLearn(12)
testPredict(12,arr)
db = database_util.database()
history = db.get_user_history(12)






#test utillib
converter = Converter()
print(converter.imdbid2mid(114709))
print(converter.mid2imdbid(1))
print(converter.imdbid2mid_batch([114709,113497,113228]))
print(converter.mid2imdbid_batch([1,2,3]))



