#!/home/nick/.virtualenvs/twitterbots/bin/python3.5

import os
import re
import time
import sqlite3
from os import path
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates
import matplotlib.patches as mpatches
from datetime import datetime as dt
from wordcloud import WordCloud
from wordcloud import ImageColorGenerator
from nltk.tokenize import TweetTokenizer


def main():

    start = time.time()

    conn = sqlite3.connect('tweet_dump.db')
    c = conn.cursor()

    # get list of user's screen names
    c.execute('SELECT username FROM tdump')
    users = c.fetchall()
    users = list(set([user[0] for user in users]))
    users = str(len(users))

    try:

        os.mkdir('/home/nick/.virtualenvs/twitterbots/bots/f_data_output/' + users)

    except Exception as e:

        pass

    save_dir = '/home/nick/.virtualenvs/twitterbots/bots/f_data_output/' + users + '/'

    c.execute('SELECT tweet FROM tdump')
    total = c.fetchall()
    print('Total tweets: {}'.format(str(len(total))))

    # Users sorted by number of tweets
    most_tweets = tweets_per_user(c, conn)
    most_tweets.sort(key=lambda x: int(x[1]), reverse=True)

    # Tweets per minute for each minute in a day
    most_times_total = total_time_tweet(tweets_date_list(c, conn))[0]
    most_times_total.sort(key=lambda x: int(x[1]), reverse=True)
    # Graphing above
    one_day_chart(most_times_total, users, save_dir)

    # Total tweets for each day in db
    most_days = day_tweet(tweets_date_list(c, conn))
    most_days.sort(key=lambda x: int(x[1]), reverse=True)
    most_days.sort(key=lambda x: str(x[0]))
    # Graphing above
    day_count_chart(most_days, users, save_dir)

    # Total tweets per month
    most_months = month_tweet(tweets_date_list(c, conn))
    most_months.sort(key=lambda x: int(x[1]), reverse=True)

    # Tweets per year
    most_years = year_tweet(tweets_date_list(c, conn))
    most_years.sort(key=lambda x: int(x[1]), reverse=True)

    # Most popular hashtags
    top_tags = popular_hash(hashtags(c, conn))
    top_tags.sort(key=lambda x: int(x[1]), reverse=True)
    # Make word cloud from top hashtags
    word_cloud(top_tags, users, save_dir)

    # Total tweets for each day of week
    most_weekday = weekday_tweet(tweets_date_list(c, conn))
    most_weekday.sort(key=lambda x: int(x[1]), reverse=True)

    # Counts number of total retweets and
    # most retweeted handles
    rt_count = retweets(c, conn)[0]
    most_rt = retweets(c, conn)[1]
    most_rt.sort(key=lambda x: int(x[1]), reverse=True)

    retweet_pie(rt_count, total, users, save_dir)

    # Plotting when users send retweets
    most_rt_time = rt_times(c, conn)
    tweet_dates = tweet_times(c, conn)[0]
    tweet_counts = tweet_times(c, conn)[1]

    rtvt_one_day_chart(most_rt_time,
                       users,
                       save_dir,
                       tweet_dates,
                       tweet_counts)

    print('Finished in {} seconds.'.format(round((time.time()) - start), 3))

# counts number of tweets from each friend
def tweets_per_user(c, conn):

    # Collect list of tweet's users
    c.execute('SELECT username FROM tdump')
    all_tweets = c.fetchall()
    all_tweets = [tweet[0] for tweet in all_tweets]

    tweet_list = []
    seen = []  # Prevents recurrences in tweet_list

    for user in all_tweets:

        if user not in seen:

            # counting username recurrences in
            # main list and creating list of results
            tweets = all_tweets.count(user)
            tweet_list.append([user, tweets])
            seen.append(user)

    # adds results to twitter_dump_data.db
    finish(tweet_list, 'tweets_per_user')

    return tweet_list

# returns list of dates without seconds values
def tweets_date_list(c, conn):

    c.execute('SELECT tweet_date FROM tdump')
    dates = c.fetchall()
    dates = [date[0][:-3] for date in dates]

    return dates

# Flattens dates to only hour and minute values
# returns number of tweets for each minute in 24 hours
def total_time_tweet(dates):

    times = [date[-5:] for date in dates]
    time_list = []
    seen = []

    for time in times:

        if time not in seen:

            count = times.count(time)
            time_list.append([time, count])
            seen.append(time)

    finish(time_list, 'tweets_per_minute')

    return time_list, seen


# finds total number of tweets for each
# yyyy/mm/dd value in db
def day_tweet(dates):

    times = [date[:10] for date in dates]

    time_list = []
    seen = []

    for time in times:

        if time not in seen:

            count = times.count(time)
            time_list.append([time, count])
            seen.append(time)

    return time_list


# counts tweets for each day of the week
# dates are coverted to weekday values('monday')
def weekday_tweet(dates):

    times = [date[:10] for date in dates]

    day_ints = []

    for time_ in times:

        dt_object = dt.strptime(time_, '%Y-%m-%d')
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


