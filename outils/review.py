import numpy as np
import sys
import os
import codecs, json 
import random
import glob
import string
import re

datas = [];
pos = glob.glob("./dataset/review/train/pos/*.txt")
neg = glob.glob("./dataset/review/train/neg/*.txt")

labels = []
texts = []
dico = {}

for p in pos:
	datas.append([0, open(p).read()])
	
for n in neg:
	datas.append([1, open(n).read()])

random.shuffle(datas)

for data in datas:
	labels.append(data[0])
	words = re.sub('<[^<]+?>', '',  re.sub(r'[\xc2\x99\xc3\xa9]','',data[1])).translate(None, string.punctuation).lower().split(' ')
	for word in words:
		if(len(word) > 3):
			if word in dico:
				dico[word] += 1
			else: 
				dico[word] = 1


for k, v in dico.items():
	if v <= 3:
		del dico[k]
	
x = 0
	
for data in datas:
	
	text = []
	dicoLocal = {}
	words = re.sub('<[^<]+?>', '',  re.sub(r'[\xc2\x99\xc3\xa9]','',data[1])).translate(None, string.punctuation).lower().split(' ')
	
	for word in words:
		if(len(word) > 3):
			if word in dicoLocal:
				dicoLocal[word] += 1
			else: 
				dicoLocal[word] = 1
	
	for k, v in dico.items():
		if k in dicoLocal:
			text.append(1.0)
		else:
			text.append(0.0)
	
	print(x)
	texts.append([text])
	x+=1

X_train = np.array(texts)
y_train = np.array(labels)

print(X_train)

count = len(labels)/10

for i in range(1, 10):
	X_t, X_v = X_train[:count*i], X_train[count*i:]
	y_t, y_v = y_train[:count*i], y_train[count*i:]
	json.dump(X_t.tolist(), codecs.open("./vx"+ str(i) +".json", 'w', encoding='utf-8'), separators=(',', ':'), sort_keys=True, indent=4)
	json.dump(y_t.tolist(), codecs.open("./vy"+ str(i) +".json", 'w', encoding='utf-8'), separators=(',', ':'), sort_keys=True, indent=4)
	json.dump(X_v.tolist(), codecs.open("./tx"+ str(i) +".json", 'w', encoding='utf-8'), separators=(',', ':'), sort_keys=True, indent=4)
	json.dump(y_v.tolist(), codecs.open("./ty"+ str(i) +".json", 'w', encoding='utf-8'), separators=(',', ':'), sort_keys=True, indent=4)
	



