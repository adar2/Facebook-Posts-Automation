from selenium import webdriver
from time import sleep, time, asctime, localtime
from datetime import datetime, timedelta
from selenium.webdriver.common.keys import Keys


def wait(delay=2):
    sleep(delay)


def post_to_url(driver, message, url='https://facebook.com/'):
    # by default posts to news feed if not given url argument
    if url != 'https://facebook.com/':
        driver.get(url)
        wait()
    try:
        post_box = driver.find_element_by_xpath("//div[@role='textbox']")  # should work in business page
    except Exception as e:
        post_box = driver.find_element_by_xpath("//*[contains(@aria-label,'on your mind')]")  # should work in news feed
        print(e)
        pass
    post_box.send_keys(message)
    wait()
    post_btn = driver.find_element_by_xpath("//button[@data-testid='react-composer-post-button']")
    post_btn.click()
    print("Successfully posted to the wall.. with the content:" + message + '\n')


def post_media_to_url(driver, url='', path_to_media='', message=''):
    # by default posts to news feed if not given url argument
    if url != '':
        driver.get(url)
        wait()
    post_elem = driver.find_element_by_xpath("//div[contains(@aria-label,'a post') or contains(@aria-label,'on your mind')]")
    wait()
    post_elem.click()
    wait()
    if message != '':
        text_box = driver.find_element_by_xpath("//div[contains(@role,'box')]")
        text_box.send_keys(message)
    wait()
    if path_to_media != '':
        try:
            post_btn = driver.find_element_by_xpath(
                "//*[@data-testid='photo-video-button']")  # should work in business page
            post_btn.click()
            wait()
        except Exception as e:
            post_btn = driver.find_element_by_xpath("//input[@name='composer_photo[]']")  # should work in news feed
        else:
            post_btn = driver.find_element_by_xpath("//input[@name='composer_photo']")

        wait()
        post_btn.send_keys(path_to_media)
    if message != '' or path_to_media != '':
        post_btn = driver.find_element_by_xpath("//button[@data-testid='react-composer-post-button']")
        post_btn.click()  # click on share button to share media
        print(
            "Successfully posted to url:" + url + " with the media:" + path_to_media + "with the message:" + message + "\n")
    else:
        print("Nothing to post\n")


def post_to_groups(driver, groups, message='', path_to_media=''):
    if '.txt' not in groups:
        print("didnt get a txt file of groups")
        return
    with open(groups, 'r+') as data_file:
        data = data_file.readlines()
        data_file.close()
    for group in data:
        post_media_to_url(driver, path_to_media, group, message)


def group_post_responder(driver, url, query, reply_content, days_delta):
    driver.get(url)
    query_box = driver.find_element_by_xpath(
        "//input[@class='inputtext' and contains(@placeholder,'Search this group')]")
    query_box.send_keys(query)
    query_box.send_keys(Keys.ENTER)
    wait()
    scroll_to_end_of_page(driver)  # you may want to comment this line out in very big groups
    posts = driver.find_elements_by_xpath("//div[contains(@data-highlight-tokens,']')]")
    print(len(posts))
    print(datetime.today())
    for post in posts:
        time_stamp = post.find_element_by_xpath(".//span[@class='timestampContent']")
        time_stamp = str(time_stamp.get_attribute('innerHTML')).replace('at', '').replace(',', '')
        try:
            # timestamp contains year
            new_time_stamp = (time_stamp.split(' ')[0])[0:3] + ' ' + time_stamp.split(' ')[1] + ' ' + \
                             time_stamp.split(' ')[2] + \
                             ' ' + time_stamp.split(' ')[3] + ' ' + time_stamp.split(' ')[4] + time_stamp.split(' ')[5]
            date_of_timestamp = datetime.strptime(new_time_stamp, '%b %d %Y %I:%M%p')
        except Exception as e:
            # timestamp doesn't contain year
            new_time_stamp = (time_stamp.split(' ')[0])[0:3] + ' ' + time_stamp.split(' ')[1] + ' ' + \
                             str(datetime.today().year) + ' ' + time_stamp.split(' ')[2] + time_stamp.split(' ')[3] + \
                             time_stamp.split(' ')[4]
            date_of_timestamp = datetime.strptime(new_time_stamp, '%b %d %Y %I:%M%p')
        if (datetime.today() - timedelta(days=days_delta)) >= date_of_timestamp:
            post.click()
            wait()
            cmnt_btn = post.find_element_by_xpath("//a[@title='Leave a comment']")
            cmnt_btn.click()
            wait()
            cmnt_box = post.find_element_by_xpath("//div[@role='textbox']")
            cmnt_box.send_keys(reply_content)
            cmnt_box.send_keys(Keys.ENTER)
            cmnt_btn.send_keys(Keys.ESCAPE)
            wait()

        print(date_of_timestamp)


