#!/home/nick/.virtualenvs/twitterbots/bin/python3.5

import sqlite3
from nltk.tokenize import TweetTokenizer
from tweet_graphs import Graphs

'''

Due to the wide array of apps and ways to send tweets,
only tweets directly from the official Twitter app for
Android and iOS will be counted. No Twitter for iPad or
Twitter for Android Tablets, etc

'''


def main():

    all_tweets = Sources.get_all_tweets()
    # all_retweets = Sources.get_all_retweets()
    # all_retweets = Sources.get_all_retweets()
    # source_list = Sources.get_all_sources()

    # sources_counted = Sources.counted_sources(source_list)
    # sources_counted.sort(key=lambda x: int(x[1]), reverse=True)

    # android_tweets = Android.tweets(all_tweets)
    # android_retweets = Android.retweets(all_retweets)

    # print('Android users are {}% original'.format(
    #       str(round(100 * (len(android_tweets) / (len(android_tweets) + len(android_retweets))), 1))))

    # iphone_tweets = Iphone.tweets(all_tweets)
    # iphone_retweets = Iphone.retweets(all_retweets)

    # print('iPhone users are {}% original'.format(
    #       str(round(100 * (len(iphone_tweets) / (len(iphone_tweets) + len(iphone_retweets))), 1))))

    # android_users = Android.num_of_users(all_tweets, all_retweets)

    # print('{} active Android users, {} have used Android to tweet.'.format(android_users[0], android_users[1]))

    # iphone_users = Iphone.num_of_users(all_tweets, all_retweets)

    # print('{} active iPhone users, {} have used iPhone to tweet.'.format(iphone_users[0], iphone_users[1]))

    # Graphs.retweet_pie(len(android_tweets), len(android_retweets))
    # Graphs.retweet_pie(len(iphone_tweets), len(iphone_retweets))

class Sources:

    def get_all_sources():

        # for connecting to main dump db
        conn = sqlite3.connect('tweet_dump.db')
        c = conn.cursor()

        c.execute('''SELECT tweet_source
                     FROM tdump''')

        all_sources = c.fetchall()

        return all_sources

    def get_all_tweets():

        # for connecting to main dump db
        conn = sqlite3.connect('tweet_dump.db')
        c = conn.cursor()

        c.execute('''SELECT tweet,
                            username,
                            tweet_date,
                            tweet_source
                     FROM tdump''')

        all_tweets = c.fetchall()
        tweets = []

        twt_token = TweetTokenizer()

        for tweet in all_tweets:

            tokenized_twt = twt_token.tokenize(tweet[0])

            if not any(token for token in tokenized_twt if
                       token.upper() == 'RT'):

                tweets.append(tweet)

        return tweets

    def get_all_retweets():

        # for connecting to main dump db
        conn = sqlite3.connect('tweet_dump.db')
        c = conn.cursor()

        c.execute('''SELECT tweet,
                            username,
                            tweet_date,
                            tweet_source
                     FROM tdump''')

        all_tweets = c.fetchall()

        # inital list of retweets
        # more added after tokenization
        all_retweets = [i for i in all_tweets if
                        i[0][:2] == 'RT']

        # now the list to be tokenized
        all_tweets = [i for i in all_tweets if
                      i[0][:2] != 'RT']

        twt_token = TweetTokenizer()

        for tweet in all_tweets:

            tokenized_twt = twt_token.tokenize(tweet[0])

            for token in tokenized_twt:

                if token.upper() == 'RT':

                    all_retweets.append(tweet)

        return all_retweets

    def counted_sources(source_list):

        source_list = [i for i in source_list]

        seen = []
        source_count = []

        for source in source_list:

            if source not in seen:

                seen.append(source)
                counted = source_list.count(source)

                source_count.append([source.strip(), counted])

        return source_count


class Android:

    def tweets(all_tweets):

        android_tweets = [x for x in all_tweets if
                          x[3].lower() == 'twitter for android']

        return android_tweets

    def retweets(all_retweets):

        android_retweets = [x for x in all_retweets if
                            x[3].lower() == 'twitter for android']

        return android_retweets

    def num_of_users(all_tweets, all_retweets):

        # for connecting to main dump db
        conn = sqlite3.connect('tweet_dump.db')
        c = conn.cursor()

        # in case a user has only done one or the other
        all_tweets = all_tweets + all_retweets

        users = set([x[1] for x in all_tweets if
                     x[3].lower() == 'twitter for android'])

        android_users = 0
        has_used_android = 0

        for user in users:

            c.execute('''SELECT username,
                                tweet_source
                         FROM tdump
                         WHERE username = ?
                         ORDER BY tweet_date DESC''',
                      [user])

            all_tweets = c.fetchall()

            # looks for last tweet from either source
            # if android found first, user is counted
            for tweet in all_tweets:

                if tweet[1].lower() == 'twitter for android':

                    android_users += 1
                    break

                if tweet[1].lower() == 'twitter for iphone':

                    break

            android = len([x for x in all_tweets if
                          x[1].lower() == 'twitter for android'])

            if android > 0:

                has_used_android += 1

        return android_users, has_used_android


class Iphone:

    def tweets(all_tweets):

        iphone_tweets = [x for x in all_tweets if
                         x[3].lower() == 'twitter for iphone']

        return iphone_tweets

    def retweets(all_retweets):

        iphone_retweets = [x for x in all_retweets if
                           x[3].lower() == 'twitter for iphone']

        return iphone_retweets

    def num_of_users(all_tweets, all_retweets):

        # for connecting to main dump db
        conn = sqlite3.connect('tweet_dump.db')
        c = conn.cursor()

        # in case a user has only done one or the other
        all_tweets = all_tweets + all_retweets

        users = set([x[1] for x in all_tweets if
                     x[3].lower() == 'twitter for iphone'])

        iphone_users = 0
        has_used_iphone = 0

        for user in users:

            c.execute('''SELECT username,
                                tweet_source
                         FROM tdump
                         WHERE username = ?
                         ORDER BY tweet_date DESC''',
                      [user])

            all_tweets = c.fetchall()

            # looks for last tweet from either source
            # if iphone found first, user is counted
            for tweet in all_tweets:

                if tweet[1].lower() == 'twitter for iphone':

                    iphone_users += 1
                    break

                if tweet[1].lower() == 'twitter for android':

                    break

            iphone = len([x for x in all_tweets if
                         x[1].lower() == 'twitter for iphone'])

            if iphone > 0:

                has_used_iphone += 1

        return iphone_users, has_used_iphone


if __name__ == '__main__':

    main()
