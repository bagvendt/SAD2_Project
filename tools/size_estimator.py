import sys
import pickle

k = 30

max_range = 845465

prime_1 = 845489.0
prime_2 = 845491.0

a_1 = 1258.0
b_1 = 8968.0

a_2 = 1176.0
b_2 = 759.0

def h1(x):
    return ((a_1 * x + b_1) % prime_1) / max_range


def h2(x):
    return ((a_2 * x + b_2) % prime_2) / max_range


def h(x,y):
    return (h1(x) - h2(y)) % 1.0


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
    p = 0.5

    #algorithm
    for i in B:
        print "Started interation i of the B-loop: " + str(i)
        Ai = movie_to_actor_index[i]
        Ci = movie_to_actor_index[i]
        x = sort_by_h1(Ai)
        y = sort_by_h2(Ci)
        s_bar = 0 #0-indexes in python
        for t in range(0, len(Ci)):
            print "Started interation of Ci: " + str(t)
            while h(x[s_bar], y[t]) > h(x[s_bar - 1], y[t]):
                s_bar = (s_bar + 1) % len(Ai)
            s = s_bar
            print "Done finding modulus pivot point - starting to check for p"
            while h(x[s], y[t]) < p:
                print 1
                F.add((x[s], y[t]))
                print 2
                if len(F) == k:
                    print 3
                    (p, S) = combine(S, F)
                    print 4
                    F.clear()
                    print 5
                s = (s + 1) % len(Ai)
            print "Done checking for p - moving on"
    (p, S) = combine(S, F)
    if len(S) == k:
        return k / p
    else:
        return k**2


def combine(S, F):
    temp_list = list(S.union(F))
    temp_list = sorted(temp_list, key=lambda t: h(t[0], t[1]))

    #find the k smallest elements in S union F, set them to S and return S and the median element

    x, y = temp_list[min(k-1, len(temp_list))]
    v = h(x, y)

    S = set(temp_list[0:k-1])
    print "Combine", v, S
    return v, S


actor_dict = get_actor_dict()
print "Done with the pickle"
index = build_movie_to_actor_index(actor_dict)
print "Done building actor index"

print dis_items(index)