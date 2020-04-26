# Facebook-Bot
created by: adar2 
if you are planning on using this code or modify it, please add me as a contributor.

Facebook-bot:

![image](https://i.ibb.co/C2mmC65/Screenshot-at-2020-04-26-18-14-13.png)

This script was made with python selenium and pyqt5 for making the task of posting to FB easier.

in order to use this script you need to have selenium and pyqt5,you can do so by using pip.

`pip install selenium pyqt5`
or
`pip install -r requirements`

you also need to have mozilla geckodriver you can get it here ![geckodriver](https://github.com/mozilla/geckodriver).

make sure you have gecko binary in path or you might want to specify the path in Bot.py.

if you wish to use other browser then firefox , i.e Chrome make sure to do the right adjustments
in the driver configuration in Bot.py file.

after you've got all of it ready, you can use the gui by running `python FB-GUI.py` or you can use directy the bot if you'd like.

you should first enter username and password and click the login button.
you only need to log in once.

once you logged in you can use the text fileds in the gui for posting some message and/or image to some url.
user wall is deafault in case no url were given.
you can choose an image to attach to your post by clicking the image file button.
when you're ready to post simply click the post button and let the bot do its job.

you can also scrape group members from facebook groups by entering the group url and hitting the scrape url button.
the output data contains names and profiles links.

if you wish to post to mulitple pages/groups you can specify a text files containg the information in the following order:

fb-url/group1,message1,image_path1

fb-url/group2,message2,image_path2

fb-url/group3,message3,image_path3

and click on the multi post button.


