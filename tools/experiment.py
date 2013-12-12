import sys
import os

look_at = [621468, 372839, 74450, 212581, 152868, 22585,
           233082, 245158, 209799, 433904]

ground_truth = {}

ground_truth[621468] = 10834
ground_truth[372839] = 6679
ground_truth[74450] = 6447
ground_truth[212581] = 6318
ground_truth[152868] = 6027
ground_truth[22585] = 5957
ground_truth[233082] = 5894
ground_truth[245158] = 5775
ground_truth[209799] = 5773
ground_truth[433904] = 5764



def parse():
	a = {}
	for fname in os.listdir("./data1"):
		if ".DS" in fname:
			continue
		with open("./data1/" + fname) as f:	
			for line in f.read().splitlines():
				info = line.split()

				the_id = int(info[0])
				value = int(info[1])
				if the_id in a:
					a[the_id].append(value) 
				else:
					a[the_id] = [value]
	return a

def compute(data, ground_truth):
	ratios = {}
	for key in data:
		with open("./output1/" + str(key)+ "_256.dat", "w") as f:
			truth = ground_truth[key]
			ratios[key] = []
			for val in data[key]:
				ratio = val / float(truth)
				ratios[key].append(ratio)
			ratios[key].sort()
			m = len(ratios[key])
			for i in range(1, m):
				f.write(str(ratios[key][i-1]) + "\t" + str(i/float(m)) + "\r\n")

data = parse() 
#print data
compute(data, ground_truth)