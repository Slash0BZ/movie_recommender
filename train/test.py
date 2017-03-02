import mrlib


def initTest():

	tl = mrlib.Tag2BinaryLearner(8)
	gl = mrlib.Genre2BinaryLearner(8)

	tl.train()
	tl.test()

	gl.train()
	gl.test()

cl = mrlib.Combined2BinaryLearner(8)
cl.train()
cl.test()
cl.scoreSet()
