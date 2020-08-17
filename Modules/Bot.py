import logging
from difflib import SequenceMatcher
import platform
from selenium import webdriver
from selenium.common.exceptions import InvalidSessionIdException, WebDriverException, NoSuchElementException
from selenium.webdriver.firefox.options import Options

logging.basicConfig(format='%(asctime)s - %(message)s', level=logging.WARNING)


def url_parse(url):
    if url is None or url == '' or url.count('.') == 0 or 'facebook.com' not in url:
        return None
    if url.count('/') == 0:
        return 'http://mbasic.facebook.com/'
    return 'http://mbasic.facebook.com/' + url[url.find('.com/') + len('.com/')::]


def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()


class Bot:
    def __init__(self, headless=False):
        self.options = Options()
        self.options.headless = headless
        self.driver = webdriver.Firefox(options=self.options)
        self.driver.implicitly_wait('5')
        self.logged_in = False

    def __del__(self):
        if self.driver.service.process is not None:
            self.driver.quit()

    def check_browser_state(self):
        try:
            x = self.driver.current_url
        except InvalidSessionIdException and WebDriverException:
            self.driver.quit()
            self.__init__(self.options.headless)
            print('Restarting browser..')

    def doLogin(self, username, password):
        if not self.logged_in:
            try:
                self.driver.get('http://mbasic.facebook.com')
                user_box = self.driver.find_element_by_xpath('//input[@name="email"]')
                user_box.send_keys(username)
                password_box = self.driver.find_element_by_xpath('//input[@name="pass"]')
                password_box.send_keys(password)
                login_btn = self.driver.find_element_by_xpath('//input[@name="login"]')
                login_btn.click()
                if self.driver.title == 'Facebook':
                    self.logged_in = True
                    return 'Login Successful'
                else:
                    return 'Failed to login'
            except NoSuchElementException and WebDriverException as e:
                logging.error(e)
        return 'Already logged in'

    def postToUrl(self, message='', media_path='', url='http://mbasic.facebook.com'):
        url = url_parse(url)
        if url is None:
            return 'Bad url'
        try:
            self.driver.get(url)

            if message != '':
                textbox = self.driver.find_element_by_xpath('//textarea[@name="xc_message"]')
                textbox.send_keys(message)

            if media_path is not None and media_path != '' and media_path != 'None':
                current_os = platform.system()
                if current_os == 'Windows':
                    media_path = media_path.replace('/', '\\')
                upload_photo = self.driver.find_element_by_xpath('//input[@name="view_photo"]')
                upload_photo.click()
                upload_photo = self.driver.find_element_by_xpath('//input[@name="file1"]')
                upload_photo.send_keys(media_path)
                upload_photo = self.driver.find_element_by_xpath('//input[@name="add_photo_done"]')
                upload_photo.click()

            if media_path != '' or message != '':
                post_btn = self.driver.find_element_by_xpath('//input[@name="view_post"]')
                post_btn.click()
                return 'Posted to :' + url
        except NoSuchElementException and WebDriverException as e:
            logging.error(e)
            return 'Failed to post to :' + url

    def groupScraper(self, url):
        if 'groups' not in url:
            return 'Not a group url'

        url = url_parse(url)
        if url is None:
            return 'Bad url'
        try:
            self.driver.get(url + '?')
            members_btn = self.driver.find_element_by_xpath('//a[text()="Members"]')
            members_btn.click()
            members_btn = self.driver.find_element_by_xpath('//a[contains(@href,"list_nonfriend_nonadmin")]')
            members_btn.click()
            data = ''
            while True:
                members = self.driver.find_elements_by_tag_name('a')
                members.remove(self.driver.find_element_by_xpath('//a[text()="Go to Home"]'))
                for member in members:
                    if similar(member.get_attribute('href'), member.text) > 0.1 and member.text != 'See More':
                        data += member.text + ' ' + member.get_attribute('href') + '\n'
                try:
                    see_more = self.driver.find_element_by_xpath('//span[text()="See More"]')
                    see_more.click()
                except Exception:
                    break
            return data
        except NoSuchElementException and WebDriverException as e:
            logging.warning(e)
            return ''

    def logout(self):
        try:
            self.logged_in = False
            self.driver.delete_all_cookies()
            self.driver.get('https://mobile.facebook.com/')
            return 'Logged out successfully'
        except WebDriverException as e:
            logging.error(e)
            return 'Failed to logout'
