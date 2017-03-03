#!/home/nick/.virtualenvs/twitterbots/bin/python3.5

import random

from text_status import Messages
from request_process import AllGraphic

'''
Using random module and dictionaries, a random dictonary
is selected and from that, a random key is selected.

'''


def main():

    pass


class RandomStatus:

    def random_post():

        text_post = {
            'active': [Messages.active, []],
            'hash': [Messages.hash, []],
            'rt': [Messages.retweet, []],
            'mention': [Messages.mention, []],
        }

        graphic_post = {
            'tweet_cloud': [AllGraphic.tweet_cloud,
                            'Most used words in tweets by people I follow. ' +
                            'Retweets omitted.'],

            'hash_cloud': [AllGraphic.hash_cloud,
                           'Most used hash tags, retweets not included.'],

            'mention_cloud': [AllGraphic.mention_cloud,
                              'Most mentioned Twitter users by people ' +
                              'I follow'],

            'rt_cloud': [AllGraphic.rt_cloud,
                         'Accounts retweeted the most by people I follow'],

            'rtvt_aio': [AllGraphic.rtvt_aio,
                         'Scatter plot of times each status was sent laid ' +
                         'over a single day.'],

            'per_day': [AllGraphic.per_day,
                        'Scatter plot showing total statuses per day since ' +
                        'first tweet in database.'],

            'sources': [AllGraphic.sources,
                        'Where you all do your tweeting from.'],

            'geo': [AllGraphic.geo,
                    'Users who share their location with each status.'],

            'retweet_pie': [AllGraphic.retweet_pie,
                            'How much you tweet vs how much you retweet.']
        }

        random_dict = random.choice([text_post, text_post, graphic_post])
        random_key = random.choice(list(random_dict.keys()))

        if random_dict == text_post:

            funct, args = random_dict[random_key]
            args = random.choice([7, 30])

            return funct(args)

        else:

            funct, message = random_dict[random_key]

            return funct(), message


if __name__ == '__main__':

    main()
