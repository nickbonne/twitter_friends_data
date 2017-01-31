#!/home/nick/.virtualenvs/twitterbots/bin/python3.5

# from scoring import ScoreCard
from hashtags import Hashtags
from retweets import Retweets
from tweets import AllTweets
from tweets import Tweets
import numpy as np
from os import path
from PIL import Image
import matplotlib.dates
from wordcloud import WordCloud
from wordcloud import ImageColorGenerator
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from datetime import datetime as dt

'''

Graphs need to share a style
Need easy way to run without saving a file
command arg likely
Graphs that rely on tweets.Source must be changed to
phone_compare.Source


'''


def main():

    # all_tweets = AllTweets.all_tweets_per_date(AllTweets.get_all_tweets())
    # Graphs.all_in_one(all_tweets)
    # Graphs.total_tweets_per_day(all_tweets)

    # hashtag_list = Hashtags.count_hashtags(Hashtags.get_all_hashtags(Hashtags.get_all_tweets()))
    # Graphs.hashtag_word_cloud(hashtag_list)

    # source_list = Sources.counted_sources(Sources.get_all_sources())

    tweets = len(Tweets.get_all_tweets())
    retweets = len(Retweets.get_all_retweets())
    Graphs.retweet_pie(tweets, retweets)

    # rtwt_coords = Retweets.retweets_per_minute(Retweets.get_all_retweets())
    # twt_coords = Tweets.tweets_per_minute(Tweets.get_all_tweets())
    # Graphs.rtwt_vs_twt_24h(rtwt_coords, twt_coords)


class Graphs:

    # all tweets plotted as if they happened
    # in 24 hours. No distinction to retweets.
    def all_in_one(coordinates):

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
        plt.savefig('/home/nick/.virtualenvs/twitterbots/bots/f_data_output/tmp/aio.png')

    def total_tweets_per_day(coordinates):

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
        plt.savefig('/home/nick/.virtualenvs/twitterbots/bots/f_data_output/tmp/per_day.png')

    def rtwt_vs_twt_24h(rtwt_coords, twt_coords):

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
        plt.show()

    def hashtag_word_cloud(hashtag_list):

        text = ''

        for hashtag in hashtag_list:

            hash_text = (hashtag[0] + ' ') * hashtag[1]
            text = text + hash_text.strip() + ' '

        d = path.dirname(__file__)

        twitter_mask = np.array(Image.open(path.join(d, 'twitter_icon.png')))

        wc = WordCloud(background_color='black',
                       max_words=2000,
                       mask=twitter_mask,)

        wc.generate(text)
        image_colors = ImageColorGenerator(twitter_mask)

        fig, ax1 = plt.subplots(figsize=(12, 9))
        plt.imshow(wc.recolor(color_func=image_colors))
        plt.axis('off'  )
        plt.show()

        #won't work here for example
        # wc.recolor(color_func=image_colors).to_file(path.join(d,
        #              save_dir + 'tweet_cloud_{}f.png'.format(users)))

    def tweeted_word_cloud(words_string):

        d = path.dirname(__file__)

        twitter_mask = np.array(Image.open(path.join(d, 'twitter_icon.png')))

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
        plt.savefig('/home/nick/.virtualenvs/twitterbots/bots/f_data_output/tmp/word_cloud.png')

    def tweet_source_pie(source_list):

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
        plt.savefig('/home/nick/.virtualenvs/twitterbots/bots/f_data_output/tmp/source_pie.png')

    def retweet_pie(tweets, retweets):

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
        plt.savefig('/home/nick/.virtualenvs/twitterbots/bots/f_data_output/tmp/originality.png')


if __name__ == '__main__':

    main()
