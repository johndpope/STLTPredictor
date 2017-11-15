from twython import Twython, TwythonError, TwythonRateLimitError
import sqlite3 as lite
import time
from textblob import TextBlob
import re
import data
from multiprocessing.dummy import Pool as ThreadPool
import csv

class Company(object):
    def __init__(self, symbol, name, sector):
        self.symbol = symbol
        self.name = name
        self.sector = sector
        self.sentiment = 0
    def set_sentiment(self, sentiment):
        self.sentiment += sentiment

class TwitterClient(object):
    def __init__(self):
        API_KEY = data.API_KEY
        API_SECRET = data.API_SECRET
        ACCESS_TOKEN = data.ACCESS_TOKEN
        ACCESS_TOKEN_SECRET = data.ACCESS_TOKEN_SECRET
        try:
            self.auth = Twython(API_KEY, API_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
            self.auth.verify_credentials()
        except:
            print "error: authentication"
    def clean_tweet(self, tweet):
        return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet).split())
    def get_tweet_sentiment(self, tweet):
        analysis = TextBlob(self.clean_tweet(tweet))
        # set sentiment
        return analysis.sentiment.polarity

    def get_tweets(self, query, count = 10):
        tweets = []
        retry = 0
        while(retry < 5):
            try:
                fetched_tweets = self.auth.search(q=query.name + " OR " + query.symbol + " -filter:retweets AND -filter:replies", count=count)
                fetched_tweets = fetched_tweets['statuses']
                for tweet in fetched_tweets:
                    parsed_tweet = {}
                    parsed_tweet['company'] = query
                    parsed_tweet['sentiment'] = self.get_tweet_sentiment(tweet['text'])
                    tweets.append(parsed_tweet)

                return tweets
            except TwythonRateLimitError as e:
                to_sleep = float(self.auth.get_lastfunction_header('x-rate-limit-reset')) - time.time()
                print "need to sleep for {0} seconds".format(int(to_sleep))
                retry += 1
                time.sleep(to_sleep)
            except TwythonError as e:
                return []

def main():
    companies = []
    with open('known.csv', 'r') as f:
        reader = csv.reader(f)
        for row in reader:
            companies.append(Company(row[0], row[1], row[2]))

    pool = ThreadPool(len(companies))
    api = TwitterClient()
    results = pool.map(api.get_tweets, companies)

    pool.close()
    pool.join()
    for re in results:
        for r in re:
            companies[next(index for (index, d) in enumerate(companies) if d.name == r['company'].name)].set_sentiment(float(r['sentiment']))

    for c in companies:
        print c.name + "|" + str(c.sentiment)

if __name__ == "__main__":
    main()
