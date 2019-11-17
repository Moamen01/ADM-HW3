#!/usr/bin/env python
# coding: utf-8

# # Collector#

# ***save All urls to Movies_urls.tsv/ 30k urls from the 3 given html files***

import csv
import pandas as pd
from bs4 import BeautifulSoup
import collector_utils


#save All urls to Movies_urls.tsv/ 30k urls from the 3 given html files
with open('Movies_urls.tsv','wt') as out_file:
    header=['Id', 'Url']
    tsv_writer = csv.writer(out_file, delimiter='\t')
    tsv_writer.writerow(header)
    
    with open("/Users/MO/Desktop/ADM/ADM-HW3/movies1.html", "r") as f1:
        contents1 = f1.read()
        soup1 = BeautifulSoup(contents1, 'lxml')
    with open("/Users/MO/Desktop/ADM/ADM-HW3/movies2.html", "r") as f2:
        contents2 = f2.read()
        soup2 = BeautifulSoup(contents2, 'lxml')
    with open("/Users/MO/Desktop/ADM/ADM-HW3/movies3.html", "r") as f3:
        contents3 = f3.read()
        soup3 = BeautifulSoup(contents3, 'lxml')
    movies_soup1= soup1.find_all('tr')[1:]
    movies_soup2= soup2.find_all('tr')[1:]
    movies_soup3= soup3.find_all('tr')[1:]
    
    for m in movies_soup1:
        tsv_writer = csv.writer(out_file, delimiter='\t')
        tsv_writer.writerow([m.find('td').text, m.find('a').text]) #writing row: ID,URL
    for m in movies_soup2:
        tsv_writer = csv.writer(out_file, delimiter='\t')
        tsv_writer.writerow([m.find('td').text, m.find('a').text]) #writing row: ID,URL
    for m in movies_soup3:
        tsv_writer = csv.writer(out_file, delimiter='\t')
        tsv_writer.writerow([m.find('td').text, m.find('a').text]) #writing row: ID,URL


# ***Then read the saved file of urls as a dataframe and start crawling using crawl_wiki function from collector_utils***

movies_links = pd.read_csv('Movies_urls.tsv', ,sep='\t')
collector_utils.crawl_wiki(movies_links)

