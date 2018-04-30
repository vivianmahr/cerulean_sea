from actions.text_processing.token_taggers import token
from data_access import text_fetcher, neural_net
import numpy as np

class Tagger():
	def __init__(self):
		self.net = neural_net.load_net("./data_access/nets/POS")
		
	def __call__(self, items, fetcher):
		result = []
		for toke in items:
			inp = toke.to_nn_input()
			output = list(self.net.feed_forward(inp))
			toke.pos = token.POS_LIST[output.index(max(output))]
			result.append(toke)
		return result
	

def _load_training_file(filename):
	data = []
	fetcher = text_fetcher.Text_Fetcher()
	with open(filename)as file:
		info = file.read()
		for line in info.split("\n"):
			inputs = line.split("\t")
			if len(inputs) == 3:
				w = token.Token(inputs[0].strip(), fetcher, inputs[1].strip())
				w_input = w.to_nn_input()
				w_answer_arr = np.zeros(len(token.POS_LIST))
				w_answer_arr[w._pos_to_int(inputs[2].strip())] = 1
				w_answer_arr = np.reshape(w_answer_arr, (len(w_answer_arr), 1))
				data.append((w_input, w_answer_arr))
	return data

def train_tagger(data, output, sizes=[token.Token.nn_length, 100, 56, 18], decay=.1):
	data = _load_training_file("./data_access/nets/training_data/" + data)
	net = neural_net.Neural_Net(sizes, decay)
#	net.stochastic_gradient_descent_train(data, 1, 200)
	net.stochastic_gradient_descent_train(data, 750, 200)
	neural_net.save_net(net, "./data_access/nets/" + output)
	
#train_tagger("output-pos-1.txt", "POS2")
	