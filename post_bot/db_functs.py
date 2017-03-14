#!/home/nick/.virtualenvs/twitternews/bin/python3.4


import sqlite3


def main():

    pass


class DbFuncts:

    def connect():

        conn = sqlite3.connect('sent_links.db')
        c = conn.cursor()

        return c, conn

    def insert_(link):

        c, conn = DbFuncts.connect()
        c.execute('INSERT INTO links(url) VALUES(?)', [link])
        conn.commit()

    def links_sent():

        c = DbFuncts.connect()[0]
        c.execute('SELECT * FROM links')

        return [x[0] for x in c.fetchall()]

    def history_sent():

        c = DbFuncts.connect()[0]
        c.execute('SELECT * FROM history')

        return [x[0] for x in c.fetchall()]

    def insert_history(date):

        c, conn = DbFuncts.connect()
        c.execute('INSERT INTO history(date) VALUES(?)', [date])
        conn.commit()

    def comic_sent():

        c = DbFuncts.connect()[0]
        c.execute('SELECT * FROM comic')

        return [x[0] for x in c.fetchall()]

    def insert_comic(date):

        c, conn = DbFuncts.connect()
        c.execute('INSERT INTO comic(date) VALUES(?)', [date])
        conn.commit()


if __name__ == '__main__':

    main()
