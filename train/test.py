import mrlib

l = mrlib.Genre2BinaryLearner(1)

l.train()
print l.test()
