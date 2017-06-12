import nltk
import gensim
from gensim.models import word2vec
import logging
import codecs
import scipy
import gc
import numpy as np
import random
import json

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
file = codecs.open('rtAll.txt', 'r', 'utf-8-sig')
text = file.read()

sentences = text.split("\n")

rtAll = word2vec.Text8Corpus('rtAll.txt')
model = word2vec.Word2Vec(rtAll, size=100)
vocabulary = model.wv.vocab.keys()
count_words = []
dataset = []
train = []
label = []
x = 1

for sentence in sentences:
	words = sentence.split(" ")
	count_words.append(len(words))
	if x > 5331:
		dataset.append([0,sentence])
	else:
		dataset.append([1,sentence])
	x+=1

max_count_words = max(count_words)
random.shuffle(dataset);

gc.disable()
for data in dataset:
	values = []
	label.append(int(data[0]))
	words = data[1].split(" ")
	for i in range(0, max_count_words):
		if i < len(words):
			if words[i] in vocabulary:
				values.append(model.wv[words[i]])
			else:
				values.append([0] * 100)
		else:
			values.append([0] * 100)
	train.append([values])
gc.enable()

print(max_count_words)

for i in range(0,1):
	X_train = np.array(train)
	y_train = np.array(label);

	X_val = X_train[1000*i:1000*(i+1)]
	y_val = y_train[1000*i:1000*(i+1)]
	
	X_t = np.concatenate((X_train[0:1000*i], X_train[1000*(i+1):]), axis=0)
	y_t = np.concatenate((y_train[0:1000*i], y_train[1000*(i+1):]), axis=0)

	print X_t.shape
	print y_t.shape
	print X_val.shape
	print y_val.shape
	
	json.dump(X_t.tolist(), codecs.open("./tx"+ str(i+1) +".json", 'w', encoding='utf-8'), separators=(',', ':'), sort_keys=True, indent=4)
	json.dump(y_t.tolist(), codecs.open("./ty"+ str(i+1) +".json", 'w', encoding='utf-8'), separators=(',', ':'), sort_keys=True, indent=4)
	json.dump(X_val.tolist(), codecs.open("./vx"+ str(i+1) +".json", 'w', encoding='utf-8'), separators=(',', ':'), sort_keys=True, indent=4)
	json.dump(y_val.tolist(), codecs.open("./vy"+ str(i+1) +".json", 'w', encoding='utf-8'), separators=(',', ':'), sort_keys=True, indent=4)