import numpy as np 

def get_ui():
	fr = open('ratings_data.txt')
	u_dict = {}
	i_dict = {}
	# for line in fr.readlines()
	data = fr.readlines()
	fr.close()
	uir = []
	for line in data:
		line = line.strip()
		listfromline = line.split()
		uir.append(listfromline)
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

	flag = 0
	while flag == 0:
		flag = 1
		for user in list(u_dict.keys()):
			if len()


if __name__ == '__main__':
	main()