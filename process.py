import pickle
import numpy as np 
import sys 
import os
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


	user2idx = {user:i for i,user in enumerate(u_dict.keys())}
	item2idx = {item:i for i,item in enumerate(i_dict.keys())}

	uir = []
	for record in uirs:
		user = record[0]
		item = record[1]
		rate = int(record[2])
		if user not in user2idx or item not in item2idx:
			continue
		uir.append([user2idx[user], item2idx[item], rate])

	data = {}
	data['uir'] = uir 
	data['num_user'] = len(user2idx)
	data['num_item'] = len(item2idx)


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

		nz_len = len(np.where(res!=0)[0])

		res = np.argsort(res)[::-1]
		sim_neighbors.append(res[:nz_len])


		# sim_neighbors.append(np.where(res!=0)[0])
		# sim_neighbors.append(res)
	# sim_neighbors = np.array(sim_neighbors)
	return sim_neighbors

def get_pair_neighbors(uir, sim_neighbors):
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
		item = idat[i]

		index = np.where(idat == item)[0]

		user = udat[i]
		users = udat[index]

		neighbors = sim_neighbors[user]

		sim_index = neighbors[users]


		sort_index = np.argsort(sim_index)[::-1] # sorted by similarity  index->user->sim_index

		if len(sort_index)<pad_num:
			temp = list(index[sort_index])+[i]*(pad_num-len(sort_index))
			pair_neighbors.append(temp)

		else:
			pair_neighbors.append(index[sort_index][:pad_num])

	return pair_neighbors









def get_neighbors():
	data = pickle.load(open('temp_data.pkl', 'rb'))

	num_user = data['num_user']
	num_item = data['num_item']
	uir = data['uir']

	mat = get_mat(data['uir'], num_user, num_item)


	if not os.path.exists('u_neighbors.pkl'):

		u_neighbors = get_sim_neighbors(mat)
		pickle.dump(u_neighbors, open('u_neighbors.pkl','wb'))
	else:
		u_neighbors = pickle.load(open('u_neighbors.pkl', 'wb'))


	pair_neighbors = get_pair_neighbors(uir, u_neighbors)

	data['pair_neighbors'] = pair_neighbors

	fr = open('data.pkl', 'wb')
	pickle.dump(data,fr)
	fr.close()





if __name__ == '__main__':
	get_ui()
	get_neighbors()