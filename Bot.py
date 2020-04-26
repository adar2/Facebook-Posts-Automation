import os

from selenium import webdriver
from selenium.webdriver.firefox.options import Options


class Bot:
    def __init__(self, user, password):
        self.options = Options()
        #self.options.headless = True
        self.driver = webdriver.Firefox(options=self.options)
        self.current_dir = os.getcwd()
        self.logged_in = False
        self.doLogin(user, password)

    def __del__(self):
        if self.driver.service.process is not None:
            self.driver.quit()

    def doLogin(self, username, passwd):
        self.driver.get('http://mbasic.facebook.com')
        user_box = self.driver.find_element_by_xpath('//input[@name="email"]')
        user_box.send_keys(username)
        password_box = self.driver.find_element_by_xpath('//input[@name="pass"]')
        password_box.send_keys(passwd)
        login_btn = self.driver.find_element_by_xpath('//input[@name="login"]')
        login_btn.click()
        try:
            loginfailed = self.driver.find_element_by_xpath('//span[text()="The password you entered is incorrect. "]')
        except Exception:
            self.logged_in = True
            return 'Login Successful'
        else:
            return 'Failed to login'

    def postToUrl(self, message='', media_path='', url='http://mbasic.facebook.com'):
        if 'mbasic' not in url:
            newurl = 'http://mbasic.facebook.com/' + url.split('/', maxsplit=3)[3]
            url = newurl
        self.driver.get(url)
        if message != '':
            textbox = self.driver.find_element_by_xpath('//textarea[@name="xc_message"]')
            textbox.send_keys(message)

        if media_path != '':
            upload_photo = self.driver.find_element_by_xpath('//input[@name="view_photo"]')
            upload_photo.click()
            upload_photo = self.driver.find_element_by_xpath('//input[@name="file1"]')
            if self.current_dir not in media_path:
                media_path = self.current_dir + '/' + media_path
            upload_photo.send_keys(media_path)
            upload_photo = self.driver.find_element_by_xpath('//input[@name="add_photo_done"]')
            upload_photo.click()

        if media_path != '' or message != '':
            post_btn = self.driver.find_element_by_xpath('//input[@name="view_post"]')
            # post_btn.click()

    def groupScraper(self, url):
        if 'groups' not in url:
            return 'the url u have entered is not a group'

        if 'mbasic' not in url:
            newurl = 'http://mbasic.facebook.com/' + url.split('/', maxsplit=3)[3]
            url = newurl
        self.driver.get(url + '?')
        members_btn = self.driver.find_element_by_xpath('//a[text()="Members"]')
        members_btn.click()
        members_btn = self.driver.find_element_by_xpath('//a[contains(@href,"list_nonfriend_nonadmin")]')
        members_btn.click()
        data = ''
        while True:
            members = self.driver.find_elements_by_xpath('//a[@class="bo" or @class="bm"]')
            print(len(members))
            for member in members:
                data += member.text + ' ' + member.get_attribute('href') + '\n'
            try:
                see_more = self.driver.find_element_by_xpath('//span[text()="See More"]')
                see_more.click()
            except Exception:
                break
        return data

    def multiPost(self, urls_file):
        if '.txt' not in urls_file:
            return 'Please enter a text file with urls one per line'
        if self.current_dir not in urls_file:
            path = self.current_dir + '/' + urls_file
        else:
            path = urls_file
        with open(path) as f:
            lines = f.readlines()
        for line in lines:
            line.strip('\n')
            line = line.split(',')
            url = line[0]
            message = line[1]
            media = line[2]
            self.postToUrl(message, media, url)



