import mrlib

p = mrlib.Parser()
(movie, rating) = p.get_user_history(1)
print movie
print rating
print p.get_movie_genre_vector(89)
