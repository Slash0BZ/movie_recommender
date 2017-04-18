import database_util
import re
import sys
import requests

from mrelearner.train import mrlib

db = database_util.database()
movie_info_file = '../data/movies.csv'

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


	
def import_feature():
	m_id = db.get_all_movie_id()
	parser = mrlib.Parser()
	for i in m_id:
		print i
		feature = db.a2s(parser.get_movie_tag_vector_fast(int(i)))
		imdb_id = parser.get_movie_imdb_id(int(i))
		db.add_feature_to_movie(i, imdb_id, feature)

def import_new_movies():
	#genre_transform_table = [28:"Action", 12:"Adventure", 35:"Comedy", 80:"Crime", 99:"Documentary", 18:"Drama", 14:"Fantasy", 36:"Documentary"]
	genreTransformTable = {'Adventure':[12], 'Animation':[16], 'Comedy':[35], 'Fantasy':[14], 'Romance':[10749], 'Drama':[18], 'Action':[28], 'Crime':[80], 'Thriller':[53], 'Horror':[27], 'Mystery':[9648], 'Sci-Fi':[878], 'Documentary':[99, 36], 'War':[10752], 'Musical':[10402], 'Western':[37]}
	url = "https://api.themoviedb.org/3/genre/movie/list"
	api_key = "0073589baa8cc3d53982b22d3833212e"
	r = requests.get(url, data={"api_key":api_key})
	print r.text
	print 1

import_new_movies()
	
	
