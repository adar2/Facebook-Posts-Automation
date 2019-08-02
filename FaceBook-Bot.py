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
    print("Successfully posted to the wall.. with the content:" + message)


def post_media_to_url(driver, path_to_media, url='https://facebook.com/', message=''):
    # by default posts to news feed if not given url argument
    if url != 'https://facebook.com/':
        driver.get(url)
        wait()
    photo_btn = driver.find_element_by_xpath("//div[@aria-label='Create a post']")
    wait()
    photo_btn.click()
    if message != '':
        text_box = driver.find_element_by_xpath("//div[contains(@aria-label,'on your mind')]")
        text_box.send_keys(message)
    wait()
    try:
        post = driver.find_element_by_xpath("//*[@data-testid='photo-video-button']")  # should work in business page
        post.click()
        wait()
    except Exception as e:
        post = driver.find_element_by_xpath("//input[@name='composer_photo[]']")  # should work in news feed
        # print(e)
        pass
    else:
        post = driver.find_element_by_xpath("//input[@name='composer_photo']")

    wait()
    post.send_keys(path_to_media)
    post_btn = driver.find_element_by_xpath("//button[@data-testid='react-composer-post-button']")
    post_btn.click()  # click on share button to share media
    print("Successfully posted to url:" + url + " with the media:" + path_to_media)


def post_to_groups(driver, data, groups):
    for group in groups:
        post_to_url(driver, data, group)
        print("Successful posting to:" + group + " with the content:" + data)
        wait()


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
    print("Successful Login")


def init_driver():
    _browser_profile = webdriver.FirefoxProfile()
    _browser_profile.set_preference("dom.webnotifications.enabled", False)
    driver = webdriver.Firefox(_browser_profile)
    return driver


def menu(driver):
    print("Please enter your facebook credentials:")
    username = input("Enter email or phone number:")
    password = input("Enter password:")
    do_login(driver, username, password)
    menu = {'1': "Post Something.", '2': "Groups Scraper.", '3': "Reply to posts in groups", '4': "Exit"}
    while True:
        options = sorted(menu.keys())
        for entry in options:
            print(entry, menu[entry])
        selection = input("Please Select:")

        if selection == '1':
            while True:
                sub_menu = {'1': "Post Text", '2': "Post media + text(optional)", '3': "Back"}
                sub_options = sorted(sub_menu.keys())
                for entry in sub_options:
                    print(entry, sub_menu[entry])
                selection = input("Please Select:")
                if selection == '1':
                    url = input("Enter url you would like to post to (by default posts to news feed):")
                    message = input("Enter the content of the post")
                    post_to_url(driver, message, url)
                if selection == '2':
                    url = input("Enter url you would like to post to (by default posts to news feed):")
                    message = input("Enter the content of the post (optional you may leave it blank)")
                    path_to_media = input("Enter full path to the desired photo/video")
                    post_media_to_url(driver, url, path_to_media, message)
                elif selection == '3':
                    break
        elif selection == '2':
            print("GROUPS SCRAPER")

        elif selection == '3':
            print("REPLY TO POSTS IN GROUPS BY QUERY")

        elif selection == '4':
            print("EXITING...")
            driver.close()
            break
        else:
            print("Unknown Option Selected!")


def main():
    try:
        driver = init_driver()
        # usr = 'warmundadar@gmail.com'
        # passwd = 'Strong$h!t30'
        # do_login(driver, usr, passwd)
        # post_media_to_url(driver, '/home/r00t/PycharmProjects/untitled/test.jpg')
        # post_to_url(driver, 'True Colors Animation Simply The Best')
        # post_to_groups(driver, data, groups, delay)
        # group_members_extractor(driver, 'https://www.facebook.com/groups/377363775634155/')
        # group_post_responder(driver, 'https://www.facebook.com/groups/810769362294321/', 'אפשר')
        # driver.close()
        menu(driver)
    except Exception as e:
        driver.close()
        print(e)
        print("Error exiting..")


main()
