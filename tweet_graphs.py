#!/home/nick/.virtualenvs/twitterbots/bin/python3.5

import numpy as np
import matplotlib.dates
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

from os import path
from PIL import Image
from wordcloud import WordCloud
from datetime import datetime as dt
from wordcloud import ImageColorGenerator

'''

Graphs need to share a style
Need easy way to run without saving a file
command arg likely
Graphs that rely on tweets.Source must be changed to
phone_compare.Source


'''


def main():

    pass


class Graphs:

    # all tweets plotted as if they happened
    # in 24 hours. No distinction to retweets.
    def all_in_one(coordinates, home_class):

        dates, y_coord = zip(*coordinates)
        list_of_datetimes = [dt.strptime(x, '%H:%M') for x in dates]
        x_coord = matplotlib.dates.date2num(list_of_datetimes)

        fig = plt.figure()

        fig, ax1 = plt.subplots(figsize=(12, 9))
        fig.subplots_adjust(top=0.9,
                            bottom=0.17,
                            left=0.08,
                            right=0.97)

        ax1.set_title('All Tweets Over 24 Hours')
        ax1.set_xlabel('Time')
        ax1.set_ylabel('Tweets')
        ax1.set_ylim(0, max(y_coord) + 2)
        plt.style.use('bmh')
        plt.xticks(rotation=45)

        matplotlib.pyplot.plot_date(x_coord, y_coord)

        # plt.show()

        if str(home_class) == "<class 'all_friends.AllFriends'>":

            plt.savefig('/home/nick/.virtualenvs/twitterbots/bots/output/tmp/f_aio.png')

        if str(home_class) == "<class 'personal.User'>":

            plt.savefig('/home/nick/.virtualenvs/twitterbots/bots/output/tmp/aio.png')

    def total_tweets_per_day(coordinates, home_class):

        dates, y_coord = zip(*coordinates)
        list_of_datetimes = [dt.strptime(x, '%Y-%m-%d') for x in dates]
        x_coord = matplotlib.dates.date2num(list_of_datetimes)

        fig = plt.figure()

        fig, ax1 = plt.subplots(figsize=(12, 9))
        fig.subplots_adjust(top=0.9,
                            bottom=0.13,
                            left=0.09,
                            right=0.98)

        ax1.set_title('Total Tweets per Day')
        ax1.set_xlabel('Date')
        ax1.set_ylabel('Tweets')
        ax1.set_ylim(0, max(y_coord) + 2)
        plt.style.use('bmh')
        plt.xticks(rotation=45)
        matplotlib.pyplot.plot_date(x_coord, y_coord)
        plt.plot(x_coord, np.poly1d(np.polyfit(x_coord, y_coord, 1))(x_coord))

        # plt.show()
        if str(home_class) == "<class 'all_friends.AllFriends'>":

            plt.savefig('/home/nick/.virtualenvs/twitterbots/bots/output/tmp/f_per_day.png')

        if str(home_class) == "<class 'personal.User'>":

            plt.savefig('/home/nick/.virtualenvs/twitterbots/bots/output/tmp/per_day.png')

    def rtwt_vs_twt_24h(rtwt_coords, twt_coords, home_class):

        rtwt_dates, rtwt_y_coord = zip(*rtwt_coords)
        list_of_rt_dts = [dt.strptime(x, '%H:%M') for x in rtwt_dates]
        rtwt_x_coord = matplotlib.dates.date2num(list_of_rt_dts)

        twt_dates, twt_y_coord = zip(*twt_coords)
        list_of_t_dts = [dt.strptime(x, '%H:%M') for x in twt_dates]
        twt_x_coord = matplotlib.dates.date2num(list_of_t_dts)

        fig = plt.figure()

        fig, ax1 = plt.subplots(figsize=(12, 9))
        fig.subplots_adjust(top=0.9,
                            bottom=0.17,
                            left=0.08,
                            right=0.97)

        ax1.set_title('Tweets and Retweets Over 24 Hours')
        ax1.set_xlabel('Time')
        ax1.set_ylabel('Occurences per minute')
        plt.style.use('bmh')
        plt.xticks(rotation=45)
        matplotlib.pyplot.plot_date(rtwt_x_coord,
                                    rtwt_y_coord,
                                    color='gray')
        matplotlib.pyplot.plot_date(twt_x_coord,
                                    twt_y_coord,
                                    color='lightskyblue')

        tweet_patch = mpatches.Patch(color='lightskyblue',
                                     label='Tweets')
        retweet_patch = mpatches.Patch(color='gray',
                                       label='Retweets')
        plt.legend(handles=[tweet_patch, retweet_patch],
                   loc='upper right',
                   shadow='True')

        # plt.show()
        if str(home_class) == "<class 'all_friends.AllFriends'>":

            plt.savefig('/home/nick/.virtualenvs/twitterbots/bots/output/tmp/f_rtvt_aio.png')

        if str(home_class) == "<class 'personal.User'>":

            plt.savefig('/home/nick/.virtualenvs/twitterbots/bots/output/tmp/rtvt_aio.png')

    def hashtag_word_cloud(hashtags, home_class):

        text = ''

        if isinstance(hashtags, list):

            for hashtag in hashtags:

                hash_text = (hashtag[0] + ' ') * hashtag[1]
                text = text + hash_text.strip() + ' '

        else:

            text = hashtags

        d = path.dirname(__file__)

        media_path = '/home/nick/.virtualenvs/twitterbots/bots/img/'

        twitter_mask = np.array(Image.open(path.join(d, media_path + 'twitter_icon.png')))

        wc = WordCloud(background_color='black',
                       max_words=2000,
                       mask=twitter_mask,)

        wc.generate(text)
        image_colors = ImageColorGenerator(twitter_mask)

        fig, ax1 = plt.subplots(figsize=(12, 9))
        plt.imshow(wc.recolor(color_func=image_colors))
        plt.axis('off')

        if str(home_class) == "<class 'all_friends.AllFriends'>":

            plt.savefig('/home/nick/.virtualenvs/twitterbots/bots/output/tmp/f_hash_cloud.png')

        # if str(home_class) == "<class '__main__.User'>":

        #     plt.savefig('/home/nick/.virtualenvs/twitterbots/bots/output/tmp/hash_cloud.png')

    def mention_word_cloud(mentions, home_class):

        text = ''

        if isinstance(mentions, list):

            for mention in mentions:

                mention_text = (mention[0] + ' ') * mention[1]
                text = text + mention_text.strip() + ' '

        else:

            text = mentions

        d = path.dirname(__file__)

        media_path = '/home/nick/.virtualenvs/twitterbots/bots/img/'

        twitter_mask = np.array(Image.open(path.join(d, media_path + 'twitter_icon.png')))

        wc = WordCloud(background_color='black',
                       max_words=2000,
                       mask=twitter_mask,)

        wc.generate(text)
        image_colors = ImageColorGenerator(twitter_mask)

        fig, ax1 = plt.subplots(figsize=(12, 9))
        plt.imshow(wc.recolor(color_func=image_colors))
        plt.axis('off')

        if str(home_class) == "<class 'all_friends.AllFriends'>":

            plt.savefig('/home/nick/.virtualenvs/twitterbots/bots/output/tmp/f_mention_cloud.png')

        if str(home_class) == "<class 'personal.User'>":

            plt.savefig('/home/nick/.virtualenvs/twitterbots/bots/output/tmp/mention_cloud.png')

    def retweeted_word_cloud(retweeted, home_class):

        text = ''

        if isinstance(retweeted, list):

            for retweet in retweeted:

                rt_text = (retweet[0] + ' ') * retweet[1]
                text = text + rt_text.strip() + ' '

        else:

            text = retweeted

        d = path.dirname(__file__)

        media_path = '/home/nick/.virtualenvs/twitterbots/bots/img/'

        twitter_mask = np.array(Image.open(path.join(d, media_path + 'twitter_icon.png')))

        wc = WordCloud(background_color='black',
                       max_words=2000,
                       mask=twitter_mask,)

        wc.generate(text)
        image_colors = ImageColorGenerator(twitter_mask)

        fig, ax1 = plt.subplots(figsize=(12, 9))
        plt.imshow(wc.recolor(color_func=image_colors))
        plt.axis('off')

        if str(home_class) == "<class 'all_friends.AllFriends'>":

            plt.savefig('/home/nick/.virtualenvs/twitterbots/bots/output/tmp/f_retweeted_cloud.png')

        if str(home_class) == "<class 'personal.User'>":

            plt.savefig('/home/nick/.virtualenvs/twitterbots/bots/output/tmp/retweeted_cloud.png')

    def tweeted_word_cloud(words_string, home_class):

        d = path.dirname(__file__)

        media_path = '/home/nick/.virtualenvs/twitterbots/bots/img/'

        twitter_mask = np.array(Image.open(path.join(d, media_path + 'twitter_icon.png')))

        wc = WordCloud(background_color='black',
                       max_words=2000,
                       mask=twitter_mask,)

        wc.generate(words_string)
        image_colors = ImageColorGenerator(twitter_mask)

        fig, ax1 = plt.subplots(figsize=(12, 9))
        ax1.set_title('Favorite Words to Tweet',
                      fontsize=24).set_position([0.5, 1.05, ])
        plt.imshow(wc.recolor(color_func=image_colors))
        plt.axis('off')
        # plt.show()

        if str(home_class) == "<class 'all_friends.AllFriends'>":

            plt.savefig('/home/nick/.virtualenvs/twitterbots/bots/output/tmp/f_word_cloud.png')

        if str(home_class) == "<class 'personal.User'>":

            plt.savefig('/home/nick/.virtualenvs/twitterbots/bots/output/tmp/word_cloud.png')

    def tweet_source_pie(source_list, home_class):

        source_list.sort(key=lambda x: int(x[1]), reverse=True)

        sources, counts = zip(*source_list)

        x_coord = list(sources[:9])  # top 9
        y_coord = list(counts[:9])
        other_count = sum(counts[9:])

        if other_count > 0:

            x_coord.append('Others')  # the tenth
            y_coord.append(other_count)

        labels = np.char.array(x_coord)
        sizes = np.array(y_coord)

        fig, ax1 = plt.subplots(figsize=(12, 9))
        ax1.set_title('Top 10 Tweet Source Distrobution',
                      fontsize=24).set_position([0.5, 1.05, ])
        colors = ['#04182A', '#032333', '#032F3C',
                  '#033B45', '#02474E', '#025358',
                  '#025F61', '#026B6A', '#017773',
                  '#01837C', '#018F86', '#00BFAB',
                  '#01B45C', '#02A916', '#2C9F03']

        percent = 100. * sizes / sizes.sum()

        ax1.pie(sizes,
                shadow=True, startangle=90, labeldistance=1, pctdistance=1.2)
        patches, texts = plt.pie(sizes, colors=colors, startangle=90)
        labels = ['{0} - {1:1.2f} %'.format(i, j) for i, j in zip(labels,
                                                                  percent)]
        plt.legend(patches, labels, loc="best")
        ax1.axis('equal')  # Equal aspect ratio ensures pie is drawn as circle.

        # plt.show()
        if str(home_class) == "<class 'all_friends.AllFriends'>":

            plt.savefig('/home/nick/.virtualenvs/twitterbots/bots/output/tmp/f_source_pie.png')

        if str(home_class) == "<class 'personal.User'>":

            plt.savefig('/home/nick/.virtualenvs/twitterbots/bots/output/tmp/source_pie.png')

    def retweet_pie(tweets, retweets, home_class):

        labels = 'Tweets', 'Retweets'
        sizes = [tweets, retweets]
        colors = ['lightskyblue', 'lightgrey']
        explode = (0, 0.1)

        fig, ax1 = plt.subplots(figsize=(12, 9))
        ax1.set_title('Tweets vs Retweets',
                      fontsize=24).set_position([0.5, 1.05, ])
        ax1.pie(sizes, explode=explode, labels=labels, autopct='%1.1f%%',
                shadow=True, startangle=90, colors=colors)
        ax1.axis('equal')

        # plt.show()
        if str(home_class) == "<class '__main__.AllFriends'>":

            plt.savefig('/home/nick/.virtualenvs/twitterbots/bots/output/tmp/f_retweet_pie.png')

        if str(home_class) == "<class 'personal.User'>":

            plt.savefig('/home/nick/.virtualenvs/twitterbots/bots/output/tmp/retweet_pie.png')

    def geo_pie(on_count, off_count):

        labels = 'On', 'Off'
        sizes = [on_count, off_count]
        colors = ['lightskyblue', 'lightgrey']
        explode = (0, 0.1)

        fig, ax1 = plt.subplots(figsize=(12, 9))
        ax1.set_title('Geolocation Usage',
                      fontsize=24).set_position([0.5, 1.05, ])
        ax1.pie(sizes, explode=explode, labels=labels, autopct='%1.1f%%',
                shadow=True, startangle=90, colors=colors)
        ax1.axis('equal')
        # plt.show()
        plt.savefig('/home/nick/.virtualenvs/twitterbots/bots/output/tmp/gelocation.png')


if __name__ == '__main__':

    main()
