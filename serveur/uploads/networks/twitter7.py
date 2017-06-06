def build_cnn(x, y, input_var=None):
	import lasagne
	
	network = lasagne.layers.InputLayer(shape=(None, x[0], x[1]),
										input_var=input_var)
	
	network = lasagne.layers.Conv1DLayer(
			network, num_filters=256, filter_size=3,
			nonlinearity=lasagne.nonlinearities.rectify,
			W=lasagne.init.GlorotUniform())
	
	network = lasagne.layers.Conv1DLayer(
		network, num_filters=128, filter_size=2,
		nonlinearity=lasagne.nonlinearities.rectify,
		W=lasagne.init.GlorotUniform())

	network = lasagne.layers.DenseLayer(
			lasagne.layers.dropout(network, p=.5),
			num_units=64,
			nonlinearity=lasagne.nonlinearities.rectify)

	network = lasagne.layers.DenseLayer(
			lasagne.layers.dropout(network, p=.5),
			num_units=y,
			nonlinearity=lasagne.nonlinearities.softmax)

	return network