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



# In[ ]:


stop_words1 = list(get_stop_words('en'))         
stop_words2 = list(stopwords.words('english')) 
stop_words=list(set(stop_words1+stop_words2)) #collection of stop words from 2 libs
stop_words.append('nan')
def remove_stopWords(text):
    #INPUT: text
    #OUTPUT: removes all stop words and reterns a cleaned text
    #print('remove_stopWords...')
    if type(text)==numpy.float64: return ''
    else:
        return ' '.join([w for w in text.split() if not w in stop_words])+' '


# In[ ]:


tokenizer = RegexpTokenizer(r'\w+')
def remove_punctuation(text):
    #INPUT: text
    #OUTPUT: cleaned text after removing all punctuation and special chars
    #print('remove_punctuation...')
    if type(text)==numpy.float64: return ''
    else:
        return ' '.join(tokenizer.tokenize(text))+' '


# In[ ]:


ps = PorterStemmer()
def stem(text):
    #INPUT: text
    #OUTPUT: returns text after stem all words using NLTK lib
    #print('stem...')
    if type(text)==numpy.float64: return ''
    else:
        return ' '.join([ps.stem(w) for w in text.split()])+' '


# In[ ]:


def remove_nonASCII(text):
    #INPUT: text
    #OUTPUT: returns text after removing all non ASCII chars, there are alot of non Latin alphabet, chinese for ex.
    #print('remove_nonASCII...')
    if type(text)==numpy.float64: return ''
    else:
        printable = set(string.printable)
        return ''.join(filter(lambda x: x in printable, text))+' '


# In[ ]:


#clean all tsv docs
for i in range(1,30001):
    print(i) if i%1000==0 else None
    path='/Users/MO/Desktop/ADM/ADM-HW3/Movies_tsv_files/Doc'+str(i)+'.tsv'
    doc=pd.read_csv(path,sep='\t')
    #print(doc['Intro'][0])
    c_title=remove_nonASCII(stem(remove_punctuation(remove_stopWords(doc['Title'][0]))))
    c_intro=remove_nonASCII(stem(remove_punctuation(remove_stopWords(doc['Intro'][0]))))
    c_plot=remove_nonASCII(stem(remove_punctuation(remove_stopWords(doc['Plot'][0]))))
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
    cleaned_text= remove_nonASCII(stem(remove_punctuation(remove_stopWords(all_text))))
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







