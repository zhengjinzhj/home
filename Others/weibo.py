# -*- coding:utf-8 -*-

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from Others.tools import *
from bs4 import BeautifulSoup
import re


class WeiBo(object):

    def __init__(self):
        self.chrome_options = webdriver.ChromeOptions()
        self.chrome_options.add_argument('user-data-dir=C:\\Users\\Administrator\\AppData\\Local\\Google\\Chrome\\User Data')
        self.browser = webdriver.Chrome(chrome_options=self.chrome_options)
        self.login_url = 'http://weibo.com/login.php'
        self.username = '15828643152'
        self.password = 'weibocnm123'
        self.my_id = '2630521620'
        self.photo_url_base = 'http://weibo.com/p/100505'  # 'model_id'/photos
        self.group_id = '3719539584307337'

    def login(self):
        # Do not need to login when using user data.
        # self.browser.set_window_position(300, 0)
        self.browser.set_page_load_timeout(6)
        try:
            self.browser.get(self.login_url)
            username = self.browser.find_element_by_id('loginname')
            password = self.browser.find_element_by_name('password')
            username.send_keys(self.username)
            password.send_keys(self.password)
            # time.sleep(10)  # Enter the verification code in this sleep time.
            self.browser.find_element_by_css_selector("*[class^='W_btn_a btn_32px']").click()
        except TimeoutException:
            self.browser.execute_script('window.stop()')  # Page loads a long time after logging in successfully.
        if self.my_id in self.browser.current_url:
            print('Log in successfully.')
        else:
            print('Cannot log in, please check your username and password.')
            self.browser.quit()

    def scroll_down(self, count):
        # scroll down the page, return false if there are still contents wrapped

        print('Scrolling down: %d...' % count)
        js = 'window.scrollTo(0, document.body.scrollHeight)'
        self.browser.execute_script(js)
        time.sleep(3)
        try:
            self.browser.find_element_by_class_name('WB_innerwrap')
        except NoSuchElementException:
            return True  # It means the page is fully loaded if 'WB_innerwrap' cannot be found.
        return False  # Otherwise, just keep scrolling down.

    def get_models_info(self):
        # get models info(model name and id) from given group in 'My Following' page

        group_page = self.photo_url_base + self.my_id + '/myfollow?gid=' + self.group_id
        print("Gathering models' info from the given page......")
        self.browser.set_page_load_timeout(6)
        try:
            self.browser.get(group_page)
        except TimeoutException:
            self.browser.execute_script('window.stop()')
        soup = BeautifulSoup(self.browser.page_source, 'html.parser')
        models = soup.select('div[class="title W_fb W_autocut "]')
        models_info = []
        for model in models:
            model_info = []
            info = model.find('a', 'S_txt1')
            model_info.append(info.string)
            model_info.append(info['usercard'][3:])
            models_info.append(model_info)
        return models_info

    def get_page_content(self, model_id):
        # get model's photo page after the page is fully loaded, and return the content

        page_url = self.photo_url_base + model_id + '/photos'
        self.browser.set_page_load_timeout(10)
        try:
            self.browser.get(page_url)
        except TimeoutException:
            self.browser.execute_script('window.stop()')
        count = 1
        # result = self.scroll_down(count)
        while not self.scroll_down(count):
            count += 1
            # result = self.scroll_down(count)
        print('Finally, the page is fully loaded. :-D')
        content = self.browser.page_source
        # soup = BeautifulSoup(content, 'html.parser')
        # html = open('photo.html', 'w')
        # print(>>html, soup.prettify().encode('utf-8')  # print(to file!!!
        return content

    def get_link_sets(self, model_id):
        # get links in every album of the model

        content = self.get_page_content(model_id)
        soup = BeautifulSoup(content, 'html.parser')
        model_name = soup.find('title').string
        model_name = model_name[:-6]  # like 梁不凉baby的微博_微博
        # print('The model\'s name is "%s"' % model_name
        # model_folder = 'Weibo/' + model_name
        make_folder(os.getcwd(), model_name)  # model name folder
        albums = soup.select('ul[class="photo_album_list clearfix"]')
        print('This user has %d albums.' % len(albums))
        total_photo_download = 0
        for album in albums:
            album_name = album['group_id']  # Album name
            make_folder(os.getcwd(), album_name)  # album name folder under model name folder
            # print(album.prettify()
            photo_links = album.find_all(src=re.compile('thumb300'))
            print('There are %d photos in album "%s".' % (len(photo_links), album_name))
            for link in photo_links:
                photo_link = str(link['src'])
                photo_link = photo_link.replace('thumb300', 'large')
                if '?tags' in photo_link:
                    photo_link = re.sub('\?tags.*', '', photo_link)
                st_downloader(photo_link)
                total_photo_download += 1
            os.chdir(os.path.pardir)  # Switch to parent folder after downloading all photos in current album
        print('Finally, ALL photos of this model are downloaded.'
              'There are %d photos in total.' % total_photo_download)
        os.chdir(os.path.pardir)  # Switch to parent folder after downloading all this model's photos

    @staticmethod
    def make_folder(folder_name):
        if not os.path.exists(folder_name):
            print('Creating folder: "%s"' % folder_name)
            os.mkdir(folder_name)
        else:
            print('Folder "%s" already exists, skip...' % folder_name)

    @staticmethod
    def save_photo(folder_name, photo_link):
        photo_name = photo_link.split('/').pop()
        full_address = folder_name + '/' + photo_name
        if not os.path.isfile(full_address):
            print('Downloading photo %s' % photo_name)
            data = requests.get(photo_link)
            data = data.content
            photo = open(full_address, 'wb')
            photo.write(data)
            photo.close()
        else:
            print('Photo %s already exists, skip...' % photo_name)

    def main(self):
        # self.login()
        make_folder('D:\Download', 'Weibo')
        models_info = self.get_models_info()
        for model_info in models_info:
            model_id = model_info[1]
            print('======Found a model, her name is: %s======' % model_info[0])
            self.get_link_sets(model_id)
        self.browser.quit()


demo = WeiBo()
# print(demo.get_models_info())
demo.main()
