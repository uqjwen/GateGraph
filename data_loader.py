import pickle
import numpy as np 
import tensorflow as tf 
from keras.preprocessing.sequence import pad_sequences
class Data_Loader():
	def __init__(self, flags):
		data = pickle.load(open('data.pkl', 'rb'))
		self.num_user = data['num_user']
		self.num_item = data['num_item']
		self.uir = np.array(data['uir'])

		self.data_size = len(self.uir)

		self.pair_neighbors = data['pair_neighbors']

		self.u_neighbors = np.genfromtxt('u_neighbors.txt', dtype=int)

		self.batch_size = flags.batch_size

		self.rate = flags.rate
		self.pointer = 0

	def split(self):

		self.train_size = int(self.data_size*rate)
		self.test_size = int(self.data_size*0.1)

		# self.train_u = self.uir[:self.train_size][:,0]
		# self.train_i = self.uir[:self.train_size][:,1]
		# self.train_r = self.uir[:self.train_size][:,2]
		self.train_uir = self.uir[:self.train_size]



	def __next__(self):
		begin = self.pointer*self.batch_size
		end = (self.pointer+1)*self.batch_size
		if end>self.train_size:
			end = self.train_size
			self.pointer = 0
		else:
			self.pointer += 1

		pair_user,pair_item, pair_rate = self.get_pair_neighbors(range(begin,end))


		return self.train_uir[begin:end][:,0],\
				self.train_uir[begin:end][:,1],\
				self.train_uir[begin:end][:,2]
	def get_pair_neighbors(self, index):
		sub_dat = self.uir[index]
		pair_user = sub_dat[:,0]
		pair_item = sub_dat[:,1]
		pair_rate = sub_dat[:,2]
		return pair_usr, pair_item, pair_rate
		# res = []
		# for item_pair, user_pair in zip(item_pairs, user_pairs):
		# 	res.append(np.intersect1d(item_pair, user_pair))
		# res = pad_sequences(res)
		# return res




if __name__ == '__main__':
	flags = tf.flags.FLAGS 	
	tf.flags.DEFINE_string('filename',filename,'name of file')
	tf.flags.DEFINE_integer('batch_size',4,'batch size')
	tf.flags.DEFINE_integer('emb_size',100, 'embedding size')
	tf.flags.DEFINE_float('rate', 0.8, 'rate of train')
	# tf.flags.DEFINE_string('base_model', 'att_cnn', 'base model')
	flags(sys.argv)

	data_loader = Data_Loader(flags)
	