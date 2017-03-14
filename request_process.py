#!/home/nick/.virtualenvs/twitterbots/bin/python3.5

from tz_fix import TimeFix
from personal import User
from all_friends import AllFriends


'''
Many functions will now require user_id to be passed in
for fixing tweet times to a users local time
'''


def main():

    pass


class Screen:

    # only finds and handles first command
    # takes list of tweets with me mentioned
    # looks for commands returns list of jobs to be
    # pooled
    def is_command(tweet_list):

        twt_cmd_pairs = []

        commands = ['--help',
                    '--user_statbox',
                    '--user_tweet_cloud',
                    '--user_retweet_pie',
                    '--user_sources',
                    '--user_aio_plot',
                    '--user_usage',
                    '--all_statbox',
                    '--all_tweet_cloud',
                    '--all_hash_cloud',
                    '--all_mention_cloud',
                    '--all_rt_cloud',
                    '--all_aio',
                    '--all_rtvt_aio',
                    '--all_per_day',
                    '--all_sources',
                    '--all_geo',
                    '--all_retweet_pie']

        for tweet in tweet_list:

            split_tweet = tweet[0].lower().split()

            try:

                cmd = [x for x in split_tweet
                       if x.rstrip('?:!.,;') in commands][0]

            except IndexError:

                cmd = ''

            # empty string
            if cmd == '':

                pass

            elif cmd in commands:

                pair = [tweet, cmd]

                twt_cmd_pairs.append(pair)

        return twt_cmd_pairs

    # sends tweet info to funct matcing command
    def direct_request(tweet, cmd):

        if cmd[:7] == '--user_':

            if cmd == '--user_statbox':

                result = UserGraphic.statbox(tweet)

            elif cmd == '--user_tweet_cloud':

                result = UserGraphic.tweet_cloud(tweet)

            elif cmd == '--user_retweet_pie':

                result = UserGraphic.retweet_pie(tweet)

            elif cmd == '--user_aio_plot':

                result = UserGraphic.aio_plot(tweet)

            elif cmd == '--user_sources':

                result = UserGraphic.sources(tweet)

            elif cmd == '--user_usage':

                result = UserGraphic.per_day(tweet)

        elif cmd[:6] == '--all_':

            if cmd == '--all_statbox':

                return Screen.help(tweet, False)

            elif cmd == '--all_tweet_cloud':

                result = AllGraphic.tweet_cloud()

            elif cmd == '--all_hash_cloud':

                result = AllGraphic.hash_cloud()

            elif cmd == '--all_mention_cloud':

                result = AllGraphic.mention_cloud()

            elif cmd == '--all_rt_cloud':

                result = AllGraphic.rt_cloud()

            elif cmd == '--all_aio':

                result = AllGraphic.aio()

            elif cmd == '--all_rtvt_aio':

                result = AllGraphic.rtvt_aio()

            elif cmd == '--all_per_day':

                result = AllGraphic.per_day()

            elif cmd == '--all_sources':

                result = AllGraphic.sources()

            elif cmd == '--all_geo':

                result = AllGraphic.geo()

            elif cmd == '--all_retweet_pie':

                result = AllGraphic.retweet_pie()

        return result

    # handling for the --help command
    def help(tweet, *args):

        path = '/home/nick/.virtualenvs/twitterbots/bots/control_files/'

        with open(path + 'help_message.txt', 'r') as f:

            help_message = f.read().strip()

        with open(path + 'command_error.txt', 'r') as f:

            command_message = f.read().strip()

        if args is False:

            return tweet, command_message

        return tweet, help_message


'''

Two classes below have functions that call functions from
tweet_graphs.py to create the graphic the user requested.

The path of the resulting file is returned.

UserGraphic class' fucntions need tweet variable because the
user data needed to create the graphic resides there.

'''


