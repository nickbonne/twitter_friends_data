#!/home/nick/.virtualenvs/twitternews/bin/python3.4

import re
import praw
import datetime

from shorten_link import Shorten
from datetime import datetime as dt
from configparser import ConfigParser

# FluffFind not working with 'i.redd.it' shortlink


def main():

    pass


# steals top post from subreddit
class FluffFind:

    def check_sub(sub_reddit):

        r = NewsFind.praw_conn()
        subreddit = r.subreddit(sub_reddit)

        for submission in subreddit.hot():

            if str(submission.url)[7:-16] != 'i.redd.it':

                print(str(submission.url[8:-17]))

                if not submission.stickied and\
                   '[oc]' in submission.title.lower():

                    print(submission.url)

                    url_ = Shorten.shorten(submission.url)
                    title = submission.title
                    title = re.sub(r'\[[^)]*\]', '', title)
                    author = '/u/' + str(submission.author)

                    title_length = 110 - len(author)

                    if len(title) + 3 > title_length:

                        title = title[:-3]
                        title = title.strip() + '... '

                    else:

                        title = title.strip() + ' ' + author

                    story = [submission.score,
                             title,
                             url_,
                             url_]

                    return story


class NewsFind:

    def praw_conn():

        parser = ConfigParser()
        parser.read('reddit_auth.ini')

        client_id = parser.get('Keys', 'client_id').strip("'")
        client_secret = parser.get('Keys', 'client_secret').strip("'")
        user_agent = parser.get('User', 'user_agent').strip("'")

        r = praw.Reddit(client_id=client_id,
                        client_secret=client_secret,
                        user_agent=user_agent)

        return r

    # gets high scoring stories from chosen subreddits
    # sorts by karma score. Returns top three.
    def top_stories():

        stories = NewsFind.check_news_sub('news') +\
            NewsFind.check_news_sub('worldnews') +\
            NewsFind.check_news_sub('technology')

        stories = sorted(stories, key=lambda x: int(x[0]), reverse=True)[:3]

        stories = [(x[1] + ' ' + x[2],
                   x[3],
                   '[{}] {}'.format(x[0], x[1]) + '\n')
                   for x in stories]

        return stories

    # checks desired subreddit for posts less than two
    # hours old with more than 900 upvotes, returns list
    def check_news_sub(sub_reddit):

        r = NewsFind.praw_conn()
        subreddit = r.subreddit(sub_reddit)
        two_hrs_ago = dt.today() + datetime.timedelta(hours=3)  # UTC

        holding = []

        for submission in subreddit.new(limit=75):

            if submission.score >= 2000 \
                    and dt.fromtimestamp(submission.created_utc) <= two_hrs_ago:

                url_ = Shorten.shorten(submission.url)
                title = submission.title

                if len(title) > 100:

                    title = submission.title[:97] + '...'

                story = [submission.score,
                         title,
                         url_,
                         url_]

                holding.append(story)

        return holding


if __name__ == '__main__':

    main()
