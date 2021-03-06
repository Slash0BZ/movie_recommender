#
# This is the databse utilities
#
import pyodbc
import secret
import datetime
import os.path
import json
import requests
from enum import Enum
import numpy as np
class database:

	here = os.path.abspath(os.path.dirname(__file__))
	log_path = here + '/../log/'

	#auth info for database
	server = secret.get_server_key()
	database = secret.get_database_key()
	username = secret.get_username_key()
	password = secret.get_password_key()
	driver= '{ODBC Driver 13 for SQL Server}'

	# cnxn: the connection to the database
	# cursor: the cursor to the connection
	cursor = object()
	cnxn = object()

	# The init funciton for class database
	# Get called everytime a database object is created
	def __init__(self, _server = server, _database = database, _username = username,_password = password):
		self.server = _server
		self.database = _database
		self.username = _username
		self.password = _password
		self.connect()
		
	
	# Disconnect from the database when thsi class object is being destroyed(see connect())
	def __del__(self):
		self.cursor.close()
		del self.cursor
		self.cnxn.close()
	
	# Connect to the database.
	# Set two members of the database class
	# cnxn: the connection to the database
	# cursor: the cursor to the connection
	# More info: search Microsoft pyodbc
	def connect(self):
		self.cnxn = pyodbc.connect('DRIVER='+self.driver+';PORT=1433;SERVER='+self.server+';PORT=1443;DATABASE='+self.database+';UID='+self.username+';PWD='+ self.password)
		self.cursor = self.cnxn.cursor()

	# Disconnect to the database.
	# This get called in the deletion function for the class
	def disconnect(self):
		self.cursor.close()

	# Write a msg with time to the end of the log_file
	# log files are saved according to log_path variable
	# log file will be created when log_file_name.log does not exist in log_path 
	def write_log(self, msg, log_file_name):
		log_file = self.log_path + log_file_name + ".log"
		time_string = str(datetime.datetime.now())
		prepared_string = "[%s]: %s \n" % (time_string, msg)
		f = open(log_file, 'a')
		f.write(prepared_string)
		f.close()

	# Return True if the (name, genre, year) tuple exists in movie_info 
	def exists_in_movie_info(self, name, genre, year):
		self.cursor.execute("SELECT * FROM movie_info WHERE name=? AND genre=? AND year=?", name, genre, year)
		row = self.cursor.fetchone()
		if row:
			return True
		else:
			return False

	# Add a movie to movie_info with name, genre, year
	# Write log after the operation finishes
	def add_movie(self, m_id, name, genre, year):
		if (self.exists_in_movie_info(name, genre, year)):
			self.write_log("INSERT FAILURE DUE TO EXISTION %s %s %s" % (name, genre, year), 'movie_info')
			return
		self.cursor.execute("INSERT INTO movie_info (id,name,genre,year) VALUES (?,?,?,?)",m_id, name, genre, year)
		self.cnxn.commit()
		self.write_log("INSERT movie_info %s %s %s" % (name, genre, year), 'movie_info')

	def add_new_movie(self, m_id, name, genre, year, imdb_id):
		if (self.exists_in_movie_info(name, genre, year)):
			self.write_log("INSERT FAILURE DUE TO EXISTION %s %s %s" % (name, genre, year), 'movie_info')
			return
		self.cursor.execute("INSERT INTO movie_info (id,name,genre,year,imdb_id, tag_feature) VALUES (?,?,?,?,?,?)",m_id, name, genre, year, imdb_id, "")
		self.cnxn.commit()

	def get_info_from_imdbid(self, imdb_id):
		url = "https://api.themoviedb.org/3/find/tt" + str(imdb_id)
		api_key = "0073589baa8cc3d53982b22d3833212e"
		external_source = "imdb_id"
		r = requests.get(url, data={"api_key":api_key, "external_source":external_source})
		info = json.loads(r.text)
		return info["movie_results"][0]

	def add_movie_by_imdbid(self, imdbid):
		movie_info = self.get_info_from_imdbid(imdbid)
		genreTransformTable = {'Adventure':[12], 'Animation':[16], 'Comedy':[35], 'Fantasy':[14], 'Romance':[10749], 'Drama':[18], 'Action':[28], 'Crime':[80], 'Thriller':[53], 'Horror':[27], 'Mystery':[9648], 'Sci-Fi':[878], 'Documentary':[99, 36], 'War':[10752], 'Musical':[10402], 'Western':[37]}
		movie_year = movie_info["release_date"]
		movie_year = movie_year[0:4]
		movie_name = movie_info["title"]
		genreList = movie_info["genre_ids"]
		genreStringList = list()
		for k in genreTransformTable.keys():
			curList = genreTransformTable[k]
			for c in curList:
				if c in genreList:
					genreStringList.append(k)
					break
		movie_genre = ""
		for g in genreStringList:
			movie_genre = movie_genre + g + "|"
		movie_genre = movie_genre[0:len(movie_genre) - 1]
		#check = self.get_mid_from_imdbid(imdbid)
                m_id = self.get_next_movie_id()
		self.add_new_movie(m_id, movie_name, movie_genre, movie_year, imdbid)

			
		
	
	# Get a list of (movielens) movie ids from the database (movie id not equal to imdbid)
	def get_all_movie_id(self):
		self.cursor.execute("SELECT id FROM movie_info")
		arr = self.cursor.fetchall()
		ret = list()
		for a in arr:
			ret.append(a[0])
		return ret

	def get_next_movie_id(self):
		self.cursor.execute("SELECT MAX(id) FROM movie_info")
		result = self.cursor.fetchall()
		cid = result[0][0]
		return cid + 1

	# Create a new column in the specified table
	# Do nothing if the column_name is invalid or already exists
	# Do nothing if column_type is invalid
	# Write log message
	def create_column(self, table_name, column_name, column_type):
		# TO DO
		self.cursor.execute("ALTER TABLE ? ADD ? ?", table_name, column_name, column_type)
	
	#For the selected movie id in database, update its imdb_id and tag_features
	def add_feature_to_movie(self, m_id, imdb_id, feature):
		self.cursor.execute("UPDATE movie_info SET imdb_id=?, tag_feature=? WHERE id=?", imdb_id, feature, m_id)
		self.cnxn.commit()

	#array to string
	#currently used only for combining tag_feature
	#convert array of float into "|" separated string
	def a2s(self, arr):
		ret = ''
		for a in arr:
			a = float(a)
			a = a * 100.0
			ret += '|' + str(a)
		#remove last '|'
		return ret
	
	#array to string
	#currently used only for spliting tag_feature
	#convert "|" separated string into array of float
	def s2a(self, s):
		ret = np.zeros(1128)
                if s:
		        group = s.split("|")
		        for i in range(1128):
			        if(i>=len(group)):
				        break
			        if group[i] == '':
				        continue
			        ret[i] = float(group[i])
		        ret /= 100.0
		return ret
	
	# return movie_info (id,name,genre,year,imdb_id,feature) of selected movie id
	def get_movie_info(self, m_id):
		self.cursor.execute("SELECT * FROM movie_info WHERE id=?", m_id)
		row = self.cursor.fetchone()
		return row

	# return movie_info (id,name,genre,year,imdb_id,feature) of selected movie ids in the m_ids list
	def get_movie_info_batch(self, m_ids):
                statement = "SELECT * FROM movie_info WHERE id IN "

                if len(m_ids) == 0:
                        return -1
                elif len(m_ids) > 1:
                        statement += str(tuple(m_ids))
                else:
                        statement += "(" + str(m_ids[0]) + ")"
                        
		self.cursor.execute(statement)
		result = self.cursor.fetchall()
		if (len(result) == 0):
			return -1
		else:
			return result

	# For a movie imdb_id, get its associated (movielens) m_id
	# return non negative integer if match is found
	# return -1 if no match, -2 if duplicate exists 
	def get_mid_from_imdbid(self, imdb_id):
                imdb_id = int(imdb_id)
		self.cursor.execute("SELECT id FROM movie_info WHERE imdb_id=?", imdb_id)
		result = self.cursor.fetchall()
		if (len(result) == 0):
                        self.add_movie_by_imdbid(imdb_id)
                        return self.get_mid_from_imdbid(imdb_id)
		elif (len(result) >= 2):
			return -2
		else:
			return result[0][0]

	# For a movie marked by (movielens) m_id, get its associated imdb_id
	# return non negative integer if match is found
	# return -1 if no match, -2 if duplicate exists 
	def get_imdbid_from_mid(self, m_id):
		self.cursor.execute("SELECT imdb_id FROM movie_info WHERE id=?", m_id)
		result = self.cursor.fetchall()
		if (len(result) == 0):
			return -1
		elif (len(result) >= 2):
			return -2
		else:
			return int(result[0][0])

	# see get_mid_from_imdbid
	# get all associated (movielens) m_id in one database access
	def get_mid_from_imdbid_batch(self, imdb_ids):
                ret = []
                for imdb_id in imdb_ids:
                        mid = self.get_mid_from_imdbid(imdb_id)
                        if mid >= 0:
                                ret.append(mid)
                return ret
		# statement = "SELECT id FROM movie_info WHERE imdb_id IN "
                # imdb_id_ints = []
                # for i in imdb_ids:
                #         imdb_id_ints.append(int(i))
                # if len(imdb_id_ints) == 0:
                #         return -1
                # elif len(imdb_id_ints) > 1:
                #         statement += str(tuple(imdb_id_ints))
                # else:
                #         statement += "(" + str(imdb_id_ints[0]) + ")"

    		# self.cursor.execute(statement)
		# result = self.cursor.fetchall()
		# if (len(result) == 0):
		# 	return -1
		# else:
		# 	return [row[0] for row in result]

	#see get_imdbid_from_mid
	# get all associated imdb_id in one database access
	def get_imdbid_from_mid_batch(self, m_ids):
		statement = "SELECT imdb_id FROM movie_info WHERE id IN "
                if len(m_ids) == 0:
                        return -1
                elif len(m_ids) > 1:
                        statement += str(tuple(m_ids))
                else:
                        statement += "(" + str(m_ids[0]) + ")"
                        
		self.cursor.execute(statement)
		result = self.cursor.fetchall()
		if (len(result) == 0):
			return -1
		else:
			return [int(row[0]) for row in result]

	# Add/Update user history into user_history table
	# Write log after the operation finishes
	def add_user_history(self, u_id, m_id, rating, timestamp):
		self.cursor.execute("SELECT * FROM user_history WHERE u_id=? AND m_id=?", u_id, m_id)
		if len(self.cursor.fetchall()) == 0:
			#user with u_id not exist in db
			self.cursor.execute("INSERT INTO user_history (u_id,m_id,rating,timestamp) VALUES (?,?,?,?)",u_id, m_id, rating, timestamp)
			self.cnxn.commit()
			self.write_log("INSERT user_history %s %s %s %s" % (u_id, m_id, rating, timestamp), 'user_history')
		else:
			self.cursor.execute("UPDATE user_history SET rating=?,timestamp=? WHERE u_id=? AND m_id=?", rating, timestamp, u_id, m_id)
			self.cnxn.commit()
			self.write_log("UPDATE user_history %s %s %s %s" % (u_id, m_id, rating, timestamp), 'user_history')
		
	#get user history from user_history table
	def get_user_history(self, u_id):
		self.cursor.execute("SELECT * FROM user_history WHERE u_id=?", u_id)
		return self.cursor.fetchall()