# dates are flatten to only months
# counts number of total tweets each month
def month_tweet(dates):

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

    times = [date[5:7] for date in dates]

    time_list = []
    seen = []

    for time_ in times:

        if time_ not in seen:

            month = months[int(time_) - 1]

            count = times.count(time_)
            time_list.append([month, count])
            seen.append(time_)

    return time_list


# dates are flattened to years
# total tweets per year counted
def year_tweet(dates):

    times = [date[:4] for date in dates]

    time_list = []
    seen = []

    for time in times:

        if time not in seen:

            count = times.count(time)
            time_list.append([time, count])
            seen.append(time)

    return time_list


#NLTK used to break down tweets so hashtags
# can be easily picked and listed
def hashtags(c, conn):

    c.execute('SELECT tweet FROM tdump')
    all_tweets = c.fetchall()
    all_tweets = [tweet[0] for tweet in all_tweets]

    hashtags = []
    tweet_elements = []

    tweet_token = TweetTokenizer()

    for tweet in all_tweets:

        broken_tweet = tweet_token.tokenize(tweet)
        tweet_elements.extend(broken_tweet)

    for te in tweet_elements:

        if re.match(r'^#', te) and (len(te) > 1):

            hashtags.append(te)

    return hashtags


# list returned by hashtag fucnt is counted
# a case lowered tag is counted on a case lowered
# list for better accuracy. listed tag is first 
# occurence in original case list
def popular_hash(hashtags):

    hash_count = []
    seen = []

    for hashtag in hashtags:

        if hashtag.lower() not in seen:

            seen.append(hashtag.lower())
            count = [ht.lower() for ht in hashtags].count(hashtag.lower())
            hash_count.append([hashtag, count])

    finish(hash_count, 'popular_hashtags')

    return hash_count   


# graph of returned value of total_time_tweet function
def one_day_chart(count_list, users, save_dir):

    counted, one_counts = zip(*count_list)
    list_of_datetimes = [dt.strptime(c, '%H:%M') for c in counted]
    one_dates = matplotlib.dates.date2num(list_of_datetimes)

    fig = plt.figure()

    ax = fig.add_subplot(111)
    fig.subplots_adjust(top=0.9,
                        bottom=0.17,
                        left=0.08,
                        right=0.97)

    ax.set_title('All Tweets Over 24 Hours')
    ax.set_xlabel('Time')
    ax.set_ylabel('Tweets')
    plt.style.use('bmh')
    plt.xticks(rotation=45)
    matplotlib.pyplot.plot_date(one_dates, one_counts)
    # plt.show()
    plt.savefig(save_dir + '24h_all_tweets_{}f'.format(users))


# retweet vs tweet graph, the one_day_chart with
# two scatter plots, one for tweets, the other retweets
def rtvt_one_day_chart(count_list, users, save_dir, t_dates, t_counts):

    counted, counts = zip(*count_list)
    list_of_datetimes = [dt.strptime(c, '%H:%M') for c in counted]
    dates = matplotlib.dates.date2num(list_of_datetimes)

    fig = plt.figure()

    ax = fig.add_subplot(111)
    fig.subplots_adjust(top=0.9,
                        bottom=0.17,
                        left=0.08,
                        right=0.97)

    ax.set_title('Tweets and Retweets Over 24 Hours')
    ax.set_xlabel('Time')
    ax.set_ylabel('Occurences per minute')
    plt.style.use('bmh')
    plt.xticks(rotation=45)
    matplotlib.pyplot.plot_date(dates, counts, color='gray')
    matplotlib.pyplot.plot_date(t_dates, t_counts, color='lightskyblue')

    tweet_patch = mpatches.Patch(color='lightskyblue', label='Tweets')
    retweet_patch = mpatches.Patch(color='gray', label='Retweets')
    plt.legend(handles=[tweet_patch, retweet_patch],
               loc='upper right',
               shadow='True')
    # plt.show()
    plt.savefig(save_dir + '24h_retweets_{}f'.format(users))


# graph of returned value of day_tweet function
def day_count_chart(count_list, users, save_dir):

    counted, counts = zip(*count_list)
    list_of_datetimes = [dt.strptime(c, '%Y-%m-%d') for c in counted]
    dates = matplotlib.dates.date2num(list_of_datetimes)

    fig = plt.figure()

    ax = fig.add_subplot(111)
    fig.subplots_adjust(top=0.9,
                        bottom=0.13,
                        left=0.09,
                        right=0.98)

    ax.set_title('Total Tweets per Day')
    ax.set_xlabel('Date')
    ax.set_ylabel('Tweets')
    plt.style.use('bmh')
    plt.xticks(rotation=45)
    matplotlib.pyplot.plot_date(dates, counts)
    plt.plot(dates, np.poly1d(np.polyfit(dates, counts, 1))(dates))
    # plt.show()
    plt.savefig(save_dir + 'tweets_per_day_{}f'.format(users))


