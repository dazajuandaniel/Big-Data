#!/usr/bin/python
import json,jsonpickle,ijson
import tweepy
import TwitterSentiment
import secret
import app_config

#Logging
from app_config import setup_custom_logger
logger=setup_custom_logger(__name__,'log/bigTwitter.log')

import sys,os,time
start_time = time.time()
start_query=time.time()

#Database Config
collection = app_config.MongoConnection(host = 'localhost',db = secret.DB,collection = secret.COLLECTION)


coord_list=[]
f = open(secret.FILE_ADDRESS,"r")
objects = ijson.items(f,'item.json')
for ind,it in enumerate(objects):
    
    tweet_ = it
    clean_tweet_text=TwitterSentiment.processTweet(tweet_['text'])
    
    try:
        tweet_['coordinates']['coordinates'][0]=float(it['coordinates']['coordinates'][0])
        tweet_['coordinates']['coordinates'][1]=float(it['coordinates']['coordinates'][1]) 
    except Exception as e:
        logger.error(e+str(ind))
    
    try:
        tweet_['geo']['coordinates'][0]=float(it['geo']['coordinates'][0])
        tweet_['geo']['coordinates'][1]=float(it['geo']['coordinates'][1])  
    except Exception as e:
        logger.error(e+str(ind))

    try:
        for index,item in enumerate(tweet_['place']['bounding_box']['coordinates'][0]):
            tweet_['place']['bounding_box']['coordinates'][0][index][0]=float(it['place']['bounding_box']['coordinates'][0][index][0])
            tweet_['place']['bounding_box']['coordinates'][0][index][1]=float(it['place']['bounding_box']['coordinates'][0][index][1])
    except Exception as e:
        logger.error(e+str(ind))

    sentiment=TwitterSentiment.getSentiment(clean_tweet_text)
    tweet_['sentiment']=sentiment
    tweet_['clean_text']=clean_tweet_text
    tweet_['_id']=tweet_['id_str']
    
    try:
        collection.insert_one(tweet_)
        logger.info(str(ind))
    except Exception as e:
        logger.error('Error Ocurred Database Write, '+str(ind))
        logger.error(e)