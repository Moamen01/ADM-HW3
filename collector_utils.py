#!/usr/bin/env python
# coding: utf-8

# # Collector_utils



import requests
import time
from random import randint
import pandas as pd


def crawl_wiki(movies):
    #Input: Urls dataframe
    #Output: crawling all articles and save them as tsv files
    missing=[] #when wiki block us the loop drops the current url, so we save those missing urls here 
    for index ,m in movies.iterrows():
        try:
            id = m['Id']
            url = m['Url']

            html =requests.get(url)
            with open("article_"+str(id)+".html", "w") as file:
                file.write(html.text)
            time.sleep(randint(1, 3))
        except requests.exceptions.RequestException as e:
            print('Rate limited. Need to wait for 20 minutes')
            print('missing: ',index)
            missing.append(index) #save the current url to missing list
            time.sleep(20*60) #sleep for 20 mins
    if len(missing)>0: crawl_wiki(movies.loc[missing]) #call the function again to crawl missing urls






