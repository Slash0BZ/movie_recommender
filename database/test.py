import database_util

d = database_util.database()
d.add_user_history(1,14,5,123124)

print(d.get_user_history(1))

#user_model
d.update_user_model(1)
d.update_user_model(1, "b", "b")
d.update_user_model(1, "c", "b")