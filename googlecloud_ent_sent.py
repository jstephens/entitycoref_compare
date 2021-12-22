# -*- coding: utf-8 -*-
"""
Created on Sat Dec 18 00:15:54 2021

@author: Jamie Stephens

Input: raw text of novel containing chapters beginning with 'Chapter'
Output: CSV file with entity information per new paragraph 

"""
import os
from google.cloud import language_v1
import csv
import pandas as pd

os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="C:/Users/Administrator/AppData/Local/Google/nsp-name-4c144f293297.json"

def analyze_entity_sentiment(bookname, version,text_content, chapterno,characters):

    client = language_v1.LanguageServiceClient()
    # Available types: PLAIN_TEXT, HTML
    type_ = language_v1.types.Document.Type.PLAIN_TEXT

    # Optional. If not specified, the language is automatically detected.
    # For list of supported languages:
    # https://cloud.google.com/natural-language/docs/languages
    language = "en"
    document = {"content": text_content, "type_": type_, "language": language}

    # Available values: NONE, UTF8, UTF16, UTF32
    encoding_type = language_v1.EncodingType.UTF8

    response = client.analyze_entity_sentiment(request = {'document': document, 'encoding_type': encoding_type})
    
    for entity in response.entities:        
        # print(u"Representative name for the entity: {}".format(entity.name))
        
        # language_v1.Entity.Type(entity.type_).name ---> entity type, e.g. PERSON, LOCATION, ADDRESS, NUMBER, et al
        # print(u"Entity type: {}".format(language_v1.Entity.Type(entity.type_).name))
        
        # Get the salience score associated with the entity in the [0, 1.0] range
        # print(u"Salience score: {}".format(entity.salience))
        
        # Get the aggregate sentiment expressed for this entity in the provided document.
        
        # print(u"Entity sentiment score: {}".format(sentiment.score))
        # print(u"Entity sentiment magnitude: {}".format(sentiment.magnitude))
        # Loop over the metadata associated with entity. For many known entities,
        # the metadata is a Wikipedia URL (wikipedia_url) and Knowledge Graph MID (mid).
        # Some entity types may have additional metadata, e.g. ADDRESS entities
        # may have metadata for the address street_name, postal_code, et al.
        # for metadata_name, metadata_value in entity.metadata.items():
        #     print(u"{} = {}".format(metadata_name, metadata_value))

        # Loop over the mentions of this entity in the input document.
        # The API currently supports proper noun mentions.
        # for mention in entity.mentions:
        #     print(u"Mention text: {}".format(mention.text.content))
        #     # Get the mention type, e.g. PROPER for proper noun
        #     print(
        #         u"Mention type: {}".format(language_v1.EntityMention.Type(mention.type_).name)
        #    )
        sentiment = entity.sentiment
        arr = [chapterno, entity.name, language_v1.Entity.Type(entity.type_).name,entity.salience,sentiment.score,sentiment.magnitude]
        if arr[1] == 'Elizabeth' or arr[1] == 'Charlotte' or arr[1] == 'Charles' or arr[1] == 'Jane' or arr[1] == 'Caroline' or arr[1] == 'Lydia' or arr[1] == 'Fitzwilliam':
            filepathway = 'input/'+bookname +version+ '_gcloud.csv'
            f = open(filepathway, "a")
            writer = csv.writer(f)
            writer.writerow(arr)
            f.close()
    return 0

bookname='Pride_and_Prejudice'
version = '_v3_allennlp'
rawfilepath= 'input/'+bookname + version+ '.txt'

with open(rawfilepath, encoding="cp1252") as f:
    booktext = list(f)    

booktext = ' '.join(booktext)
booktext1 = booktext.split('Chapter')

rawcharacterpath = 'input/'+bookname+'_characters.csv'

characterdf = pd.read_csv(rawcharacterpath,names=['Names'])
characters = characterdf['Names'].tolist()

i= 1
for x in booktext1:
    x.replace('Chapter','')
    y = x.split('\n')
    if i > 0: 
        for a in y:
            a.replace('\n','')
            if len(a)> 4:
                print(a)
                if 'Elizabeth' in a or 'Fitzwilliam' in a or 'Jane' in a or 'Charlotte' in a or 'Charles' in a or 'Caroline' in a or 'Lydia' in a:
                    analyze_entity_sentiment(bookname,version,a,i,characters)
    print(i)
    i += 1