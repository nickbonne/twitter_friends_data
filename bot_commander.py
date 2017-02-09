#!/home/nick/.virtualenvs/twitterbots/bin/python3.5

import re
import os
import json
import time
import tweepy
import sqlite3

from user_data import AllData
from user_data import ScreenNames
from request_process import Screen
from tweet_collect import Collector
from datetime import datetime as dt
from configparser import ConfigParser


def main():

    Actions.run_listener()


class MyStreamListener(tweepy.StreamListener):

    def on_status(self, status):

        print(status.text)

    def off_status(self, status):

        print(status.text)

    def on_data(self, data):

        friend_ids = ScreenNames.screennames()

        all_data = json.loads(data)
        tweet = all_data["text"]
        created_at = all_data["created_at"]
        username = all_data["user"]["screen_name"]
        user_id = all_data["user"]["id_str"]
        tweet_id = all_data["id"]

        tweet_source = all_data["source"]
        tweet_source = str(re.search(r'\>(.*?)\<',
                           tweet_source).group(0))[1:-1]

        tweet_data = [tweet,
                      username,
                      created_at,
                      tweet_id,
                      tweet_source,
                      user_id]

        if user_id in friend_ids:

            print('{}({}) - {}'.format(username, created_at, tweet))
            print()

        if '@BonneNick' in tweet:

            Actions.add_mention_db(tweet_data)
            Screen.is_command(tweet_data)

        return True

    def on_error(self, status_code):

        if status_code == 420:

            # disconnects stream
            return False


class Actions:

    def db_connect():

        conn = sqlite3.connect('tweet_dump_main.db')
        c = conn.cursor()

        return c, conn

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

    def run_collector():

        Collector.collect()
        CopyDb.copy_database()

    def run_listener():

        api = Actions.get_api()
        friend_ids = AllData.friend_ids()

        while True:

            try:

                myStreamListener = MyStreamListener()
                myStream = tweepy.Stream(auth=api.auth,
                                         listener=myStreamListener)

                myStream.filter(follow=friend_ids)

            except Exception as e:

                print(str(e) + '\n')
                continue

    # looks for any commands missed by listener
    def check_db_cmds():

        filename = '/home/nick/.virtualenvs/twitterbots/bots/' +\
            'control_files/last_cmd_check.txt'

        with open(filename, 'r') as f:

            last_seen = int(f.read().strip())

        # main tweet dump connection
        db_conn = Actions.db_connect()
        c = db_conn[0]

        c.execute('''SELECT *
                     FROM tdump''')

        tweets = c.fetchall()
        new_tweets = [x for x in tweets if int(x[3]) > last_seen]
        new_tweets = sorted(new_tweets,
                            key=lambda x: int(x[3]),
                            reverse=True)

        mention_db = Collector.mention_tweet_db()
        mention_c = mention_db[0]

        mention_c.execute('SELECT tweet_id FROM mentioned')
        mentioned_ids = [x[0] for x in mention_c.fetchall()]

        for tweet in new_tweets:

            if '@BonneNick' in tweet[0] and \
               tweet[3] not in mentioned_ids:

                Actions.add_mention_db(tweet)
                Screen.is_command(tweet)

        if len(new_tweets) > 0:

            with open(filename, 'w') as f:

                f.write(new_tweets[0][3])

    def add_mention_db(tweet):

        db = Collector.mention_tweet_db()
        c = db[0]
        conn = db[1]

        c.execute('''INSERT INTO mentioned
                             (tweet,
                              username,
                              tweet_date,
                              tweet_id,
                              tweet_source,
                              user_id)
                     VALUES(?,?,?,?,?,?)''',
                  [tweet[0],
                   tweet[1],
                   tweet[2],
                   tweet[3],
                   tweet[4],
                   tweet[5]])

        conn.commit()

    def requests_serve(tweet):

        request = Screen.is_command(tweet)

        # if False
        if not request[0]:

            Actions.reply_request(tweet, request[1])

        elif request[0]:

            Actions.reply_request(tweet)

    # for replying with a standard tweet
    def reply_request(tweet_data, *args, **kwargs):

        api = Actions.get_api()

        username = tweet_data[1]
        reply_id = tweet_data[2]
        img = tweet_data[3]
        message = username + ', here is the graphic you requested.'

        if args:

            message = args
            api.update_status(status=message,
                              in_reply_to_status_id=reply_id)

        else:

            api.update_with_media(img,
                                  status=message,
                                  in_reply_to_status_id=reply_id)


class CopyDb:

    def last_modified():

        path = '/home/nick/.virtualenvs/twitterbots/bots/tweet_dump_main.db'

        if os.path.getmtime(path) > 6000:

            CopyDb.copy_database(path)

    def copy_database(source_path):

        dst = '/home/nick/.virtualenvs/twitterbots/bots/tweet_dump.db'

        shutil.copy2(source_path,
                     dst)


if __name__ == '__main__':

    main()
