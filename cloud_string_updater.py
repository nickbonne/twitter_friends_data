#!/home/nick/.virtualenvs/twitterbots/bin/python3.5

from mentions import Mentions
from hashtags import Hashtags
from retweets import Retweets
from all_friends import AllFriends
from datetime import datetime as dt
from nltk.tokenize import TweetTokenizer


def main():

    pass


class Update:

    def updater():

        everything, tweets, retweets = Update.get_statuses()

        Update.update_only_tweets(tweets)
        Update.update_only_rtwtd(retweets)
        Update.update_only_hashtags(tweets)
        Update.update_only_mentions(everything)

    def get_statuses():

        all_statuses = AllFriends.get_friend_statuses()
        just_tweets = AllFriends.get_friends_tweets()
        just_retweets = AllFriends.get_friends_retweets()

        return (all_statuses,
                just_tweets,
                just_retweets)

    def update_only_tweets(tweet_list):

        # Folder where text files containing
        # stopwords, holding places in databases, counts, etc
        filter_path = '/home/nick/.virtualenvs/twitterbots/bots/control_files/'

        # newest tweet_id
        new_placemarker = tweet_list[-1][3]

        with open((filter_path + 'place_holder.txt'), 'r') as f:

            placemarker = int(f.read().strip())

        with open((filter_path + 'place_holder.txt'), 'w') as f:

            f.write(new_placemarker)

        twt_token = TweetTokenizer()

        # Gets rid of '\n' and creates lists of filter items
        stopwords = [line.strip() for line in
                     open(filter_path + 'stopwords.txt')]

        tweet_list = [x[0] for x in tweet_list
                      if int(x[3]) > placemarker]

        tweet_list = ' '.join([x for x in tweet_list])

        tokenized_twt = twt_token.tokenize(tweet_list)

        words = ''

        for i in tokenized_twt:

            if i.lower() not in stopwords \
                and i[0] != '@' \
                    and i[0] != '#' \
                    and i[:4].lower() != 'http':

                words = (words + ' ') + i

        words = ' ' + words

        with open((filter_path + 'massive_tweet.txt'), 'a') as f:

            f.write(words.lower())

    def update_only_mentions(tweet_list):

        f_path = '/home/nick/.virtualenvs/twitterbots/bots/control_files/'

        tweet_list = sorted(tweet_list,
                            key=lambda x: dt.strptime(x[2],
                                                      '%Y-%m-%d %H:%M:%S'))

        new_placemarker = tweet_list[-1][2]

        with open((f_path + 'place_holder_mention.txt'), 'r') as f:

            placemarker = f.read()

        with open((f_path + 'place_holder_mention.txt'), 'w') as f:

            f.write(new_placemarker)

        placemarker = placemarker.strip()

        tweet_list = [x for x in tweet_list
                      if dt.strptime(x[2], '%Y-%m-%d %H:%M:%S') >
                      dt.strptime(placemarker, '%Y-%m-%d %H:%M:%S')]

        mention_stats = Mentions.users_mentioned(tweet_list)[1]

        mentioned_users = [x[0] for x in mention_stats]
        mention_nums = [x[1] for x in mention_stats]

        mention_counts = zip(mentioned_users, mention_nums)

        mention_string = ''

        for mention in mention_counts:

            baby_string = (mention[0] + ' ') * int(mention[1])
            baby_string = baby_string.strip()
            mention_string = (mention_string + ' ') + baby_string

        mention_string = ' ' + mention_string

        with open((f_path + 'massive_mention.txt'), 'a') as f:

            f.write(mention_string)

    def update_only_rtwtd(tweet_list):

        f_path = '/home/nick/.virtualenvs/twitterbots/bots/control_files/'

        tweet_list = sorted(tweet_list,
                            key=lambda x: dt.strptime(x[2],
                                                      '%Y-%m-%d %H:%M:%S'))

        new_placemarker = tweet_list[-1][2]

        with open((f_path + 'place_holder_retweet.txt'), 'r') as f:

            placemarker = f.read()

        with open((f_path + 'place_holder_retweet.txt'), 'w') as f:

            f.write(new_placemarker)

        placemarker = placemarker.strip()

        tweet_list = [x for x in tweet_list
                      if dt.strptime(x[2], '%Y-%m-%d %H:%M:%S') >
                      dt.strptime(placemarker, '%Y-%m-%d %H:%M:%S')]

        retweeted_stats = Retweets.get_retweeted_users(tweet_list)[1]

        retweeted_users = [x[0] for x in retweeted_stats]
        retweet_nums = [x[1] for x in retweeted_stats]

        retweet_counts = zip(retweeted_users, retweet_nums)

        retweet_string = ''

        for retweet in retweet_counts:

            baby_string = (retweet[0] + ' ') * int(retweet[1])
            baby_string = baby_string.strip()
            retweet_string = (retweet_string + ' ') + baby_string

        retweet_string = ' ' + retweet_string

        with open((f_path + 'massive_retweet.txt'), 'a') as f:

            f.write(retweet_string)

    def update_only_hashtags(tweet_list):

        f_path = '/home/nick/.virtualenvs/twitterbots/bots/control_files/'

        tweet_list = sorted(tweet_list,
                            key=lambda x: dt.strptime(x[2],
                                                      '%Y-%m-%d %H:%M:%S'))

        new_placemarker = tweet_list[-1][2]

        with open((f_path + 'place_holder_hashtag.txt'), 'r') as f:

            placemarker = f.read()

        with open((f_path + 'place_holder_hashtag.txt'), 'w') as f:

            f.write(new_placemarker)

        placemarker = placemarker.strip()

        tweet_list = [x for x in tweet_list
                      if dt.strptime(x[2], '%Y-%m-%d %H:%M:%S') >
                      dt.strptime(placemarker, '%Y-%m-%d %H:%M:%S')]

        hashtag_list = Hashtags.get_all_hashtags(tweet_list)

        hashtag_stats = Hashtags.count_hashtags(hashtag_list)

        hashtags = [x[0] for x in hashtag_stats]
        hash_nums = [x[1] for x in hashtag_stats]

        hashtag_counts = zip(hashtags, hash_nums)

        hashtag_string = ''

        for hash_data in hashtag_counts:

            baby_string = (hash_data[0] + ' ') * int(hash_data[1])
            baby_string = baby_string.strip()
            hashtag_string = (hashtag_string + ' ') + baby_string

        hashtag_string = ' ' + hashtag_string

        with open((f_path + 'massive_hashtag.txt'), 'a') as f:

            f.write(hashtag_string)


if __name__ == '__main__':

    main()
