import sys
import pickle

def get_actor_dict():
	#actor->list of movies
	with open('../projections/cached.pickle', 'rb') as handle:
		return pickle.load(handle)

def build_reverse_index(actor_dict):
	#movie->list of actors
	#create the "who played in this movie index"
	movie_dict = {}
	for actor_id in actor_dict:
		movies = actor_dict[actor_id]
		for movie_id in movies:
			if (not movie_id in movie_dict):
				movie_dict[movie_id] = []
			movie_dict[movie_id].append(actor_id)
	return movie_dict

def count_co_actors_for_actor(actor_id, actor_dict, movie_dict):
	movies = actor_dict[actor_id]
	co_actors = {}
	for movie in movies:
		for actor in movie_dict[movie]:
			if actor != actor_id: #playing in a movie with yourself doesn't count
				co_actors[actor] = 1 #set bool flag to signal that actor played with co_actor
	return len(co_actors)

def build_output_list(actor_dict, movie_dict):
	output_list = []
	for actor_id in actor_dict:
		count = count_co_actors_for_actor(actor_id, actor_dict, movie_dict)
		if count > 0: #discard actors with zero count
			output_list.append(str(actor_id) + "\t" + str(count))
	return output_list

def do_print(output_list):
	for line in output_list:
		print(line)

actor_dict = get_actor_dict()
movie_dict = build_reverse_index(actor_dict)
do_print(build_output_list(actor_dict, movie_dict))