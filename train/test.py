import mrlib
import numpy as np
import sys
sys.path.insert(0, '../database')
import database_util


def initTest(i):
	print ""
	print "Testing tag vector"
	tl = mrlib.Tag2BinaryLearner(i)
	tl.train()
	tl.test()
	print "Testing combined vector"
	gl = mrlib.Genre2BinaryLearner(i)
	gl.train()
	gl.test()

def tester():
	for i in range(1, 50):
		initTest(i)

def importRatings(uid):
	db = database_util.database()
	parser = mrlib.Parser()
	(movies, ratings) = parser.get_user_history(uid)
	num = len(movies) * 0.9
	for i in range (0, int(num)):
		db.add_user_history(uid + 10, movies[i], ratings[i], 0)

importRatings(2)
