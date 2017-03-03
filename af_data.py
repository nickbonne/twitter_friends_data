#!/home/nick/.virtualenvs/twitterbots/bin/python3.5

# import sqlite3

from tweets import AllTweets
from hashtags import Hashtags
from retweets import Retweets
from mentions import Mentions

# for a stat box similar to the one a user can request about themself
# no file to creating the graphic has been made yet.
# may just use this stuff for text posts in auto_st


def main():

    pass


class FriendStats:

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

    def users_mentioned():

        totals = Mentions.users_mentioned(AllTweets.get_all_tweets())

        return ('Total users mentioned {}'.format(str(len(totals[0]))),
                'Total unique mentions {}'.format(str(len(totals[1]))))


if __name__ == '__main__':

    main()
