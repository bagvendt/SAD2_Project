import sys
import pickle
import random

k = 1024
#num_actors = 817718
#num_movies_with_actors = 300252
#num_movies_total = 388269
#res 2: 84546500.0004 (k: 200)
#res 3: 84546500.0 (k: 1000)
#res(k=500) = 105683125
#res(k=200) = 84545600

look_at = [621468, 372839, 74450, 212581, 152868, 22585, 233082, 245158, 209799, 433904] # Top 10 film_count actors

m = 845465  #largest item to be hashed

prime = 845491.0

#a_1 = 1258.0
a_1 = random.random() * 10000
#b_1 = 8968.0
b_1 = random.random() * 10000
print "a_1,b_1", a_1, b_1
#a_2 = 1176.0
a_2 = random.random() * 10000
#b_2 = 759.0
b_2 = random.random() * 10000
print "a_2,b_2",a_2,b_2

def h1(x):
    return (((a_1 * x + b_1) % prime) % 621468) / 621468  # Highest id by Bess


def h2(x):
    return (((a_2 * x + b_2) % prime) % m) / m


def h(x,y):
    val = (h1(x) - h2(y)) % 1.0
    if h1(x) > 1.0 or h2(y) > 1.0:
        print "ALARM", h1(x), h2(y)
        exit()
    return val


def sort_by_h1(Ai):
    return sorted(Ai, key=lambda x: h1(x))


def sort_by_h2(Ci):
    return sorted(Ci, key=lambda x: h2(x))

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
    count_temp = 0
    B = movie_to_actor_index.keys()
    p_init = 1
    p_max = p_init

    buffer_dict = {}
    for key in look_at:
        buffer_dict[key] = (set(), set(), p_init)

    #algorithm
    pos = 0
    for i in B:
        pos += 1
        # if pos % 10000 == 0:
        #     print "Doing B-loop: " + str(round(100 * pos / float(len(B)), 2)) + "%"
        Ai = list(set(look_at).intersection(set(movie_to_actor_index[i])))
        if len(Ai) == 0:
            continue

        Ci = movie_to_actor_index[i]

        x = sort_by_h1(Ai)
        y = sort_by_h2(Ci)
        s_bar = 0  # 0-indexes in python
        for t in range(0, len(Ci)):
            while h(x[s_bar], y[t]) > h(x[s_bar - 1], y[t]):
                s_bar = (s_bar + 1) % len(Ai)
            s = s_bar
            first = True
            while h(x[s], y[t]) < p_max and (s_bar != s or first):
                first = False
                (S, F, p) = buffer_dict[x[s]] 
                if h(x[s], y[t]) < p:
                    F.add((x[s], y[t]))
                    if x[s] == 621468:
                        count_temp += 1
                    if len(F) == k:
                        (p, S) = combine(S, F)
                        buffer_dict[x[s]] = (S, set(), p)
                        p_max = find_p_max(buffer_dict)
                s = (s + 1) % len(Ai)
    combine_all(buffer_dict)

    print "Bess Flowers F.add", count_temp
    #(p, S) = combine(S, F)
    for key in buffer_dict:
        (S, F, p) = buffer_dict[key]
        if len(S) == k:
            print key, k/p
        else:
            print key, k**2


def combine(S, F):
    temp_list = list(S.union(F))
    temp_list = sorted(temp_list, key=lambda t: h(t[0], t[1]))

    #find the k smallest elements in S union F, set them to S and return S and the median element
    i = min(k-1, len(temp_list) - 1)
    x, y = temp_list[i]
    v = h(x, y)

    S = set(temp_list[0:k])

    #print "Combined, new p=" + str(v)
    return v, S

def find_p_max(buffer_dict):
    p_max = 1
    for key in buffer_dict:
        (S, F, p) = buffer_dict[key]
        if p > p_max:
            p_max = p
    return p_max 

def combine_all(buffer_dict):
    for key in buffer_dict:
        (S, F, p) = buffer_dict[key]
        if len(S) + len(F) > 0:
            (p, S) = combine(S, F)
            buffer_dict[key] = (S, set(), p)



actor_dict = get_actor_dict()
print len(actor_dict)
print "Done with the pickle"
index = build_movie_to_actor_index(actor_dict)
print len(index)
print "Done building actor index"

dis_items(index)