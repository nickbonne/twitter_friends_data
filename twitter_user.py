#!/home/nick/.virtualenvs/twitterbots/bin/python3.5

import PIL
import sqlite3
import numpy as np
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw
from tweets import Tweets
from mentions import Mentions
from hashtags import Hashtags
from retweets import Retweets
from tweet_graphs import Graphs
from phone_compare import Sources
from datetime import datetime as dt



def main():

    user_statuses = User('sebastianrichey').get_user_status()

    all_user_tweets = user_statuses[0]
    user_tweets = user_statuses[1]
    user_retweets = user_statuses[2]

    # Counted list of all hashtags used
    user_hashtags = Hashtags.get_user_hashtags(all_user_tweets)
    all_user_hash = user_hashtags[0]
    all_user_hash = list(Hashtags.count_hashtags(all_user_hash))
    all_user_hash.sort(key=lambda x: int(x[1]), reverse=True)

    # Counted list of all hashtags used outside of retweets
    not_rt_user_hash = user_hashtags[1]
    not_rt_user_hash = list(Hashtags.count_hashtags(not_rt_user_hash))
    not_rt_user_hash.sort(key=lambda x: int(x[1]), reverse=True)

    # Word cloud of a users most popular tokens
    user_word_string = Tweets.tweeted_words(user_tweets)
    Graphs.tweeted_word_cloud(user_word_string)

    # Tweet to retweet ratio graph
    Graphs.retweet_pie(len(user_tweets), len(user_retweets))

    # All tweets plotted in 24 hour period
    graph_coords = Tweets.tweets_per_minute(all_user_tweets)
    graph_coords.sort(key=lambda x: int(x[1]), reverse=True)
    most_active_time = graph_coords[0]
    Graphs.all_in_one(graph_coords)

    # Total tweets per day since beginning of data
    graph_coords_2 = Tweets.tweets_per_date(all_user_tweets)
    graph_coords_2.sort(key=lambda x: int(x[1]), reverse=True)
    most_active_date = graph_coords_2[0]
    Graphs.total_tweets_per_day(graph_coords_2)

    # Where a user's tweets came from
    sources = [i[3] for i in all_user_tweets]
    graph_coords_3 = Sources.counted_sources(sources)
    graph_coords_3.sort(key=lambda x: int(x[1]), reverse=True)
    most_used_source = graph_coords_3[0]
    Graphs.tweet_source_pie(graph_coords_3)

    # Users top 5 most mentioned users
    user_mentions = list(Mentions.users_mentioned(user_tweets)[1])
    user_mentions.sort(key=lambda x: int(x[1]), reverse=True)
    user_mentions = user_mentions[:5]

    # Users top 5 most retweeted users
    users_retweeted = Retweets.get_retweeted_users(all_user_tweets)
    users_retweeted = list(set([(x, users_retweeted.count(x)) for x in users_retweeted]))
    users_retweeted.sort(key=lambda x: int(x[1]), reverse=True)
    users_retweeted = users_retweeted[:5]

    summary_string = '''
 User: {}

 Total tweets recorded: {}
 Earliest tweet on record: {}

 {}

 Most tweets in one day: {} tweets on {}
 Favorite time to tweet: {} tweets at {}
 Favorite Twitter medium: {} tweets sent from {}

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
                 '''.format(all_user_tweets[0][1],
                            str(len(all_user_tweets)),
                            user_statuses[3][2],
                            user_statuses[3][0],
                            str(most_active_date[1]),
                            most_active_date[0],
                            str(most_active_time[1]),
                            most_active_time[0],
                            str(most_used_source[1]),
                            most_used_source[0],
                            user_mentions[0][0],
                            user_mentions[0][1],
                            user_mentions[1][0],
                            user_mentions[1][1],
                            user_mentions[2][0],
                            user_mentions[2][1],
                            user_mentions[3][0],
                            user_mentions[3][1],
                            user_mentions[4][0],
                            user_mentions[4][1],
                            users_retweeted[0][0],
                            users_retweeted[0][1],
                            users_retweeted[1][0],
                            users_retweeted[1][1],
                            users_retweeted[2][0],
                            users_retweeted[2][1],
                            users_retweeted[3][0],
                            users_retweeted[3][1],
                            users_retweeted[4][0],
                            users_retweeted[4][1])

    img = Image.open('/home/nick/.virtualenvs/twitterbots/bots/f_data_output/tmp/stat_box.png')
    draw = ImageDraw.Draw(img)

    font = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf', 14)

    draw.text((0, 0), summary_string, (0, 0, 0), font=font)
    img.save('/home/nick/.virtualenvs/twitterbots/bots/f_data_output/tmp/filled_box.png')

    image_1 = '/home/nick/.virtualenvs/twitterbots/bots/f_data_output/tmp/filled_box.png'
    image_2 = '/home/nick/.virtualenvs/twitterbots/bots/f_data_output/tmp/word_cloud.png'
    image_3 = '/home/nick/.virtualenvs/twitterbots/bots/f_data_output/tmp/per_day.png'
    image_4 = '/home/nick/.virtualenvs/twitterbots/bots/f_data_output/tmp/aio.png'
    image_5 = '/home/nick/.virtualenvs/twitterbots/bots/f_data_output/tmp/source_pie.png'
    image_6 = '/home/nick/.virtualenvs/twitterbots/bots/f_data_output/tmp/originality.png'

    list_im = [image_1, image_2, image_3, image_4, image_5, image_6]
    imgs    = [PIL.Image.open(i) for i in list_im]
    # pick the image which is the smallest, and resize the others to match it (can be arbitrary image shape here)
    min_shape = sorted([(np.sum(i.size), i.size) for i in imgs], reverse=True)[0][1]
    imgs_comb = np.hstack((np.asarray(i.resize(min_shape)) for i in imgs))

    # for a vertical stacking it is simple: use vstack
    imgs_comb = np.vstack((np.asarray(i.resize(min_shape)) for i in imgs))
    imgs_comb = PIL.Image.fromarray(imgs_comb)
    imgs_comb.save('/home/nick/.virtualenvs/twitterbots/bots/f_data_output/tmp/user_graphic.jpg')


class User:

    def __init__(self, user):

        self.user = user

    # returns lists of all user's tweets/retweets
    # tweets and retweets
    def get_user_status(self):

        all_tweets = Tweets.get_all_tweets()
        user_tweets = [x for x in all_tweets if
                       x[1] == self.user]

        all_retweets = Retweets.get_all_retweets()
        user_retweets = [x for x in all_retweets if
                         x[1] == self.user]

        all_user_tweets = user_tweets + user_retweets

        first_tweet = sorted(all_user_tweets, key=lambda x: dt.strptime(x[2], '%Y-%m-%d %H:%M:%S'))
        first_tweet = first_tweet[0]

        return all_user_tweets, user_tweets, user_retweets, first_tweet

if __name__ == '__main__':

    main()