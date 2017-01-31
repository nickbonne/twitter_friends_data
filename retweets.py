#!/home/nick/.virtualenvs/twitterbots/bin/python3.5

import sqlite3
from nltk.tokenize import TweetTokenizer


def main():

    all_retweets = Retweets.get_all_retweets()

    # user_retweets = Retweets.get_user_retweets('jhudddd', all_retweets)
    # retweeted_users = Retweets.get_retweeted_users(all_retweets)
    # rt_time_count = Retweets.retweets_per_minute(all_retweets)

    # for i in rt_time_count:
    #     print(i)
    # print(len(all_retweets))


class Retweets:

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

    def get_user_retweets(user, retweet_list):

        user_retweets = [i for i in retweet_list if
                         i[1] == user]

        return user_retweets

    def retweets_per_user(user, retweet_list):

        return len([i for i in retweet_list if
                i[1] == user])

    # return list of every time a user was retweeted
    def get_retweeted_users(retweet_list):

        twt_token = TweetTokenizer()
        retweeted_users = []

        for retweet in retweet_list:

            tokenized_twt = twt_token.tokenize(retweet[0])

            last_token = ''

            if tokenized_twt[0] == 'RT':

                last_token = 'RT'

            for token in tokenized_twt[1:]:

                if token[0] == '@' and last_token == 'RT':

                    retweeted_users.append(token)
                    last_token = token

        return retweeted_users

    # for 24H flattened graph
    # dates are trimmed to just times (HH:MM)
    # duplicates are counted
    def retweets_per_minute(retweet_list):

        retweet_times = [i[2][-8:-3] for i in retweet_list]

        time_counts = []
        seen_times = []

        for rt_time in retweet_times:

            if rt_time not in seen_times:

                seen_times.append(rt_time)
                counted = retweet_times.count(rt_time)
                time_counts.append([rt_time, counted])

        return time_counts


if __name__ == '__main__':

    main()