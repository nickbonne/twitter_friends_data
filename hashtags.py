#!/home/nick/.virtualenvs/twitterbots/bin/python3.5

import sqlite3
from nltk.tokenize import TweetTokenizer


def main():

    all_tweets = Hashtags.get_all_tweets()
    # all_hashtags = Hashtags.get_all_hashtags(all_tweets)
    user_hashtags = Hashtags.get_user_hashtags('jhudddd', all_tweets)
    counted_tags = Hashtags.count_hashtags(user_hashtags[0])

    print(counted_tags)


class Hashtags:

    def get_all_tweets():

        # for connecting to main dump db
        conn = sqlite3.connect('tweet_dump.db')
        c = conn.cursor()

        c.execute('''SELECT tweet,
                            username,
                            tweet_date
                     FROM tdump''')

        all_tweets = c.fetchall()

        return all_tweets

    def get_all_hashtags(tweet_list):

        all_tweets = [i[0] for i in tweet_list]
        twt_tokenize = TweetTokenizer()
        tweet_tokens = []

        for tweet in all_tweets:

            tokenized_twt = twt_tokenize.tokenize(tweet)
            tweet_tokens.extend(tokenized_twt)

        hashtags = [token for token in tweet_tokens if
                    token[0] == '#' and
                    len(token) > 1]

        return hashtags

    def get_user_hashtags(tweet_list):

        # user_tweets = [i for i in tweet_list if
        #                i[1] == user]

        all_user_hashtags = Hashtags.get_all_hashtags(tweet_list)

        # rest of funct will find hashtags
        # that are not in retweets

        twt_tokenize = TweetTokenizer()
        tweet_tokens = []

        for tweet in tweet_list:

            tokenized_twt = twt_tokenize.tokenize(tweet[0])

            if not any(token for token in tokenized_twt if token == 'RT'):

                tweet_tokens.extend(tokenized_twt)

        not_retweet_hashtags = [token for token in tweet_tokens if
                                token[0] == '#' and
                                len(token) > 1]

        return [all_user_hashtags, not_retweet_hashtags]

    def count_hashtags(hashtag_list):

        return set([(x, hashtag_list.count(x)) for x in hashtag_list])


if __name__ == '__main__':

    main()
