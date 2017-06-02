import nltk
import sys  
import random
import gc
import numpy as np
import codecs, json 

reload(sys)  
sys.setdefaultencoding('ISO-8859-1')
file = open("../dataset/rtAll.txt", 'rb')

text = file.read()

STOP_TYPES = ['NN']

tokens = nltk.pos_tag(nltk.word_tokenize(text))
good_words = [w for w, wtype in tokens if wtype in STOP_TYPES]

fdist1 = nltk.FreqDist(good_words)
dico = fdist1.keys()

datas = text.split("\n")
split = []
x = 1

for data in datas:
	if x > 5331:
		split.append([0,data])
	else:
		split.append([1,data])
	x+=1
	
random.shuffle(split);
	
labels = []
texts = []

x = 0
gc.disable()
for data in split:
	text = []
	labels.append(int(data[0]))
	localDico = nltk.word_tokenize(data[1])
	for k in dico:
		if k in localDico:
			text.append(1.0)
		else:
			text.append(0.0)
	texts.append([text])
	x+=1
	print(x)
gc.enable()



for i in range(0,10):
	X_train = np.array(texts)
	y_train = np.array(labels);

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

	
print(X_train.shape)
print(X_val.shape)
print(len(dico))