import mrlib

for i in range (1, 51):
	l = mrlib.Genre2BinaryLearner(i)
	l.train()
	l.test()
