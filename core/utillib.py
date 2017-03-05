import sys
sys.path.insert(0, '../database')
import database_util

# Converter is used as an abstract layer between API callers and handlers
# It transforms Caller u_id conventions and imdb_id to learner u_id and m_id

class Converter:
	
	def __init__(self):
		return
	
	# imdbid: imdb id of movies, used by caller	
	# mid: internal m_id of learner
	# mid should not be known by caller

	# @params
	# imdb_id: a single imdb_id
	# @return
	# A single m_id if the input matches the database
	# -1 if the input does not match the database
	def imdbid2mid(self, imdb_id):
		#TODO
		return
	
	# @params
	# m_id: a single m_id
	# return
	# A single imdb_id.
	# -1 if m_id is not valid
	def mid2imdbid(self, m_id):
		#TODO
		return
	
	# @params
	# imdb_ids: an array of imdb_id
	# call imdbid2mid
	# @return
	# An array of m_ids
	def imdbid2mid_batch(self, imdb_ids):
		#TODO
		return
		
	# @params
	# m_ids: an array of imdb_id
	# call mid2imdbid
	# @return
	# An array of imdb_ids
	def mid2imdbid_batch(self, m_ids):
		#TODO
		return
	
	# callerid: the user identifier used by caller
	# uid: internal u_id of learner
	# uid should not be known by caller

	# Corner cases: 
	# When caller_id does not match id_convention,
	# increment a internal u_id for the new called_id
	# Should always returns a valid value
	def callerid2uid(self, caller_id):
		#TODO
		return

	# return -1 if u_id does not exists
	def uid2callerid(self, u_id):
		#TODO
		return
