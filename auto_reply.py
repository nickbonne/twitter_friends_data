#!/home/nick/.virtualenvs/twitterbots/bin/python3.5

import sqlite3

# Unlike other bot functions, this will only be called from the listener.
# if the auto posts generate enough reponses, might have to extend coverage


def main():

    pass


class AutoReply:

    # if a tweet has mentions @BonneNick
    # check if in_reply_to_status_id is in auto_log.db
    def check_4_id(api, reply_id, tweet_id, username):

        if reply_id in GetId.tweets():

            AutoReply.send_auto_reply(api, tweet_id, 0)

        elif reply_id in GetId.reply_1():

            AutoReply.send_auto_reply(api, tweet_id, 1, username)

        elif reply_id in GetId.reply_2():

            AutoReply.send_auto_reply(api, tweet_id, 2)

    # sends appropriate message back to user depending on which
    # level of status they replied to
    def send_auto_reply(api, tweet_id, level, *args):

        conn = sqlite3.connect('auto_log.db')
        c = conn.cursor()

        msg_0 = 'You have replied to a bot post. If that is your' +\
                ' question. Check the link in my profile description'

        msg_1 = '*beep bop boop* I am Bot.' +\
                ' Nice to meet you, @{}'.format(args) +\
                'I am limited in my responses, you must not ask a question.'

        msg_2 = "Hi again, I would love to converse with you" +\
                " but the guy in charge clearly isn't smart" +\
                " enough to give me the capability, Bot out. *mic drop*"

        if level == 0:

            tweet = api.update_status(status=msg_0,
                                      in_reply_to_status_id=tweet_id)

            c.execute('INSERT INTO autolog(tweet) VALUES(?)', [tweet.id])

        elif level == 1:

            tweet = api.update_status(status=msg_1,
                                      in_reply_to_status_id=tweet_id)
            c.execute('INSERT INTO autolog(reply_1) VALUES(?)', [tweet.id])

        elif level == 2:

            tweet = api.update_status(status=msg_2,
                                      in_reply_to_status_id=tweet_id)
            c.execute('INSERT INTO autolog(reply_2) VALUES(?)', [tweet.id])

        conn.commit()


class GetId:

    def tweets():

        conn = sqlite3.connect('auto_log.db')
        c = conn.cursor()

        c.execute('SELECT tweet FROM autolog')
        ids = [x[0] for x in c.fetchall()]

        return ids

    def reply_1():

        conn = sqlite3.connect('auto_log.db')
        c = conn.cursor()

        c.execute('SELECT reply_1 FROM autolog')
        ids = [x[0] for x in c.fetchall()]

        return ids

    def reply_2():

        conn = sqlite3.connect('auto_log.db')
        c = conn.cursor()

        c.execute('SELECT reply_2 FROM autolog')
        ids = [x[0] for x in c.fetchall()]

        return ids


if __name__ == '__main__':

    main()
