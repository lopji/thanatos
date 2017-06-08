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
count = []
hs = []

gc.disable()
for data in split:
	labels.append(int(data[0]))
	localDico = nltk.word_tokenize(data[1])
	count.append(len(localDico))
	for k in localDico:
		hs.append(hash(k))
		for y in localDico:
			hs.append(hash(k + y))
gc.enable()

max_count = max(count)
max_hash = max(hs)
min_hash = min(hs)

print(max_count)
print(max_hash)
print(min_hash)

gc.disable()
for data in split:
	first = []
	localDico = nltk.word_tokenize(data[1])
	
	for i in range(0, max_count):
		second = []
		for y in range(0, max_count):
			second.append(0.0)	
		first.append(second)
		
	for i in range(0, len(localDico)):
		for y in range(0, len(localDico)):
			if i == y:
				first[i][y] = (hash(localDico[i]) * 1.0 - min_hash * 1.0)/(max_hash * 1.0 - min_hash * 1.0)
			elif i == 0:
				first[i][y] = (hash(localDico[y]) * 1.0 - min_hash * 1.0)/(max_hash * 1.0 - min_hash * 1.0)
			elif y == 0:
				first[i][y] = (hash(localDico[i]) * 1.0 - min_hash * 1.0)/(max_hash * 1.0 - min_hash * 1.0)
			else:
				first[i][y] = (hash(localDico[i]+localDico[y]) * 1.0 - min_hash * 1.0)/(max_hash * 1.0 - min_hash * 1.0)
		
	texts.append([first])
gc.enable()


for i in range(0,1):
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
