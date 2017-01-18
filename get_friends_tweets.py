#!/home/nick/.virtualenvs/twitterbots/bin/python3.5

import tweepy
import sqlite3
from configparser import ConfigParser


def main(api):

    # Checks for new friends, passes findings on to
    # download Twitter's limit of user's tweets
    # before downloading any new tweets on authenticated
    # user's timeline which is done if no new frends are
    # found.

    new_friends = check_friends(api)

    if len(new_friends) != 0:

        download_all(api, new_friends)
        timeline_download(api)

    else:

        timeline_download(api)


def download_all(api, new_friends):

    # List of tweet ids already in db
    c.execute('SELECT tweet_id FROM tdump')
    tweet_ids = c.fetchall()
    tweet_ids = [e[0] for e in tweet_ids]

    all_friends_tweets = []

    for friend_id in new_friends:

        try:
            # try to get most recent 200 tweets from friend
            get_friend_tweets = api.user_timeline(id=friend_id, count=200)

        except Exception as e:

            print('''
                Error with {}.
                {}
                  '''.format(friend_id, e))

        # add to list of all of this friend's tweets
        all_friends_tweets.extend(get_friend_tweets)

        # find oldest retrieved tweet's id number less 1
        oldest = all_friends_tweets[-1].id - 1

        # get tweets until 3200 limit hit
        while len(get_friend_tweets) > 0:

            try:
                # max_id arg looks for id's less than arg's value
                get_friend_tweets = api.user_timeline(id=friend_id,
                                                      count=200,
                                                      max_id=oldest)

            except Exception as e:

                print('''
                Error with {}.
                {}
                  '''.format(friend_id, e))

            all_friends_tweets.extend(get_friend_tweets)

            oldest = all_friends_tweets[-1].id - 1

    for tweet in all_friends_tweets:

        # for each of friend's tweets, add attributes
        # to db if id not already in db

        if tweet.id_str not in tweet_ids:

            c.execute('''INSERT INTO tdump
                     (tweet,
                      username,
                      tweet_date,
                      tweet_id,
                      tweet_source)
                            VALUES(?,?,?,?,?)''',
                             [tweet.text,
                              tweet.user.screen_name,
                              tweet.created_at,
                              tweet.id_strd,
                              tweet.source])

    conn.commit()


def timeline_download(api):

    c.execute('SELECT max(tweet_id) FROM tdump')
    last_tweet = c.fetchone()[0]

    c.execute('SELECT tweet_id FROM tdump')
    tweet_ids = c.fetchall()
    tweet_ids = [e[0] for e in tweet_ids]

    # gets most recent posts to authenticated timeline
    get_timeline_tweets = api.home_timeline(since_id=last_tweet, count=500)

    for tweet in get_timeline_tweets:

        if tweet.id_str not in tweet_ids:

            c.execute('''INSERT INTO tdump
                     (tweet,
                      username,
                      tweet_date,
                      tweet_id,
                      tweet_source)
                            VALUES(?,?,?,?,?)''',
                             [tweet.text,
                              tweet.user.screen_name,
                              tweet.created_at,
                              tweet.id_strd,
                              tweet.source])

    conn.commit()


def check_friends(api):

    # get list of user's screen names
    c.execute('SELECT username FROM tdump')
    users = c.fetchall()
    users = list(set([user[0] for user in users]))

    # get list of friends_id from twitter
    get_friends = api.friends_ids()

    # covert list of ids to screen names
    gf_names = [api.get_user(f_id).screen_name for f_id in get_friends]

    difference = []

    # find differences in friends lists
    # return list of ids for use in
    # download function
    for gf_name in gf_names:

        if gf_name not in users:

            new_friend = gf_names.index(gf_name)
            difference.append(get_friends[new_friend])

    return difference


if __name__ == '__main__':

    parser = ConfigParser()
    parser.read('twitter_auth.ini')

    conn = sqlite3.connect('tweet_dump.db')
    c = conn.cursor()

    c.execute('''CREATE TABLE IF NOT EXISTS tdump
                 (tweet TEXT,
                  username TEXT,
                  tweet_date TEXT,
                  tweet_id TEXT,
                  tweet_source TEXT)''')

    consumer_key = parser.get('Keys', 'consumer_key')
    consumer_secret = parser.get('Secrets', 'consumer_secret')
    access_token = parser.get('Tokens', 'access_token')
    access_token_secret = parser.get('Secrets', 'access_token_secret')

    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth, wait_on_rate_limit=True)

    main(api)
