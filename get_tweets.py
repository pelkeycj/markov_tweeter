'''
get_tweets.py

Gather all tweets for a provided screen_name and store in a csv file.
Subsequent tweets will be appended regularly using another file

'''

import tweepy
import csv
import auth_keys as ak

consumer_key = ak.CONSUMER_KEY
consumer_secret = ak.CONSUMER_SECRET
access_token = ak.ACCESS_TOKEN
access_secret = ak.ACCESS_TOKEN_SECRET

def get_tweets(screen_name):
        #authorize twitter
        auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_token, access_secret)
        api = tweepy.API(auth)

        #initial request for newest tweets, append 
        all_tweets = []
        new_tweets = api.user_timeline(screen_name = screen_name, count=200) #200 is the max allowed
        all_tweets.extend(new_tweets)

        
        oldest_tweet = all_tweets[-1].id -1
        while len(new_tweets) > 0:
                print('getting tweets before %s' % (oldest_tweet))
                #get next 200 tweets older than the current oldest
                new_tweets = api.user_timeline(screen_name = screen_name,
                                               count=200, max_id=oldest_tweet)
                all_tweets.extend(new_tweets)
                oldest_tweet = all_tweets[-1].id - 1

                print('. . .%s tweets downloaded so far . . .' % (len(all_tweets)))

        #create matrix to populate csv
        out_tweets = [[tweet.id_str, tweet.created_at,
                       tweet.text.encode('utf-8')] for tweet in all_tweets]

        
        with open('%s_tweets.csv' % screen_name, 'w') as writefile:
                writer = csv.writer(writefile)
                writer.writerow(['id', 'created_at', 'text'])
                writer.writerows(out_tweets)

if __name__ == '__main__':
        get_tweets('VancityReynolds')

        
