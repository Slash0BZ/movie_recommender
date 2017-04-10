from celery import Celery

from mrelearner.database import database_util
from mrelearner.core import corelib

app = Celery('tasks', broker='amqp://')

@app.task
def test_task():
    print "hello celery"

@app.task
def update_history(uid, mid, rating, timestamp):
    db = database_util.database()
    db.add_user_history(uid, mid, rating, timestamp)
    print "added user " + str(uid) 
    learner = corelib.Learner(uid)
    if not learner.not_enough_history:
        learner.train()
        learner.save_model()
    
