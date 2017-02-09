#!/home/nick/.virtualenvs/twitterbots/bin/python3.5

import tweepy
import sqlite3
import datetime

from datetime import datetime as dt
from configparser import ConfigParser


def main():

    pass


class Connect:

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

    def db_connect():

        # for connecting to main dump db
        conn = sqlite3.connect('tweet_dump_main.db')
        c = conn.cursor()

        return c, conn


class TimeFix():

    def timezones():

        user_utc = []
        api = Connect.get_api()
        db_info = Connect.db_connect()

        c = db_info[0]
        c.execute('''SELECT user_id, username
                     FROM user_data''')
        users_list = c.fetchall()

        for user in users_list:

            user_object = api.get_user(user[0])
            utc_fix = user_object.utc_offset

            if utc_fix is None:

                utc_fix = 0

            user_utc.append([user[0], utc_fix])

        return user_utc

    def append_tz_2_db(user_utc_list):

        db_info = Connect.db_connect()
        c = db_info[0]
        conn = db_info[1]

        for pair in user_utc_list:

            c.execute('''UPDATE user_data
                         SET utc_offset=?
                         WHERE user_id=?''',
                      (pair[1],
                       pair[0]))

        conn.commit()

    # for adjusting tweet times to a user's
    # local time as defined by their utc offset
    def adjust_datetimes(user_id, tweet_list):

        db_conn = Connect.db_connect()
        c = db_conn[0]

        c.execute('''SELECT utc_offset
                     FROM user_data
                     WHERE user_id=?''',
                  [user_id])

        user_time_offset = c.fetchone()[0]

        new_tweet_list = []

        for tweet in tweet_list:

            tweet = list(tweet)
            old_date = tweet[2]

            del tweet[2]

            old_date_obj = dt.strptime(old_date, '%Y-%m-%d %H:%M:%S')
            new_date_obj = old_date_obj +\
                datetime.timedelta(seconds=user_time_offset)

            new_date = dt.strftime(new_date_obj, '%Y-%m-%d %H:%M:%S')
            tweet.insert(2, new_date)
            new_tweet_list.append(tweet)

        return new_tweet_list


if __name__ == '__main__':

    main()
