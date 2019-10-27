import pickle
import numpy as np 
import sys 
import os
from keras.preprocessing.sequence import pad_sequences
def get_ui():
	fr = open('ratings_data.txt')
	u_dict = {}
	i_dict = {}
	# for line in fr.readlines()
	data = fr.readlines()
	fr.close()
	uirs = []
	for line in data:
		line = line.strip()
		listfromline = line.split()
		uirs.append(listfromline)
		user = listfromline[0]
		item = listfromline[1]
		if user not in u_dict:
			u_dict[user] = [item]
		else:
			u_dict[user].append(item)
		if item not in i_dict:
			i_dict[item] = [user]
		else:
			i_dict[item].append(user)


	u_min = 5
	i_min = 5
	print(len(u_dict), len(i_dict))
	flag = 0
	while flag == 0:
		flag = 1
		for user in list(u_dict.keys()):
			if len(u_dict[user])<u_min:
				for item in u_dict[user]:
					i_dict[item].remove(user)
				del u_dict[user]
				flag = 0
		for item in list(i_dict.keys()):
			if len(i_dict[item])<i_min:
				for user in i_dict[item]:
					u_dict[user].remove(item)
				del i_dict[item]
				flag = 0


	user2idx = {user:i+1 for i,user in enumerate(u_dict.keys())}
	item2idx = {item:i+1 for i,item in enumerate(i_dict.keys())}

	uir = [[0,0,0]]
	for record in uirs:
		user = record[0]
		item = record[1]
		rate = int(record[2])
		if user not in user2idx or item not in item2idx:
			continue
		uir.append([user2idx[user], item2idx[item], rate])

	if not os.path.exists('pmtt.npy'):
		pmtt = np.random.permutation(len(uir)-1)+1
		pmtt = np.array([0]+list(pmtt))
		np.save('pmtt', pmtt)

	else:
		pmtt = np.load('pmtt.npy')

	uir = np.array(uir)[pmtt]
	data = {}
	data['uir'] = uir 
	data['num_user'] = len(user2idx)+1
	data['num_item'] = len(item2idx)+1


	print(len(uir), len(user2idx), len(item2idx))
	fr = open('temp_data.pkl', 'wb')
	pickle.dump(data, fr)
	fr.close()

def get_mat(uir, num_user, num_item):
	uir = np.array(uir)
	mat = np.zeros((num_user, num_item))
	for record in uir:
		user = record[0]
		item = record[1]
		rate = record[2]
		mat[user,item] = rate
	return mat 

def get_sim_neighbors(mat):
	rows, cols = mat.shape
	sim_neighbors = []
	for i in range(rows):
		sys.stdout.write('\r{}/{}'.format(i,rows))
		vec = mat[i]
		nz_index = np.where(vec!=0)[0]
		vec = vec[vec!=0]
		vecs = mat[:,nz_index]

		commo_vec = (vec*vecs!=0).astype(int)
		equal_vec = (vec==vecs).astype(int)

		coeq_vote = np.sum(commo_vec*equal_vec, axis=1)
		comm_vote = np.sum(commo_vec, axis=1)

		norm = np.sqrt(comm_vote)
		norm = np.maximum(norm, 1)
		res = coeq_vote/norm 


		# res = sorted(res)[::-1]

		nz_index = np.where(res!=0)[0]

		# res = res[nz_index]
		# sort_index = np.argsort(res)[::-1]
		# nz_index = nz_index[sort_index]





		# sim_neighbors.append(res[:nz_len])
		sim_neighbors.append(nz_index)


		# sim_neighbors.append(np.where(res!=0)[0])
		# sim_neighbors.append(res)
	# sim_neighbors = np.array(sim_neighbors)
	lens = [len(item) for item in sim_neighbors]
	print('sim 90 percentile: ', np.percentile(lens,90))
	maxlen = int(np.percentile(lens, 90))
	sim_neighbors = pad_sequences(sim_neighbors, maxlen)

	return sim_neighbors

def get_pair_neighbors(uir, u_neighbors):
	uir = np.array(uir)

	udat = uir[:,0]
	idat = uir[:,1]
	length = len(udat)
	pair_neighbors = []

	pad_num = 20
	for i in range(length):
		# r1,r2,r = record
		sys.stdout.write('\r{}/{}'.format(i,length))
		sys.stdout.flush()
		# item = idat[i]

		index = np.where(idat == idat[i])[0]
		# print(index)

		user = udat[i]
		users = udat[index]

		sims = u_neighbors[user]

		temp = []


		for user,idx in zip(users,index):
			if user in sims:
				temp.append(idx)





		pair_neighbors.append(temp)

		if i==10:
			break

	lens = [len(item) for item in pair_neighbors]
	maxlen = np.round(np.percentile(lens,90))

	print('\n',pair_neighbors[-1])
	pair_neighbors = pad_sequences(pair_neighbors, maxlen = int(maxlen))

	return pair_neighbors









def get_neighbors():
	if not os.path.exists('temp_data.pkl'):
		get_ui()
	
	data = pickle.load(open('temp_data.pkl', 'rb'))

	num_user = data['num_user']
	num_item = data['num_item']
	uir = data['uir']
	print(uir.shape)

	mat = get_mat(data['uir'], num_user, num_item)


	if not os.path.exists('u_neighbors.pkl'):

		u_neighbors = get_sim_neighbors(mat)
		pickle.dump(u_neighbors, open('u_neighbors.pkl','wb'))
		# np.savetxt('u_neighbors.txt', u_neighbors, fmt='%d')
	else:
		u_neighbors = pickle.load(open('u_neighbors.pkl', 'rb'))
		# u_neighbors = np.genfromtxt('u_neighbors.txt', dtype=int)


	pair_neighbors = get_pair_neighbors(uir, u_neighbors)

	data['pair_neighbors'] = pair_neighbors

	fr = open('data.pkl', 'wb')
	pickle.dump(data,fr)
	fr.close()





if __name__ == '__main__':
	# get_ui()
	get_neighbors()