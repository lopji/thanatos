import numpy as np
import sys
import os
import codecs, json 
import random
import string
import re
import gc

file = open("../dataset/rtAll.txt")
datas = file.read().split("\n")

labels = []
texts = []
split = []
dico = {}
x = 1

for data in datas:
	if x > 5331:
		split.append([0,data])
	else:
		split.append([1,data])
	x+=1

random.shuffle(split);

#for data in split:
#	labels.append(data[0])
#	words = re.sub('<[^<]+?>', '',  re.sub(r'[\xc2\x99\xc3\xa9]','',data[1])).translate(None, string.punctuation).lower().split(' ')
#	for word in words:
#		if(len(word) > 3):
#			if word in dico:
#				dico[word] += 1
#			else: 
#				dico[word] = 1


#for k, v in dico.items():
#	if v <= 3:
#		del dico[k]
		
#x = 0

#gc.disable()

#for data in split:
#	text = []
#	dicoLocal = {}
#	words = re.sub('<[^<]+?>', '',  re.sub(r'[\xc2\x99\xc3\xa9]','',data[1])).translate(None, string.punctuation).lower().split(' ')
#	
#	for word in words:
#		if(len(word) > 3):
#			if word in dicoLocal:
#				dicoLocal[word] += 1
#			else: 
#				dicoLocal[word] = 1
				
#	print(len(dicoLocal))
	
#	for k, v in dico.items():
#		if k in dicoLocal:
#			text.append(1.0)
#		else:
#			text.append(0.0)
	
#	print(x)
#	texts.append([text])
#	x+=1

#gc.enable()

	
#X_train = np.array(texts)
#y_train = np.array(labels);
#X_train, X_val = X_train[:-1066], X_train[-1066:]
#y_train, y_val = y_train[:-1066], y_train[-1066:]

#print(X_train.shape)
#print(X_val.shape)

#json.dump(X_train.tolist(), codecs.open("./tx.json", 'w', encoding='utf-8'), separators=(',', ':'), sort_keys=True, indent=4)
#json.dump(y_train.tolist(), codecs.open("./ty.json", 'w', encoding='utf-8'), separators=(',', ':'), sort_keys=True, indent=4)
#json.dump(X_val.tolist(), codecs.open("./vx.json", 'w', encoding='utf-8'), separators=(',', ':'), sort_keys=True, indent=4)
#json.dump(y_val.tolist(), codecs.open("./vy.json", 'w', encoding='utf-8'), separators=(',', ':'), sort_keys=True, indent=4)




list = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 59, 61, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 101, 113, 118, 119, 157, 169, 186, 192, 193, 194, 195, 198, 199, 200, 201, 202, 205, 207, 209, 211, 212, 213, 214, 218, 219, 220]


for values in split:
	labels.append(int(values[0]))
	length  = len(values[1])

	text = []
	for i in range(0, 268):
		if length  > i:
			value = ord(values[1][i])-32
			id = list.index(value)
			text.append(id / 86.0)
		else:
			text.append(0.0)
	texts.append([text])

X_train = np.array(texts)
y_train = np.array(labels);
X_train, X_val = X_train[:-1066], X_train[-1066:]
y_train, y_val = y_train[:-1066], y_train[-1066:]

print(len(list))
print(X_train.shape)
print(X_val.shape)

json.dump(X_train.tolist(), codecs.open("./tx.json", 'w', encoding='utf-8'), separators=(',', ':'), sort_keys=True, indent=4)
json.dump(y_train.tolist(), codecs.open("./ty.json", 'w', encoding='utf-8'), separators=(',', ':'), sort_keys=True, indent=4)
json.dump(X_val.tolist(), codecs.open("./vx.json", 'w', encoding='utf-8'), separators=(',', ':'), sort_keys=True, indent=4)
json.dump(y_val.tolist(), codecs.open("./vy.json", 'w', encoding='utf-8'), separators=(',', ':'), sort_keys=True, indent=4)

