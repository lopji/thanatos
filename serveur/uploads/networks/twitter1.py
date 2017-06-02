def build_cnn(x, y, input_var=None):
	import lasagne
	
	network = lasagne.layers.InputLayer(shape=(None, x[0], x[1]),
										input_var=input_var)
	
	network = lasagne.layers.Conv1DLayer(
			network, num_filters=32, filter_size=3,
			nonlinearity=lasagne.nonlinearities.rectify,
			W=lasagne.init.GlorotUniform())
			
	network = lasagne.layers.MaxPool1DLayer(network, pool_size=2)

	network = lasagne.layers.DenseLayer(
			lasagne.layers.dropout(network, p=.5),
			num_units=16,
			nonlinearity=lasagne.nonlinearities.rectify)

	network = lasagne.layers.DenseLayer(
			lasagne.layers.dropout(network, p=.5),
			num_units=y,
			nonlinearity=lasagne.nonlinearities.softmax)

	return network