#!../venv/bin/python

from flask import Flask, jsonify, request, abort
import sys
sys.path.inser(0, "../database")
import database_util
import time
import math

app = Flask(__name__)

# For testing purposes without a database
history = [
    {
        'id': 1,
        'user_id': 1,
        'movie_imdb_id': 1000, 
        'user_rating': 4 
    },
    {
        'id': 2,
        'user_id': 1,
        'movie_imdb_id': 9001, 
        'user_rating': 5 
    }
]

# for development purposes
@app.route('/mrelearner/api/v1.0/history', methods=['GET'])
def get_history():
    return jsonify({'history': history})

@app.route('/mrelearner/api/v1.0/history', methods=['POST'])
def update_history():
    if not request.json: 
        abort(400)
    history_entry = {
        #'id': history[-1]['id'] + 1,
        'user_id': request.json['user_id'],
        'movie_imdb_id': request.json["movie_imdb_id"],
        'user_rating': request.json["user_rating"]
        "timestamp": request.json["timestamp"]
    }
    history.append(history_entry)
    db = database_util.database()
    
    #return jsonify({'history': history}) #replace with function to update database

@app.route('/mrelearner/api/v1.0/recommend',methods=['POST'])
def get_recommendation():
    if not request.json: 
        abort(400)
    user_id = request.json["user_id"]
    candidate_list = request.json["candidate_list"]
    #return predict(user_id, condidate_list)

    
if __name__ == '__main__':
    app.run(debug=True)

