#!/home/nick/.virtualenvs/twitterbots/bin/python3.5

import sqlite3
from datetime import datetime as dt
from nltk.tokenize import TweetTokenizer

'''

AllTweets doesn't filter anything.

Tweet class is for just tweets, retweets are filtered out.

'''


def main():

    # all_tweets = Tweets.get_all_tweets()

    # user_tweet_count = Tweets.tweets_per_user('jhudddd', all_tweets)
    # tpm_count = Tweets.tweets_per_minute(all_tweets)
    # tph_count = Tweets.tweets_per_hour(all_tweets)
    # tpd_count = Tweets.tweets_per_date(all_tweets)
    # weekday_count = Tweets.tweets_per_weekday(all_tweets)
    # monthly_count = Tweets.tweets_per_month(all_tweets)
    # tpy_count = Tweets.tweets_per_year(all_tweets)

    all_sources = Sources.get_all_sources()

    source_count = Sources.counted_sources(all_sources)
    source_count.sort(key=lambda x: int(x[1]), reverse=True)

    for i in source_count[:25]:

        print(i)

    # print(user_tweet_count)


class AllTweets:

    def get_all_tweets():

        # for connecting to main dump db
        conn = sqlite3.connect('tweet_dump.db')
        c = conn.cursor()

        c.execute('''SELECT tweet,
                            username,
                            tweet_date,
                            tweet_source
                     FROM tdump''')

        return c.fetchall()

    def all_tweets_per_user(user, tweet_list):

        return [x[1] for x in
                tweet_list if
                x[1] == user].count(user)

    def all_tweets_per_minute(tweet_list):

        tweet_times = [i[2][-8:-3] for i in tweet_list]

        time_counts = []
        seen_times = []

        for t_time in tweet_times:
            if t_time not in seen_times:

                seen_times.append(t_time)
                counted = tweet_times.count(t_time)
                time_counts.append([t_time, counted])

        return time_counts

    def all_tweets_per_hour(tweet_list):

        tweet_times = [i[2][-8:-6] for i in tweet_list]

        time_counts = []
        seen_times = []

        for t_time in tweet_times:
            if t_time not in seen_times:

                seen_times.append(t_time)
                counted = tweet_times.count(t_time)
                time_counts.append([t_time, counted])

        return time_counts

    def all_tweets_per_date(tweet_list):

        tweet_times = [i[2][:10] for i in tweet_list]

        time_counts = []
        seen_times = []

        for t_time in tweet_times:
            if t_time not in seen_times:

                seen_times.append(t_time)
                counted = tweet_times.count(t_time)
                time_counts.append([t_time, counted])

        return time_counts

    def all_tweets_per_weekday(tweet_list):

        tweet_times = [i[2][:10] for i in tweet_list]

        day_ints = []

        for t_time in tweet_times:

            dt_object = dt.strptime(t_time, '%Y-%m-%d')
            day_int = dt_object.weekday()
            day_ints.append(day_int)

        day_count = []
        seen_day = []

        for day in day_ints:

            if day not in seen_day:

                week = ['Monday', 'Tuesday', 'Wednesday', 'Thursday',
                        'Friday', 'Saturday', 'Sunday']

                seen_day.append(day)
                count = day_ints.count(day)
                day = week[day]
                day_count.append([day, count])

        return day_count

    def all_tweets_per_month(tweet_list):

        months = (
            'January',
            'Febuary',
            'March',
            'April',
            'May',
            'June',
            'July',
            'August',
            'September',
            'October',
            'November',
            'December',)

        times = [i[2][5:7] for i in tweet_list]

        time_list = []
        seen = []

        for t_time in times:

            if t_time not in seen:

                month = months[int(t_time) - 1]

                count = times.count(t_time)
                time_list.append([month, count])
                seen.append(t_time)

        return time_list

    def all_tweets_per_year(tweet_list):

            times = [i[2][:4] for i in tweet_list]

            time_list = []
            seen = []

            for t_time in times:

                if t_time not in seen:

                    count = times.count(t_time)
                    time_list.append([t_time, count])
                    seen.append(t_time)

            return time_list


