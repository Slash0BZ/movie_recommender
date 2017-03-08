
from flask import Flask, jsonify, request, abort, make_response
from flask_httpauth import HTTPBasicAuth

from mrelearner.database import database_util
from mrelearner.core import corelib
import web_api_security

### Security Features Code ###
auth = HTTPBasicAuth()

@auth.get_password
def get_password(username):
    if username == web_api_security.web_api_username():
        return web_api_security.web_api_password()
    return None

@auth.error_handler
def unauthorized():
    return make_response(jsonify({'error': 'Unauthorized access'}), 401)
### End Security Features Code ###


app = Flask(__name__)


@app.route('/mrelearner/api/v1.0/history', methods=['POST'])
@auth.login_required
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
    #learner = corelib.Learner(user_id)
    #learner.train()
    #learner.save_model()
    return "success", 201


@app.route('/mrelearner/api/v1.0/recommender',methods=['POST'])
@auth.login_required
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

