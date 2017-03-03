#!/home/nick/.virtualenvs/twitterbots/bin/python3.5

import re
import tweepy
import sqlite3
import datetime

from tweets import AllTweets
from hashtags import Hashtags
from retweets import Retweets
from mentions import Mentions
from datetime import datetime as dt
from configparser import ConfigParser


def main():

    pass


# results of functions in this class take inputs
# from data from Twitter about users with entries
# in db such as their total status count or # of followers
class UserData:

    # function will be used to create and update
    # hence the usage of CREATE, and inclusion
    # of tweepy
    def user_database():

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

        conn = sqlite3.connect('tweet_dump_main.db')
        c = conn.cursor()

        c.execute('''CREATE TABLE IF NOT EXISTS user_data
                     (username TEXT,
                      user_id TEXT,
                      account_date TEXT,
                      statuses INTEGER,
                      friends INTEGER,
                      followers INTEGER,
                      geoloc TEXT,
                      utc_offset INTEGER,
                      db_entries INTEGER)''')

        c.execute('SELECT user_id FROM tdump')
        users = sorted([int(x[0]) for x in set(c.fetchall())])

        c.execute('SELECT user_id from user_data')
        tracked_users = sorted([int(x[0]) for x in set(c.fetchall())])

        print('Insert Active')

        for user in users:

            try:

                user_object = api.get_user(user)

                c.execute('''SELECT COUNT(*)
                             FROM tdump
                             WHERE user_id=?''',
                          [user_object.id_str])
                status_count = c.fetchone()[0]

                # get lat/long from status object
                # 1 if enabled, 0 if not
                user_geo = user_object.geo_enabled

                # utc time offset
                user_utc = user_object.utc_offset

                if user_utc is None:

                    user_utc = 0

                if int(user_object.id_str) in tracked_users:

                    c.execute('''UPDATE user_data
                                 SET username=?,
                                     user_id=?,
                                     account_date=?,
                                     statuses=?,
                                     friends=?,
                                     followers=?,
                                     geoloc=?,
                                     utc_offset=?,
                                     db_entries=?
                                 WHERE user_id=?
                                     ''',
                              [user_object.screen_name,     # "TwitterUser10"
                               user_object.id_str,          # '2435547867865'
                               user_object.created_at,      # datetime object
                               user_object.statuses_count,  # total tweets
                               user_object.friends_count,   # number of
                               user_object.followers_count,
                               user_geo,
                               user_utc,
                               status_count,
                               int(user_object.id_str)])

                else:

                    c.execute('''INSERT INTO user_data
                                 VALUES (?,?,?,?,?,?,?,?,?)''',
                              [user_object.screen_name,
                               user_object.id_str,
                               user_object.created_at,
                               user_object.statuses_count,
                               user_object.friends_count,
                               user_object.followers_count,
                               user_geo,
                               user_utc,
                               status_count])

            # if error occurs getting user, just skip
            # will try again next time
            except Exception as e:

                print(str(e) + '\n')
                continue

        conn.commit()
        conn.close()
        print('Insert Done' + '\n')

    # returns list of id strings
    # of users in friends list
    def friend_ids():

        conn = sqlite3.connect('tweet_dump_main.db')
        c = conn.cursor()

        c.execute('''SELECT user_id FROM user_data''')
        user_ids = [x[0] for x in c.fetchall()]

        return user_ids

    # returns user with oldest account
    # creation date
    def oldest_user():

        conn = sqlite3.connect('tweet_dump_main.db')
        c = conn.cursor()

        c.execute('''SELECT username
                     FROM user_data
                     ORDER BY account_date ASC''')
        user = [x[0] for x in (c.fetchall())][0]

        return user

    # user with most recent creation date
    def newest_user():

        conn = sqlite3.connect('tweet_dump_main.db')
        c = conn.cursor()

        c.execute('''SELECT username
                     FROM user_data
                     ORDER BY account_date ASC''')
        user = [x[0] for x in c.fetchall()][-1]

        return user

    # total lifetime status counts taken from
    # Twitter then averaged
    def tweet_average():

        conn = sqlite3.connect('tweet_dump_main.db')
        c = conn.cursor()

        c.execute('''SELECT statuses FROM user_data''')
        statuses = [x[0] for x in c.fetchall()]

        return sum(statuses) / len(statuses)

    # returns average number of
    # friends and followers of users in db
    def friends_2_followers():

        conn = sqlite3.connect('tweet_dump_main.db')
        c = conn.cursor()

        c.execute('''SELECT friends, followers FROM user_data''')
        f_f = c.fetchall()

        friends = f_f[0]
        followers = f_f[1]

        friend_avg = sum(friends) / len(friends)
        follower_avg = sum(followers) / len(followers)

        return friend_avg, follower_avg

    def most_friends():

        conn = sqlite3.connect('tweet_dump_main.db')
        c = conn.cursor()

        c.execute('''SELECT username, friends FROM user_data''')
        user_friends = c.fetchall()
        most_friends = sorted(user_friends, key=lambda x: int(x[1]))[-1]

        return most_friends

    def most_followers():

        conn = sqlite3.connect('tweet_dump_main.db')
        c = conn.cursor()

        c.execute('''SELECT username, followers FROM user_data''')
        user_followers = c.fetchall()
        most_followers = sorted(user_followers, key=lambda x: int(x[1]))[-1]

        return most_followers


