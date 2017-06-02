import numpy as np
import sys
import os
import codecs, json 
import random

file = open("data-twiter.txt")
datas = file.read().split("\n")

labels = []
texts = []

random.shuffle(datas);

for data in datas:
	values = data.split("\t")
	labels.append(int(values[0]))
	length  = len(values[1])
	text = []
	text1 = []
	for i in range(0, 227):
		if length  > i:
			text.append(ord(values[1][i]) / 239.0)
			#print ord(values[1][i])
		else:
			text.append(0.0)
	text1.append(text)
	texts.append(text1)

X_train = np.array(texts)
y_train = np.array(labels);
X_train, X_val = X_train[:-1000], X_train[-1000:]
y_train, y_val = y_train[:-1000], y_train[-1000:]

json.dump(X_train.tolist(), codecs.open("./tx.json", 'w', encoding='utf-8'), separators=(',', ':'), sort_keys=True, indent=4)
json.dump(y_train.tolist(), codecs.open("./ty.json", 'w', encoding='utf-8'), separators=(',', ':'), sort_keys=True, indent=4)
json.dump(X_val.tolist(), codecs.open("./vx.json", 'w', encoding='utf-8'), separators=(',', ':'), sort_keys=True, indent=4)
json.dump(y_val.tolist(), codecs.open("./vy.json", 'w', encoding='utf-8'), separators=(',', ':'), sort_keys=True, indent=4)

