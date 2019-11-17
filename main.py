#!/usr/bin/env python
# coding: utf-8

# In[4]:


from nltk.tokenize import RegexpTokenizer
import pandas as pd
import collections
from bs4 import BeautifulSoup
import csv
import string
import json
import math
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from heapq import heappush, heappop


# In[2]:


import utils


# In[20]:


#load pre-calculated data for search engune 1
with open('vocabulary.txt', 'r')as f1:
    vocabulary = f1.read()
    vocab_list = vocabulary.split()
with open('All_text_title_intro_plot.txt', 'r') as file:
    all_text = file.read()
with open('words_per_doc.txt', 'r') as f2:
    words_per_doc = json.loads(f2.read())
with open('Inverted_index1.txt', 'r') as f2:
    inverted_index = json.loads(f2.read())
with open('vocab_dic.txt', 'r') as f3:
    vocab_dic = json.loads(f3.read())
with open('Inverted_index2.txt', 'r') as f4:
    inverted_index2 = json.loads(f4.read())
with open('Inverted_index3.txt', 'r') as f5:
    inverted_index3 = json.loads(f5.read())
with open('Inverted_index4.txt', 'r') as f6:
    inverted_index4 = json.loads(f6.read())
with open('features_text_dict.txt', 'r') as f:
    features_text_dict = json.loads(f.read())


# In[6]:


def get_movies1(result):
    if len(result)!=0:
        result_df = pd.DataFrame(columns=['Id', 'Title', 'Intro', 'Url'])
        urls= pd.read_csv("/Users/MO/Desktop/ADM/ADM-HW3/Movies_urls.tsv",sep='\t')
        df_idx=0
        for i in result:
            movie =pd.read_csv("/Users/MO/Desktop/ADM/ADM-HW3/Movies_tsv_files/Doc"+str(i)+".tsv",sep='\t')
            id_= movie['Id'][0]
            title=movie['Title'][0]
            intro=movie['Intro'][0]
            url=urls.Url[i-1]
            result_df.loc[df_idx]=[id_,title,intro,url]
            df_idx+=1
        return result_df
    else: print('No result1...')


# # Search Engine 1

# In[17]:


def engine1():
    query = input()
    query= utils.clean_text(query) #clean query
    docs=[]
    for w in query.split():
        try:
            docs.append(inverted_index[str(vocab_dic.get(w))]) #getting ALL docs containing query words
        except:
            continue
    try:
        result=set(docs[0]).intersection(*docs)
        return get_movies1(result)
    except:
        return 'No result...'


# In[19]:


engine1()


# In[9]:


def tf_idf_query(query):
    #INPUT: query
    #OUTPUT: tf-idf of the query terms
    query_list=query.split()
    tf_idf={}
    for w in set(query_list):
        #print(term_id)
        try:
            term_id=vocab_dic[w]
            tf= query_list.count(w)/len(query_list)
            idf= math.log( 30000/len(inverted_index2[str(term_id)]))
            tf_idf[term_id]= tf*idf
        except:
            
            continue
    
    return tf_idf


# In[10]:


def get_movies2(result,cos_sim):
    if len(result)!=0:
        result_df = pd.DataFrame(columns=['Title', 'Intro', 'Url','Cos_sim'])
        urls= pd.read_csv("/Users/MO/Desktop/ADM/ADM-HW3/Movies_urls.tsv",sep='\t')
        df_idx=0
        for i,j in zip(result,cos_sim):
            movie =pd.read_csv("/Users/MO/Desktop/ADM/ADM-HW3/Movies_tsv_files/Doc"+str(i)+".tsv",sep='\t')
            title=movie['Title'][0]
            intro=movie['Intro'][0]
            url=urls.Url[i-1]
            result_df.loc[df_idx]=[title,intro,url,str(j)]
            df_idx+=1
        return result_df
    else: print('No result...')


# # Search Engine 2

# In[14]:


