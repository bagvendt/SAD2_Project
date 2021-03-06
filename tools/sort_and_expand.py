import pickle

USE_CACHE = True

if not USE_CACHE:
	import MySQLdb as mdb

SQL_GET_ACTOR_NAMES = """SELECT id,first_name, last_name FROM actors"""

def get_actor_names_from_db():
	con = mdb.connect('127.0.0.1', 'root', '', 'imdb');
	cur = con.cursor()
	cur.execute(SQL_GET_ACTOR_NAMES)
	rows = cur.fetchall()
	names = {}
	for row in rows:
		actor_id = int(row[0])
		first_name = str(row[1])
		last_name = str(row[2])
		names[actor_id] = first_name + " " + last_name
	return names

def read_output(location):
	data = []
	with open(location, 'r') as f:
		read_data = f.read().splitlines()
		for line in read_data:
			split = line.split("\t")
			actor_id = int(split[0])
			count = int(split[1])
			val = (actor_id, count)
			data.append(val)
	return data

def expand_with_actor_names(sorted_list, names):
	new_list = []
	for val in sorted_list:
		actor_id, count = val
		actor_name = names[actor_id]
		new_val = (actor_id, actor_name, count)
		new_list.append(new_val)
	return new_list

if not USE_CACHE:
	actor_names = get_actor_names_from_db()
	with open('cached.pickle', 'wb') as handle:
		pickle.dump(actor_names, handle)
else:
	with open('cached.pickle', 'rb') as handle:
		actor_names = pickle.load(handle)


#data = read_output("../data/Actor-Number.out")
data = read_output("../data/sequential_output.out")
#print len(data)


data = expand_with_actor_names(data, actor_names)
result = sorted(data,key=lambda x: (x[2], -x[0]))

for val in result:
	print val