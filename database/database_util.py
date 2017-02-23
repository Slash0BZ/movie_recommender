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

	def __init__(self, _server = server, _database = database, _username = username,_password = password):
		self.server = _server
		self.database = _database
		self.username = _username
		self.password = _password
		self.connect()
	
	def __del__(self):
		self.cursor.close()
		del self.cursor
		self.cnxn.close()
	
	def connect(self):
		self.cnxn = pyodbc.connect('DRIVER='+self.driver+';PORT=1433;SERVER='+self.server+';PORT=1443;DATABASE='+self.database+';UID='+self.username+';PWD='+ self.password)
		self.cursor = self.cnxn.cursor()

	def disconnect(self):
		self.cursor.close()

	def write_log(self, msg):
		time_string = str(datetime.datetime.now())
		prepared_string = "[%s]: %s" % (time_string, msg)
		f = open(self.log_file, 'a')
		f.write(prepared_string)
		f.close()

	def exists_in_movie_info(self, name, genre, year):
		self.cursor.execute("SELECT * FROM movie_info WHERE name=? AND genre=? AND year=?", name, genre, year)
		row = self.cursor.fetchone()
		if row:
			return True
		else:
			return False

	def add_movie(self, name, genre, year):
		if (self.exists_in_movie_info(name, genre, year)):
			self.write_log("INSERT FAILURE DUE TO EXISTION %s %s %s" % (name, genre, year))
			return
		self.cursor.execute("INSERT INTO movie_info (name,genre,year) VALUES (?, ?, ?)", name, genre, year)
		self.cnxn.commit()
		self.write_log("INSERT movie_info %s %s %s" % (name, genre, year))

