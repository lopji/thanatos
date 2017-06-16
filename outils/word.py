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
model = word2vec.Word2Vec(rtAll, size=300, iter=700)
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
#random.shuffle(dataset);

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
				values.append([0] * 300)
		else:
			values.append([0] * 300)
	train.append([values])
gc.enable()

print(max_count_words)

np_x_train = np.array(train)
np_y_train = np.array(label);

for i in range(0,10):
	x_train = np.concatenate((np_x_train[0:533*i], np_x_train[533*(i+1):5331], np_x_train[5331:5331+533*i], np_x_train[5331+533*(i+1):]), axis=0)
	y_train = np.concatenate((np_y_train[0:533*i], np_y_train[533*(i+1):5331], np_y_train[5331:5331+533*i], np_y_train[5331+533*(i+1):]), axis=0)
	x_val = np.concatenate((np_x_train[533*i:533*(i+1)], np_x_train[5331+533*i:5331+533*(i+1)]), axis=0)
	y_val = np.concatenate((np_y_train[533*i:533*(i+1)], np_y_train[5331+533*i:5331+533*(i+1)]), axis=0)

	print x_train.shape
	print y_train.shape
	print x_val.shape
	print y_val.shape
	
	json.dump(x_train.tolist(), codecs.open("./tx"+ str(i+1) +".json", 'w', encoding='utf-8'), separators=(',', ':'), sort_keys=True, indent=4)
	json.dump(y_train.tolist(), codecs.open("./ty"+ str(i+1) +".json", 'w', encoding='utf-8'), separators=(',', ':'), sort_keys=True, indent=4)
	json.dump(x_val.tolist(), codecs.open("./vx"+ str(i+1) +".json", 'w', encoding='utf-8'), separators=(',', ':'), sort_keys=True, indent=4)
	json.dump(y_val.tolist(), codecs.open("./vy"+ str(i+1) +".json", 'w', encoding='utf-8'), separators=(',', ':'), sort_keys=True, indent=4)