def scroll_to_end_of_page(driver):
    try:
        last_height = driver.execute_script("return document.body.scrollHeight")
        print("Started at:" + asctime(localtime(time())))
        while True:
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            wait(3)
            current_height = driver.execute_script("return document.body.scrollHeight")
            if current_height != last_height:
                last_height = current_height
            else:
                print("End of page")
                break
        print("Finish at:" + asctime(localtime(time())))
    except Exception as e:
        print(e)


def group_members_extractor(driver, url):
    driver.get(url + "members/")
    scroll_to_end_of_page(driver)
    data_file = open(url + '-members.txt', 'w+')
    members_list = driver.find_elements_by_xpath("//a[contains(@data-hovercard,'/ajax/hovercard/user.php') and "
                                                 "contains(@ajaxify,'/groups/member_bio/bio_dialog/')]")
    clean_list = set()
    for member in members_list:
        member_title = member.get_attribute('title')
        member_profile = member.get_attribute('href')
        if 'profile.php' not in member_profile:
            member_profile = (member.get_attribute('href').split('?')[0])
        else:
            member_profile = (member.get_attribute('href').split('&')[0])
        clean_list.add((member_title, member_profile))
    clean_list = sorted(clean_list)
    for item in clean_list:
        data_file.write(str(item) + "\n")
        print(item)
    print(len(clean_list))
    data_file.close()


def do_login(driver, usr, passwd):
    driver.get("https://facebook.com/login")
    wait()
    usr_box = driver.find_element_by_id('email')
    pass_box = driver.find_element_by_id('pass')
    usr_box.send_keys(usr)
    pass_box.send_keys(passwd)
    wait()
    submit_btn = driver.find_element_by_id('loginbutton')
    submit_btn.click()
    print("Successful Login\n")


def init_driver():
    _browser_profile = webdriver.FirefoxProfile()
    _browser_profile.set_preference("dom.webnotifications.enabled", False)
    driver = webdriver.Firefox(_browser_profile)
    return driver


def menu(driver):
    print("Please enter your facebook credentials:\n")
    username = input("Enter email or phone number:\n")
    password = input("Enter password:\n")
    do_login(driver, username, password)
    menu_dict = {'1': "Post Something.", '2': "Groups Scraper.", '3': "Reply to posts in groups",
                 '4': "Post to multiple pages", '5': "Exit"}
    while True:
        options = sorted(menu_dict.keys())
        for entry in options:
            print(entry, menu_dict[entry])
        selection = input("Please Select:\n")

        if selection == '1':
            print("Post something")
            url = input("Enter url you would like to post to (by default posts to news feed):\n")
            message = input("Enter the content of the post (optional you may leave it blank):\n")
            path_to_media = input("Enter full path to the desired photo/video:\n")
            post_media_to_url(driver, url, path_to_media, message)

        elif selection == '2':
            print("Group members extractor")
            url = input("Enter url you would like to post to:\n")
            while url == '' or 'facebook.com' not in url:
                print("Invalid value")
                url = input("Enter url you would like to post to:\n")
            group_members_extractor(driver, url)

        elif selection == '3':
            print("REPLY TO POSTS IN GROUPS BY QUERY")
            url = input("Enter url you would like to reply to his posts:\n")
            query = input("Enter query you want search for in url posts:\n")
            reply_content = input("Enter the reply you want to leave to posts containing your query:\n")
            days_delta = input("Enter time delta in days for posts that are relevant for reply:\n")
            group_post_responder(driver, url, query, reply_content, days_delta)

        elif selection == '4':
            print("Post to multiple pages")
            groups = input("Enter path to txt file containing your group list, one group per line:\n")
            message = input("Enter message you would like to leave in this pages:(optional)\n")
            path_to_media = input("Enter path to the media you would like to post in this pages:(optional)\n")
            post_to_groups(driver, groups, message, path_to_media)
        elif selection == '5':
            print("Exiting...")
            driver.close()
            break
        else:
            print("Unknown Option Selected!")


def main():
    try:
        driver = init_driver()
        menu(driver)

    except Exception as e:
        driver.close()
        print(e)
        print("Error exiting..")


main()
