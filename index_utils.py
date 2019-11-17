#!/usr/bin/env python
# coding: utf-8

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
import utils





# In[ ]:


#clean all tsv docs
for i in range(1,30001):
    print(i) if i%1000==0 else None
    path='/Users/MO/Desktop/ADM/ADM-HW3/Movies_tsv_files/Doc'+str(i)+'.tsv'
    doc=pd.read_csv(path,sep='\t')
    #print(doc['Intro'][0])
    c_title=utils.clean_text(doc['Title'][0])
    c_intro=utils.clean_text(doc['Intro'][0])
    c_plot=utils.clean_text(doc['Plot'][0])
    f_name = 'Doc'+str(i)+".tsv"
    with open(f_name, 'w') as out_file:
        header=['Id','Title', 'Intro', 'Plot']
        tsv_writer = csv.writer(out_file, delimiter='\t')
        tsv_writer.writerow(header)
        tsv_writer.writerow([i, c_title, c_intro, c_plot])


# In[ ]:


#reading all documents and extract all text from[title,intro,plot] 
#then write all text in one txt file for faster computation to get VOCABULARY list
with open('All_text_title_intro_plot.txt', 'w') as out_file:
    for i in range(1,30001):
        print(i) if i%2000==0 else None
        path='/Users/MO/Desktop/ADM/ADM-HW3/Movies_tsv_files/Doc'+str(i)+'.tsv'
        doc=pd.read_csv(path,sep='\t')
        out_file.write(str(doc['Title'][0])+' '+str(doc['Intro'][0])+' '+str(doc['Plot'][0])+' ')
with open('All_text_title_intro_plot.txt', 'r') as file:
    all_text = file.read()


# In[ ]:


with open('All_text_cleaned.txt', 'w') as file:
    #clean all text
    cleaned_text= utils.clean_text(all_text)
    #save cleaned text to txt file
    file.write(cleaned_text)


# In[ ]:


#vocabulary
with open('vocabulary.txt', 'w') as file:
    v=list(set(cleaned_text.split())) #set of cleaned text geves us the unique vocabularies
    v.sort() #sort vocabularies
    vocabulary=' '.join(v)
    #save vocabularies to txt file
    file.write(vocabulary)


# In[ ]:


vocab_list = vocabulary.split()
vocab_dic = dict( zip(vocab_list, range(len(vocab_list))))
with open('vocab_dic.txt', 'w')as f2:
    f2.write(json.dumps(vocab_dic))


# In[ ]:


#Counting number of words for each document
words_per_doc= dict( zip(range(1,30001),[0 for i in range(1,30001)]))
for i in range(1,30001):
    print(i) if i%1000 ==0 else None
    path='/Users/MO/Desktop/ADM/ADM-HW3/cleaned_tsv_files/Doc'+str(i)+'.tsv'
    doc=pd.read_csv(path,sep='\t')
    text = doc['Title'][0].split()+doc['Intro'][0].split()+doc['Plot'][0].split()
    while '  ' in text: text.remove('  ') 
    words_per_doc[i]=len(text)
    
with open('words_per_doc.txt', 'w') as file:
     file.write(json.dumps(words_per_doc))


# In[ ]:


def tf_idf(term_id, doc_id):
    #INPUT: term_id(str), doc_id(int)
    #OUTPUT: tf-idf
    tf = inverted_index[term_id].count(doc_id)/words_per_doc[str(doc_id)]
    idf=math.log( 30000/len(inverted_index2[term_id]))
    return tf*idf


# In[ ]:







