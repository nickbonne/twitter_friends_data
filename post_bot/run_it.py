#!/home/nick/.virtualenvs/twitternews/bin/python3.4

import time

from comic_scrape import Comics
from history_scrape import History
from datetime import datetime as dt
from db_functs import DbFuncts as df
from get_stories import NewsFind as nf
from send_stories import TwtFuncts as tf


print('''
------------------------------------
|            Twitter Bot           |
------------------------------------
     by: nbonne, tweepy, praw, python 3.4, Google API

    ''')

while True:

    # current time
    now = str(dt.today())[11:-7]

    already_sent = df.links_sent()
    # 'today in history'
    tih_sent = df.history_sent()
    # daily comic
    dc_sent = df.comic_sent()

    stories_to_tweet = []

    # if current hour is noon and current date not in
    # database, tweets daily history and daily comic
    if int(now[:2]) == 12:

        if str(dt.today())[:10] not in tih_sent:

            history = History.get_history()
            tf.send_tweet(history)
            df.insert_history(str(dt.today())[:10])
            time.sleep(30)

        if str(dt.today())[:10] not in dc_sent:

            comic = Comics.random_comic()
            src = Comics.get_comic_source(comic)
            file_ = Comics.save_comic(src)
            tf.send_comic_tweet(file_)
            df.insert_comic(str(dt.today())[:10])
            time.sleep(60)
            Comics.delete_comic()

    # if current time is between 7am and 10pm
    # last tweet should be no later than midnight
    if int(now[:2]) in range(7, 24) or\
       int(now[:2]) in range(0, 3):

        news = nf.top_stories()
        stories_to_tweet.extend(news)

        # add story to database if shortlink not already there
        # and trim list to match
        [df.insert_(x[1]) for x in stories_to_tweet
         if x[1] not in already_sent]

        [print(x[2]) for x in stories_to_tweet
         if x[1] not in already_sent]

        stories_to_tweet = [x[0] for x in stories_to_tweet
                            if x[1] not in already_sent]

        # tweets and waits 3 mins to tweet again
        for story in stories_to_tweet:

            tf.send_tweet(story)
            time.sleep(600)

        # Waits 2 hours between checking for tweets
        # time spent waiting between tweets is subtracted
        # by the wait time between sending stories just found
        if len(stories_to_tweet) > 1:

            less_sleep_time = len(stories_to_tweet) * 600

        else:

            less_sleep_time = 0

        wake_time = dt.fromtimestamp(time.time() + (7200 - less_sleep_time))

        print('Will check for new stories at {}'.format(str(wake_time)[11:-7]))
        print()

        time.sleep(7200 - less_sleep_time)

    else:

        time.sleep(300)
