#!/usr/bin/python
import json,jsonpickle
import tweepy
import TwitterSentiment
import secret
import app_config

#Logging
from app_config import setup_custom_logger
logger=setup_custom_logger(__name__,'log/SearchHarvester.log')

import sys,os,time
start_time = time.time()
start_query=time.time()

#Database Config
collection = app_config.MongoConnection()

auth = tweepy.AppAuthHandler(secret.CONSUMER_KEY, secret.CONSUMER_SECRET)
api = tweepy.API(auth, wait_on_rate_limit=True,wait_on_rate_limit_notify=True)
if (not api):
    logger.error('API Error')
    sys.exit()

#Search KeyWords
words=['#Australia','australia','customer service','customer','amazon',
'field service','utility','coca-cola','essential energy',
'melbourne','sydney','perth australia','victoria australia','#afl']

searchList=words
maxTweets = 100000000000000
tweetsPerQry = 100
sinceId = None
max_id = -1L

#Initialize Dict for Max_Id of each keyword
query_maxid={}
for i in words:
    query_maxid[i]=-1L

# Search Criteria
lang = 'en'
#Melbourne Area
geocode = '-37.810279,144.962619,100000mi'

searchListCount=0
maxlistcount=len(searchList)
tweetCount = 0
loops = 0
while tweetCount < maxTweets:
    loops+=1
    
    if (searchListCount>maxlistcount-1):
        searchListCount=0

    if (loops>maxlistcount*5) or (time.time()-start_time)>14*60 or (searchListCount>maxlistcount-1):
        searchListCount=0
        logger.warning('Reached the end of the Loop, taking a break...')
        time.sleep(15*60)
        start_time=time.time()
        collection = app_config.MongoConnection()
        loops=0

    searchQuery=searchList[searchListCount]
    logger.info('Searching For: '+searchQuery)
    try:
        if (query_maxid[searchQuery] <= 0):
        #if (max_id <= 0):
            if (not sinceId):
                new_tweets = api.search(q=searchQuery, count=tweetsPerQry,lang=lang,geocode=geocode)
            else:
                new_tweets = api.search(q=searchQuery, count=tweetsPerQry,lang=lang,geocode=geocode,
                                        since_id=sinceId)
        else:
            if (not sinceId):
                new_tweets = api.search(q=searchQuery, count=tweetsPerQry,lang=lang,geocode=geocode,
                                        max_id=str(query_maxid[searchQuery] - 1))
            else:
                new_tweets = api.search(q=searchQuery, count=tweetsPerQry,lang=lang,geocode=geocode,
                                        max_id=str(query_maxid[searchQuery] - 1),
                                        since_id=sinceId)
        if not new_tweets:
            
            if tweetCount%18000==0:
                logger.warning('Reached 18k limit, sleeping for 15 minutes')
                time.sleep(15*60)
                start_time=time.time()
                collection = app_config.MongoConnection()

            if (time.time()-start_time)>14*60:
                logger.warning('Reached 15 minute limit, sleeping for 15 minutes')
                time.sleep(15*60)
                start_time=time.time()
                collection = app_config.MongoConnection()
                
            searchListCount+=1
            continue
        
        for tweet in new_tweets:
            tweet_ = json.loads(jsonpickle.encode(tweet._json, unpicklable=False))
            clean_tweet_text=TwitterSentiment.processTweet(tweet_['text'])
            sentiment=TwitterSentiment.getSentiment(clean_tweet_text)
            tweet_['sentiment']=sentiment
            tweet_['clean_text']=clean_tweet_text
            tweet_['_id']=tweet_['id_str']
            try:
                collection.insert_one(tweet_)
                logger.info('Wrote Tweet Succesfully')
            except Exception as e:
                logger.error('Error Ocurred Database Write')
                logger.error(e)
        
        searchListCount+=1     
        tweetCount += len(new_tweets)
        query_maxid[searchQuery] = new_tweets[-1].id

        if (time.time()-start_query)>1296000:
            for i in words:
                query_maxid[i]=-1L
            start_query=time.time()
            logger.info("Resetting maxid, more than two weeks have passed...")
    
    except tweepy.TweepError as e:
        logger.error("tweepy Exception Exit")
        logger.error(e)
        sys.exit()

    except Exception as e:
        logger.error("Exception Exit")
        logger.error(e)
        searchListCount+=1
        sys.exit()