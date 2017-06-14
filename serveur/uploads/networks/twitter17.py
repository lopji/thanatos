def build_cnn(x, y, input_var=None):
	import lasagne
	
	network = lasagne.layers.InputLayer(shape=(None, x[0], x[1], x[2]),
										input_var=input_var)
										
	convolution1 = lasagne.layers.Conv2DLayer(
			network, num_filters=30, filter_size=(2, x[2]),
			nonlinearity=lasagne.nonlinearities.rectify,
			W=lasagne.init.GlorotUniform())
										
	convolution2 = lasagne.layers.Conv2DLayer(
			network, num_filters=20, filter_size=(3, x[2]),
			nonlinearity=lasagne.nonlinearities.rectify,
			W=lasagne.init.GlorotUniform())
				
	convolution3 = lasagne.layers.Conv2DLayer(
			network, num_filters=30, filter_size=(4, x[2]),
			nonlinearity=lasagne.nonlinearities.rectify,
			W=lasagne.init.GlorotUniform())	
			
	convolution4 = lasagne.layers.Conv2DLayer(
			network, num_filters=24, filter_size=(5, x[2]),
			nonlinearity=lasagne.nonlinearities.rectify,
			W=lasagne.init.GlorotUniform())	
			
	map1 = lasagne.layers.reshape(convolution1, ([0], [1], [2]))
	map2 = lasagne.layers.reshape(convolution2, ([0], [1], [2]))
	map3 = lasagne.layers.reshape(convolution3, ([0], [1], [2]))
	map4 = lasagne.layers.reshape(convolution4, ([0], [1], [2]))

	maxpool1 = lasagne.layers.MaxPool1DLayer(map1, pool_size=(map1.output_shape[2]))
	maxpool2 = lasagne.layers.MaxPool1DLayer(map2, pool_size=(map2.output_shape[2]))
	maxpool3 = lasagne.layers.MaxPool1DLayer(map3, pool_size=(map3.output_shape[2]))
	maxpool4 = lasagne.layers.MaxPool1DLayer(map4, pool_size=(map4.output_shape[2]))

	network = lasagne.layers.ConcatLayer((maxpool1, maxpool2, maxpool3, maxpool4))
			
	network = lasagne.layers.DenseLayer(
			lasagne.layers.dropout(network, p=.5),
			num_units=y,
			nonlinearity=lasagne.nonlinearities.softmax)

	return network