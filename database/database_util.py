#
# This is the databse utilities
#
import pyodbc
import secret
import datetime

class database:
	
	log_file = '../log/database.log'

	server = secret.get_server_key()
	database = secret.get_database_key()
	username = secret.get_username_key()
	password = secret.get_password_key()
	driver= '{ODBC Driver 13 for SQL Server}'
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
	
	# Get callde everytime a database object is collected
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
	def write_log(self, msg):
		time_string = str(datetime.datetime.now())
		prepared_string = "[%s]: %s" % (time_string, msg)
		f = open(self.log_file, 'a')
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
			self.write_log("INSERT FAILURE DUE TO EXISTION %s %s %s" % (name, genre, year))
			return
		self.cursor.execute("INSERT INTO movie_info (id,name,genre,year) VALUES (?,?,?,?)",m_id, name, genre, year)
		self.cnxn.commit()
		self.write_log("INSERT movie_info %s %s %s" % (name, genre, year))
	
	def get_all_movie_id(self):
		self.cursor.execute("SELECT id FROM movie_info")
		arr = self.cursor.fetchall()
		ret = list()
		for a in arr:
			ret.append(a[0])
		return ret

	# Create a new column in the specified table
	# Do nothing if the column_name is invalid or already exists
	# Do nothing if column_type is invalid
	# Write log message
	def create_column(self, table_name, column_name, column_type):
		# TO DO
		self.cursor.execute("ALTER TABLE ? ADD ? ?", table_name, column_name, column_type)
	
	def add_feature_to_movie(self, m_id, imdb_id, feature):
		self.cursor.execute("UPDATE movie_info SET imdb_id=?, tag_feature=? WHERE id=?", imdb_id, feature, m_id)
		self.cnxn.commit()

	def a2s(self, arr):
		ret = ''
		for a in arr:
			a = float(a)
			a = a * 100.0
			ret = ret + "|" + str(a)
		return ret
	
	def s2a(self, s):
		group = s.split("|")
		ret = list()
		for g in group:
			if (g == ''):
				continue
			ret.append(float(g) / 100.0)
		return ret

	# Add info to the specifies rows in the specifies column with value	
	#def add_movie_additional(self, m_id, column_name, value):






	# Add user history into user_history table
	# Write log after the operation finishes
	def add_user_history(self, u_id, m_id, rating, timestamp):
		self.cursor.execute("SELECT * FROM user_history WHERE u_id=? AND m_id=?", u_id, m_id)
		if len(self.cursor.fetchall()) == 0:
			self.cursor.execute("INSERT INTO user_history (u_id,m_id,rating,timestamp) VALUES (?,?,?,?)",u_id, m_id, rating, timestamp)
			self.cnxn.commit()
			self.write_log("INSERT user_history %s %s %s %s" % (u_id, m_id, rating, timestamp))
		else:
			self.cursor.execute("UPDATE user_history SET rating=?,timestamp=? WHERE u_id=? AND m_id=?", rating, timestamp, u_id, m_id)
			self.cnxn.commit()
			self.write_log("UPDATE user_history %s %s %s %s" % (u_id, m_id, rating, timestamp))
		
