import database_util
import re

db = database_util.database()
movie_info_file = './data/movies.csv'

def import_movie():
	count = 0
	f = open(movie_info_file, 'r')
	for line in f:
		count = count + 1
		if (count == 1):
			continue
		if (count > 10):
			break
		line = line.replace("\r\n", "")
		featureList = line.split(',')

		name = featureList[1]
		year = featureList[1]
		genre = featureList[2]
		name = name[0:name.find("(") - 1]
		year = year[year.find("(")+1:year.find(")")]
		db.add_movie(name, genre, year)
	f.close()
	
import_movie()
