import database_util
import re
import sys
import requests
import json

from mrelearner.train import mrlib

db = database_util.database()
movie_info_file = '../data/movies.csv'

#read movie details from movie_info_file, and update online database
def import_movie():
	count = 0
	f = open(movie_info_file, 'r')
	for line in f:
		count = count + 1
		line = line.replace("\r\n", "")
		featureList = []
		if (line.find("\"") != -1):
			featureList = line.split('"')
			featureList[0] = featureList[0].replace(",", "")
			featureList[2] = featureList[2].replace(",", "")
		else:
			featureList = line.split(',')
		
		m_id = featureList[0]
		name = featureList[1]
		year = featureList[1]
		genre = featureList[2]
		name = name[0:name.find("(") - 1]
		pattern = re.compile(r'\((\d\d\d\d)\)', flags=re.DOTALL)
		year = pattern.findall(year)
		if (len(year) > 0):
			year = year[0]
		else:
			year = ""
		db.add_movie(m_id, name, genre, year)
	f.close()


#read movie imdb_id and tags from files selected in parser, and append those information to  online database
def import_feature():
	m_id = db.get_all_movie_id()
	parser = mrlib.Parser()
	for i in m_id:
		print i
		feature = db.a2s(parser.get_movie_tag_vector_fast(int(i)))
		imdb_id = parser.get_movie_imdb_id(int(i))
		db.add_feature_to_movie(i, imdb_id, feature)

#print id of themoviedb according to the input imdb_id
def get_tmdbid_from_imdbid(imdb_id):
	url = "https://api.themoviedb.org/3/find/tt" + str(imdb_id)
	api_key = "0073589baa8cc3d53982b22d3833212e"
	external_source = "imdb_id"
	r = requests.get(url, data={"api_key":api_key, "external_source":external_source})
	info = json.loads(r.text)
	print db.get_next_movie_id()
	print info['movie_results']

#return imdb_id according to the input id of themoviedb
def get_imdbid_from_tmdbid(tmdb_id):
	url = "https://api.themoviedb.org/3/movie/" + str(tmdb_id)
	api_key = "0073589baa8cc3d53982b22d3833212e"
	r = requests.get(url, data={"api_key":api_key})
	info = json.loads(r.text)
	return info["imdb_id"]	

#grab a list of popular(new) movie, if any of them not in database, add those into online database 
def import_popular_movies():
	genreTransformTable = {'Adventure':[12], 'Animation':[16], 'Comedy':[35], 'Fantasy':[14], 'Romance':[10749], 'Drama':[18], 'Action':[28], 'Crime':[80], 'Thriller':[53], 'Horror':[27], 'Mystery':[9648], 'Sci-Fi':[878], 'Documentary':[99, 36], 'War':[10752], 'Musical':[10402], 'Western':[37]}
	url = "https://api.themoviedb.org/3/movie/popular"
	api_key = "0073589baa8cc3d53982b22d3833212e"
	r = requests.get(url, data={"api_key":api_key})
	info = json.loads(r.text)
	for movie in info["results"]:	
		movie_imdb_id = get_imdbid_from_tmdbid(movie["id"])
		movie_imdb_id = movie_imdb_id.replace("t", "")
		movie_release_date = movie["release_date"]
		movie_release_date = movie_release_date[0:4]
		movie_name = movie["title"]
		genreList = movie["genre_ids"]
		genreStringList = list()
		for k in genreTransformTable.keys():
			curList = genreTransformTable[k]
			for c in curList:
				if c in genreList:
					genreStringList.append(k)
					break
		genreString = ""
		for g in genreStringList:
			genreString = genreString + g + "|"
		genreString = genreString[0:len(genreString) - 1]
		check = db.get_mid_from_imdbid(movie_imdb_id)
		if (check == -1):
			m_id = db.get_next_movie_id()
			print "[m_id] " + str(m_id) + " [name] " + movie_name + " [genre] " + genreString + " [year] " + str(movie_release_date)
			db.add_movie(m_id, movie_name, genreString, movie_release_date)

	
