#!/home/nick/.virtualenvs/twitterbots/bin/python3.5

import tweepy
import sqlite3
from configparser import ConfigParser


def main():

    parser = ConfigParser()
    parser.read('twitter_auth.ini')

    consumer_key = parser.get('Keys',
                              'consumer_key').strip("'")
    consumer_secret = parser.get('Secrets',
                                 'consumer_secret').strip("'")
    access_token = parser.get('Tokens',
                              'access_token').strip("'")
    access_token_secret = parser.get('Secrets',
                                     'access_token_secret').strip("'")

    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth, wait_on_rate_limit=True)

    conn = sqlite3.connect('tweet_dump.db')
    c = conn.cursor()

    c.execute('SELECT user_id FROM tdump ORDER BY user_id ASC')
    tweets = [x[0] for x in c.fetchall()]

    seen = []
    count = 0

    for tweet in tweets:

        if tweet not in seen:

            get_id = api.get_user(tweet)
            id_ = get_id.id_str
            screen_name = get_id.screen_name
            count += 1
            if count % 1000 == 0:
                print(count)

            if tweet != id_:

                print(tweet, id_, screen_name)

            seen.append(tweet)


if __name__ == '__main__':
    main()
