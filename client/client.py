from socketIO_client import SocketIO, BaseNamespace
import socket
from threading import Thread
import urllib, json
import sys
import os
import time
import numpy as np
import theano
import theano.tensor as T
import lasagne
import requests
import zipfile

ip = "129.194.184.108"
port = 8080

def download(filename, source):
	r = requests.get(source + filename, stream=True)
	with open(filename, 'wb') as f:
		for chunk in r.iter_content(chunk_size=1024): 
			if chunk: 
				f.write(chunk)
	
def download_zip_file(filename, source):
	download(filename, source)	
	zip = zipfile.ZipFile(filename)
	zip.extractall()

class Error(Exception):
	pass

class ComputerNamespace(BaseNamespace):

	def __init__(self, arg1, arg2):
		BaseNamespace.__init__(self, arg1, arg2)
		self.status = 0
		self.error = 0
		self.state = 0
		self.instance = None

	def data(self):
		self.emit('data', {'name' : socket.gethostname(), 'status' : self.status, 'error' : self.error, 'state' : self.state})
		
	def setStatus(self, status):
		self.status = status
		self.data()
		
	def setError(self, error):
		self.error = error
		self.data()

	def setState(self, state):
		self.state = state
		self.data()

	def on_connect(self):
		print('[Connected]')
		self.data()

	def on_reconnect(self):
		print('[Reconnected]')
		self.data()

	def on_disconnect(self):
		print('[Disconnected]')
		
	def on_resume(self, *args):
		print('on_resume')
		if args[0]['name'] == socket.gethostname():
			if self.state == 3:
				self.setStatus(3)
				self.setState(1)
		
	def on_break(self, *args):
		print('on_break')
		if args[0]['name'] == socket.gethostname():
			if self.state == 1:
				self.setStatus(6)
				self.setState(3)
		
	def on_stop(self, *args):
		print('on_stop')
		if args[0]['name'] == socket.gethostname():
			if self.state != 0:
				self.setStatus(4)
				self.setState(4)
				
	def on_save(self, *args):
		print('on_save')
		if args[0]['name'] == socket.gethostname():
			if self.state == 1:
				self.setStatus(5)
				self.setState(2)

	def on_launch(self, *args):
		print('on_launch')
		if args[0]['name'] == socket.gethostname():
			if self.state == 0:
				self.instance = Instance(self, args[0]["id"], args[0]["network"], args[0]["dataset"], args[0]["number"], args[0]["last"])
				self.instance.start()

class Instance(Thread):

	def __init__(self, ComputerNamespace, id, network, dataset, number, last):
		Thread.__init__(self)
		self.ComputerNamespace = ComputerNamespace
		self.id = str(id)
		self.network = str(network)
		self.dataset = str(dataset)
		self.number = str(number)
		self.last = last
		self.running = True
		
	def load_dataset(self):
		download_zip_file(self.number + '.zip', 'http://' + ip + ':' + str(port) + '/datasets/' + self.dataset + '/')
		X_train = np.array(json.loads(open('tx.json').read()))
		y_train = np.array(json.loads(open('ty.json').read()))
		X_val = np.array(json.loads(open('vx.json').read()))
		y_val = np.array(json.loads(open('vy.json').read()))
		return X_train, y_train, X_val, y_val

	def load_network(self, x, y, input_var=None):
		download(self.network, 'http://' + ip + ':' + str(port) + '/networks/')
		script_locals = dict()
		execfile(self.network, dict(), script_locals)
		network = script_locals["build_cnn"](x, y, input_var)
		if self.last:
			download(self.id + '.npz', 'http://' + ip + ':' + str(port) + '/saves/get/')
			with np.load(self.id + '.npz') as f:
				param_values = [f['arr_%d' % i] for i in range(len(f.files))]
			lasagne.layers.set_all_param_values(network, param_values)
		return network
		
	def load_function(self, network, input_var, target_var):
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
		
		return train_fn, val_fn
		
	def run(self):
		self.ComputerNamespace.setError(0)
		self.ComputerNamespace.setState(1)
	
		try:
			self.main()
		except Error as e:
			print "Error:", e.args[0]
			self.ComputerNamespace.setError(e.args[0])
		
		self.ComputerNamespace.setStatus(0)
		self.ComputerNamespace.setState(0)
			
	def main(self):
		try:
			self.ComputerNamespace.setStatus(1)
			time.sleep(self.number * 60)
			X_train, y_train, X_val, y_val = self.load_dataset()
		except:
			print "Unexpected error:", sys.exc_info()[0]
			raise Error(1)
			
		try:
			self.ComputerNamespace.setStatus(2)
			
			x = X_train.shape[1:]
			y = np.bincount(y_train).size
			
			options = {2 : T.tensor3('inputs'), 3 : T.tensor4('inputs')}
			
			input_var = options[len(x)]
			target_var = T.ivector('targets')
			
			network = self.load_network(x, y, input_var)
			train_fn, val_fn = self.load_function(network, input_var, target_var)
		except:
			print "Unexpected error:", sys.exc_info()[0]
			raise Error(2)

		try:
			self.ComputerNamespace.setStatus(3)
			
			epoch = 0
			
			while self.running:
				if self.ComputerNamespace.state == 1:
					self.training(epoch, train_fn, val_fn, X_train, X_val, y_train, y_val)
				elif self.ComputerNamespace.state == 2:
					self.save(network)
					self.ComputerNamespace.setStatus(3)
					self.ComputerNamespace.setState(1)
				elif self.ComputerNamespace.state == 3:
					time.sleep(1)
				elif self.ComputerNamespace.state == 4:
					self.running = False
				epoch += 1
				
			self.save(network)
		except:
			print "Unexpected error:", sys.exc_info()[0]
			raise Error(3)
	
	def training(self, epoch, train_fn, val_fn, X_train, X_val, y_train, y_val):
		train_err = 0
		train_batches = 0
		
		for batch in self.iterate_minibatches(X_train, y_train, 100, shuffle=True):
			inputs, targets = batch
			train_err += train_fn(inputs, targets)
			train_batches += 1

		val_err = 0
		val_acc = 0
		val_batches = 0
		
		for batch in self.iterate_minibatches(X_val, y_val, 100, shuffle=False):
			inputs, targets = batch
			err, acc = val_fn(inputs, targets)
			val_err += err
			val_acc += acc
			val_batches += 1

		self.ComputerNamespace.emit('validation', {'name' : socket.gethostname(), 'epoch' : epoch + 1, 'training' : train_err / train_batches, 'validation' : val_err / val_batches, 'accuracy' : val_acc / val_batches * 100})
	
	def save(self, network):
		np.savez('model.npz', *lasagne.layers.get_all_param_values(network))
		files = {'file': open('model.npz')}
		response = requests.post('http://' + ip + ':' + str(port) + '/saves/post/' + self.id, files=files)

	def iterate_minibatches(self, inputs, targets, batchsize, shuffle=False):
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
	socketIO = SocketIO(ip, port)
	computer_namespace = socketIO.define(ComputerNamespace, '/python')
	try:
		socketIO.wait()
	except KeyboardInterrupt:
		print 'Interrupted'
		computer_namespace.on_stop({'name' : socket.gethostname()})