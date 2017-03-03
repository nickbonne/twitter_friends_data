#!/home/nick/.virtualenvs/twitterbots/bin/python3.5
# -*- coding: utf-8 -*-

import tweepy
import sqlite3

from configparser import ConfigParser

'''
A little OOP would be good later for
authenticated user data, c, conn, api
'''


def main():

    Collector.collect()


class Collector:

    # Main function
    def collect():

        api = Collector.get_api()

        tweet_dump = Collector.all_tweet_db()
        c = tweet_dump[0]
        conn = tweet_dump[1]
        last_list = Collector.last_tweets(c, conn)

        # Look for new friends, add to db
        new_friends = Collector.new_f_check(api, c)

        Collector.download_to_limit(api, c, conn, new_friends)

        # Checks timelines of everyone in db already
        # adds anything new to db
        Collector.download_recent(api, c, conn, last_list)

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

    # connects to tweet_dump.db creates tdump if not exists
    # tdump stores all tweets from anyone in list
    def all_tweet_db():

        conn = sqlite3.connect('tweet_dump_main.db')
        c = conn.cursor()

        c.execute('''CREATE TABLE IF NOT EXISTS tdump
                     (tweet TEXT,
                      username TEXT,
                      tweet_date TEXT,
                      tweet_id TEXT,
                      tweet_source TEXT,
                      user_id TEXT)''')

        return c, conn

    # connects to tweet_dump.db creats served if not exists
    # served stores tweets that are mention authenticated user
    def mention_tweet_db():

        conn = sqlite3.connect('tweet_dump_main.db')
        c = conn.cursor()

        c.execute('''CREATE TABLE IF NOT EXISTS mentioned
                     (tweet TEXT,
                      username TEXT,
                      tweet_date TEXT,
                      tweet_id TEXT,
                      tweet_source TEXT,
                      user_id TEXT)''')

        return c, conn

    # looks for new friends by comparing authenticated
    # user's friend list with list of friends in tdump
    def new_f_check(api, c):

        # get list of user's ids
        c.execute('SELECT user_id FROM tdump')
        users = c.fetchall()
        users = list(set([user[0] for user in users]))

        # get list of friends_ids from twitter
        friends_ids = api.friends_ids()

        new_friends = [x for x in friends_ids if str(x) not in users]

        return new_friends

    # downloads up to 3200 of a user's most
    # recent tweets commits to tdump
    def download_to_limit(api, c, conn, friend_list):

        # List of tweet ids already in db
        c.execute('SELECT tweet_id FROM tdump')
        tweet_ids = c.fetchall()
        tweet_ids = [e[0] for e in tweet_ids]

        new_tweets = []

        for friend in friend_list:

            try:
                # try to get most recent 200 tweets from friend
                get_tweets = api.user_timeline(id=friend, count=200)

            except Exception as e:

                continue

            # add to list of all of this friend's tweets
            new_tweets.extend(get_tweets)

            # find oldest retrieved tweet's id number less 1
            oldest = new_tweets[-1].id - 1

            # get tweets until 3200 limit hit
            while len(get_tweets) > 0:

                try:
                    # max_id arg looks for id's less than arg's value
                    get_tweets = api.user_timeline(id=friend,
                                                   count=200,
                                                   max_id=oldest)

                except Exception as e:

                    continue

                new_tweets.extend(get_tweets)

                oldest = new_tweets[-1].id - 1

        if len(new_tweets) != 0:

            print('Insert Active')

        for tweet in new_tweets:

            c.execute('''INSERT INTO tdump
                            (tweet,
                            username,
                            tweet_date,
                            tweet_id,
                            tweet_source,
                            user_id)
                             VALUES(?,?,?,?,?,?)''',
                      [tweet.text,
                       tweet.user.screen_name,
                       tweet.created_at,
                       tweet.id_str,
                       tweet.source,
                       tweet.user.id_str])

        conn.commit()

        if len(new_tweets) != 0:

            print('Insert Done' + '\n')

    # simply check if tweet text contains my screen name
    # change from hard code later
    def mention_me(new_tweet_list, c, conn):

        mentioned = [x for x in new_tweet_list if '@BonneNick' in x[0]]

        if len(new_tweet_list) != 0:

            print('Insert Active')

        for tweet in mentioned:

            c.execute('''INSERT INTO served
                            (tweet,
                            username,
                            tweet_date,
                            tweet_id,
                            tweet_source,
                            user_id)
                             VALUES(?,?,?,?,?,?)''',
                      [tweet.text,
                       tweet.user.screen_name,
                       tweet.created_at,
                       tweet.id_str,
                       tweet.source,
                       tweet.user.id_str])

        conn.commit()

        if len(new_tweet_list) != 0:

            print('Insert Done' + '\n')

    # returns list of user_id and created_at pairs
    # date associated with user_id is date of last
    # tweet in database
    def last_tweets(c, conn):

            # list of user ids and the date of the
            # last tweet in db
            user_last_tweets = []

            # get list of user's ids
            c.execute('SELECT user_id FROM tdump')
            users = c.fetchall()
            users = list(set([user[0] for user in users]))

            for user in users:

                c.execute('''SELECT user_id, tweet_id
                             FROM tdump
                             WHERE user_id = ?
                             ORDER BY tweet_date DESC''',
                          [user])

                last_tweet = c.fetchone()
                user_last_tweets.append(last_tweet)

            return user_last_tweets

    # downloads most recent posts in each users timelines
    def download_recent(api, c, conn, last_tweets):

        c.execute('SELECT tweet_id FROM tdump')
        tweet_ids = [x[0] for x in c.fetchall()]

        new_tweets = []

        for pair in last_tweets:

            user_id = pair[0]
            tweet_id = pair[1]

            try:

                get_tweets = api.user_timeline(id=user_id,
                                               since_id=tweet_id,
                                               count=200)

            except Exception:

                continue

            if len(get_tweets) != 0:

                # add to list of all of this friend's tweets
                new_tweets.extend(get_tweets)

                # find newest retrieved tweet's id number plus 1
                newest = get_tweets[0].id + 1

                while len(get_tweets) > 0:

                    try:
                        # max_id arg looks for id's less than arg's value
                        get_tweets = api.user_timeline(id=user_id,
                                                       count=200,
                                                       since_id=newest)

                        new_tweets.extend(get_tweets)

                        newest = get_tweets[0].id + 1

                    except Exception:

                        continue

        if len(new_tweets) != 0:

            print('Insert Active')

        for tweet in new_tweets:

            if tweet.user.screen_name != 'BonneNick' \
               and tweet.id not in tweet_ids:

                c.execute('''INSERT INTO tdump
                                (tweet,
                                username,
                                tweet_date,
                                tweet_id,
                                tweet_source,
                                user_id)
                                 VALUES(?,?,?,?,?,?)''',
                          [tweet.text,
                           tweet.user.screen_name,
                           tweet.created_at,
                           tweet.id_str,
                           tweet.source,
                           tweet.user.id_str])

        conn.commit()
        conn.close()

        if len(new_tweets) != 0:

            print('Insert Done' + '\n')


if __name__ == '__main__':

    main()