#table user_model

	#update user genre model and/or tag model on the database
	def update_user_model(self, u_id, genre_model=None, tag_model=None):
		data = self.get_user_model(u_id)

		if len(data) == 0:
			#TODO set default value
			if genre_model==None:
				genre_model = 'None'
			if tag_model==None:
				tag_model= 'None'

			#user with u_id not exist in db
			self.cursor.execute("INSERT INTO user_model(u_id,genre_model,tag_model) VALUES (?,?,?)",u_id, genre_model, tag_model)
			self.cnxn.commit()
			self.write_log("INSERT user_model %s %s %s" % (u_id, genre_model, tag_model), 'user_model')
		else:
			#check input param
			if (genre_model==None) & (tag_model==None):
				return
			if genre_model==None:
				genre_model = data[1]
			if tag_model==None:
				tag_model = data[2]

			self.cursor.execute("UPDATE user_model SET genre_model=?,tag_model=? WHERE u_id=?", genre_model, tag_model, u_id)
			self.cnxn.commit()
			self.write_log("UPDATE user_model %s %s %s" % (u_id, genre_model, tag_model), 'user_model')
	
	#add user genre model, tag model and average to the database
	def add_user_model(self, u_id, g_model, t_model, average):
		self.cursor.execute("SELECT * FROM user_model WHERE u_id=?", u_id)
		if (len(self.cursor.fetchall()) == 0):
			self.cursor.execute("INSERT INTO user_model (u_id, genre_model, tag_model, average) VALUES (?,?,?,?)", u_id, g_model, t_model, average)
			self.cnxn.commit()
		else:
			self.cursor.execute("UPDATE user_model SET genre_model=?,tag_model=?,average=? WHERE u_id=?", g_model, t_model, average, u_id)
			self.cnxn.commit()
	
	#get all user models (u_id, genre_model, tag_model, average) from the database
	def get_user_model(self, u_id):
		self.cursor.execute("SELECT * FROM user_model WHERE u_id=?", u_id)
		return self.cursor.fetchall()

	
# table user_info
# u_id (int): the user id for learning db
# identifier (int): the user id for api caller

	# if the caller_id exists, return the u_id
	# otherwise insert the caller_id with a new u_id
	# TODO: add logger
	def get_uid(self, caller_id):
		self.cursor.execute("SELECT * FROM user_info WHERE identifier=?", caller_id)
		result = self.cursor.fetchall()
		if (len(result) == 0):
			self.cursor.execute("SELECT MAX(u_id) AS max_u_id FROM user_info")
			max_u_id = self.cursor.fetchall()[0][0]
			if (max_u_id == None):
				max_u_id = 0
			new_u_id = max_u_id + 1
			self.cursor.execute("INSERT INTO user_info (u_id, identifier) VALUES (?,?)", new_u_id, caller_id)
			self.cnxn.commit()
			return new_u_id
		return result[0][0]
	
	# if u_id exists, return caller_id
	# else return -1
	# TODO: add logger
	def get_identifier(self, u_id):
		self.cursor.execute("SELECT * FROM user_info WHERE u_id=?", u_id)
		result = self.cursor.fetchall()
		if (len(result) == 0):
			return -1
		else:
			return result[0][1]


