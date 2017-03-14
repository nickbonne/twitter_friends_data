#!/home/nick/.virtualenvs/twitternews/bin/python3.4

import tweepy

from datetime import datetime as dt
from configparser import ConfigParser


def main():

    pass


class TwtFuncts:

    def get_api():

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

        return api

    def send_tweet(message):

        api = TwtFuncts.get_api()
        api.update_status(status=message)

    def send_comic_tweet(comic_path):

        today = str(dt.today())[:10]
        message = 'Daily comic strip for ' + today

        api = TwtFuncts.get_api()
        api.update_with_media(comic_path,
                              status=message)


if __name__ == '__main__':

    main()
