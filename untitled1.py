# -*- coding: utf-8 -*-
"""
Created on Fri Dec 17 07:59:49 2021

@author: Administrator
"""


from allennlp.predictors.predictor import Predictor
import allennlp_models.tagging
from ncr.replace_corefs import resolve

predictor = Predictor.from_path("https://storage.googleapis.com/allennlp-public-models/coref-spanbert-large-2021.03.10.tar.gz")
    
def prediction(bookname,version,text):
    outputpath = './input/'+bookname+'_v3_allennlp.txt'
    file1 = open(outputpath, "a")
    file1.write('Chapter')
    file1.close()
    
    try:
        xyz = predictor.predict(document=text)
        resolved_toks = resolve(xyz['document'], xyz['clusters'])
        chapteroutput = ' '.join(resolved_toks)
        print(chapteroutput)
        file1 = open(outputpath, "a")
        file1.write(chapteroutput)
        file1.close()
    except:
        file1 = open(outputpath, "a")  # append mode
        file1.write(text)
        print("Didn't do prediction")
        file1.close()
        
bookname='Pride_and_Prejudice'
version = '_v1'
rawfilepath= 'input/'+bookname + version+ '.txt'

with open(rawfilepath, encoding="utf8") as f:
    booktext = list(f)    

booktext = ' '.join(booktext)
booktext1 = booktext.split('Chapter')

counter = 1
for y in booktext1:
    y.replace('Chapter','')
    print(counter)
    prediction(bookname,version,y)
    counter += 1