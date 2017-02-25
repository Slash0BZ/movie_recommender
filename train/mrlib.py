import re
class Parser:
	
	movie_file = "../data/movies.csv"
	rating_file = "../data/ratings.csv"
	genreList = ['Adventure', 'Animation', 'Children', 'Comedy', 'Fantasy', 'Romance', 'Drama', 'Action', 'Crime', 'Thriller', 'Horror', 'Mystery', 'Sci-Fi', 'IMAX', 'Documentary', 'War', 'Musical', 'Western', 'Film-Noir', '(no genres listed)']

	def __init__(self, _movie_file = movie_file, _rating_file = rating_file):
		self.movie_file = _movie_file
		self.rating_file = _rating_file
	
	def pre_process_line(self, line):
		line = line.replace("\r\n", "")
		line = line.replace("\n", "")
		return line

	def parse_history_entry(self, line):
		line = self.pre_process_line(line)
		lineGroup = line.split(",")
		return [lineGroup[0], lineGroup[1], lineGroup[2], lineGroup[3]]
	
	def get_user_history(self, u_id):
		count = 0
		fp = open(self.rating_file, 'r')
		foundFlag = False
		ret_movie = list()
		ret_rating = list()
		for line in fp:
			count = count + 1
			if (count == 1):
				continue
			[c_u_id, m_id, rating, timeStamp] = self.parse_history_entry(line)
			if (u_id == int(c_u_id)):
				foundFlag = True
				ret_movie.append(m_id)
				ret_rating.append(rating)
			if (foundFlag and u_id != int(c_u_id)):
				break
		fp.close()
		if (len(ret_movie) != len(ret_rating)):
			print "[Error]: movie does not correspond a rating"
			return (list(), list())
		else:
			return (ret_movie, ret_rating)
	
	def parse_movie_entry(self, line):
		line = self.pre_process_line(line)
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
		return [m_id, name, genre, year]
	
	def genre2vec(self, genre):
		gl = genre.split("|")
		ret = list()
		for g in self.genreList:
			if g in gl:
				ret.append(1)
			else:
				ret.append(0)
		return ret
	
	def get_movie_genre_vector(self, m_id):
		count = 0
		ret_vec = list()
		fp = open(self.movie_file, 'r')
		for line in fp:
			count = count + 1
			if (count == 1):
				continue
			[c_m_id, name, genre, year] = self.parse_movie_entry(line)
			if (m_id == int(c_m_id)):
				return self.genre2vec(genre)
		fp.close()
		return list()
			
