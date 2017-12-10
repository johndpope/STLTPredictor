from twython import Twython, TwythonError, TwythonRateLimitError
import sqlite3
import time
import datetime
from textblob import TextBlob
import re
import data
from multiprocessing.dummy import Pool as ThreadPool
import csv
import sys
sys.path.append("./GetOldTweets-python-master/")
import got
from functools import partial

# import pandas_datareader.data as web
# import pandas as pd

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
        """
        1) tokenizes tweet
        2) removes stop words
        3) does part of speech tagging, selecting significant words
        4) pass tokens to sentiment classifier which labels tokens from -1 to 1
           based on data trained from a Naive Bayes Classfier
        """
        analysis = TextBlob(self.clean_tweet(tweet))
        return analysis.sentiment.polarity
    # def get_tweets(self, query, count = 50):
    #     tweets = []
    #     retry = 0
    #     while(retry < 5):
    #         try:
    #             """
    #             search for tweets or replies that countain the company name or
    #             stock symbol get sentiment for a tweet, record the company and
    #             add to array to be returned
    #             """
    #
    #             fetched_tweets = self.auth.search(q=query.name + " OR " + query.symbol + " -filter:retweets", count=count)
    #             fetched_tweets = fetched_tweets['statuses']
    #             for tweet in fetched_tweets:
    #                 parsed_tweet = {}
    #                 parsed_tweet['company'] = query
    #                 parsed_tweet['tweet'] = tweet['text'].encode('utf8')
    #                 parsed_tweet['sentiment'] = self.get_tweet_sentiment(tweet['text'].encode('utf8'))
    #                 tweets.append(parsed_tweet)
    #
    #             return tweets
    #         except TwythonRateLimitError as e:
    #             """
    #             if we hit the rate limit, get the UTC epoch formatted time when
    #             the limit will be reset, and wait for that long retry this 5
    #             times, there is sort of a race condition here, as all remaining
    #             threads in the pool will compete for resources (querying twitter)
    #             """
    #             to_sleep = float(self.auth.get_lastfunction_header('x-rate-limit-reset')) - time.time()
    #             print "need to sleep for {0} seconds".format(int(to_sleep))
    #             retry += 1
    #             time.sleep(to_sleep)
    #         except TwythonError as e:
    #             print e
    #             return []

    def get_tweets_from_past(self, query, start, end, count = 200):
        tweets = []

        """
        search for tweets or replies that countain the company name or
        stock symbol get sentiment for a tweet, record the company and
        add to array to be returned
        """
        fetched_tweets = got.manager.TweetManager.getTweets(got.manager.TweetCriteria().setQuerySearch(query.name + " OR " + query.symbol).setSince(start).setUntil(end).setMaxTweets(count))

        for tweet in fetched_tweets:
            parsed_tweet = {}
            parsed_tweet['company'] = query
            parsed_tweet['tweet'] = tweet.text
            parsed_tweet['sentiment'] = self.get_tweet_sentiment(tweet.text)
            tweets.append(parsed_tweet)

        return tweets
def update_database(companies):
    conn = sqlite3.connect('../static/project_db.sqlite')
    with conn:
        cur = conn.cursor()
        cur.execute("CREATE TABLE IF NOT EXISTS Company (symbol TEXT PRIMARY KEY UNIQUE, name TEXT UNIQUE, sector TEXT, overall_sentiment REAL default 0);")
        cur.execute("CREATE TABLE IF NOT EXISTS Sentiment (sid INTEGER PRIMARY KEY UNIQUE, value REAL, date_added TEXT, company_symbol TEXT, FOREIGN KEY(company_symbol) REFERENCES Company(symbol));")

    for c in companies:
        with conn:
            cur = conn.cursor()
            cur.execute("SELECT overall_sentiment from Company WHERE symbol=?", (c.symbol,))
            cur_sent = cur.fetchone()
            if cur_sent is None:
                cur.execute("INSERT OR REPLACE INTO Company(symbol, name, sector, overall_sentiment) VALUES (?, ?, ?, ?);", \
                        (c.symbol, c.name, c.sector, c.sentiment))
            else:
                cur_sent = float(cur_sent[0])
                # partial solution to not adding to sentiment if same
                if cur_sent != c.sentiment:
                    cur.execute("INSERT OR REPLACE INTO Company(symbol, name, sector, overall_sentiment) VALUES (?, ?, ?, ?);", \
                            (c.symbol, c.name, c.sector, cur_sent + c.sentiment))


            dt = datetime.utcnow().strftime('%Y%m%d')
            cur.execute("INSERT INTO Sentiment(value, date_added, company_symbol) VALUES (?, ?, ?);", \
                        (c.sentiment, str(dt), c.symbol))
    conn.commit()
    conn.close()

def main(company, start_date):
    # create array of Company objects from selected csv file
    companies = []
    with open('../static/companyList.csv', 'r') as f:
        reader = csv.reader(f)
        for row in reader:
            companies.append(Company(row[0], row[1], row[2]))
    if len(companies) == 0:
        print "{0} not found".format(company)
        return 0
    mycomp = [x for x in companies if x.symbol == company]


    """
    create N threads in a pool
    each thread will query twitter with the company info
    store in results
    """
    start_d = datetime.datetime.strptime(start_date, "%Y-%m-%d")
    end_d = start_d + datetime.timedelta(days=7)


    pool = ThreadPool(len(mycomp))
    api = TwitterClient()
    from_past = partial(api.get_tweets_from_past, start=start_d.strftime("%Y-%m-%d"), end=end_d.strftime("%Y-%m-%d"))
    results = pool.map(from_past, mycomp)
    pool.close()
    pool.join()

    for re in results:
        for r in re:
            #increment sentiment of selected company
            try:
                mycomp[next(index for (index, d) in enumerate(mycomp) if d.name == r['company'].name)].set_sentiment(float(r['sentiment']))
            except:
                continue
        #average out that companies sentiment on a tweet by tweet basis
        try:
            mycomp[next(index for (index, d) in enumerate(mycomp) if d.name == re[0]['company'].name)].sentiment = mycomp[next(index for (index, d) in enumerate(mycomp) if d.name == re[0]['company'].name)].sentiment / len(re)
        except:
            continue


    # for c in mycomp:
    #     print c.name + "|" + str(c.sentiment)

    return mycomp[0].sentiment
    #update_database(companies)

if __name__ == "__main__":
    print main("TSLA", "2017-04-30")
