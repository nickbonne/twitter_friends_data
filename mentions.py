#!/home/nick/.virtualenvs/twitterbots/bin/python3.5

import sqlite3
from nltk.tokenize import TweetTokenizer


def main():

    pass


class Mentions:

    # returns list of all users mentioned if 
    # token before is not 'RT' or 'rt'
    def users_mentioned(tweet_list):

        twt_token = TweetTokenizer()
        mentioned = []

        for tweet in tweet_list:

            tokenized_twt = twt_token.tokenize(tweet[0])
            last_token = ''

            for i in tokenized_twt:

                if i[0] == '@' and last_token.lower() != 'rt':

                    mentioned.append(i)

        mention_count = set([(x, mentioned.count(x)) for x in mentioned])

        return mentioned, mention_count


if __name__ == '__main__':

    main()
