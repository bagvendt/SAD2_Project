import sys
import pickle

def get_actor_dict():
	#actor->list of movies
	with open('../projections/cached.pickle', 'rb') as handle:
		return pickle.load(handle)

def build_movie_to_actor_index(actor_dict):
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

def dis_items(movie_to_actor_index):
	#setup
	k = 30
	F = {}
	B = movie_to_actor_index.keys()
	p = 1
	
	#algorithm
	for i in B:
		Ai = movie_to_actor_index[i]
		Ci = movie_to_actor_index[i]
		x = sort_by_h1(Ai)
		y = sort_by_h2(Ci)
		s_bar = 0 #0-indexes in python
		for t in range(0, len(Ci)):
			while h(x[s_bar], y[t]) > h(x[s_bar - 1], y[t]):
				s_bar = (s_bar + 1) % len(Ai)
			s = s_bar
			while h(x[s], y[t]) < p:
				F[(x[s], y[t])] = True
				if len(F) == k:
					(p, S) = combine(S, F)
					F = {}
				s = (s + 1) % len(Ai)
	(p, S) = combine(S, F)
	if len(S) == k:
		return k / p
	else:
		return k^2

def combine(S, F):
	#find the k smallest elements in S union F, set them to S and return S and the median element
	return (1, F)

def h(x, y):
	return 0.5

def h1(x):
	return 0.4

def h2(x):
	return 0.3

def sort_by_h1(Ai):
	return Ai

def sort_by_h2(Ci):
	return Ci

actor_dict = get_actor_dict()
index = build_movie_to_actor_index(actor_dict)

print dis_items(index)