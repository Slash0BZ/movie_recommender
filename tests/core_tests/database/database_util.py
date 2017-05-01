#
# This is the databse utilities
#
import datetime
import os.path
import numpy as np
import base64
class database:

	here = os.path.abspath(os.path.dirname(__file__))
	log_path = here + '/../log/'

	def __init__(self):
		self.connect()
		
	def connect(self):
		print "Pseudo connect called"

	def disconnect(self):
		print "Pseudo disconnect called"

	def write_log(self, msg, log_file_name):
		log_file = self.log_path + log_file_name + ".log"
		time_string = str(datetime.datetime.now())
		prepared_string = "[%s]: %s \n" % (time_string, msg)
		f = open(log_file, 'a')
		f.write(prepared_string)
		f.close()

	def a2s(self, arr):
		ret = ''
		for a in arr:
			a = float(a)
			a = a * 100.0
			ret = ret + "|" + str(a)
		return ret
	
	def s2a(self, s):
		group = s.split("|")
		ret = np.zeros(1128)

		for i in range(1128):
			if(i>=len(group)):
				break
			if group[i] == '':
				continue
			ret[i] = float(group[i])
		ret /= 100.0
		return ret
	
	def get_movie_info(self, m_id):
		with open(self.here + "/pseudo_db/movie_info") as f:
			content = f.readlines()
		for line in content:
			line = line.strip("\n")
			line = line.strip("\r")
			info = line.split("\t")
			return info
		return list()

	def get_movie_info_batch(self, m_ids):
		ret = list()
		for m_id in m_ids:
			ret.append(self.get_movie_info(m_id))
		return ret

	def get_mid_from_imdbid(self, imdb_id):
		with open(self.here + "/pseudo_db/movie_info") as f:
			content = f.readlines()
		for line in content:
			line = line.strip("\n")
			line = line.strip("\r")
			info = line.split("\t")
			if (int(info[4]) == int(imdb_id)):
				return info[0]
		return 0

	def get_imdbid_from_mid(self, m_id):
		with open(self.here + "/pseudo_db/movie_info") as f:
			content = f.readlines()
		for line in content:
			line = line.strip("\n")
			line = line.strip("\r")
			info = line.split("\t")
			if (int(info[0]) == int(m_id)):
				return info[4]
		return 0

	def get_mid_from_imdbid_batch(self, imdb_ids):
		ret = list()
		for imdb_id in imdb_ids:
			ret.append(self.get_mid_from_imdbid(imdb_id))
		return ret

	def get_imdbid_from_mid_batch(self, m_ids):
		ret = list()
		for m_id in m_ids:
			ret.append(self.get_imdbid_from_mid(m_id))
		return ret

	def get_user_history(self, u_id):
		ret = list()
		with open(self.here + "/pseudo_db/user_history") as f:
			content = f.readlines()
		for line in content:
			line = line.strip("\n")
			line = line.strip("\r")
			info = line.split("\t")
			if (int(info[0]) == int(u_id)):
				ret.append(info)
		return ret	
			

	def add_user_model(self, u_id, g_model, t_model, average):
		if (len(self.get_user_model(u_id)) > 0):
			return
		with open(self.here + "/pseudo_db/user_model", "a") as f:
			f.write(str(u_id) + "\t" + base64.b64encode(str(g_model)) + "\t" + base64.b64encode(str(t_model)) + "\t" + str(average) + "\n")

	def get_user_model(self, u_id):
		ret = list()
		with open(self.here + "/pseudo_db/user_model") as f:
			content = f.readlines()
		for line in content:
			line = line.strip("\n")
			line = line.strip("\r")
			info = line.split("\t")
			if (int(info[0]) == int(u_id)):
				info[1] = base64.b64decode(info[1])
				info[2] = base64.b64decode(info[2])
				ret.append(info)
		return ret

	def get_uid(self, caller_id):
		return caller_id
	
	def get_identifier(self, u_id):
		return u_id
