
from flask import Flask, jsonify, request, abort, make_response
from flask_httpauth import HTTPBasicAuth

from mrelearner.database import database_util
from mrelearner.core import corelib
from mrelearner.core import utilib
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


# For testing purposes                                                          
@app.route('/')
def hello_world():
    return 'Hello, World!'


@app.route('/mrelearner/api/v1.0/history', methods=['POST'])
@auth.login_required
def update_history():
    if not request.json: 
        abort(400)
    if not "user_id" in request.json:
        abort(400)
    if not "movie_imdb_id" in request.json:
        abort(400)
    if not "user_rating" in request.json:
        abort(400)
    if not "timestamp" in request.json:
        abort(400)
        
    user_id = request.json['user_id']
    movie_imdb_id = request.json["movie_imdb_id"]
    user_rating = request.json["user_rating"]
    timestamp = request.json["timestamp"]
    db = database_util.database()
    conv = utilib.Converter()

    our_mid = conv.imdbid2mid(movie_imdb_id)
    our_uid = conv.callerid2uid(user_id)
    db.add_user_history(our_uid, our_mid, user_rating, timestamp)

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
    if not "user_id" in request.json:
        abort(400)
        
    user_id = request.json["user_id"]
    candidate_list = request.json.get("candidate_list")
    num_recommendations = request.json.get("num_recommendations")

    conv = utilib.Converter()

    our_uid = conv.callerid2uid(user_id)
    
    if not num_recommendations:
        num_recommendations = 5
        
    predictor = corelib.Predictor(our_uid)
    if predictor.invalid_user:
        return jsonify({"result": "no model"}), 200
        
    if candidate_list:
        our_ids_candidate_list = conv.imdbid2mid_batch(candidate_list)
        predictor.getMovies(our_ids_candidate_list)
        result = predictor.getRecommendations(num_recommendations)
        return jsonify({"result": result}), 200
    else:
        #What to do if candidate_list is not given
        return "not implemented yet", 200

    
if __name__ == '__main__':
    app.run(debug=False)

