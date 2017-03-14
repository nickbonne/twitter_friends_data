#!/home/nick/.virtualenvs/twitternews/bin/python3.4

import json
import requests

from configparser import ConfigParser


def main():

    pass


class Shorten:

    def shorten(url):

        api_key = API.get_()

        post_url = 'https://www.googleapis.com/urlshortener/v1/url?key='
        post_url = post_url + api_key
        payload = {'longUrl': url}
        headers = {'content-type': 'application/json'}
        r = requests.post(post_url,
                          data=json.dumps(payload),
                          headers=headers)

        try:

            r = json.loads(r.text)['id']

        except:

            pass

        if r:

            return r


class API:

    def get_():

        parser = ConfigParser()
        parser.read('g_auth.ini')

        api_key = parser.get('Keys', 'api_key').strip("'")

        return api_key


if __name__ == '__main__':

    main()
