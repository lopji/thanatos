def build_cnn(x, y, input_var=None):
	import lasagne

	print("test1")
	network = lasagne.layers.InputLayer(shape=(None, x[0], x[1], x[2]),
										input_var=input_var)
										
	convolution1 = lasagne.layers.Conv2DLayer(
			network, num_filters=30, filter_size=(2, 100),
			nonlinearity=lasagne.nonlinearities.rectify,
			W=lasagne.init.GlorotUniform())
										
	convolution2 = lasagne.layers.Conv2DLayer(
			network, num_filters=20, filter_size=(3, 100),
			nonlinearity=lasagne.nonlinearities.rectify,
			W=lasagne.init.GlorotUniform())
				
	convolution3 = lasagne.layers.Conv2DLayer(
			network, num_filters=15, filter_size=(4, 100),
			nonlinearity=lasagne.nonlinearities.rectify)

	print("test2")
	maxpool1 = lasagne.layers.MaxPool2DLayer(convolution1, pool_size=(2, 2))
	maxpool2 = lasagne.layers.MaxPool2DLayer(convolution2, pool_size=(2, 2))
	maxpool3 = lasagne.layers.MaxPool2DLayer(convolution3, pool_size=(2, 2))

	print("test3")
	network = lasagne.layers.MergeLayer((maxpool1, maxpool2, maxpool3))

	print("test4")
	network = lasagne.layers.DenseLayer(
			lasagne.layers.dropout(network, p=.5),
			num_units=y,
			nonlinearity=lasagne.nonlinearities.softmax)

	return network