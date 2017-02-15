#!/home/nick/.virtualenvs/twitterbots/bin/python3.5

import re
import tweepy
import sqlite3

from configparser import ConfigParser


def main():

    pass


class Stats:

    def all_statistics():

        return [AllData.oldest_user(),
                AllData.newest_user(),
                AllData.tweet_average(),
                AllData.friends_2_followers(),
                AllData.most_friends(),
                AllData.most_followers(),
                AllData.geo_on_off(),
                ScreenNames.length(),
                ScreenNames.all_alpha(),
                ScreenNames.digits(),
                ScreenNames.underscore_division()]


class AllData:

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

        conn = sqlite3.connect('tweet_dump.db')
        c = conn.cursor()

        c.execute('''CREATE TABLE IF NOT EXISTS user_data
                     (username TEXT,
                      user_id TEXT,
                      account_date TEXT,
                      statuses INTEGER,
                      friends INTEGER,
                      followers INTEGER,
                      geoloc TEXT,
                      utc_offset INTEGER)''')

        c.execute('SELECT user_id FROM tdump')
        users = [x[0] for x in set(c.fetchall())]

        c.execute('SELECT user_id from user_data')
        tracked_users = [x[0] for x in set(c.fetchall())]

        for user in users:

            if user not in tracked_users:

                user_object = api.get_user(user)

                # id number
                user_id_ = user

                # "TwitterUser10"
                user = user_object.screen_name

                # datetime object
                user_created = user_object.created_at

                # number of
                user_follwers = user_object.followers_count
                user_friends = user_object.friends_count

                # total tweets since account created
                user_statuses = user_object.statuses_count

                # chance to get lat/long from status object
                user_geo = user_object.geo_enabled

                # utc time offset
                user_utc = user_object.utc_offset

                c.execute('''INSERT INTO user_data
                             VALUES (?,?,?,?,?,?,?,?)''',
                          [user,
                           user_id_,
                           user_created,
                           user_statuses,
                           user_friends,
                           user_follwers,
                           user_geo,
                           user_utc])

            else:

                user_object = api.get_user(user)

                # id number
                user_id_ = user

                # "TwitterUser10"
                user = user_object.screen_name

                # datetime object
                user_created = user_object.created_at

                # number of
                user_follwers = user_object.followers_count
                user_friends = user_object.friends_count

                # total tweets since account created
                user_statuses = user_object.statuses_count

                # chance to get lat/long from status object
                user_geo = user_object.geo_enabled

                # utc time offset
                user_utc = user_object.utc_offset

                c.execute('''INSERT INTO user_data
                             VALUES (?,?,?,?,?,?,?,?)''',
                          [user,
                           user_id_,
                           user_created,
                           user_statuses,
                           user_friends,
                           user_follwers,
                           user_geo,
                           user_utc])

        conn.commit()

    def friend_ids():

        conn = sqlite3.connect('tweet_dump.db')
        c = conn.cursor()

        c.execute('''SELECT user_id FROM user_data''')
        user_ids = [x[0] for x in c.fetchall()]

        return user_ids

    def oldest_user():

        conn = sqlite3.connect('tweet_dump.db')
        c = conn.cursor()

        c.execute('''SELECT username
                     FROM user_data
                     ORDER BY account_date ASC''')
        user = [x[0] for x in (c.fetchall())][0]

        return user

    def newest_user():

        conn = sqlite3.connect('tweet_dump.db')
        c = conn.cursor()

        c.execute('''SELECT username
                     FROM user_data
                     ORDER BY account_date ASC''')
        user = [x[0] for x in c.fetchall()][-1]

        return user

    def tweet_average():

        conn = sqlite3.connect('tweet_dump.db')
        c = conn.cursor()

        c.execute('''SELECT statuses FROM user_data''')
        statuses = [x[0] for x in c.fetchall()]

        return sum(statuses) / len(statuses)

    def friends_2_followers():

        conn = sqlite3.connect('tweet_dump.db')
        c = conn.cursor()

        c.execute('''SELECT friends, followers FROM user_data''')
        f_f = c.fetchall()

        friends = f_f[0]
        followers = f_f[1]

        friend_avg = sum(friends) / len(friends)
        follower_avg = sum(followers) / len(followers)

        return friend_avg, follower_avg

    def most_friends():

        conn = sqlite3.connect('tweet_dump.db')
        c = conn.cursor()

        c.execute('''SELECT username, friends FROM user_data''')
        user_friends = c.fetchall()
        most_friends = sorted(user_friends, key=lambda x: int(x[1]))[-1]

        return most_friends

    def most_followers():

        conn = sqlite3.connect('tweet_dump.db')
        c = conn.cursor()

        c.execute('''SELECT username, followers FROM user_data''')
        user_followers = c.fetchall()
        most_followers = sorted(user_followers, key=lambda x: int(x[1]))[-1]

        return most_followers

    def geo_on_off():

        conn = sqlite3.connect('tweet_dump.db')
        c = conn.cursor()

        c.execute('SELECT geoloc FROM user_data')
        geo_data = [int(x[0]) for x in c.fetchall()]

        geo_on = sum(geo_data)

        geo_off = len(geo_data) - sum(geo_data)

        return geo_on, geo_off


class ScreenNames:

    def screennames():

        conn = sqlite3.connect('tweet_dump.db')
        c = conn.cursor()

        c.execute('SELECT user_id FROM user_data')
        user_list = list(set(x[0] for x in c.fetchall()))
        user_list = sorted(user_list, key=lambda x: int(x))

        return user_list

    def length():

        conn = sqlite3.connect('tweet_dump.db')
        c = conn.cursor()

        c.execute('SELECT username FROM user_data')
        user_list = list(set(x[0] for x in c.fetchall()))
        user_list = sorted(user_list, key=lambda x: len(x))

        lengths = [len(x) for x in user_list]

        longest = user_list[-1]
        shortest = user_list[0]
        avg_length = round(sum(lengths) / len(lengths), 0)

        return avg_length, longest, shortest

    def all_alpha():

        conn = sqlite3.connect('tweet_dump.db')
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

        conn = sqlite3.connect('tweet_dump.db')
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

        conn = sqlite3.connect('tweet_dump.db')
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
