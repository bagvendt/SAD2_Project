import sys
import pickle

sys.setrecursionlimit(50000)

USE_CACHE = False

if not USE_CACHE:
	import MySQLdb as mdb

SQL_GET_ACTORS_IN_MOVIES = """
SELECT A.id, M.id FROM actors as A 
	JOIN roles R
	ON R.`actor_id` = A.`id`
		JOIN movies M 
		ON M.`id` = R.`movie_id` """

def get_data():
	con = mdb.connect('127.0.0.1', 'root', '', 'imdb');
	cur = con.cursor()
	cur.execute(SQL_GET_ACTORS_IN_MOVIES)
	rows = cur.fetchall()

	actor_dict = {}

	for row in rows:
		actor_id = int(row[0])
		movie_id = int(row[1])

		if actor_id in actor_dict:
			movie_list = actor_dict[actor_id]
			movie_list.append(movie_id)
		else:
			movie_list = [movie_id]
		actor_dict[actor_id] = movie_list

	return actor_dict

def print_data(data):
	for key in data:
		val = data[key]
		to_print = str(key) + " "
		for movie_id in val:
			to_print += str(movie_id) + " "
		print to_print

if not USE_CACHE:
	data = get_data()
	with open('cached.pickle', 'wb') as handle:
		pickle.dump(data, handle)
else:
	with open('cached.pickle', 'rb') as handle:
		data = pickle.load(handle)

print_data(data)
