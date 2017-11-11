#!/usr/bin/python
import json, time, sys,os
import tweepy
import app_config

#Logging
from app_config import custom_logger
logger=custom_logger(__name__,'logs/search.log')

start_time = time.time()
start_query=time.time()
sleep_time = 600

auth = tweepy.AppAuthHandler(app_config.CONSUMER_KEY, app_config.CONSUMER_SECRET)
api = tweepy.API(auth, wait_on_rate_limit=True,wait_on_rate_limit_notify=True)

if (not api):
    logger.error('API Error')
    sys.exit()

# Setup Parameters
search_list = app_config.WORDS
tweetsPerQry = 100

# Setup Tweepy Parameters
sinceId = None
max_id = -1

# Initialize Dict for Max_Id and Since_Id of each keyword
query_maxid={}
query_sinceid={}
for i in search_list:
    query_maxid[i] = -1
    query_sinceid[i] = None

#Melbourne Area
geocode = '-37.810279,144.962619,100000mi'

word_index=0
total_words = len(search_list)
tweetCount = 0

while True:
    
    if (word_index>total_words-1):
        word_index=0

    if (time.time()-start_time) > sleep_time:
        word_index = 0
        logger.warning('Reached the end of the Loop, taking a break...')
        time.sleep(sleep_time)
        start_time = time.time()


    searchQuery = search_list[word_index]
    # Get values
    temp_maxid = query_maxid[searchQuery]
    temp_sinceid = query_sinceid[searchQuery]
    logger.info('Searching For: ' + searchQuery)
    try:
        if (temp_maxid <= 0):
            if (not temp_sinceid):
                new_tweets = api.search(q=searchQuery, count=tweetsPerQry,geocode=geocode)
            else:
                new_tweets = api.search(q=searchQuery, count=tweetsPerQry,geocode=geocode,
                                        since_id=sinceId)
        else:
            if (not temp_sinceid):
                new_tweets = api.search(q=searchQuery, count=tweetsPerQry,geocode=geocode,
                                        max_id=str(temp_maxid - 1))
            else:
                new_tweets = api.search(q=searchQuery, count=tweetsPerQry,geocode=geocode,
                                        max_id=str(temp_maxid - 1),
                                        since_id=sinceId)
        if not new_tweets:
            if tweetCount % 18000 == 0:
                logger.warning('Reached 18k limit, sleeping')
                time.sleep(sleep_time)
                start_time=time.time()

            if (time.time()-start_time)>14*60:
                logger.warning('Reached 15 minute limit, sleeping')
                time.sleep(sleep_time)
                start_time=time.time()
                
            word_index += 1
            continue
        
        for tweet in new_tweets:
            # Push to Queue
            logger.info("Ok")

        word_index += 1     
        tweetCount += len(new_tweets)

        # Update Tweets Window
        query_maxid[searchQuery] = new_tweets[-1].id
        query_sinceid[searchQuery] = new_tweets[0].id
    
    except tweepy.TweepError as e:
        logger.error("tweepy Exception Exit")
        logger.error(e)
        sys.exit()

    except Exception as e:
        logger.error("Exception Exit")
        logger.error(e)
        sys.exit()