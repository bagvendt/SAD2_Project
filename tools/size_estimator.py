import sys
import pickle

k = 200
#num_actors = 817718
#num_movies_with_actors = 300252
#num_movies_total = 388269
#res 2: 84546500.0004 (k: 200)
#res 3: 84546500.0 (k: 1000)
#res(k=500) = 105683125
#res(k=200) = 84545600
m = 845465 #largest item to be hashed

prime = 845491.0

a_1 = 1258.0
b_1 = 8968.0

a_2 = 1176.0
b_2 = 759.0

def h1(x):
    return (((a_1 * x + b_1) % prime) % m) / m


def h2(x):
    return (((a_2 * x + b_2) % prime) % m) / m


def h(x,y):
    val = (h1(x) - h2(y)) % 1.0
    return val


def sort_by_h1(Ai):
    return sorted(Ai, key=lambda x: h1(x))


def sort_by_h2(Ci):
    return sorted(Ci, key=lambda x: h1(x))

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
    F = set()
    S = set()
    B = movie_to_actor_index.keys()
    p = 0.7

    #algorithm
    pos = 0
    for i in B:
        pos += 1
        if pos % 10000 == 0:
            print "Doing B-loop: " + str(round(100 * pos / float(len(B)), 2)) + "%"
        Ai = movie_to_actor_index[i]
        Ci = movie_to_actor_index[i]
        x = sort_by_h1(Ai)
        y = sort_by_h2(Ci)
        s_bar = 0  # 0-indexes in python
        for t in range(0, len(Ci)):
            while h(x[s_bar], y[t]) > h(x[s_bar - 1], y[t]):
                s_bar = (s_bar + 1) % len(Ai)
            s = s_bar
            while h(x[s], y[t]) < p and s_bar != (s-1) % len(Ai):
                F.add((x[s], y[t]))
                if len(F) == k:
                    (p, S) = combine(S, F)
                    F.clear()
                s = (s + 1) % len(Ai)
    (p, S) = combine(S, F)
    if len(S) == k:
        return k / p
    else:
        return k**2


def combine(S, F):
    temp_list = list(S.union(F))
    temp_list = sorted(temp_list, key=lambda t: h(t[0], t[1]))

    #find the k smallest elements in S union F, set them to S and return S and the median element
    i = min(k-1, len(temp_list) - 1)
    x, y = temp_list[i]
    v = h(x, y)

    S = set(temp_list[0:k])

    print "Combined, new p=" + str(v)
    return v, S


actor_dict = get_actor_dict()
print len(actor_dict)
print "Done with the pickle"
index = build_movie_to_actor_index(actor_dict)
print len(index)
print "Done building actor index"

print dis_items(index)