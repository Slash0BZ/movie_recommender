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

print d.get_movie_info_batch(range(10))
print '====='
result = []
m_id = d.get_all_movie_id()[:10]
for i in m_id:
	result.append(tuple(d.get_movie_info(i)))
print result
