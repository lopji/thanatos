import urllib, json
import sys
import os
import time
import numpy as np
import theano
import theano.tensor as T
import lasagne
from urllib import urlretrieve
import zipfile

ip = "172.20.10.170"

def download(filename, source):
	urlretrieve(source + filename, filename)
	
def download_zip_file(filename, source):
	download(filename, source)	
	zip = zipfile.ZipFile(filename)
	zip.extractall()

def main():
	X_train, y_train, X_val, y_val = load_dataset()
		
	input_var = T.tensor3('inputs')
	target_var = T.ivector('targets')
		
	x = X_train.shape
	print(x)
	x = x[1:]
	y = np.bincount(y_train).size
	network = load_cnn(x, y, input_var)

	prediction = lasagne.layers.get_output(network)
	loss = lasagne.objectives.categorical_crossentropy(prediction, target_var)
	loss = loss.mean()

	params = lasagne.layers.get_all_params(network, trainable=True)
	updates = lasagne.updates.nesterov_momentum(
			loss, params, learning_rate=0.01, momentum=0.9)

	test_prediction = lasagne.layers.get_output(network, deterministic=True)
	test_loss = lasagne.objectives.categorical_crossentropy(test_prediction,
															target_var)
	test_loss = test_loss.mean()
	test_acc = T.mean(T.eq(T.argmax(test_prediction, axis=1), target_var),
					  dtype=theano.config.floatX)

	train_fn = theano.function([input_var, target_var], loss, updates=updates, allow_input_downcast=True)
	val_fn = theano.function([input_var, target_var], [test_loss, test_acc], allow_input_downcast=True)

	epoch = 0
	while True:
		# In each epoch, we do a full pass over the training data:
		train_err = 0
		train_batches = 0
		start_time = time.time()
		for batch in iterate_minibatches(X_train, y_train, 500, shuffle=True):
			inputs, targets = batch
			train_err += train_fn(inputs, targets)
			train_batches += 1

		# And a full pass over the validation data:
		val_err = 0
		val_acc = 0
		val_batches = 0
		for batch in iterate_minibatches(X_val, y_val, 500, shuffle=False):
			inputs, targets = batch
			err, acc = val_fn(inputs, targets)
			val_err += err
			val_acc += acc
			val_batches += 1

		epoch += 1
		print("test")
		np.savez('model.npz', *lasagne.layers.get_all_param_values(network))
		
def load_dataset():
	download_zip_file('twitter.zip', 'http://'+ ip +'/Symfony/web/upload/dataset/')
	X_train = np.array(json.loads(open('twitter/tx.json').read()))
	y_train = np.array(json.loads(open('twitter/ty.json').read()))
	X_val = np.array(json.loads(open('twitter/vx.json').read()))
	y_val = np.array(json.loads(open('twitter/vy.json').read()))
	return X_train, y_train, X_val, y_val

def load_cnn(x, y, input_var=None):
	print("1")
	download("twitter1.py", 'http://'+ ip +'/Symfony/web/upload/network/')
	script_locals = dict()
	execfile("twitter1.py", dict(), script_locals)
	network = script_locals["build_cnn"](x, y, input_var)
	print("2")
	download("save5.npz", 'http://' + ip + '/Symfony/web/upload/save/184/')
	print("3")
	loadedweights = np.load("save5.npz")
	lasagne.layers.set_all_param_values(network, loadedweights)
	return network

def iterate_minibatches(inputs, targets, batchsize, shuffle=False):
	assert len(inputs) == len(targets)
	if shuffle:
		indices = np.arange(len(inputs))
		np.random.shuffle(indices)
	for start_idx in range(0, len(inputs) - batchsize + 1, batchsize):
		if shuffle:
			excerpt = indices[start_idx:start_idx + batchsize]
		else:
			excerpt = slice(start_idx, start_idx + batchsize)
		yield inputs[excerpt], targets[excerpt]

if __name__ == '__main__':
	main()