import database_util
import datetime

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


test_uid = 1
test_m_id = 0
#create test movie
d.add_movie(0, 'test_movie001', 'aa|aa', 1234)
d.add_feature_to_movie(0, 0,'1.0|1.1')

#get_next_movie_id
m_id = d.get_all_movie_id()
new_id = d.get_new_movie_id()
assert(new_id not in m_id)
assert(new_id > m_id[-1])
print('pass get_new_movie_id retval not in existing m_id')	

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

#test add_movie cannot add movie name already in db


#get (0, 'test_movie001', 'aa|aa', 1234)
retval = d.get_movie_info(test_m_id)
d.add_movie(0, 'aaa', 'genre|genre2', 1221)
ret2 = d.get_movie_info(test_m_id)

assert(retval[0] == ret2[0])
assert(retval[1] == ret2[1])
assert(retval[2] == ret2[2])
assert(retval[3] == ret2[3])
print('pass test add_movie fail if m_id already exists')


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
#s2a to process tag
#a2s
m_id = d.get_all_movie_id()[:10]
for i in m_id:
	retval = d.get_movie_info(i)
	#tag
	tag = retval[5]
	#tag str will be modified, but should be consistent after that
	array1 = d.s2a(tag)
	str1 = d.a2s(array1)
	array2 = d.s2a(str1)
	str2 = d.a2s(array2)
	array3 = d.s2a(str2)
	str3 = d.a2s(array3)
	assert(str1 == str2)
	assert(str2 == str3)
print('pass s2a, a2s check')

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

#add_movie_by_imdbid
m_id = d.get_all_movie_id()
ret = d.get_imdbid_from_mid(m_id[-1])
assert(d.add_movie_by_imdbid(ret) == False)



#TODO user_history
#check user history update with m_id already in record will replace the record
history = d.get_user_history(test_uid)[0]
mid = history[1]
newRating = int(history[2]) + 1
if newRating > 5:
	newRating -= 5

time = str(datetime.datetime.now())
d.add_user_history(test_uid, mid, newRating, time)
	#check
history2 = d.get_user_history(test_uid)[0]
assert(test_uid == int(history2[0]))
assert(mid == int(history2[1]))
assert(newRating == int(history2[2]))
assert(time == history2[3])

#revert to original value
d.add_user_history(history[0], history[1], history[2], history[3])
print('pass check user history update w/ replace the record')

#TODO user_model
#temp save values before test
	#get first set of model
original_models = d.get_user_model(test_uid)[0]	

d.update_user_model(test_uid, '555','678')
modified = d.get_user_model(test_uid)[0]
assert(int(modified[0]) == test_uid)
assert(modified[1] == '555')
assert(modified[2] == '678')
d.add_user_model(test_uid, '599','610', 1.3)
modified = d.get_user_model(test_uid)[0]
assert(int(modified[0]) == test_uid)
assert(modified[1] == '599')
assert(modified[2] == '610')
assert(float(modified[3]) == 1.3)

#revert to original value
d.add_user_model(test_uid, original_models[1], original_models[2], original_models[3])
print('pass check user model update w/ replace the record')

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