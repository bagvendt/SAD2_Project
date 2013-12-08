max_range = 845465

prime_1 = 845489.0
prime_2 = 845491.0

a_1 = 1258.0
b_1 = 8968.0

a_2 = 1176.0
b_2 = 759.0

def h_1(x):
	#print (a_1 * x + b_1) % prime_1
	return ((a_1 * x + b_1) % prime_1) / max_range

def h_2(y):
	return ((a_2 * y + b_2) % prime_2) / max_range

def h(x,y):
	return (h_1(x) - h_2(y)) % 1.0