# as class name indicates, everthing here gets its
# numbers and results from statuses in the db
class DatabaseStats:

    def total_statuses():

        total = len(AllTweets.get_all_tweets())

        return 'Total statuses in database {}'.format(str(total))

    def total_retweets():

        total = len(Retweets.get_all_retweets())

        return 'Total retweets in database {}'.format(str(total))

    # only counted if doesn't occur in retweet
    # return total number and total unique
    def hashtags():

        totals = Hashtags.get_user_hashtags(Hashtags.get_all_tweets())

        return ('Total hashtags used {}'.format(str(len(totals[0]))),
                'Total unique hashtags {}'.format(str(len(totals[1]))))

    # only counted if token preceeding mention
    # is not 'rt'.
    def users_mentioned():

        totals = Mentions.users_mentioned(AllTweets.get_all_tweets())

        return ('Total users mentioned {}'.format(str(len(totals[0]))),
                'Total unique mentions {}'.format(str(len(totals[1]))))

    def avg_statuses():

        conn = sqlite3.connect('tweet_dump_main.db')
        c = conn.cursor()

        c.execute('SELECT COUNT(*)  FROM user_data')
        num_of_users = c.fetchone()[0]

        c.execute('SELECT COUNT(*) FROM tdump')
        total_statuses = c.fetchone()[0]

        return int(round(total_statuses / num_of_users, 0))

    def most_statuses():

        conn = sqlite3.connect('tweet_dump_main.db')
        c = conn.cursor()

        c.execute('''SELECT db_entries
                     FROM user_data
                     ORDER BY db_entries DESC''')

        return c.fetchone()[0]

    def least_statuses():

        conn = sqlite3.connect('tweet_dump_main.db')
        c = conn.cursor()

        c.execute('''SELECT db_entries
                     FROM user_data
                     ORDER BY db_entries ASC''')

        return c.fetchone()[0]

    # gets number of users who have
    # geolocation enabled
    def geo_on_off():

        conn = sqlite3.connect('tweet_dump_main.db')
        c = conn.cursor()

        c.execute('SELECT geoloc FROM user_data')
        geo_data = [int(x[0]) for x in c.fetchall()]

        geo_on = sum(geo_data)

        geo_off = len(geo_data) - sum(geo_data)

        return geo_on, geo_off

    # use to create graphic
    def quarter_activity():

        activity = []

        for i in range(1, 91):

            activity.append((i, DatabaseStats.active_in_last(i)))

        return activity

    def all_statuses_in_last(days_):

        today = dt.today()
        past_date = today - datetime.timedelta(days=days_)

        conn = sqlite3.connect('tweet_dump_main.db')
        c = conn.cursor()

        c.execute('''SELECT *
                     FROM tdump
                     WHERE tweet_date>?
                     ORDER BY tweet_date DESC''',
                  [past_date])
        tweets = c.fetchall()

        return len(tweets)

    def most_one_day():

        tweets = AllTweets.get_all_tweets()
        day_counts = AllTweets.all_tweets_per_date(tweets)
        day_counts = sorted(day_counts,
                            key=lambda x: int(x[1]),
                            reverse=True)

        return day_counts[0]


