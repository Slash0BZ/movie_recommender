import database_util

d = database_util.database()
# d.add_user_history(1,14,5,123124)
# 
# print(d.get_user_history(1))
# 
# #user_model
# d.update_user_model(1)
# d.update_user_model(1, "b", "b")
# d.update_user_model(1, "c", "b")

#print d.get_movie_info_batch(range(10))
print '===test==='



#test  get_movie_info()

#check we can get movie_info using m_id from get_all_movie_id
m_id = d.get_all_movie_id()[:10]
for i in m_id:
	retval = d.get_movie_info(i)
	#movieid | name | genre | year | imdb | tag, (should be 6 values)
	assert len(retval) > 5
	#movieid match
	assert retval[0] == i
print('pass get movie_info using m_id from get_all_movie_id')




#check we cannot get movie_info not in m_id from get_all_movie_id
m_id = d.get_all_movie_id()

	#select candidate from id not in m_id
candidate = []
for i in range(m_id[-1]):
	#we get n movies not in m_id (n = 6)
	if len(candidate) == 6:
		break

	if i not in m_id:
		candidate.append(i)

for i in candidate:
	retval = d.get_movie_info(i)
	assert retval==None
print('pass cannot get movie_info not in m_id from get_all_movie_id')

#test  get_movie_info_batch()
#check we can get movie_info using m_id from get_all_movie_id
m_id = d.get_all_movie_id()[:10]
retval = d.get_movie_info_batch(m_id)
for i in retval:
	assert len(i) > 5
print('pass get movie_info_batch check')

#test exists_in_movie_info() for attribute return from get_movie_info
m_id = d.get_all_movie_id()[:10]
for i in m_id:
	retval = d.get_movie_info(i)
	assert(d.exists_in_movie_info(retval[1],retval[2],retval[3]))
print('pass exists_in_movie_info() for attribute return from get_movie_info')

#test not exists_in_movie_info() with some input
#check according to Toy Story (m_id=1) 	|('Toy Story', 'Adventure|Animation|Children|Comedy|Fantasy','1995')
#(m_id=2) is used to make other test 	|('Jumanji', 'Adventure|Children|Fantasy','1995')
#trash input
assert(d.exists_in_movie_info('ssss','Anime','1995')==False)
#only movie name not correct
assert(d.exists_in_movie_info('ssss','Adventure|Animation|Children|Comedy|Fantasy','1995')==False)
#movie name of other movie
assert(d.exists_in_movie_info('Jumanji','Adventure|Animation|Children|Comedy|Fantasy','1995')==False)
#movie genre of other movie
assert(d.exists_in_movie_info('Toy Story','Adventure|Children|Fantasy','1995')==False)
#movie year not correct
assert(d.exists_in_movie_info('Toy Story','Adventure|Animation|Children|Comedy|Fantasy','2000')==False)

print('pass test exists_in_movie_info() with some invalid input')

#TODO
#s2a
#a2s

#get_mid_from_imdbid() and get_mid_from_imdbid_batch()
#using get_movie_info()

m_id = d.get_all_movie_id()[:10]
check_batch = []

#get_mid_from_imdbid() part
for i in m_id:
	retval = d.get_movie_info(i)
	#movieid | name | genre | year | imdb | tag, (should be 6 values)
	mid = d.get_mid_from_imdbid(retval[4])
	check_batch.append(retval[4])
	assert mid == i
#get_mid_from_imdbid_batch() part
ret = d.get_mid_from_imdbid_batch(check_batch)
for n in range(len(m_id)):
	assert(m_id[n] == ret[n])
print('pass get_mid_from_imdbid and get_mid_from_imdbid_batch (check by get_movie_info)')



#get_imdbid_from_mid() and get_imdbid_from_mid_batch()
#using get_movie_info()
m_id = d.get_all_movie_id()[:10]
imdb_batch = []

#get_mid_from_imdbid() part
for i in m_id:
	retval = d.get_movie_info(i)
	#movieid | name | genre | year | imdb | tag, (should be 6 values)
	imdb = retval[4]
	ret = d.get_imdbid_from_mid(i)
	imdb_batch.append(int(imdb))
	assert int(imdb) == int(ret)
#get_mid_from_imdbid_batch() part
ret = d.get_imdbid_from_mid_batch(m_id)
for n in range(len(ret)):
	assert(imdb_batch[n] == int(ret[n]))
print('pass get_imdbid_from_mid and get_imdbid_from_mid_batch (check by get_movie_info)')

#TODO user_history
#TODO user_model

#test caller_id from get_identifier(u_id) will get back u_id in get_uid(caller_id)
i = 0 
count = 0 #id that can check
b_count = 0 #id that cannot check
while (count < 10) & (count + b_count < 25):
	i += 1
	caller_id = d.get_identifier(i)
	if (caller_id == -1) | (caller_id == None):
		b_count += 1
		continue
	ret = d.get_uid(caller_id)
	assert(int(ret) == int(i))
	count += 1

print('pass test caller_id from get_identifier(u_id) will get back u_id in get_uid(caller_id)')