class AllGraphic:

    def tweet_cloud():

        return AllFriends.create_tweet_word_cloud()

    def hash_cloud():

        return AllFriends.create_hashtag_cloud()

    def mention_cloud():

        return AllFriends.create_mention_cloud()

    def rt_cloud():

        return AllFriends.create_retweet_cloud()

    def aio():

        statuses = TimeFix.adjust_datetimes('1413240876',
                                            AllFriends.get_friend_statuses()[0])

        return AllFriends.create_aio_plot(statuses)

    def rtvt_aio():

        tweets = TimeFix.adjust_datetimes('1413240876',
                                          AllFriends.get_friends_tweets())

        retweets = TimeFix.adjust_datetimes('1413240876',
                                            AllFriends.get_friends_retweets())

        return AllFriends.create_rtvt_aio_plot(tweets,
                                               retweets)

    def per_day():

        return AllFriends.create_per_day_plot(AllFriends.get_friends_tweets())

    def sources():

        return AllFriends.create_source_pie()

    def geo():

        return AllFriends.create_geo_pie()

    def retweet_pie():

        return AllFriends.create_retweet_pie(AllFriends.get_friends_tweets(),
                                             AllFriends.get_friends_retweets())


# Not as many options because of lack of data
# points on individual users.
class UserGraphic:

    def statbox(tweet):

        tweets = User(tweet[5]).user_tweets()
        tweets = TimeFix.adjust_datetimes(tweet[5], tweets)

        retweets = User(tweet[5]).user_retweets()
        retweets = TimeFix.adjust_datetimes(tweet[5], retweets)

        statuses = User(tweet[5]).user_statuses()[0]
        statuses = TimeFix.adjust_datetimes(tweet[5], statuses)

        box_data = User.user_data_box(tweet[5],
                                      tweets,
                                      retweets,
                                      statuses)

        box_strings = User.box_string(tweet[5], box_data)
        create = User.create_stat_box(tweet[5], box_strings)

        return str(create)

    def tweet_cloud(tweet):

        path = '/home/nick/.virtualenvs/twitterbots/bots/output/tmp/'
        filename = 'word_cloud.png'

        tweets = User(tweet[5]).user_tweets()
        tweets = TimeFix.adjust_datetimes(tweet[5], tweets)

        User.create_tweet_cloud(tweet[5],
                                tweets)

        return path + filename

    def retweet_pie(tweet):

        path = '/home/nick/.virtualenvs/twitterbots/bots/output/tmp/'
        filename = 'retweet_pie.png'

        tweets = User(tweet[5]).user_tweets()
        tweets = TimeFix.adjust_datetimes(tweet[5], tweets)

        retweets = User(tweet[5]).user_retweets()
        retweets = TimeFix.adjust_datetimes(tweet[5], retweets)

        User.create_retweet_pie(tweet[5],
                                tweets,
                                retweets)
        return path + filename

    def sources(tweet):

        path = '/home/nick/.virtualenvs/twitterbots/bots/output/tmp/'
        filename = 'source_pie'

        statuses = User(tweet[5]).user_statuses()[0]
        statuses = TimeFix.adjust_datetimes(tweet[5], statuses)

        User.create_source_pie(tweet[5],
                               statuses)

        return path + filename

    def aio_plot(tweet):

        path = '/home/nick/.virtualenvs/twitterbots/bots/output/tmp/'
        filename = 'aio.png'

        statuses = User(tweet[5]).user_statuses()[0]
        statuses = TimeFix.adjust_datetimes(tweet[5], statuses)

        User.create_aio_plot(tweet[5],
                             statuses)

        return path + filename

    def per_day(tweet):

        path = '/home/nick/.virtualenvs/twitterbots/bots/output/tmp/'
        filename = 'per_day.png'

        statuses = User(tweet[5]).user_statuses()[0]
        statuses = TimeFix.adjust_datetimes(tweet[5], statuses)

        User.create_per_day_plot(tweet[5],
                                 statuses)

        return path + filename


if __name__ == '__main__':

    main()
