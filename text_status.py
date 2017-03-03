#!/home/nick/.virtualenvs/twitterbots/bin/python3.5

import tweepy
import sqlite3
import datetime

from hashtags import Hashtags
from mentions import Mentions
from retweets import Retweets
from datetime import datetime as dt
from configparser import ConfigParser

# results of functions used to create random text statuses
# add percentage of users who tweeted at least once a day


def main():

    pass


class TextFuncts:

    # returns percentage of users active in x number of days
    def active(days_):

        seen = []
        active_count = 0
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

        for tweet in tweets:

            if tweet[5] not in seen:

                active_count += 1
                seen.append(tweet[5])

        c.execute('SELECT COUNT(*) FROM user_data')
        num_users = c.fetchone()[0]

        active = round(active_count / num_users, 2) * 100

        return '{}%'.format(str(active))

    # returns top 3 hashtags from last x days
    # tags in retweets omitted, counts shown
    def hash(days_):

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

        # extracting hashtags
        hashtags_ = tuple([x.lower() for x in
                           Hashtags.get_user_hashtags(tweets)[1]])

        # counted & sorted
        hashtags_ = Hashtags.count_hashtags(hashtags_)
        hashtags_ = sorted(hashtags_,
                           key=lambda x: int(x[1]),
                           reverse=True)

        return hashtags_[:3]

    # top 3 users retweeted from last x days
    def retweet(days_):

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

        # extracting retweets from status list
        retweeted = Retweets.extract_retweets(tweets)

        # extracting retweeted user handles & counting
        retweeted = Retweets.get_retweeted_users(retweeted)[1]
        retweeted = sorted(retweeted,
                           key=lambda x: int(x[1]),
                           reverse=True)

        return retweeted[:3]

    # top 3 mentioned users from last x days
    # users mentioned after 'RT' token omitted
    def mention(days_):

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

        # extracting user handles mentioned in tweets
        mentioned = Mentions.users_mentioned(tweets)[1]
        mentioned = sorted(mentioned,
                           key=lambda x: int(x[1]),
                           reverse=True)

        return mentioned[:3]

    # top 3 users with most statuses posted in last
    # x days. Retweets do not count
    def statuses(days_):

        api = ApiGrab.get_api()

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
        tweets = [x[5] for x in tweets]

        status_counts = list(set([(x, tweets.count(x)) for x in tweets]))
        status_counts = sorted(status_counts,
                               key=lambda x: int(x[1]),
                               reverse=True)
        status_counts = [(api.get_user(x[0]).screen_name, x[1])
                         for x in status_counts[:3]]

        return status_counts


# tweets created within this class will be used in
# a reply function later on
class Messages:

    def active(days_):

        result = TextFuncts.active(days_)
        msg = '{} of friends tweeted at least once last week'.format(result)

        return msg

    def hash(days_):

        result = TextFuncts.hash(days_)

        if days_ == 7:

            days_ = 'week'

        elif days_ == 30:

            days_ = 'month'

        msg = '''Top 3 hashtags last {}

     {} {}
     {} {}
     {} {}'''.format(days_,
                     result[0][0],
                     result[0][1],
                     result[1][0],
                     result[1][1],
                     result[2][0],
                     result[2][1])

        return msg

    def retweet(days_):

        result = TextFuncts.retweet(days_)

        if days_ == 7:

            days_ = 'week'

        elif days_ == 30:

            days_ = 'month'

        msg = '''Top 3 retweeted users last {}

     {} {}
     {} {}
     {} {}'''.format(days_,
                     result[0][0],
                     result[0][1],
                     result[1][0],
                     result[1][1],
                     result[2][0],
                     result[2][1])

        return msg

    def mention(days_):

        result = TextFuncts.mention(days_)

        if days_ == 7:

            days_ = 'week'

        elif days_ == 30:

            days_ = 'month'

        msg = '''Top 3 most mentioned last {}

     {} {}
     {} {}
     {} {}'''.format(days_,
                     result[0][0],
                     result[0][1],
                     result[1][0],
                     result[1][1],
                     result[2][0],
                     result[2][1])

        return msg

    def statuses(days_):

        result = TextFuncts.statuses(days_)

        if days_ == 7:

            days_ = 'week'

        elif days_ == 30:

            days_ = 'month'

        msg = '''Top 3 most tweets sent last {}

     @{} {}
     @{} {}
     @{} {}'''.format(days_,
                      result[0][0],
                      result[0][1],
                      result[1][0],
                      result[1][1],
                      result[2][0],
                      result[2][1])

        return msg


class ApiGrab:

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


if __name__ == '__main__':

    main()
