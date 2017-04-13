import sys

from mrelearner.database import database_util

# Converter is used as an abstract layer between API callers and handlers
# It transforms Caller u_id conventions and imdb_id to learner u_id and m_id

class Converter:
	
	db = object()
	def __init__(self):
		self.db = database_util.database()
	
	# imdbid: imdb id of movies, used by caller	
	# mid: internal m_id of learner
	# mid should not be known by caller

	# @params
	# imdb_id: a single imdb_id
	# @return
	# A single m_id if the input matches the database
	# -1 if the input does not match the database
	def imdbid2mid(self, imdb_id):
		return self.db.get_mid_from_imdbid(imdb_id)
	
	# @params
	# m_id: a single m_id
	# return
	# A single imdb_id.
	# -1 if m_id is not valid
	def mid2imdbid(self, m_id):
		return self.db.get_imdbid_from_mid(m_id)
	
	# @params
	# imdb_ids: an array of imdb_id
	# call imdbid2mid
	# @return
	# An array of m_ids
	def imdbid2mid_batch(self, imdb_ids):
		return self.db.get_mid_from_imdbid_batch(imdb_ids)
		
	# @params
	# m_ids: an array of imdb_id
	# call mid2imdbid
	# @return
	# An array of imdb_ids
	def mid2imdbid_batch(self, m_ids):
		return self.db.get_imdbid_from_mid_batch(m_ids)
	
	# callerid: the user identifier used by caller
	# uid: internal u_id of learner
	# uid should not be known by caller

	# Corner cases: 
	# When caller_id does not match id_convention,
	# increment a internal u_id for the new called_id
	# Should always returns a valid value
	def callerid2uid(self, caller_id):
		return self.db.get_uid(caller_id)

	# return -1 if u_id does not exists
	def uid2callerid(self, u_id):
		return self.db.get_identifier(u_id)


class PoolGenerator:

	db = object()
	converter = object()

	def __init__(self, input_list):
		self.db = database_util.database()
		self.converter = Converter()
		self.imdb_list = input_list
		self.m_id_list = list()
		self.fill_m_id_list()

	def fill_m_id_list(self):
		if (len(self.imdb_list) == 0):
			return
		self.m_id_list = converter.imdbid2mid_batch(self.imdb_list)
		
		# If imdb_id passed does not exist, remove from m_id
		self.m_id_list = [x for x in self.m_id_list if x != -1]

