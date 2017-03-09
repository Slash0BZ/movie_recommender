import json 
import requests

# Updating user history
url1 = "http://ec2-54-200-205-223.us-west-2.compute.amazonaws.com:5000/mrelearner/api/v1.0/history"
data1 = {"user_id": 3, "movie_imdb_id": 1001, "user_rating": 4, "timestamp": 1488587217}

r1 = requests.post(url1, json=data1)
print r1.status_code


# Getting recommendations for a user
url2 = "http://ec2-54-200-205-223.us-west-2.compute.amazonaws.com:5000/mrelearner/api/v1.0/recommender"
data2 = {"user_id": 11, "candidate_list": [62, 70, 266, 480, 891]}

r2 = requests.post(url2, json=data2)
print r2.json()
