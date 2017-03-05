
from flask import Flask, jsonify, request, abort

import sys
sys.path.append("../")
from database import database_util
from core import corelib


app = Flask(__name__)


# for development purposes
@app.route('/mrelearner/api/v1.0/history', methods=['GET'])
def get_history():
    return jsonify({'history': history})

@app.route('/mrelearner/api/v1.0/history', methods=['POST'])
def update_history():
    if not request.json: 
        abort(400)

    user_id = request.json['user_id']
    movie_imdb_id = request.json["movie_imdb_id"]
    user_rating = request.json["user_rating"]
    timestamp = request.json["timestamp"]
    db = database_util.database()
    db.add_user_history(user_id, movie_imdb_id, user_rating, timestamp)

    #retrain the model
    learner = corelib.Learner(user_id)
    learner.train()
    laerner.save_model()
    return 201

@app.route('/mrelearner/api/v1.0/recommender',methods=['POST'])
def get_recommendation():
    if not request.json: 
        abort(400)
    user_id = request.json["user_id"]
    candidate_list = request.json["candidate_list"]
    predictor = corelib.Predictor(user_id)
    predictor.getMovies(candidate_list)
    result = predictor.getRecommendations(5)
    return jsonify({"result": result}), 200
    #return predict(user_id, condidate_list)

    
if __name__ == '__main__':
    app.run(debug=False)

