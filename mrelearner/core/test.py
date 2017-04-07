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
for h in history:
	if h[1] in arr:
		print(str(h[1])+'|||'+str(h[2]))





#test utillib
# converter = Converter()
# print(converter.imdbid2mid(114709))
# print(converter.mid2imdbid(1))
# print(converter.imdbid2mid_batch([114709,113497,113228]))
# print(converter.mid2imdbid_batch([1,2,3]))

print('--------------------')

def get_feature(db, parser, history):
	movies = []
	ratings = []
	genre_features = []
	tag_features = []

	for h in history:
		movies.append(h[1])
		ratings.append(h[2])

	info = db.get_movie_info_batch(movies)

	for i,m in enumerate(movies):
		t = db.s2a(info[i][5])
		if  (t.shape[0] != 1128):
			t = np.zeros(1128)
		g = parser.genre2vec(info[i][2])
		genre_features.append(g)
		tag_features.append(t)

	rating_sum = 0
	for r in ratings:
		rating_sum = rating_sum + float(r)
	average_rating = rating_sum / float(len(ratings))

	comp = []
	for r in ratings:
		if (float(r) > average_rating):
			comp.append(1.0)
		else:
			comp.append(0.0)

	return movies, genre_features, tag_features, comp 

#main test setting
u_id = 12
db = database_util.database()
parser = mrlib.Parser()
history = db.get_user_history(u_id)
print(len(history))
shuffle(history)
movies, genre_features, tag_features, comp = get_feature(db, parser, history)

train_set_size = int(len(history)*0.8)
model = corelib.SVMModel()

model.train(genre_features[:train_set_size], comp[:train_set_size], tag_features[:train_set_size], comp[:train_set_size])

print(model.test(genre_features[train_set_size:], tag_features[train_set_size:], comp[train_set_size:]))