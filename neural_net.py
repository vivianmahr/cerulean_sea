import numpy as np
import pickle

import numpy as np
def sigmoid(x):
    return 1/(1+np.exp(-x))

def sigmoid_derivative(x):
    return sigmoid(x)*(1-sigmoid(x))

# This is going to be a disaster pile of notes until I figure things out better
# Heavily based on http://neuralnetworksanddeeplearning.com/
    
class Neural_Net():
    def __init__(self, sizes):
        # Numbers that influence how things learn
        # How strong the corrections on each learning cycle is
        self.learning_rate = 0
        # Some kind of regulization variable
        self.l2_factor = 0
        # Dropout is how often? a neuron is ignored so the others try and step in to generalize
        self.dropout = 0
        # Generally, I'm not sure where I want this set to true...
        self.use_learning_rate_decay = False 

        # Generate the matrices
        self.num_layers = len(sizes)
        self.sizes = sizes
        # layer 0 is input so there's no biases stored for that layer
        self.biases = [np.random.randn(y, 1) for y in sizes[1:]]
        # way of putting all the links between the neurons
        self.weights = [(np.random.randn(y, x)) for x, y in zip(sizes[:-1], sizes[1:])]

    def feed_forward(self, data):   
        for bias, weight in zip(self.biases, self.weights):
            data = sigmoid(np.dot(weight, data) + bias)
        return data

    def stochastic_gradient_descent_train(self, training_data, epochs, mini_batch_size, eta, test_data=None):
        """Train the neural network using mini-batch stochastic
        gradient descent."""
        # eta = learning rate
        # If there is test data, also test it each epoch and report back on how accurate it is
        if test_data: 
            n_test = len(test_data)
        n = len(training_data)
        for ep in range(epochs):
            np.random.shuffle(training_data) 
            # divide up the shuffled training data into mini batches of size mini_batch_size
            mini_batches = [
                training_data[k:k+mini_batch_size] for k in range(0, n, mini_batch_size)
            ]
            for mini_batch in mini_batches:
                self.update_mini_batch(mini_batch, eta)
            if test_data:
                print("Epoch {} {} / {}".format(ep, self.evaluate(test_data), n_test))
            else:
                print("Epoch {} complete".format(ep))
  
    def update_mini_batch(self, mini_batch, eta):
        """Update the network's weights and biases by applying
        gradient descent using backpropagation to a single mini batch.
        The "mini_batch" is a list of tuples "(x, y)", and "eta"
        is the learning rate."""

        # nabla looks like delta upside down. for current notes, used as symbol for gradient vector
        # get the shape of the biases and weights, zero them out
        nabla_b = [np.zeros(b.shape) for b in self.biases]
        nabla_w = [np.zeros(w.shape) for w in self.weights]

        # for input, expected_output in minibatch:
        for x, y in mini_batch: 
            # get the change in gradient for biases and weights
            delta_nabla_b, delta_nabla_w = self.backprop(x, y)
            # add the nabla with the expected change in gradient 
            nabla_b = [nb + dnb for nb, dnb in zip(nabla_b, delta_nabla_b)]
            nabla_w = [nw + dnw for nw, dnw in zip(nabla_w, delta_nabla_w)]
        # update weights and bias where weight = old_weight - learning_rate / len(batch) * gradient_weight
        self.weights = [w - eta/len(mini_batch) * nw for w, nw in zip(self.weights, nabla_w)]
        self.biases = [b - eta/len(mini_batch) * nb for b, nb in zip(self.biases, nabla_b)]


    def backprop(self, x, y):
        """Return a tuple ``(nabla_b, nabla_w)`` representing the
        gradient for the cost function C_x.  ``nabla_b`` and
        ``nabla_w`` are layer-by-layer lists of numpy arrays, similar
        to ``self.biases`` and ``self.weights``."""
        nabla_b = [np.zeros(b.shape) for b in self.biases]
        nabla_w = [np.zeros(w.shape) for w in self.weights]
        # feedforward
        activation = x
        activations = [x] # list to store all the activations, layer by layer
        zs = [] # list to store all the z vectors, layer by layer
        for b, w in zip(self.biases, self.weights):
            z = np.dot(w, activation)+b
            zs.append(z)
            activation = sigmoid(z)
            activations.append(activation)
        # backward pass
        delta = self.cost_derivative(activations[-1], y) *sigmoid_derivative(zs[-1])
        nabla_b[-1] = delta
        nabla_w[-1] = np.dot(delta, activations[-2].transpose())

        for l in range(2, self.num_layers):
            z = zs[-l]
            sp = sigmoid_derivative(z)
            delta = np.dot(self.weights[-l+1].transpose(), delta) * sp
            nabla_b[-l] = delta
            nabla_w[-l] = np.dot(delta, activations[-l-1].transpose())
        return (nabla_b, nabla_w)

    def evaluate(self, test_data):
        """Return the number of test inputs for which the neural
        network outputs the correct result. Note that the neural
        network's output is assumed to be the index of whichever
        neuron in the final layer has the highest activation."""
        test_results = [(np.argmax(self.feedforward(x)), y)
                        for (x, y) in test_data]
        return sum(int(x == y) for (x, y) in test_results)

    def cost_derivative(self, output_activations, y):
        """Return the vector of partial derivatives \partial C_x /
        \partial a for the output activations."""
        return (output_activations-y)

    def save_net(self):
        pass
    
    def load_net(self):
        pass

if __name__=="__main__":
    #sample usage
    net = Neural_Net([3,3, 2])

    training = [[0, 0, 1],
                [0, 1, 1],
                [1, 0, 1],
                [1, 1, 1]]
    answers = [[1, 0], [1, 0], [0, 1], [0, 1]]

    for i in range(len(training)):
        training[i] = np.reshape(training[i], (3, 1))
        answers[i] = np.reshape(answers[i], (2, 1))

    inp = [(x, y) for x, y in zip(training, answers)]

    print(inp)
    net.stochastic_gradient_descent_train(inp, 1000, 2,.3)

    print("---------------------------")
    print(net.feed_forward(training[0]))
    print(net.weights)
#Notes for self and for implementing saving later
"""
import pickle

example_dict = {1:"6",2:"2",3:"f"}

pickle_out = open("dict.pickle","wb")
pickle.dump(example_dict, pickle_out)
pickle_out.close()

pickle_in = open("dict.pickle","rb")
example_dict = pickle.load(pickle_in)

print(example_dict)
print(example_dict[3])
"""
