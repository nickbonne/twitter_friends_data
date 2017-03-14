#!/home/nick/.virtualenvs/twitternews/bin/python3.4

import re
import requests
import bs4 as bs


def main():

    pass


# scrapes for featured story from History Channel's
# 'this day in history' page
class History:

    def make_soup():

        url = 'http://www.history.com/this-day-in-history/'
        cookies = dict(cookie='value')
        headers = {'User-Agent':
                   'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) ' +
                   ' AppleWebKit/537.36 (KHTML, like Gecko) ' +
                   ' Chrome/35.0.1916.47 Safari/537.36'}

        response = requests.get(url, headers=headers, cookies=cookies)
        html = response.content
        soup = bs.BeautifulSoup(html, 'lxml')

        return soup, url

    def get_history():

        soup, url = History.make_soup()

        year = soup.body.find('strong', class_='year')

        sentence = soup.body.find('article', class_='article')
        sentence = re.sub(r'\([^)]*\)', '', sentence.text)
        sentence = re.split(r'(?<=[.:;!?])\s', sentence)[0].strip()
        sentence = sentence.split()
        new_sentence = ''

        for word in sentence:

            if word.strip('.,:;?!') == 'and':

                word = '&'

                new_sentence = new_sentence + ' ' + word

            elif word.strip('.,:;?!') == 'the':

                pass

            else:

                new_sentence = new_sentence + ' ' + word

        new_sentence = new_sentence.replace('  ', ' ')
        new_sentence = new_sentence.replace('On this day ', 'Today ')
        new_sentence = new_sentence.strip()

        status_length = 133 - len(year.text)

        message = '{}: {}'.format(year.text, new_sentence[:status_length])

        return message


if __name__ == '__main__':

    main()
