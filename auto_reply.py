#!/home/nick/.virtualenvs/twitterbots/bin/python3.5

import sqlite3

# Unlike other bot functions, this will only be called from the listener.
# if the auto posts generate enough reponses, might have to extend coverage


def main():

    pass


class AutoReply:

    # if a tweet has mentions @BonneNick
    # check if in_reply_to_status_id is in auto_log.db
    def check_4_id(api, reply_id, tweet_id):

        conn = sqlite3.connect('auto_log.db')
        c = conn.cursor()

        c.execute('SELECT * FROM autolog')
        auto_status_ids = [x[0] for x in c.fetchall()]

        if reply_id in auto_status_ids:

            AutoReply.send_auto_reply(api, c, conn, tweet_id)

    # check_4_id will call if conditions met
    # api arg comes from bot_commander.py as
    # does the id of the tweet responding to OP
    def send_auto_reply(api, c, conn, tweet_id):

        msg = 'You have responded to a bot on this account.' +\
              ' Follow the link in the profile description.' +\
              ' Replying to this is an infinite loop.'

        tweet = api.update_status(status=msg,
                                  in_reply_to_status_id=tweet_id)

        c.execute('INSERT INTO autolog VALUES(?)', [tweet.id])
        conn.commit()


if __name__ == '__main__':

    main()
