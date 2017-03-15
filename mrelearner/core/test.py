import corelib
from utillib import Converter

def testLearn(i):
	learner = corelib.Learner(i)
	learner.train()
	learner.save_model()

def testPredict(i):
	predictor = corelib.Predictor(i)
	#arr = [151, 253, 260, 293, 296, 318, 1370]
	arr = [62, 70, 266, 480, 891]
	predictor.getMovies(arr)
	result = predictor.getRecommendations(2)
	print(result)

# testLearn(12)
testPredict(12)

#test utillib
# converter = Converter()
# print(converter.imdbid2mid(114709))
# print(converter.mid2imdbid(1))
# print(converter.imdbid2mid_batch([114709,113497,113228]))
# print(converter.mid2imdbid_batch([1,2,3]))