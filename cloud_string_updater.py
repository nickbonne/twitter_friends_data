#!/home/nick/.virtualenvs/twitterbots/bin/python3.5

from all_friends import AllFriends


def main():

    Update.update()


class Update:

    def update():

        all_statuses = AllFriends.get_friend_statuses()[0]
        just_tweets = AllFriends.get_friends_tweets()
        just_retweets = AllFriends.get_friends_retweets()

        AllFriends.update_cloud_strings_only_tweets(just_tweets)
        AllFriends.update_cloud_string_mentions(all_statuses)
        AllFriends.update_cloud_string_retweeted_users(just_retweets)
        AllFriends.update_cloud_string_hashtags(just_tweets)


if __name__ == '__main__':

    main()