# thanks to https://github.com/amueller/word_cloud
# input is a text field of all occurences of
# every hashtag. Image used to shape and
# color the cloud
def word_cloud(hash_count, users, save_dir):

    text = ''

    for hashtag in hash_count:

        hash_text = (hashtag[0] + ' ') * hashtag[1]
        text = text + hash_text.strip() + ' '

    d = path.dirname(__file__)

    twitter_mask = np.array(Image.open(path.join(d, 'twitter_icon.png')))

    wc = WordCloud(background_color='black',
                   max_words=2000,
                   mask=twitter_mask,)

    wc.generate(text)
    image_colors = ImageColorGenerator(twitter_mask)
    wc.recolor(color_func=image_colors).to_file(path.join(d,
                         save_dir + 'tweet_cloud_{}f.png'.format(users)))


# simple pie graph of tweet to retweet ratio
def retweet_pie(retweets, total, users, save_dir):

    labels = 'Tweets', 'Retweets'
    sizes = [len(total) - retweets, retweets]
    colors = ['lightskyblue', 'lightgrey']
    explode = (0, 0.1)

    fig1, ax1 = plt.subplots(111)
    ax1.pie(sizes, explode=explode, labels=labels, autopct='%1.1f%%',
            shadow=True, startangle=90, colors=colors)
    ax1.axis('equal')
    # plt.show()
    plt.savefig(save_dir + 'tweet_rt_ratio_{}f'.format(users))


# returns number of retweets and
# retweeted account
def retweets(c, conn):

    c.execute('SELECT tweet FROM tdump')
    all_tweets = c.fetchall()
    all_tweets = [tweet[0] for tweet in all_tweets]

    from_retweet = []  # '@twitter_user '
    retweeted_users = []  # ['@twitter_user', 304]
    retweets = 0
    seen_users = []

    # NLTK module
    tweet_token = TweetTokenizer()

    for tweet in all_tweets:

        # list of tokens (elements) defined
        # by TweetTokenizer
        broken_tweet = tweet_token.tokenize(tweet)

        if broken_tweet[0] == 'RT':

            retweets += 1
            # creating list of retweeted users
            from_retweet.append(broken_tweet[1])

    for rt in from_retweet:

        if rt not in seen_users:

            counted = from_retweet.count(rt)
            retweeted_users.append([rt, counted])
            seen_users.append(rt)

    finish(retweeted_users, 'retweeted_accounts')

    return retweets, retweeted_users


# fucntions above that count values' occurences
# have tables created in tweet_dumo_data.db
# results are saved there
def finish(results, name):

    conn_2 = sqlite3.connect('tweet_dump_data.db')
    c_2 = conn_2.cursor()

    c_2.execute('CREATE TABLE IF NOT EXISTS '
                    + name + ''' (value TEXT,
                      recurs TEXT)''')

    c_2.execute('SELECT value FROM ' + name)
    users = c_2.fetchall()
    users = [user[0] for user in users]

    for result in results:

        if result[0] not in users:

            c_2.execute('INSERT INTO ' + name + ' (value, recurs) VALUES (?, ?)', [result[0], result[1]])

        else:

            c_2.execute('UPDATE ' + name + ' SET recurs=? WHERE value=?',
                        [result[0], result[1]])

    conn_2.commit()


# counts times anything that isn't starting with
# 'RT @twitter_user'
# counted for every minute in 24h period
def tweet_times(c, conn):

    c.execute('SELECT tweet, tweet_date FROM tdump')
    all_tweets = c.fetchall()
    all_tweets = [tweet for tweet in all_tweets if tweet[0][:2] != 'RT']

    tweet_times = [tweet[1][-8:-3] for tweet in all_tweets]

    seen_times = []
    tweet_time_counts = []

    for tweet_time in tweet_times:

        if tweet_time not in seen_times:

            counted = tweet_times.count(tweet_time)
            tweet_time_counts.append([tweet_time, counted])
            seen_times.append(tweet_time)

    finish(tweet_time_counts, 'tweet_times')

    counted, counts = zip(*tweet_time_counts)
    list_of_datetimes = [dt.strptime(c, '%H:%M') for c in counted]
    dates = matplotlib.dates.date2num(list_of_datetimes)

    return dates, counts

# same as tweet_times funct above
# for retweets
# these functs used for rtvt graph 
def rt_times(c, conn):

    c.execute('SELECT tweet, tweet_date FROM tdump')
    all_tweets = c.fetchall()
    all_tweets = [tweet for tweet in all_tweets if tweet[0][:2] == 'RT']

    retweet_times = [retweet[1][-8:-3] for retweet in all_tweets]

    seen_times = []
    rt_time_counts = []

    for rt_time in retweet_times:

        if rt_time not in seen_times:

            counted = retweet_times.count(rt_time)
            rt_time_counts.append([rt_time, counted])
            seen_times.append(rt_time)

    finish(rt_time_counts, 'retweet_times')

    return rt_time_counts


if __name__ == '__main__':

    main()
