#!/usr/bin/env python
# coding: utf-8

# a python file that contains the line of code needed to parse the entire collection of html pages and save those in tsv files.

# In[6]:


import parser_utils

import urllib
import pandas as pd
from bs4 import BeautifulSoup
import requests
import time
from random import randint
import codecs
import csv
import unicodedata


def create_tsvs(in_p):
    #INPUT: path of all 30k articles
    missing_pages=[]   
    for i in range(1,30001):
        path = in_p+str(i)+".html" #target article path by id
        with open(path, "r") as f: #read target article file
            contents = f.read()
            page = BeautifulSoup(contents, 'lxml') #soup object for target article page
            
        f_name = 'Doc'+str(i)+".tsv"
        with open(f_name, 'wt') as out_file: #open file to write the output 
            header=['Id', 'Title', 'Intro', 'Plot', 'Name', 'Directed_by', 'Produced_by','Written_by', 'Starring', 'Music_by',
            'Release_date', 'Running_time', 'Country','Language', 'Budget']
            tsv_writer = csv.writer(out_file, delimiter='\t')
            tsv_writer.writerow(header) #write header line
            
            #the following 3 condition are to skip 'write all values as NA' all pages that contains 'disambiguation table'
            #because that means the url is wrong or not clear enough to return a specific movie page
            if page.find("table", id="disambigbox")!=None or page.find("table", id="setindexbox")!=None or page.find("table", id="noarticletext")!=None:
                row=[i]+[parser_utils.get_title(page)]+['NA' for i in range(13)]
                tsv_writer = csv.writer(out_file, delimiter='\t')
                tsv_writer.writerow(row)
                missing_pages.append(i)
            else:
                #getting all needed data from page as a row/ list
                row = [i, parser_utils.get_title(page), parser_utils.get_intro(page), parser_utils.get_plot(page)]+ parser_utils.extract_infobox(page)   
                tsv_writer = csv.writer(out_file, delimiter='\t')
                tsv_writer.writerow(row) #writing the row to tsv file
    #write ids of all missing pages in txt file
    with open('Missing_movies.txt', 'w') as mis_file:
        mis_file.write(str(missing_pages))



create_tsvs("/Users/MO/Desktop/ADM/ADM-HW3/Movies_htmls/article_")






