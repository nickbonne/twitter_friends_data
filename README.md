<h1>Twitter Friend Data</h1>
<br>
<p>With the help of cron, friend_tweets.py is run every 30min looking for new friends and new timeline posts.
For new posts, the post time, screen name, and tweet contents are stored in database.</p>
<br>
<p><strong>[no long updating]</strong> friends_data.py contains all the functions for counting and graphing.
<br><br>
tweepy_status_object.txt is where the information about each tweet comes from.
<br><br>
Below is an example of what my idea is moving forward. One of these will be made for the friend's list as a whole and will include something covering hashtags. Not enough from individuals to make anything interesting in that area. 
<br><br>
A couple more additions to be made will include a look into screennames(length, use of numbers, case, underscore separations), account creation date, status counts, friends vs followers. More matplotlib to come there as well, yay!
<br><br>
The reason behind user_graphic.jpg existing in a tmp directory is to conserve storage space. The program lives on my laptop's 250GB solid state drive. The goal to switch the database to gather both friends and followers data and to allow them to tweet my account for a personal graphic. I also don't care enough to have directories for every friend or follower. 
</p>

<h3> twitter_user.py output example<h3>
<img src="https://github.com/nickbonne/twitter_friends_data/blob/master/f_data_output/tmp/user_graphic.jpg" width=400>
