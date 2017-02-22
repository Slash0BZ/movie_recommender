import pyodbc
import secret

class database:

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

	def add_movie(self, name, genre):
		self.cursor.execute("INSERT INTO movie_info (name,genre) VALUES (?, ?)", name, genre)
		self.cnxn.commit()
