import numpy as np
import sys
import os
import gzip
import codecs, json 

if sys.version_info[0] == 2:
	from urllib import urlretrieve
else:
	from urllib.request import urlretrieve

def download(filename, source='http://yann.lecun.com/exdb/mnist/'):
	print("Downloading %s" % filename)
	urlretrieve(source + filename, filename)

def load_mnist_images(filename):
	if not os.path.exists(filename):
		download(filename)

	with gzip.open(filename, 'rb') as f:
		data = np.frombuffer(f.read(), np.uint8, offset=16)

	data = data.reshape(-1, 1, 28, 28)
	return data / np.float32(256)

def load_mnist_labels(filename):
	if not os.path.exists(filename):
		download(filename)

	with gzip.open(filename, 'rb') as f:
		data = np.frombuffer(f.read(), np.uint8, offset=8)

	return data


X_train = load_mnist_images('train-images-idx3-ubyte.gz')
y_train = load_mnist_labels('train-labels-idx1-ubyte.gz')
X_train, X_val = X_train[:-10000], X_train[-10000:]
y_train, y_val = y_train[:-10000], y_train[-10000:]

json.dump(X_train.tolist(), codecs.open("./tx.json", 'w', encoding='utf-8'), separators=(',', ':'), sort_keys=True, indent=4)
json.dump(y_train.tolist(), codecs.open("./ty.json", 'w', encoding='utf-8'), separators=(',', ':'), sort_keys=True, indent=4)
json.dump(X_val.tolist(), codecs.open("./vx.json", 'w', encoding='utf-8'), separators=(',', ':'), sort_keys=True, indent=4)
json.dump(y_val.tolist(), codecs.open("./vy.json", 'w', encoding='utf-8'), separators=(',', ':'), sort_keys=True, indent=4)