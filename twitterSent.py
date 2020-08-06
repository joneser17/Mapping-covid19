'''
    @author- Erik Jones
    This program is a twitter sentiment analysis for the main program 'covidMap.py'.Uses twitter api
'''

import re 
import tweepy 
from tweepy import OAuthHandler 
from textblob import TextBlob  
  
class TwitterClient(): 
    ''' 
    Twitter class for sentiment analysis. 
    '''
    def __init__(self): 
        ''' 
        initialization method. 
        '''
        #Keys and tokens for twitter api
        #Removed personal keys, if you wanna use enter your own api for twitter sentiment analysis
        consumer_key = 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'
        consumer_secret = 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'
        access_token = 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'
        access_token_secret = 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'
  
        #Attempts authentication 
        try:  
            self.auth = OAuthHandler(consumer_key, consumer_secret) 
            self.auth.set_access_token(access_token, access_token_secret)  
            self.api = tweepy.API(self.auth) 
        except: 
            print("Error: API code not working") 
    def remove_junk_from_tweet(self, tweet): 
        '''
        Uses regex to remove special character and url links
        '''
        return ' '.join(re.sub(r"(@[A-Za-z0-9]+) | ([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet).split())  
    def sentiment_tweet(self, tweet): 
        ''' 
        classify sentiment of passed tweet using textblob's sentiment method
        '''
        #Create TextBlob object of passed tweet text 
        analysis = TextBlob(self.remove_junk_from_tweet(tweet)) 
        #Set sentiment from the library TextBlob library 
        if analysis.sentiment.polarity > 0: 
            return 'positive'
        elif analysis.sentiment.polarity == 0: 
            return 'neutral'
        else: 
            return 'negative'
  
    
    def get_tweets(self,query,count,listofalltweets): 
        ''' 
        Gets the tweets and does pre-processing. 
        '''
        #Empty list to store parsed tweets
        tweets = [] 
  
        try:  
            fetched_tweets = self.api.search(q = query, count = count) 
            #Parsinging tweets
            for tweet in fetched_tweets: 
                #Empty dictionary to store required params of a tweet 
                parsed_tweet = {} 
                #Checks to see if tweet has already been seen
                if tweet.text not in listofalltweets:
                    #Saving text of tweet 
                    listofalltweets.append(tweet.text)
                    parsed_tweet['text'] = tweet.text 
                    #Saving sentiment of tweet 
                    parsed_tweet['sentiment'] = self.sentiment_tweet(tweet.text) 
                else:
                    continue
                #Adding the tweet to the current tweets list
                if tweet.retweet_count > 0: 
                    #If tweet has retweets, ensure that it is appended only once 
                    if parsed_tweet not in tweets: 
                        tweets.append(parsed_tweet) 
                else: 
                    tweets.append(parsed_tweet) 
  
            #Return the tweets 
            return tweets 
  
        except tweepy.TweepError as a:  
            print("Error: " + str(a)) 
  
def info(): 
    #TwitterClient Class 
    api = TwitterClient() 
    
    #How many total tweets that has been retrieved
    tweetcount = 0

    #These lists will store all of the tweets retrived from twitter, possitive,negative,and neutral respectivally.
    listofalltweets = []
    allPositive = []
    allnegative = []
    allneutral = []

    #Loop to get a new page of tweets each run through. Twitter limits 100 tweets per page, so a range of 10 in this instance will get 10 page of tweets
    #of 100 each, so 1000 total (not aall 100 will be returned because of duplicates).
    for _ in range (0,2):
        tweets = api.get_tweets(query = 'Covid-19', count = 100,listofalltweets = listofalltweets)
        print("Amount of tweets pulled from current page:",len(tweets))
        tweetcount = tweetcount + len(tweets)

        ptweets = [tweet for tweet in tweets if tweet['sentiment'] == 'positive'] 
        allPositive = allPositive + ptweets

        ntweets = [tweet for tweet in tweets if tweet['sentiment'] == 'negative'] 
        allnegative = allnegative + ntweets

        nutweets = [tweet for tweet in tweets if tweet['sentiment'] == 'neutral']
        allneutral = allneutral + nutweets 
    pos = len(allPositive)  
    neg = len(allnegative)
    neu = len(allneutral)

    #The data that needs to be sent to covidMap.py, which is in a dictonary form which includes the emotion,total number of tweets,
    #and the total number of tweets with the highest emotion.
    final_answer = {}
    if(pos > neg and pos > neu):
        final_answer = {'positive' : pos}
        final_answer['emotion'] = 'positive'
    elif(neg > neu and neg > pos):
        final_answer = {'negative' : neg}
        final_answer['emotion'] = 'negative'
    elif(neu > pos and neu > neg):
        final_answer = {'neutral' : neu}
        final_answer['emotion'] = 'neutral'
    final_answer['total'] = tweetcount
    return final_answer                               
