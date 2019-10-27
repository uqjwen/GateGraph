import numpy as np 
import pickle
import sys
import collections


def rating_per_ui():
	temp_dat = pickle.load(open('temp_data.pkl','rb'))
	uir = temp_dat['uir']
	num_user = temp_dat['num_user']
	num_item = temp_dat['num_item']

	u_ratings = []
	i_ratings = []
	# print(type(uir))
	uir = np.array(uir)
	# for i in range(num_user):
	# 	sys.stdout.write('\r{}/{}'.format(i,num_user))
	# 	u_ratings.append(len(np.where(uir[:,0] == i)[0]))
	# print(np.mean(u_ratings))

	for j in range(num_item):
		sys.stdout.write('\r{}/{}'.format(j,num_item))
		i_ratings.append(len(np.where(uir[:,1] == j)[0]))

	print('\n',np.mean(i_ratings))

	print('percentile:', np.percentile(i_ratings, 90))

	counter = collections.Counter(i_ratings)
	sort_counter = np.array(sorted(counter.items(), key = lambda x:x[0]))
	lens,counts = sort_counter[:,0], sort_counter[:,1]

	for length, ratio in zip(lens, np.cumsum(counts)/np.sum(counts)):
		print(length, ratio)






if __name__ == '__main__':
	rating_per_ui()