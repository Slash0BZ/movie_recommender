import mrlib


p = mrlib.Parser()

l = mrlib.Tag2BinaryLearner(4)
l.train()
l.scoreSet()
