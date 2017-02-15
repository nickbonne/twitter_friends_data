#!/home/nick/.virtualenvs/twitterbots/bin/python3.5

from tz_fix import TimeFix
from personal import User
from all_friends import AllFriends


'''
Many functions will now require user_id to be passed in
for fixing tweet times to a users local time
'''


def main():

    tweet = ['Okay, I\'ll bite @BonneNick --user_statbox',
             'jhudddd',
             '2017-02-02 22:45:54',
             '827286951837458433',
             'Twitter for iPhone',
             '61561677']

    Screen.is_command(tweet)


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

                cmd = [x for x in split_tweet if x in commands][0]

            except IndexError:

                cmd = ''

            # empty string
            if cmd == '':

                pass

            elif cmd in commands:

                pair = [tweet, cmd]

                twt_cmd_pairs.append(pair)

        return twt_cmd_pairs

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

                result = UserGraphic.usage(tweet)

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

    def help(tweet, *args):

        path = '/home/nick/.virtualenvs/twitterbots/bots/control_files/'

        with open(path + 'help_message.txt', 'r') as f:

            help_message = f.read().strip()

        with open(path + 'command_error.txt', 'r') as f:

            command_message = f.read().strip()

        if args is False:

            return tweet, command_message

        return tweet, help_message


class AllGraphic:

    def tweet_cloud():

        path = '/home/nick/.virtualenvs/twitterbots/bots/output/tmp/'
        filename = 'f_word_cloud'
        AllFriends.create_tweet_word_cloud()

        return path + filename

    def hash_cloud():

        path = '/home/nick/.virtualenvs/twitterbots/bots/output/tmp/'
        filename = 'f_hash_cloud'
        AllFriends.create_hashtag_cloud()

        return path + filename

    def mention_cloud():

        path = '/home/nick/.virtualenvs/twitterbots/bots/output/tmp/'
        filename = 'f_mention_cloud'
        AllFriends.create_mention_cloud()

        return path + filename

    def rt_cloud():

        path = '/home/nick/.virtualenvs/twitterbots/bots/output/tmp/'
        filename = 'f_rt_cloud'
        AllFriends.create_retweet_cloud()

        return path + filename

    def aio():

        path = '/home/nick/.virtualenvs/twitterbots/bots/output/tmp/'
        filename = 'f_aio'
        AllFriends.create_aio_plot(AllFriends.get_friend_statuses()[0])

        return path + filename

    def rtvt_aio():

        path = '/home/nick/.virtualenvs/twitterbots/bots/output/tmp/'
        filename = 'f_rtvt_aio'
        AllFriends.create_rtvt_aio_plot(AllFriends.get_friends_tweets(),
                                        AllFriends.get_friends_retweets())

        return path + filename

    def per_day():

        path = '/home/nick/.virtualenvs/twitterbots/bots/output/tmp/'
        filename = 'f_per_day'
        AllFriends.create_per_day_plot(AllFriends.get_friends_tweets())

        return path + filename

    def sources():

        path = '/home/nick/.virtualenvs/twitterbots/bots/output/tmp/'
        filename = 'f_source_pie'
        AllFriends.create_source_pie()

        return path + filename

    def geo():

        path = '/home/nick/.virtualenvs/twitterbots/bots/output/tmp/'
        filename = 'geolocation'
        AllFriends.create_geo_pie()

        return path + filename

    def retweet_pie():

        path = '/home/nick/.virtualenvs/twitterbots/bots/output/tmp/'
        filename = 'f_retweet_pie'
        AllFriends.create_retweet_pie(AllFriends.get_friends_tweets(),
                                      AllFriends.get_friends_retweets())

        return path + filename


# tweet already contains user_id
# isolate var and call tz_fix before
# passing list of tweets on
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

    def usage(tweet):

        path = '/home/nick/.virtualenvs/twitterbots/bots/output/tmp/'
        filename = 'per_day.png'

        statuses = User(tweet[5]).user_statuses()[0]
        statuses = TimeFix.adjust_datetimes(tweet[5], statuses)

        User.create_per_day_plot(tweet[5],
                                 statuses)

        return path + filename


if __name__ == '__main__':

    main()
