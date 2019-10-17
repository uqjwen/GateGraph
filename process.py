import pickle
import numpy as np 

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
		rate = record[2]
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


if __name__ == '__main__':
	get_ui()