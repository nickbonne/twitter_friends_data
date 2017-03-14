#!/home/nick/.virtualenvs/twitternews/bin/python3.4

import os
import random
import requests
import bs4 as bs
import urllib.request

# For tweeting a daily comic strip from any one of the
# comic strips listed in random_comic


def main():

    pass


class Comics:

    def random_comic():

        comics = ['garfield',
                  'calvinandhobbes',
                  'boondocks']

        return random.choice(comics)

    def make_soup(comic):

        url = 'http://www.gocomics.com/' + comic
        cookies = dict(cookie='value')
        headers = {'User-Agent':
                   'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) ' +
                   ' AppleWebKit/537.36 (KHTML, like Gecko) ' +
                   ' Chrome/35.0.1916.47 Safari/537.36'}

        response = requests.get(url, headers=headers, cookies=cookies)
        html = response.content
        soup = bs.BeautifulSoup(html, 'lxml')

        return soup, url

    def get_comic_source(comic):

        soup, url = Comics.make_soup(comic)

        c_strip = soup.body.find('picture',
                                 class_='img-fluid item-comic-image')

        return c_strip.img['src']

    def save_comic(comic_url):

        path = '/home/nick/.virtualenvs/twitternews/news_bot/imgs/'

        urllib.request.urlretrieve(comic_url,
                                   path + 'comic.gif')

        return path + 'comic.gif'

    def delete_comic():

        os.remove('/home/nick/.virtualenvs/twitternews/news_bot/imgs/comic.gif')


if __name__ == '__main__':

    main()