#Search engine 2
def engine2():
    query= input()
    query= utils.clean_text(query) #clean query
    query_tfidf= tf_idf_query(query)
    docs=[]
    for w in query.split():
        try:
            docs.append(inverted_index[str(vocab_dic.get(w))]) #getting ALL docs containing query words
        except:
            continue
    try:        
        result=set(docs[0]).intersection(*docs)
        docs_tfidf=dict( zip(result,[[] for i in range(len(result))]))
        for term_id in query_tfidf:
            for doc in inverted_index4[str(term_id)]:
                if doc[0] in result: docs_tfidf[doc[0]].append(doc[1])

        vec1= np.array([list(query_tfidf.values())])
        vec2= np.array(list(docs_tfidf.values()))
        result2= cosine_similarity(vec1, vec2)
        result_df = pd.DataFrame([result,result2[0]],index=['doc_id', 'cos_sim'])
        result_df=result_df.sort_values(by ='cos_sim', axis=1,ascending=False)
        top_ten_result=list(map(int,result_df.loc['doc_id'][:10]))
        top_ten_cos_sim= list(result_df.loc['cos_sim'][:10])
        return get_movies2(top_ten_result, top_ten_cos_sim)
    except:
        return 'No result...'



# In[16]:


engine2()


# In[21]:


def get_tf_idf_query_similarity(vectorizer, docs_tfidf, query):
    """
    vectorizer: TfIdfVectorizer model
    docs_tfidf: tfidf vectors for all docs
    query: query doc

    return: cosine similarity between query and all docs
    """
    query_tfidf = vectorizer.transform([query])
    cosineSimilarities = cosine_similarity(query_tfidf, docs_tfidf).flatten()
    return cosineSimilarities


# In[22]:


def heap(sims,doc_ids):
    data=[]
    heap = []
    for i in range(len(result)):
        data.append((-sims[i],doc_ids[i]))
    for item in data:
         heappush(heap, item)
    output=[]
    while heap:
         output.append(-heappop(heap)[0])
    return output


# # Search Engine 3


def engine3():
    query = input() #first search query, get engine1 result
    query2= input()
    query2= utils.clean_text(query2)
    query= utils.clean_text(query) #clean query
    docs=[]
    for w in query.split():
        try:
            docs.append(inverted_index2[str(vocab_dic.get(w))]) #getting ALL docs containing query words
        except:
            continue
    try:
        result=set(docs[0]).intersection(*docs)

        result_features= [utils.clean_text(features_text_dict[str(i)]) for i in result]
        vectorizer = TfidfVectorizer()
        docs_tfidf = vectorizer.fit_transform(result_features)
        result_sim = get_tf_idf_query_similarity(vectorizer, docs_tfidf, query2)
        movies = get_movies1(result)
        sorted_sims = heap(result_sim,list(result))
        movies.insert(4, "Similarity", sorted_sims)
        return movies.head(10)

    except:
        return 'No result...6'



result3 = engine3()




def create_Graph(movies):
    

    final_ac_list = []
    act_dict={}
    films_ = movies.head(10)
    need_info=pd.merge(films_,all_data,how='inner')

    for i in range(len(need_info)):
        for a in need_info['Starring'][i].split('-'):
            final_ac_list.append(a)

    for i in final_ac_list:
           act_dict[i]=[]

    for i in range(len(need_info)):
        for a in need_info['Starring'][i].split('-'):
                act_dict[a].append(need_info['Title'][i])

    G=nx.Graph()
    G.add_nodes_from(act_dict.keys())  


    for i in act_dict:
           for j in act_dict: 
                if i!= j:
                     if (len(set(act_dict[i]).intersection(set(act_dict[j]))))>=2 :
                            G.add_edge(i,j)

    nx.draw_circular(G,with_labels=True,node_size=90,alpha=0.7)




all_data=pd.read_csv('movies_features.csv', sep='\t')
del all_data['Unnamed: 0']






