# -*- coding: utf-8 -*-
"""
Created on Fri Dec 17 07:11:46 2021

@author: Administrator
"""


import neuralcoref
import csv
import spacy

nlp = spacy.load('en_core_web_sm')  # load the model
neuralcoref.add_to_pipe(nlp)
bookname='Pride_and_Prejudice'

rawfilepath= 'inputs/'+bookname+'_v1.txt'
# with open(rawfilepath, encoding="utf8") as f:
#     booktext = list(f)

with open(rawfilepath, encoding="utf8") as f:
    booktext = list(f)    

booktext = ' '.join(booktext)

print(booktext)