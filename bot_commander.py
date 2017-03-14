#!/home/nick/.virtualenvs/twitterbots/bin/python3.5

import re
import os
import json
import time
import shutil
import tweepy
import sqlite3

from user_data import UserData
from auto_reply import AutoReply
from multiprocessing import Pool
from multiprocessing import Lock
from request_process import Screen
from datetime import datetime as dt
from tweet_collect import Collector
from multiprocessing import Process
from configparser import ConfigParser
from random_status import RandomStatus
from cloud_string_updater import Update


def main():

    Start.start_app()


class Start:

    def start_app():

        process_one = Process(target=Actions.run_listener)
        process_two = Process(target=Actions.job_timer)
        process_three = Process(target=Actions.mention_check)

        process_one.start()
        print('Listener started.')

        process_two.start()
        print('Collections started.')

        process_three.start()
        print('Mention check started.' + '\n')

        process_one.join()
        process_two.join()
        process_three.join()


class MyStreamListener(tweepy.StreamListener):

    '''
    Job of the listener is only to get tweets mentioning
    me and add them to the mentioned table.
    '''

    def on_status(self, status):

        print(status.text)

    def off_status(self, status):

        print(status.text)

    def on_data(self, data):

        friend_ids = UserData.friend_ids()

        all_data = json.loads(data)
        tweet = all_data["text"]
        created_at = all_data["created_at"]
        username = all_data["user"]["screen_name"]
        user_id = all_data["user"]["id_str"]
        tweet_id = all_data["id"]
        reply_id = all_data["in_reply_to_status_id"]

        tweet_source = all_data["source"]
        tweet_source = str(re.search(r'\>(.*?)\<',
                           tweet_source).group(0))[1:-1]

        tweet_data = [tweet,
                      username,
                      created_at,
                      tweet_id,
                      tweet_source,
                      user_id,
                      str(reply_id)]

        if user_id in friend_ids:

            if '@BonneNick' in tweet:

                print('{}({}) - {}'.format(username, created_at, tweet))

                Actions.add_mention_db(tweet_data)

                if reply_id is not None:

                    AutoReply.check_4_id(Actions.get_api(),
                                         reply_id,
                                         tweet_id,
                                         username)

            else:

                print('{}({}) - {}'.format(username, created_at, tweet))

            print()

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

    # Where tweets are actually logged into the tdump table
    # tweets caught by listener only go into mentioned table
    def run_collector():

        lock = Lock()

        lock.acquire()
        Collector.collect()
        Actions.check_db_mention()
        Update.updater()
        time.sleep(5)
        UserData.user_database()
        CopyDb.copy_database()
        lock.release()

    # calls run_collector every 5 min
    # checks date and time for auto_status
    def job_timer():

        while True:

            Actions.auto_status_date()
            Actions.run_collector()
            time.sleep(300)

    def run_listener():

        api = Actions.get_api()
        friend_ids = UserData.friend_ids()

        while True:

            try:

                myStreamListener = MyStreamListener()
                myStream = tweepy.Stream(auth=api.auth,
                                         listener=myStreamListener)

                myStream.filter(follow=friend_ids)

            except Exception as e:

                print(str(e) + '\n')
                continue

    # called to add a tweet to mentioned table
    def add_mention_db(tweet):

        print(tweet)

        lock = Lock()
        db = Collector.mention_tweet_db()
        c = db[0]
        conn = db[1]

        lock.acquire()

        c.execute('''INSERT INTO mentioned
                             (tweet,
                              username,
                              tweet_date,
                              tweet_id,
                              tweet_source,
                              user_id,
                              reply_id)
                     VALUES(?,?,?,?,?,?,?)''',
                  [tweet[0],
                   tweet[1],
                   tweet[2],
                   tweet[3],
                   tweet[4],
                   tweet[5],
                   tweet[6]])

        conn.commit()
        lock.release()

    # looks for any tweets that mention me that were missed
    # by the listener. Adds to mentioned table
    def check_db_mention():

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

                tweet = list(tweet)
                tweet.append(None)
                Actions.add_mention_db(tweet)

        if len(new_tweets) > 0:

            with open(filename, 'w') as f:

                f.write(new_tweets[0][3])

    # looks for new mentions in mentioned table
    # starts Screen process on matches
    def mention_check():

        # placeholder file keeps from doing things twice
        # if new mentions are found, calls Screen.is_command
        # adds results of Screen.is_command to queue via
        # add_2_queue

        path = '/home/nick/.virtualenvs/twitterbots/bots/control_files/'
        db_info = Actions.db_connect()
        c = db_info[0]

        while True:

            with open(path + 'last_mention.txt', 'r') as f:

                last_seen = int(f.read().strip())

            c.execute('SELECT * FROM mentioned')

            new_mentions = [x for x in c.fetchall()
                            if int(x[3]) > last_seen]

            try:

                newest = max([int(x[3]) for x in new_mentions])

                with open(path + 'last_mention.txt', 'w') as f:

                    f.write(str(newest))

                twt_cmd_pairs = Screen.is_command(new_mentions)

                if len(twt_cmd_pairs) > 1:

                    Actions.add_2_pool(twt_cmd_pairs)

                elif len(twt_cmd_pairs) == 1:

                    Actions.requests_serve(twt_cmd_pairs[0])

            except Exception:

                pass

            time.sleep(45)

    # Takes a list of tweets with commands, adds to pool
    def add_2_pool(twt_cmd_pairs):

        pool = Pool(4)
        pool.map(Actions.requests_serve, twt_cmd_pairs)

    # commands sent to direct_request funct then
    # on to the approriate reply funct
    def requests_serve(twt_cmd_pair):

        tweet = twt_cmd_pair[0]
        cmd = twt_cmd_pair[1]

        print('Processing request for {}'.format(tweet[1]))
        print()

        if cmd == '--help':

            Actions.reply_help(tweet)

        else:

            # name of file user wanted made
            graphic_file = Screen.direct_request(tweet, cmd)

            Actions.reply_request(tweet, graphic_file)

    # for replying to command for graphic
    def reply_request(tweet, file_):

        api = Actions.get_api()

        username = tweet[1]
        reply_status_id = tweet[3]

        message = username + ', here is the graphic you requested.'

        api.update_with_media(file_,
                              status=message,
                              in_reply_to_status_id=reply_status_id)

        time.sleep(5)
        os.remove(file_)

    # for replying to commands for help
    def reply_help(tweet):

        reply_status_id = tweet[3]
        api = Actions.get_api()
        path = '/home/nick/.virtualenvs/twitterbots/bots/control_files/'

        with open(path + 'help_message.txt', 'r') as f:

            help_message = f.read().strip()

        api.update_status(status=help_message,
                          in_reply_to_status_id=reply_status_id)

    # random command processed and graphic
    # posted to timeline with message
    def auto_status():

        conn = sqlite3.connect('auto_log.db')
        c = conn.cursor()

        status = RandomStatus.random_post()
        api = Actions.get_api()

        if type(status) is list(status):

            tweet = api.update_with_media(status[0], status=status[1])
            time.sleep(5)
            os.remove(status[0])

            c.execute('INSERT INTO autolog VALUES(?)', [tweet.id])
            conn.commit()

        elif type(status) is str:

            tweet = api.update_status(status=status)

            c.execute('INSERT INTO autolog(tweet) VALUES(?)', [tweet.id])
            conn.commit()

    # sends a random --all graphic every Friday
    # if the hour is 10p, uses txt file to log activity
    def auto_status_date():

        d = dt.now()
        hour = dt.strftime(d, '%H')
        d = d.isoweekday()
        days = [2, 5]

        path = '/home/nick/.virtualenvs/twitterbots/bots/'\
               'control_files/auto_status.txt'

        with open(path, 'r') as f:
            sent = f.read().strip()

        # if day is  Tuesday or Friday and hour = 8pm
        # and if control file says 'False'
        if int(d) in days and str(sent) == 'False' and int(hour) == 20:

            Actions.auto_status()
            with open(path, 'w') as f:
                f.write('True')

        # once friday's 8pm hour passes control
        # file changed back to 'False'
        elif int(hour) != 20:

            with open(path, 'w') as f:

                f.write('False')


class CopyDb:

    '''
    Simple class and fuctions to copy the database
    only if its been more than an hour since last
    backup.
    '''

    def last_modified():

        path = '/home/nick/.virtualenvs/twitterbots/bots/tweet_dump_main.db'

        mod_time = os.path.getmtime(path)

        return mod_time

    def copy_database():

        if CopyDb.last_modified() >= 3600:

            source_path = '/home/nick/.virtualenvs/twitterbots/bots/tweet_dump_main.db'
            dst = '/home/nick/.virtualenvs/twitterbots/bots/tweet_dump.db'

            shutil.copy2(source_path,
                         dst)


if __name__ == '__main__':

    main()
