#!/usr/bin/env python
# coding: utf-8

# In[2]:


from stop_words import get_stop_words
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer 
import nltk
from nltk.tokenize import RegexpTokenizer
import numpy


# In[ ]:





# In[ ]:





# In[3]:


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

tokenizer = RegexpTokenizer(r'\w+')
def remove_punctuation(text):
    #INPUT: text
    #OUTPUT: cleaned text after removing all punctuation and special chars
    #print('remove_punctuation...')
    if type(text)==numpy.float64: return ''
    else:
        return ' '.join(tokenizer.tokenize(text))+' '
    
ps = PorterStemmer()
def stem(text):
    #INPUT: text
    #OUTPUT: returns text after stem all words using NLTK lib
    #print('stem...')
    if type(text)==numpy.float64: return ''
    else:
        return ' '.join([ps.stem(w) for w in text.split()])+' '

def remove_nonASCII(text):
    #INPUT: text
    #OUTPUT: returns text after removing all non ASCII chars, there are alot of non Latin alphabet, chinese for ex.
    #print('remove_nonASCII...')
    if type(text)==numpy.float64: return ''
    else:
        printable = set(string.printable)
        return ''.join(filter(lambda x: x in printable, text))+' '


# In[4]:


def clean_text(text):
    return remove_nonASCII(stem(remove_punctuation(remove_stopWords(text))))


# In[ ]:





# In[ ]:




