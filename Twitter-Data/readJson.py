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
collection = app_config.MongoConnection()

coord_list=[]
f = open(r'C:\Users\User\Desktop\CCC Tweets\bigTwitter.json',"r")
objects = ijson.items(f,'item.json')
for ind,it in enumerate(objects):
    #try 60000 to 80000
    #try 100000 to 250000
    if ind < 331284:
        continue
    if ind == 331290:
        logger.info('Ok')
    tweet_ = it
    clean_tweet_text=TwitterSentiment.processTweet(tweet_['text'])
    try:
        tweet_['coordinates']['coordinates'][0]=float(it['coordinates']['coordinates'][0])
        tweet_['coordinates']['coordinates'][1]=float(it['coordinates']['coordinates'][1]) 
    except Exception as e:
        logger.error(e)
    
    try:
        tweet_['geo']['coordinates'][0]=float(it['geo']['coordinates'][0])
        tweet_['geo']['coordinates'][1]=float(it['geo']['coordinates'][1])  
    except Exception as e:
        logger.error(e)

    try:
        for index,item in enumerate(tweet_['place']['bounding_box']['coordinates'][0]):
            tweet_['place']['bounding_box']['coordinates'][0][index][0]=float(it['place']['bounding_box']['coordinates'][0][index][0])
            tweet_['place']['bounding_box']['coordinates'][0][index][1]=float(it['place']['bounding_box']['coordinates'][0][index][1])
    except Exception as e:
        logger.error(e)


    sentiment=TwitterSentiment.getSentiment(clean_tweet_text)
    tweet_['sentiment']=sentiment
    tweet_['clean_text']=clean_tweet_text
    tweet_['_id']=tweet_['id_str']
    #print it
    try:
        collection.insert_one(tweet_)
        #logger.info('Wrote Tweet Succesfully, '+str(ind))
    except Exception as e:
        logger.error('Error Ocurred Database Write, '+str(ind))
        logger.error(e)