class Tweets:

    def get_all_tweets():

        # for connecting to main dump db
        conn = sqlite3.connect('tweet_dump.db')
        c = conn.cursor()

        c.execute('''SELECT tweet,
                            username,
                            tweet_date,
                            tweet_source
                     FROM tdump''')

        all_tweets = c.fetchall()
        tweets = []

        twt_token = TweetTokenizer()

        for tweet in all_tweets:

            tokenized_twt = twt_token.tokenize(tweet[0])

            if not any(token for token in tokenized_twt if
                       token.upper() == 'RT'):

                tweets.append(tweet)

        return tweets

    def tweets_per_user(user, tweet_list):

        return [x[1] for x in
                tweet_list if
                x[1] == user].count(user)

    def tweets_per_minute(tweet_list):

        tweet_times = [i[2][-8:-3] for i in tweet_list]

        time_counts = []
        seen_times = []

        for t_time in tweet_times:
            if t_time not in seen_times:

                seen_times.append(t_time)
                counted = tweet_times.count(t_time)
                time_counts.append([t_time, counted])

        return time_counts

    def tweets_per_hour(tweet_list):

        tweet_times = [i[2][-8:-6] for i in tweet_list]

        time_counts = []
        seen_times = []

        for t_time in tweet_times:
            if t_time not in seen_times:

                seen_times.append(t_time)
                counted = tweet_times.count(t_time)
                time_counts.append([t_time, counted])

        return time_counts

    def tweets_per_date(tweet_list):

        tweet_times = [i[2][:10] for i in tweet_list]

        time_counts = []
        seen_times = []

        for t_time in tweet_times:
            if t_time not in seen_times:

                seen_times.append(t_time)
                counted = tweet_times.count(t_time)
                time_counts.append([t_time, counted])

        return time_counts

    def tweets_per_weekday(tweet_list):

        tweet_times = [i[2][:10] for i in tweet_list]

        day_ints = []

        for t_time in tweet_times:

            dt_object = dt.strptime(t_time, '%Y-%m-%d')
            day_int = dt_object.weekday()
            day_ints.append(day_int)

        day_count = []
        seen_day = []

        for day in day_ints:

            if day not in seen_day:

                week = ['Monday', 'Tuesday', 'Wednesday', 'Thursday',
                        'Friday', 'Saturday', 'Sunday']

                seen_day.append(day)
                count = day_ints.count(day)
                day = week[day]
                day_count.append([day, count])

        return day_count

    def tweets_per_month(tweet_list):

        months = (
            'January',
            'Febuary',
            'March',
            'April',
            'May',
            'June',
            'July',
            'August',
            'September',
            'October',
            'November',
            'December',)

        times = [i[2][5:7] for i in tweet_list]

        time_list = []
        seen = []

        for t_time in times:

            if t_time not in seen:

                month = months[int(t_time) - 1]

                count = times.count(t_time)
                time_list.append([month, count])
                seen.append(t_time)

        return time_list

    def tweets_per_year(tweet_list):

            times = [i[2][:4] for i in tweet_list]

            time_list = []
            seen = []

            for t_time in times:

                if t_time not in seen:

                    count = times.count(t_time)
                    time_list.append([t_time, count])
                    seen.append(t_time)

            return time_list

    def tweeted_words(tweet_list):

        twt_token = TweetTokenizer()
        words = ''

        # Folder where text files containing strings to be allowed or forbidden
        filter_path = '/home/nick/.virtualenvs/twitterbots/bots/'

        # Gets rid of '\n' and creates lists of filter items
        stopwords = [line.strip() for line in
                     open(filter_path + 'stopwords.txt')]

        for tweet in tweet_list:

            tokenized_twt = twt_token.tokenize(tweet[0])

            for i in tokenized_twt:

                if i.lower() not in stopwords \
                    and i[0] != '@' \
                        and i[0] != '#' \
                        and i[:4].lower() != 'http':

                    words = (words + ' ') + i

        return words


if __name__ == '__main__':

    main()
