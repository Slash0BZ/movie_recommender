import corelib

def testLearn(i):
	learner = corelib.Learner(i)
	learner.train()
	learner.save_model()

def testPredict(i):
	predictor = corelib.Predictor(i)
	arr = [1, 2, 3, 104]
	predictor.getMovies(arr)
	predictor.getRecommendations(2)

testLearn(6)
testPredict(6)
