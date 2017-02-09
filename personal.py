#!/home/nick/.virtualenvs/twitterbots/bin/python3.5

import time
import tweepy

from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw
from tweets import Tweets
from tweets import AllTweets
from mentions import Mentions
from hashtags import Hashtags
from retweets import Retweets
from tweet_graphs import Graphs
from phone_compare import Sources
from datetime import datetime as dt
from configparser import ConfigParser


'''
statuses = both tweets and retweets
tweets = just tweets
retweets = just retweets

need to add tweets and retweet total to user_data table in db
25 seconds per retweet pie too long

'''


def main():

    pass


class User:

    # user variable must be a user_id
    def __init__(self, user):

        self.user = user

    def user_statuses(self):

        all_statuses = AllTweets.get_all_tweets()
        all_statuses = [x for x in all_statuses if x[5] == self.user]
        all_statuses = sorted(all_statuses,
                              key=lambda x: dt.strptime(x[2],
                                                        '%Y-%m-%d %H:%M:%S'))

        first = all_statuses[0]
        last = all_statuses[-1]

        return all_statuses, first, last

    def user_tweets(self):

        all_tweets = Tweets.get_all_tweets()
        all_tweets = [x for x in all_tweets if x[5] == self.user]

        return all_tweets

    def user_retweets(self):

        all_retweets = Retweets.get_all_retweets()
        all_retweets = [x for x in all_retweets if x[5] == self.user]

        return all_retweets

    # returns list containing datetime object of
    # account creation, friend count, follower count
    # total tweets, and geo enabled (T/F)
    def get_user_data_tweepy(self):

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

        user_object = api.get_user(self)

        # datetime object
        user_created = user_object.created_at

        # number of
        user_follwers = user_object.followers_count
        user_friends = user_object.friends_count

        # total tweets since account created
        user_statuses = user_object.statuses_count

        # chance to get lat/long from status object
        user_geo = user_object.geo_enabled

        # screen name 'BonneNick'
        user_name = user_object.screen_name

        return (user_created,
                user_follwers,
                user_friends,
                user_statuses,
                user_geo,
                user_name)

    def user_data_box(self, tweets, retweets, statuses):

        tweepy_data = User.get_user_data_tweepy(self)

        account_created = tweepy_data[0]
        total_followers = tweepy_data[1]
        total_friends = tweepy_data[2]
        total_statuses = tweepy_data[3]
        geo_status = tweepy_data[4]
        screen_name = tweepy_data[5]

        # num of user's tweets in db
        total_on_record = len(statuses)

        # percentage of user's total tweets in db
        coverage = round(((len(statuses) / total_statuses) * 100), 2)
        coverage = str(coverage) + '%'

        # Users top 10 most mentioned users
        user_mentions = list(Mentions.users_mentioned(tweets)[1])
        user_mentions = sorted(user_mentions,
                               key=lambda x: int(x[1]),
                               reverse=True)
        user_mentions = user_mentions[:10]

        # top 10 hashtags used
        user_hashtags = Hashtags.get_user_hashtags(tweets)[0]
        top_hash = list(Hashtags.count_hashtags(user_hashtags))
        top_hash = sorted(top_hash,
                          key=lambda x: int(x[1]),
                          reverse=True)
        top_hash = top_hash[:10]

        # Users top 10 most retweeted users
        users_retweeted = Retweets.get_retweeted_users(retweets)
        users_retweeted = users_retweeted[0]

        count_retweeted = list(set([(x, users_retweeted.count(x))
                                    for x in users_retweeted]))
        fav_retweeted = sorted(count_retweeted,
                               key=lambda x: int(x[1]),
                               reverse=True)
        fav_retweeted = fav_retweeted[:10]

        first_on_record = statuses[0]
        most_recent_on_record = statuses[-1]

        # favourite tweet time
        fav_time = Tweets.tweets_per_minute(statuses)
        fav_time = sorted(fav_time,
                          key=lambda x: int(x[1]),
                          reverse=True)
        fav_time = fav_time[0]

        # day with most statuses sent
        busy_day = Tweets.tweets_per_date(statuses)
        busy_day = sorted(busy_day,
                          key=lambda x: int(x[1]),
                          reverse=True)
        busy_day = busy_day[0]

        # most used medium to tweet
        sources = [i[4] for i in statuses]
        fav_source = Sources.counted_sources(sources)
        fav_source = sorted(fav_source,
                            key=lambda x: int(x[1]),
                            reverse=True)
        fav_source = fav_source[0]
        print(fav_source)

        return (screen_name,
                account_created,
                total_statuses,
                total_on_record,
                total_followers,
                total_friends,
                geo_status,
                first_on_record,
                most_recent_on_record,
                coverage,
                top_hash,
                fav_retweeted,
                user_mentions,
                fav_time,
                busy_day,
                fav_source)

    def box_string(self, box_data):

        screen_name = box_data[0]
        account_created = box_data[1]
        total_statuses = str(box_data[2])
        total_on_record = str(box_data[3])
        followers = str(box_data[4])
        friends = str(box_data[5])
        geo_status = box_data[6]
        first_on_record = box_data[7]
        most_recent_on_record = box_data[8]
        coverage = box_data[9]
        top_hash = box_data[10]
        fav_retweeted = box_data[11]
        user_mentions = box_data[12]
        fav_time = box_data[13]
        busy_day = box_data[14]
        fav_source = box_data[15]

        box_string_1 = '''

    User: {}


    Account created: {}

    Total statuses: {}
    Statuses in database: {}
    Coverage: {}

    Friends: {}
    Followers: {}

    Oldest on record: {}
    Most recent: {}

    Geolocation status: {}
    Favorite medium: {} tweets from {}
    Most tweets in one day: {} tweets on {}
    Favorite time to tweet: {} tweets at {}

            '''.format(screen_name,
                       account_created,
                       total_statuses,
                       total_on_record,
                       coverage,
                       friends,
                       followers,
                       first_on_record[2],
                       most_recent_on_record[2],
                       geo_status,
                       str(fav_source[1]),
                       fav_source[0],
                       str(busy_day[1]),
                       busy_day[0],
                       str(fav_time[1]),
                       fav_time[0])

        box_string_2 = '''

    Top 5 Most Mentioned Users:

        {} tweeted at {} times
        {} tweeted at {} times
        {} tweeted at {} times
        {} tweeted at {} times
        {} tweeted at {} times

    Top 5 Most Retweeted Users:

        {} retweeted {} times
        {} retweeted {} times
        {} retweeted {} times
        {} retweeted {} times
        {} retweeted {} times

    Top 5 Most Used Hashtags:

        {} used {} times
        {} used {} times
        {} used {} times
        {} used {} times
        {} used {} times

            '''.format(user_mentions[0][0], user_mentions[0][1],
                       user_mentions[1][0], user_mentions[1][1],
                       user_mentions[2][0], user_mentions[2][1],
                       user_mentions[3][0], user_mentions[3][1],
                       user_mentions[4][0], user_mentions[4][1],
                       fav_retweeted[0][0], fav_retweeted[0][1],
                       fav_retweeted[1][0], fav_retweeted[1][1],
                       fav_retweeted[2][0], fav_retweeted[2][1],
                       fav_retweeted[3][0], fav_retweeted[3][1],
                       fav_retweeted[4][0], fav_retweeted[4][1],
                       top_hash[0][0], top_hash[0][1],
                       top_hash[1][0], top_hash[1][1],
                       top_hash[2][0], top_hash[2][1],
                       top_hash[3][0], top_hash[3][1],
                       top_hash[4][0], top_hash[4][1],
                       )

        return box_string_1, box_string_2

    def create_tweet_cloud(self, tweets):

        word_string = Tweets.tweeted_words(tweets)
        Graphs.tweeted_word_cloud(word_string, __class__)

    def create_retweet_pie(self, tweets, retweets):

        Graphs.retweet_pie(len(tweets), len(retweets), __class__)

    def create_aio_plot(self, statuses):

        graph_coords = AllTweets.all_tweets_per_minute(statuses)
        graph_coords = sorted(graph_coords,
                              key=lambda x: int(x[1]),
                              reverse=True)
        Graphs.all_in_one(graph_coords, __class__)

    # not users may request this, not enough data on
    # any one of them, perhaps @ 10k statuses in db
    def create_rtvt_aio_plot(self, tweets, retweets):

        tweet_coords = Tweets.tweets_per_minute(tweets)
        retweet_coords = Retweets.retweets_per_minute(retweets)

        tweet_coords.sort(key=lambda x: int(x[1]), reverse=True)
        retweet_coords.sort(key=lambda x: int(x[1]), reverse=True)

        Graphs.rtwt_vs_twt_24h(retweet_coords, tweet_coords, __class__)

    # statuses per day since beginning of database
    def create_per_day_plot(self, statuses):

        graph_coords = AllTweets.all_tweets_per_date(statuses)
        graph_coords = sorted(graph_coords,
                              key=lambda x: int(x[1]),
                              reverse=True)
        Graphs.total_tweets_per_day(graph_coords, __class__)

    def create_source_pie(self, statuses):

        sources = [i[3] for i in statuses]
        graph_coords = Sources.counted_sources(sources)
        graph_coords = sorted(graph_coords,
                              key=lambda x: int(x[1]),
                              reverse=True)
        Graphs.tweet_source_pie(graph_coords, __class__)

    def create_stat_box(self, stat_strings):

        img = Image.open('/home/nick/.virtualenvs/twitterbots/bots/img/stat_box.png')
        draw = ImageDraw.Draw(img)

        font = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf', 18)

        draw.text((0, 0), stat_strings[0], (0, 0, 0), font=font)
        draw.text((550, 0), stat_strings[1], (0, 0, 0), font=font)
        img.save('/home/nick/.virtualenvs/twitterbots/bots/output/tmp/filled_box.png')


if __name__ == '__main__':

    main()
