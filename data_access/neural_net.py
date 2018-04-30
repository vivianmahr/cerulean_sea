import numpy as np
import pickle
from decimal import Decimal

def sigmoid(x):
    return 1/(1+np.exp(-x, dtype=np.complex128))

def sigmoid_derivative(x):
    return sigmoid(x)*(1-sigmoid(x))

def random_weighted(d):
    items = sorted(d.items())
    for i in range(1, len(items)):
        items[i] = (items[i][0], items[i][1] + items[i-1][1])
    sum_values = sum(d.values())
    choice = sum_values * random.random()
    for item in items:
        if item[1] >= choice:
            return item[0]
    return item[-1][0]

class Neural_Net():
    def __init__(self, sizes, learning_rate):
        # How strong the corrections on each learning cycle is
        self.learning_rate = learning_rate
        
        # Dropout is how often? a neuron is ignored so the others try and step in to generalize
        # Unused as  of now
        self.dropout = 0
        
        # Generally, I'm not sure where I want this set to true but I know I'll want it at some point.
        self.use_learning_rate_decay = False 

        # Generate the matrices
        self.num_layers = len(sizes)
        self.sizes = sizes
        # Store all the biases for each layer
        self.biases = [np.random.randn(y, 1) for y in sizes[1:]]
        # Store all the weights between neurons
        self.weights = [(np.random.randn(y, x)) for x, y in zip(sizes[:-1], sizes[1:])]


        #UNUSED - CONCEPTS TO LOOK INTO
        # Dropout is how often? a neuron is ignored so the others try and step in to generalize
        # Unused as  of now
        self.dropout = 0
        
        # Generally, I'm not sure where I want this set to true but I know I'll want it at some point.
        self.use_learning_rate_decay = False 


    def feed_forward(self, data):
        for bias, weight in zip(self.biases, self.weights):
            data = sigmoid(np.dot(weight, data) + bias)
        return data

    def stochastic_gradient_descent_train(self, training_data, epochs, mini_batch_size, test_data=None):
        """Train the neural network using mini-batch stochastic
        gradient descent."""
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
                self.update_mini_batch(mini_batch)
            print("Epoch {} complete".format(ep))
            """
            if test_data:
                print("Epoch {} {} / {}".format(ep, self.evaluate(test_data), n_test))
            else:
                print("Epoch {} complete".format(ep))
            """
            
    def update_mini_batch(self, mini_batch):
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
        self.weights = [w - self.learning_rate/len(mini_batch) * nw for w, nw in zip(self.weights, nabla_w)]
        self.biases = [b - self.learning_rate/len(mini_batch) * nb for b, nb in zip(self.biases, nabla_b)]


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

    def evaluate(self, test_data, breaks):
        """Return percentage of correct result. Breaks = when there's
        multiple pieces of information in the output and you want to
        check each section individually.

        I think breaks should generally be replaced with a comparison function
        that determines how the end data should be read
        """
        test_results = [(np.argmax(self.feedforward(x)), y)
                        for (x, y) in test_data]
        return sum(int(x == y) for (x, y) in test_results)
		
    def cost_derivative(self, output_activations, y):
        """Return the vector of partial derivatives \partial C_x /
        \partial a for the output activations."""
        return (output_activations-y)

def save_net(net, name):
    with open(name + ".pickle", "wb") as out:
        pickle.dump(net, out)
    
def load_net(name):
    with open(name + ".pickle", "rb") as file:
        return pickle.load(file)




"""
if __name__=="__main__":
    #sample usage
    net = Neural_Net([3,5, 2], .3)

    training = [[0, 0, 1],
                [0, 1, 1],
                [1, 0, 1],
                [1, 1, 1]]
    answers = [[1, 0], [1, 0], [0, 1], [1, 0]]


    
    for i in range(len(training)):
        training[i] = np.reshape(training[i], (3, 1))
        answers[i] = np.reshape(answers[i], (2, 1))

    inp = [(x, y) for x, y in zip(training, answers)]
    net.stochastic_gradient_descent_train(inp, 1000, 2)

    print("---------------------------")
    for i in range(len(training)):
        print(net.feed_forward(training[i]))
    print(net.evaluate(inp))
"""
"""
    #sample usage
net = Neural_Net([3,5, 2], .3)

training = [[0, 0, 1],
            [0, 1, 1],
            [1, 0, 1],
            [1, 1, 1]]
answers = [[0, 1], [1, 0], [1, 1], [0, 0]]



for i in range(len(training)):
    training[i] = np.reshape(training[i], (3, 1))
    answers[i] = np.reshape(answers[i], (2, 1))

inp = [(x, y) for x, y in zip(training, answers)]
net.stochastic_gradient_descent_train(inp, 5000, 2)

print("---------------------------")
for i in range(len(training)):
    print(net.feed_forward(training[i]))
#print(net.evaluate(inp, []))
save_net(net, "test")


net = load_net("test")

training = [[0, 0, 1],
            [0, 1, 1],
            [1, 0, 1],
            [1, 1, 1]]

for i in range(len(training)):
    training[i] = np.reshape(training[i], (3, 1))

for i in range(len(training)):
    print(net.feed_forward(training[i])) 

"""