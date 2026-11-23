#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Sep 7 07:54:41 2022

@author: ESTERBET Julien and LEGEARD Hugo
"""

import csv
import re
from math import log
import webbrowser
from tkinter import * 
from tkinter import ttk


########################## Initialisation Interface Graphique ##########################

# Creation of the graphic interface
root = Tk()
root.title("TED Search Engine")
root.geometry("800x500")

# Search bar zone
top = ttk.Frame(root)
top.pack(side=TOP, fill=X, padx=10, pady=10)

# Results zone
bottom = ttk.Frame(root)
bottom.pack(side=TOP, fill=BOTH, expand=True, padx=10, pady=(0, 10))

#ScrollBar creation
scrollbar = ttk.Scrollbar(bottom)
scrollbar.pack(side=RIGHT, fill=Y)

#Label Creation 
L1 = ttk.Label(top, text="Your keywords :")
L1.pack(side=LEFT, padx=(0, 5))

#Entry to enter and get the keywords
keywords = StringVar()
keywordInput = ttk.Entry(top, textvariable=keywords)
keywordInput.pack(side=LEFT, fill=X, expand=True, padx=5)
keywordInput.focus()

currentUrls = []

########################## Fonctions ##########################

def csv_to_dict(csv_file) :
    """Transform the csv file to a Dictionnary with the keys as the Transcript and the value as the url """
    myDict = {} 
    with csv_file as infile:
        reader = csv.reader(infile)
        next(reader, None) 
        myDict = {rows[0] : rows[1] for rows in reader}
    return myDict

def index_words_to_urls(dico) :
    """Create an index { words --> Urls }"""
    res = {}
    for key, value in dico.items() :
        pattern = re.compile(r'\W+')
        val = key
        val = re.sub(pattern, ' ', val)
        val = val.lower()
        for word in val.split() :
            if word not in res :
                res[word] = [value]
            elif value not in res[word] :
                res[word].append(value)
    return res

def index_words_to_idf(index1) : 
    """Create an index { words --> IDF }"""
    idf = {}
    length = len(index1)
    for key, value in index1.items() : 
        idf[key] = log(length / len(value))
    return idf

def index_urls_to_words(dico) :
    """Create an index { Urls --> { Words --> TF } }"""
    res = {}
    for key, value in dico.items() :
        tab = {}
        pattern = re.compile('\W+')
        val = key
        val = re.sub(pattern, ' ', val)
        val = val.lower()
        length = len(val.split())
        for word in val.split() :
            if word not in tab :
                tab[word] = 1
            else : 
                tab[word] += 1
        for x in tab : 
            tab[x] = tab[x]/length
        res[value] = tab
    return res

def find_a_word(index1, index2, index3, wordToFind) :
    """Return a dict { Url --> Tf-Idf score }"""
    res = {}
    if wordToFind in index1 :
        urls = index1[wordToFind]
        idf = index2[wordToFind]
        for x in urls : 
            for key, value in index3.items() :
                if key == x :
                    res[key] = value[wordToFind]*idf
    return res

def find_some_words(index1, index2, index3) :
    """Take an input of some words and call the previous function so return a dict of a dict { word --> { Url --> Tf-Idf score } }"""
    inputWordsToFind = keywordInput.get()
    res = {}
    setWordsToFind = inputWordsToFind.lower().split()
    for x in setWordsToFind :
        res[x] = find_a_word(index1, index2, index3, x)
    return res

def intersection_of_results(dico) :
    """return the intersection of all the url associated with all the keywords"""
    n = 0
    tab = {}
    res = {}
    for key, value in dico.items() : 
        if len(dico) == 1 : 
            res = value
        elif n == 0 :
            tab = value
            n = 1
        elif n == 1 :
            for keyBis, valueBis in value.items() :
                if keyBis in tab : 
                    x = tab[keyBis] + valueBis
                    res[keyBis] = x
                    n = 2
        else : 
            tab = dict(res)
            res.clear()
            for keyBis, valueBis in value.items() : 
                if keyBis in tab : 
                    x = tab[keyBis] + valueBis
                    if x >= 0.0025 : 
                        res[keyBis] = x
    return sorted(res.items(), key=lambda x: x[1], reverse=True)

def url_to_title(url):
    url = url.rstrip('\n')
    splitUrl = url.split('/')
    title = splitUrl[-1]
    spaceTitle = title.replace('_', ' ')
    finalTitle = spaceTitle.title()
    return finalTitle


########################## Fonction de l'Interface Graphique ######################

#Open the url of the selected result in the browser
def weblink(*args):
    selection = lb.curselection()
    if not selection : 
        return
    if not currentUrls : 
        return
    index = selection[0]
    item = currentUrls[index]
    webbrowser.open_new(item)

#Insert The url in the list
def printUrl(*args): 
    currentUrls.clear()
    lb.delete(0, END)
    tupleUrlTFIDF = intersection_of_results(find_some_words(index1, index2, index3))
    listeUrl = []
    for tupleUrl in tupleUrlTFIDF :
        listeUrl.append(tupleUrl[0])

    if not listeUrl : 
        lb.insert(END, "No result for this search.")
        return
    
    for url in listeUrl :
        url = url.rstrip('\n')
        currentUrls.append(url)
        lb.insert(END, url_to_title(url))
        
#Clear the list and the input entry
def deleteUrl() :
    lb.delete(0, END)
    keywordInput.delete(0, END)
    
########################## Main ##########################

#Open the csv file
doc = open('TED_transcripts.csv', 'r', encoding='utf-8')
dictionnaire = csv_to_dict(doc)

print('Index charging...')
index1 = index_words_to_urls(dictionnaire)
index2 = index_words_to_idf(index1)
index3 = index_urls_to_words(dictionnaire)
print('Index charged.')

########################## Fin Initialisation Interface Graphique ##########################

#Creation of a button that will submit the keywords
button= ttk.Button(top, text="Search", command= printUrl)
button.pack(side=LEFT, padx=5)

buttonDelete = ttk.Button(top, text="Clear", command= deleteUrl)
buttonDelete.pack(side=LEFT)


#Creation of a ListBox where all the urls will be
lb = Listbox(bottom,  yscrollcommand = scrollbar.set, font=('Segoe UI', 10),
             activestyle="none", borderwidth=0, highlightthickness=0)
lb.bind('<<ListboxSelect>>', weblink)
lb.pack(side=LEFT, fill=BOTH, expand=True)

keywordInput.bind('<Return>', printUrl)

scrollbar.config(command=lb.yview)
     
root.mainloop()
