# movie_recommender

Status:
![alt text](https://travis-ci.com/Slash0BZ/movie_recommender.svg?token=XxdMDeqYpxGFmYzEwzAd&branch=master "Status")

The learning part of the project movie recommender.

## Install

Create a secret.py under ```mrelearner/database```, follow the interface of ```example_secret.py```, for you own database.

Currently, we are using MS-ODBC for database driver.

Create a web_api_security.py under ```mrelearner/webapi```, follow the interface of ```web_api_security_example.py``` using your own chosen username and password.

run ```pip install --editable .```

## Deploy
Install the package using the instructions above.

Make sure apache2 and openssl are isntalled.

Create an certificate and key using ```openssl req -new -x509 -days 365 -sha1 -newkey rsa:1024 -nodes -keyout server.key -out server.crt -subj '/O=Company/OU=Department/CN=www.example.com/'```

Move web_api.wsgi to a location under ```/var/www/```.

Edit ```mrelearner_webapi.conf``` with the following: your own server name(url), the paths to your own certificate and key, and the path to where you put the .wsgi file.

run ```a2enmod ssl```

Restart apache.

## Log

Packaging was done on March 2017.
