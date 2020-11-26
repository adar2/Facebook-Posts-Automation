# Facebook-Posts-Automation

Making publishing posts on Facebook easier and faster by using a bot posting to many pages very fast,
getting a list of group members out of Facebook group and even scheduling posts to different dates and
hours. The bot was built using pure python with selenium as the client, SQLite3 for database and PyQt5
for GUI.


![img](https://i.ibb.co/ysYqVdj/mainwindowfb.png)

# Dependencies
selenium~=3.141.0

pyqt5~=5.14.2

pysqlite3

keyring~=10.6.0

cryptography>=3.2

# Installation

`pip install selenium pyqt5 pysqlite3 cryptography keyring`

or

`pip install -r requirements.txt`

You also need to have mozilla geckodriver you can get it here ![geckodriver](https://github.com/mozilla/geckodriver).

If you wish to use some other browser binary supported by selenium (i.e. Chrome), you need to edit 'Bot.py'.

replace :

`self.driver = webdriver.Firefox(options=self.options)` 

with something like :

`self.driver = webdriver.Chrome(options=self.options)`

Make sure you have geckodriver binary (or any other browser) in project directory or you might want to specify the path in `Bot.py`.

E.g. `self.driver = webdriver.Firefox(executable_path="/data/Drivers/geckodriver",options=self.options)`

# Usage

When you've got all of it ready, you can start the gui by execute `python main.py` in command line.

You need first to create a user by clicking the add user button, a dialog window will open, enter username and password and click ok.

![img](https://i.ibb.co/bd1L6dD/adduser.png)


Once you've got your user created you can continue and add posts,targets and scheduled tasks all of those will be stored in the database for the user who created them and will remain there until you delete them.


__Login:__

Select the user from the existing users dropdown, and click the login button.
You can choose to run the browser driver headless or not by checking the `hide browser` checkbox.

__Post:__

First you need to create post by clicking the add post button, insert the post content and select the media file using the dialog browse button.
both field are optional but at least one of them must be non empty in order to create new post.

![img](https://i.ibb.co/zVk5n97/addpost.png)

Add target by clicking the add target button and entering facebook url you wish to post to.

![img](https://i.ibb.co/mFFSF8L/addtarget.png)

Now go ahead and select one post from the posts list, you can select one or more targets from the targets list by using `Ctrl` or `Shift` and click the post button.

__Scrape:__

Add a group target i.e `facebook.com/group/123456`, using the add target button.

Select the group target you've added and click the scrape button.

List with group users and their facebook profile link will show in the log text. 

__Tasks:__

Tasks are comprised of post, one or more targets,date and task name.

![img](https://i.ibb.co/xF715Zs/addtask.png)

Each task is associated with the user created that task, means that the task will execute as that user, you can schedule multiple tasks for multiple users at the same time.

The tasks executor runs on separate thread so you can select the tasks you want to schedule to run and continue to use the script.

You can run tasks by selecting one or more tasks from the tasks list and click the run task button. 

__Load File:__

You can load a json file containing your posts and targets.

the structure for the json file should be as follow:

`{"posts":[{"msg":"some_post","media":"path_to_meida"},...],
    "targets":[{"target":"facebook.com/some_page},.....]}`