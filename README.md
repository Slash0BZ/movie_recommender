# movie_recommender

Status:
![alt text](https://travis-ci.com/Slash0BZ/movie_recommender.svg?token=XxdMDeqYpxGFmYzEwzAd&branch=master "Status")
[![codecov](https://codecov.io/gh/Slash0BZ/movie_recommender/branch/master/graph/badge.svg)](https://codecov.io/gh/Slash0BZ/movie_recommender)

## Introduction

This repo contains the learning component of the movie recommender project. The front end of the project can be found [here](https://github.com/rohitramkumar/Movie-Recommender).

Movie recommender is a project that recommends movies based on two factors: the trending/in-theater movies and the recommendation based on user past histories. This repo only handles the recommendation part. In the user environment, each user has the ability of adding a movie that he/she watched before and associate the movie with a rating. In this program, we can recommend movies based on the user history and ratings.

We provide an API for the front end to use the recommendation services.

## Learning Algorithm Guideline

We used a dataset from [MovieLens](https://movielens.org), which contains about 27,000 movies. Each movies is associated with a 1128 long tag vector, which represents the "features" of a movie. We used this vector as the main feature vector of a movie, combining with Genres to achieve the final feature vector. 

We used a SVM learner which predicts a binary tag (like / dislike) for every user on each movie. There is a score associated with the prediction so that we can rate and sort the candidate list that front end API passes with the likelihood that the user is going to like the movie. 

We tested and tuned our learner using the real-world user ratings that MovieLens provides.

## Code and File Structure

* ./mrelearner/core

The core libraries for learning. Specifically it includes two libraries `corelib.py` and `utillib.py`. 

`corelib.py`

The core learning library. It provides a class `Learner` and a class `Predictor`. `Learner` handles the training process for each user, and it is normally called when a new movie history is added for consideration for a user. Specifically, `Learner` reads the user history and train a new SVM model and then saves the model to database. This process is time consuming. `Predictor` handles predicts the score for newly input movies. It reads and loads the learning model directly from database and calculates the score. This process is relatively fast.

`utillib.py`

This is the utilities library to assist core learning. Mainly only one class `Converter` is used. This class handles the cases of transforming API caller ids to our internal ids.

* ./mrelearner/database

`database_utils.py` 

This contains a `database` class which processes and handles all operations that are directly connected with the database. The current class relies on Microsoft ODBC driver.

`parser.py`

This file includes all the functions for establishing initial movie database tables.

* ./mrelearner/taskqueue

`tasks.py`

This file processes training jobs in a workqueue built on Celery. This ensures that the API agent is non-block so that all user requests can receive immediate return values. 

* ./mrelearner/train

`mrlib.py`

This class was used mainly for tuning parameter purposes so most of the functions are not used in a working environment. However, some functions that helps building feature vectors are still in use.
	
* ./mrelearner/webapi

Web api interface

## Install and Deploy

Create a secret.py under ```mrelearner/database```, follow the interface of ```example_secret.py```, for you own database.

Currently, we are using MS-ODBC for database driver.

Create a web_api_security.py under ```mrelearner/webapi```, follow the interface of ```web_api_security_example.py``` using your own chosen username and password.

run ```pip install --editable .```

Install the package using the instructions above.

Make sure apache2, mod-wsgi and openssl are isntalled.

Create an certificate and key using ```openssl req -new -x509 -days 365 -sha3 -newkey rsa:2048 -nodes -keyout server.key -out server.crt -subj '/O=Company/OU=Department/CN=www.example.com/'```

Move web_api.wsgi to a location under ```/var/www/```.

Edit ```mrelearner_webapi.conf``` with the following: your own server name(url), the paths to your own certificate and key, and the path to where you put the .wsgi file.

Move ```mrelearner_webapi.conf``` to /etc/apache2/sites-available/ .

run ```a2enmod ssl```
run ```a2ensite mrelearner_webapi```

Restart apache.

Install rabbitmq ``` sudo apt-get install rabbitmq-server ```

Start Celery worker ```celery worker -A mrelearner.taskqueue.tasks --concurrency=1 &```

## Testing

The webapi was tested by manually issuing POST requests to the api.  The following cases were covered: Updating user history with a brand new user, updating user history with a user with insufficient history to train a model, updating user history with sufficient history to train a model, getting recommendations from a user that is not in the database, getting recommendations from a user with insufficient history to train a model, and getting recommendations from a user with sufficient history to train a model.

## Log

Packaging was done on March 2017.


