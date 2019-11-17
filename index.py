#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import index_utils


# In[ ]:


import nltk
from stop_words import get_stop_words
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer 
from nltk.tokenize import RegexpTokenizer
import pandas as pd
import collections
import numpy
from bs4 import BeautifulSoup
import csv
import string
import json
import math
import numpy as np


#creat first inverted index(with repetition)
inverted_index = dict( zip(range(len(vocab_list)),[[] for i in range(len(vocab_list))]))

for i in range(1,30001):
    print(i) if i%1000 ==0 else None
    path='/Users/MO/Desktop/ADM/ADM-HW3/cleaned_tsv_files/Doc'+str(i)+'.tsv'
    doc=pd.read_csv(path,sep='\t')
    text = doc['Title'][0].split()+doc['Intro'][0].split()+doc['Plot'][0].split()
    for w in text:
        if w == '  ': continue
        else:
            inverted_index[vocab_dic[w]].append(i)
            
            
with open('Inverted_index1.txt', 'w') as file:
     file.write(json.dumps(inverted_index))


# In[ ]:


#creat second inverted index(without repetition)
inverted_index2 = dict( zip(range(len(vocab_list)),[[] for i in range(len(vocab_list))]))
for i in inverted_index.items(): #remove repeated docs
    counter=collections.Counter(i[1])
    inverted_index2[i[0]]=list(counter.keys())

with open('Inverted_index2.txt', 'w') as file:
     file.write(json.dumps(inverted_index2))


# In[ ]:


#creat third inverted index(with tf-idf)
inverted_index4 = dict( zip(range(len(vocab_list)),[[] for i in range(len(vocab_list))]))

for i in inverted_index2.items():
    for j in i[1]:
        #j is doc_id(int)
        #i[0] is term_id(str)
        inverted_index4[int(i[0])].append((j,tf_idf(i[0],j)))
            
            
with open('Inverted_index4.txt', 'w') as file:
     file.write(json.dumps(inverted_index4))




