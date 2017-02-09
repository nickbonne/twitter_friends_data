<h1>Twitter Friend Data</h1>
<br>
<p><strong>As of 09-02-2017 I am looking into what I have to do to thread this application. I want bot_commander.py to run the whole show, only using cron to automatically run the program on startup.</strong>

<p>With the help of cron, tweet_collect.py is run every 15min looking for new friends and new timeline posts.
For new posts, the post time, screen name, and tweet contents are stored in database.</p>
<br>
tweepy_status_object.txt is where the information about each tweet comes from.
<br><br>
Below are some examples of what a user may request. Some graphics aren't available for showing a user's individual data simply because there isn't enough yet.
<br><br>
More graphics may be added, more stat's may be tracked in the future but right now I'm focusing on deployment.
<br><br>
The reason behind grapics existing in a tmp directory is to conserve storage space. The program lives on my laptop's 250GB solid state drive. The goal to switch the database to gather both friends and followers data and to allow them to tweet my account for a personal graphic or one for the whole. I also don't care enough to have directories for every friend or follower. If the app is well recieved I will offload to Heroku or Digital Ocean and continue running it.
</p>

<h3> twitter_user.py output example<h3>
<img src="https://github.com/nickbonne/twitter_friends_data/blob/master/output/tmp/f_hash_cloud.png" width=400>
<img src="https://github.com/nickbonne/twitter_friends_data/blob/master/output/tmp/f_rtvt_aio.png" width=400>
<img src="https://github.com/nickbonne/twitter_friends_data/blob/master/output/tmp/f_source_pie.png" width=400>
