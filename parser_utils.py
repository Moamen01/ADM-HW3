#!/usr/bin/env python
# coding: utf-8

# a python file that gathers the function you used in parser.py


def get_title(page):
    return page.find('h1', class_='firstHeading').get_text('i')


def get_intro(page):
    # intro is always after infobox table or before contents div
    #if one of them is not exist in the page then we use the other class to get the intro
    if page.find("div", class_="toc") != None:
        content = page.find("div", class_="toc")
        pre = content.findPreviousSiblings()
        #pre.reverse()
        intro = ''
        for i in pre:
            if i.name =='p':
                intro+=i.text
            else: break 
        return intro
    elif page.find("table", class_="infobox vevent")!=None:
        table = page.find("table", class_="infobox vevent")
        intro = ''
        for i in table.find_next_siblings():
            if i.name !='div':
                intro+=i.text

            else: break
        return intro
    else: return 'NA'




def get_plot(page):
    #the plot is always the first mw-headline class in the page if the url is not wrong
    plot_head= page.find(class_="mw-headline").find_parent()
    plot= ''
    for i in plot_head.find_next_siblings():
        if i.name != 'h2':
            plot+=i.text
        else: break
    return plot



def extract_infobox(page):
    d = {'name':'NA', 'Directed by': 'NA', 'Produced by': 'NA','Written by': 'NA', 'Starring': 'NA', 'Music by': 'NA',
      'Release date': 'NA', 'Running time': 'NA', 'Country': 'NA','Language': 'NA', 'Budget': 'NA'}
    if page.find("table", class_="infobox vevent")==None: return list(d.values())
    table = page.find("table", class_="infobox vevent") #table infobox
    
    d['name'] = table.find("th", class_="summary").text if table.find("th", class_="summary") else 'NA'
    for record in table.findAll('tr'):
        for attr in record.findAll('th'):
            for data in record.findAll('td'):
                if attr.text in d:
                    if attr.text == 'Release date': 
                        d[attr.text] =unicodedata.normalize("NFKD",data.get_text(strip=True))
                    else:
                        d[attr.text] = ' - '.join(list(data.stripped_strings))
                else: continue 
    return list(d.values())




