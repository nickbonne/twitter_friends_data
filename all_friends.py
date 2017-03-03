#!/home/nick/.virtualenvs/twitterbots/bin/python3.5

from tweets import Tweets
from tweets import AllTweets
from mentions import Mentions
from hashtags import Hashtags
from retweets import Retweets
from tweet_graphs import Graphs
from user_data import DatabaseStats
from phone_compare import Sources
from datetime import datetime as dt
from nltk.tokenize import TweetTokenizer


def main():

    pass


class AllFriends:

    # get lists of all friend's tweets and retweets
    def get_friend_statuses():

        # list of every tweet/retweet
        everything = AllTweets.get_all_tweets()
        everything = sorted(everything,
                            key=lambda x: dt.strptime(x[2],
                                                      '%Y-%m-%d %H:%M:%S'))

        return everything

    # just tweets
    def get_friends_tweets():

        return Tweets.get_all_tweets()

    # just retweets
    def get_friends_retweets():

        return Retweets.get_all_retweets()

    # checks database for new entries, appends text files
    # tracking tweets, retweeted users, hashtags, or mentions
    # running for first time on 200k+ entries took well over an hour
    def update_cloud_strings_only_tweets(tweet_list):

        # Folder where text files containing
        # stopwords, holding places in databases, counts, etc
        filter_path = '/home/nick/.virtualenvs/twitterbots/bots/control_files/'

        # newest tweet_id
        new_placemarker = tweet_list[-1][3]

        with open((filter_path + 'place_holder.txt'), 'r') as f:

            placemarker = int(f.read().strip())

        with open((filter_path + 'place_holder.txt'), 'w') as f:

            f.write(new_placemarker)

        twt_token = TweetTokenizer()

        # Gets rid of '\n' and creates lists of filter items
        stopwords = [line.strip() for line in
                     open(filter_path + 'stopwords.txt')]

        tweet_list = [x[0] for x in tweet_list
                      if int(x[3]) > placemarker]

        tweet_list = ' '.join([x for x in tweet_list])

        tokenized_twt = twt_token.tokenize(tweet_list)

        words = ''

        for i in tokenized_twt:

            if i.lower() not in stopwords \
                and i[0] != '@' \
                    and i[0] != '#' \
                    and i[:4].lower() != 'http':

                words = (words + ' ') + i

        words = ' ' + words

        with open((filter_path + 'massive_tweet.txt'), 'a') as f:

            f.write(words.lower())

    def update_cloud_string_hashtags(tweet_list):

        f_path = '/home/nick/.virtualenvs/twitterbots/bots/control_files/'

        tweet_list = sorted(tweet_list,
                            key=lambda x: dt.strptime(x[2],
                                                      '%Y-%m-%d %H:%M:%S'))

        new_placemarker = tweet_list[-1][2]

        with open((f_path + 'place_holder_hashtag.txt'), 'r') as f:

            placemarker = f.read()

        with open((f_path + 'place_holder_hashtag.txt'), 'w') as f:

            f.write(new_placemarker)

        placemarker = placemarker.strip()

        tweet_list = [x for x in tweet_list
                      if dt.strptime(x[2], '%Y-%m-%d %H:%M:%S') >
                      dt.strptime(placemarker, '%Y-%m-%d %H:%M:%S')]

        hashtag_list = Hashtags.get_all_hashtags(tweet_list)

        hashtag_stats = Hashtags.count_hashtags(hashtag_list)

        hashtags = [x[0] for x in hashtag_stats]
        hash_nums = [x[1] for x in hashtag_stats]

        hashtag_counts = zip(hashtags, hash_nums)

        hashtag_string = ''

        for hash_data in hashtag_counts:

            baby_string = (hash_data[0] + ' ') * int(hash_data[1])
            baby_string = baby_string.strip()
            hashtag_string = (hashtag_string + ' ') + baby_string

        hashtag_string = ' ' + hashtag_string

        with open((f_path + 'massive_hashtag.txt'), 'a') as f:

            f.write(hashtag_string)

    def update_cloud_string_mentions(tweet_list):

        f_path = '/home/nick/.virtualenvs/twitterbots/bots/control_files/'

        tweet_list = sorted(tweet_list,
                            key=lambda x: dt.strptime(x[2],
                                                      '%Y-%m-%d %H:%M:%S'))

        new_placemarker = tweet_list[-1][2]

        with open((f_path + 'place_holder_mention.txt'), 'r') as f:

            placemarker = f.read()

        with open((f_path + 'place_holder_mention.txt'), 'w') as f:

            f.write(new_placemarker)

        placemarker = placemarker.strip()

        tweet_list = [x for x in tweet_list
                      if dt.strptime(x[2], '%Y-%m-%d %H:%M:%S') >
                      dt.strptime(placemarker, '%Y-%m-%d %H:%M:%S')]

        mention_stats = Mentions.users_mentioned(tweet_list)[1]

        mentioned_users = [x[0] for x in mention_stats]
        mention_nums = [x[1] for x in mention_stats]

        mention_counts = zip(mentioned_users, mention_nums)

        mention_string = ''

        for mention in mention_counts:

            baby_string = (mention[0] + ' ') * int(mention[1])
            baby_string = baby_string.strip()
            mention_string = (mention_string + ' ') + baby_string

        mention_string = ' ' + mention_string

        with open((f_path + 'massive_mention.txt'), 'a') as f:

            f.write(mention_string)

    def update_cloud_string_retweeted_users(tweet_list):

        f_path = '/home/nick/.virtualenvs/twitterbots/bots/control_files/'

        tweet_list = sorted(tweet_list,
                            key=lambda x: dt.strptime(x[2],
                                                      '%Y-%m-%d %H:%M:%S'))

        new_placemarker = tweet_list[-1][2]

        with open((f_path + 'place_holder_retweet.txt'), 'r') as f:

            placemarker = f.read()

        with open((f_path + 'place_holder_retweet.txt'), 'w') as f:

            f.write(new_placemarker)

        placemarker = placemarker.strip()

        tweet_list = [x for x in tweet_list
                      if dt.strptime(x[2], '%Y-%m-%d %H:%M:%S') >
                      dt.strptime(placemarker, '%Y-%m-%d %H:%M:%S')]

        retweeted_stats = Retweets.get_retweeted_users(tweet_list)[1]

        retweeted_users = [x[0] for x in retweeted_stats]
        retweet_nums = [x[1] for x in retweeted_stats]

        retweet_counts = zip(retweeted_users, retweet_nums)

        retweet_string = ''

        for retweet in retweet_counts:

            baby_string = (retweet[0] + ' ') * int(retweet[1])
            baby_string = baby_string.strip()
            retweet_string = (retweet_string + ' ') + baby_string

        retweet_string = ' ' + retweet_string

        with open((f_path + 'massive_retweet.txt'), 'a') as f:

            f.write(retweet_string)

    # text files maintained by above functions read
    # into strings and used to create word clouds
    def create_tweet_word_cloud():

        path = '/home/nick/.virtualenvs/twitterbots/bots/control_files/'

        with open(path + 'massive_tweet.txt', 'r') as f:

            tweet_string = f.read()

        tweet_string = tweet_string.strip()

        return Graphs.tweeted_word_cloud(tweet_string, __class__)

    def create_retweet_cloud():

        path = '/home/nick/.virtualenvs/twitterbots/bots/control_files/'

        with open(path + 'massive_retweet.txt', 'r') as f:

            retweet_string = f.read()

        retweet_string = retweet_string.strip()

        return Graphs.retweeted_word_cloud(retweet_string, __class__)

    def create_hashtag_cloud():

        path = '/home/nick/.virtualenvs/twitterbots/bots/control_files/'

        with open(path + 'massive_hashtag.txt', 'r') as f:

            hashtag_string = f.read()

        hashtag_string = hashtag_string.strip()

        return Graphs.hashtag_word_cloud(hashtag_string, __class__)

    def create_mention_cloud():

        path = '/home/nick/.virtualenvs/twitterbots/bots/control_files/'

        with open(path + 'massive_mention.txt', 'r') as f:

            mention_string = f.read()

        mention_string = mention_string.strip()

        return Graphs.mention_word_cloud(mention_string, __class__)

    # who has geolocation enabled and who doesn't
    def create_geo_pie():

        geo_data = DatabaseStats.geo_on_off()
        true_count, false_count = geo_data[0], geo_data[1]
        return Graphs.geo_pie(true_count, false_count)

    # which apps are being used to send tweets
    def create_source_pie():

        source_list = Sources.get_all_sources()
        source_count = Sources.counted_sources(source_list)
        return Graphs.tweet_source_pie(source_count, __class__)

    # makeup of database when looking at regular
    # tweets versuses retweets
    def create_retweet_pie(tweet_list, retweet_list):

        tweets = len(tweet_list)
        retweets = len(retweet_list)

        return Graphs.retweet_pie(tweets, retweets, __class__)

    # All tweets plotted in 24 hour period
    def create_aio_plot(tweet_list):

        graph_coords = Tweets.tweets_per_minute(tweet_list)
        graph_coords.sort(key=lambda x: int(x[1]), reverse=True)

        return Graphs.all_in_one(graph_coords, __class__)

    # Total number of statuses sent each day
    # on a scatter plot
    def create_per_day_plot(tweet_list):

        graph_coords = AllTweets.all_tweets_per_date(tweet_list)
        graph_coords.sort(key=lambda x: int(x[1]), reverse=True)

        return Graphs.total_tweets_per_day(graph_coords, __class__)

    # looks the same as aio plot but two sets
    # of data are graphed, regular tweets and retweets
    def create_rtvt_aio_plot(tweet_list, retweet_list):

        tweet_coords = Tweets.tweets_per_minute(tweet_list)
        retweet_coords = Retweets.retweets_per_minute(retweet_list)

        tweet_coords.sort(key=lambda x: int(x[1]), reverse=True)
        retweet_coords.sort(key=lambda x: int(x[1]), reverse=True)

        return Graphs.rtwt_vs_twt_24h(retweet_coords,
                                      tweet_coords,
                                      __class__)

# More graphs?


if __name__ == '__main__':

    main()
