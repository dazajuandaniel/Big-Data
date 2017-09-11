#!/usr/bin/python
import json#,jsonpickle,ijson
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
collection = app_config.MongoConnection(db = secret.DB,collection = secret.COLLECTION)

count = 0
with open(secret.FILE_ADDRESS) as f:
    for line in f:
        try:
            data = json.loads(line[0:len(line) - 2])
            tweet_ = data['json']
            count = count + 1
        except Exception as e:
            logger.error(e)
            count = count + 1
            continue
        
        clean_tweet_text=TwitterSentiment.processTweet(tweet_['text'])
        
        sentiment=TwitterSentiment.getSentiment(clean_tweet_text)
        tweet_['sentiment']=sentiment
        tweet_['clean_text']=clean_tweet_text
        tweet_['_id']=tweet_['id_str']
        
        try:
            collection.insert_one(tweet_)
            logger.info("Ok Database")
        except Exception as e:
            logger.error('Error Ocurred Database Write, '+str(count))
            logger.error(e)
            continue

    logger.info("Done")