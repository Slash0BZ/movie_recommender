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

tester()
