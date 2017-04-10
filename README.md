# movie_recommender

Status:
![alt text](https://travis-ci.com/Slash0BZ/movie_recommender.svg?token=XxdMDeqYpxGFmYzEwzAd&branch=master "Status")
[![codecov](https://codecov.io/gh/Slash0BZ/movie_recommender/branch/master/graph/badge.svg)](https://codecov.io/gh/Slash0BZ/movie_recommender)


The learning part of the project movie recommender.

## Install

Create a secret.py under ```mrelearner/database```, follow the interface of ```example_secret.py```, for you own database.

Currently, we are using MS-ODBC for database driver.

Create a web_api_security.py under ```mrelearner/webapi```, follow the interface of ```web_api_security_example.py``` using your own chosen username and password.

run ```pip install --editable .```

## Deploy
Install the package using the instructions above.

Make sure apache2, mod-wsgi and openssl are isntalled.

Create an certificate and key using ```openssl req -new -x509 -days 365 -sha3 -newkey rsa:2048 -nodes -keyout server.key -out server.crt -subj '/O=Company/OU=Department/CN=www.example.com/'```

Move web_api.wsgi to a location under ```/var/www/```.

Edit ```mrelearner_webapi.conf``` with the following: your own server name(url), the paths to your own certificate and key, and the path to where you put the .wsgi file.

Move ```mrelearner_webapi.conf``` to /etc/apache2/sites-available/ .

run ```a2enmod ssl```
run ```a2ensite mrelearner_webapi```

Restart apache.

## Log

Packaging was done on March 2017.
