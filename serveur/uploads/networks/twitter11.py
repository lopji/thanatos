def build_cnn(x, y, input_var=None):
	import lasagne
	
	network = lasagne.layers.InputLayer(shape=(None, x[0], x[1], x[2]),
										input_var=input_var)
										
	network = lasagne.layers.Conv2DLayer(
			network, num_filters=32, filter_size=(3, 3),
			nonlinearity=lasagne.nonlinearities.rectify,
			W=lasagne.init.GlorotUniform())
			
	network = lasagne.layers.MaxPool2DLayer(network, pool_size=(2, 2))
	
	network = lasagne.layers.Conv2DLayer(
			network, num_filters=32, filter_size=(2, 2),
			nonlinearity=lasagne.nonlinearities.rectify)
	network = lasagne.layers.MaxPool2DLayer(network, pool_size=(2, 2))
	
	network = lasagne.layers.DenseLayer(
			lasagne.layers.dropout(network, p=.5),
			num_units=256,
			nonlinearity=lasagne.nonlinearities.rectify)
			
	network = lasagne.layers.DenseLayer(
			lasagne.layers.dropout(network, p=.5),
			num_units=y,
			nonlinearity=lasagne.nonlinearities.softmax)

	return network