# going to do something to visualize how
# screennames are composed
class ScreenNames:

    # returns list of screennames
    # probably don't need set() in there
    def screennames():

        conn = sqlite3.connect('tweet_dump_main.db')
        c = conn.cursor()

        c.execute('SELECT user_id FROM user_data')
        user_list = list(set(x[0] for x in c.fetchall()))
        user_list = sorted(user_list, key=lambda x: int(x))

        return user_list

    def length():

        conn = sqlite3.connect('tweet_dump_main.db')
        c = conn.cursor()

        c.execute('SELECT username FROM user_data')
        user_list = list(set(x[0] for x in c.fetchall()))
        user_list = sorted(user_list, key=lambda x: len(x))

        lengths = [len(x) for x in user_list]

        longest = user_list[-1]
        shortest = user_list[0]
        avg_length = round(sum(lengths) / len(lengths), 0)

        return avg_length, longest, shortest

    # no symbols or numbers in name
    def all_alpha():

        conn = sqlite3.connect('tweet_dump_main.db')
        c = conn.cursor()

        c.execute('SELECT username FROM user_data')
        user_list = list(set(x[0] for x in c.fetchall()))
        user_list = sorted(user_list, key=lambda x: len(x))

        true_count = 0
        false_count = 0

        for user in user_list:

            user = user.replace('_', '')

            if user.isalpha():

                true_count += 1

            else:

                false_count += 1

        return true_count, false_count

    def digits():

        conn = sqlite3.connect('tweet_dump_main.db')
        c = conn.cursor()

        c.execute('SELECT username FROM user_data')
        user_list = list(set(x[0] for x in c.fetchall()))
        user_list = sorted(user_list, key=lambda x: len(x))

        user_string = ' '.join(user_list)

        # list of individual numbers [1,0,] for 'user10'
        all_digits = re.findall(r'\d', user_string)
        digit_count = list(set([(x, all_digits.count(x)) for x in all_digits]))
        digit_count = sorted(digit_count,
                             key=lambda x: int(x[1]),
                             reverse=True)

        # list of integers [10,] for 'user10'
        all_ints = re.findall(r'\d+', user_string)
        int_count = list(set([(x, all_ints.count(x)) for x in all_ints]))

        return digit_count, int_count

    def underscore_division():

        conn = sqlite3.connect('tweet_dump_main.db')
        c = conn.cursor()

        c.execute('SELECT username FROM user_data')
        user_list = list(set(x[0] for x in c.fetchall()))
        user_list = sorted(user_list, key=lambda x: len(x))

        with_underscore = [x.strip('_') for x in user_list]
        with_underscore = [x.split('_') for x in with_underscore if '_' in x]

        # number of users with underscores in username
        underscore_count = len(with_underscore)

        # list of number of strings separated by
        # underscores in each username

        strings_separated = [[x for x in i if x != '']
                             for i in with_underscore]

        strings_separated = [len(x) for x in strings_separated]

        ss_avg = round(sum(strings_separated) / underscore_count, 2)

        return underscore_count, ss_avg


if __name__ == '__main__':

    main()
