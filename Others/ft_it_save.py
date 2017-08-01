# -*- coding:utf-8 -*-

from selenium import webdriver
import time
# from selenium.webdriver.support.wait import WebDriverWait
# from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.by import By
# from selenium.common.exceptions import NoSuchElementException
from bs4 import BeautifulSoup


chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('user-data-dir=C:\\Users\\zheng\\AppData\\Local\\Google\\Chrome\\User Data')
chrome = webdriver.Chrome(chrome_options=chrome_options)


def get_page_url():
    url_title_dict = {}
    # 222-Xiuren, 223-MyGirl, 224-Tukmo(Bololi), 225-MiStar, 226-IMiss
    # 227-MFStar, 228-FEILIN, 229-UXing, 230-YouWu, 231-MiiTao, 232-TASTE
    # 15-Ugirls, 18-Rosi, 13-Disi, 39-Ligui, 209-TouTiao, 239-QingDouKe

    main_url = 'http://www.ftoow.com/thread.php?fid-222-page-'
    # main_url = 'http://www.itokoo.com/thread-htm-fid-15-page-'
    # temp = 'http://www.ftoow.com/thread.php?fid-61-type-82-page-'
    for i in range(8, 10):  # 3 means get 2 pages
        index_page_url = main_url + str(i) + '.html'
        chrome.get(index_page_url)
        soup = BeautifulSoup(chrome.page_source, 'html.parser')
        if i == 1:
            contents = soup.find('tr', class_='tr4').find_next_siblings('tr')  # siblings(trs after first tr)
        else:
            contents = soup.find('table', class_='z').find_all('tr')  # children(trs under table)
        for content in contents:  # a content is a tr
            item = content.find('a', class_='subject_t')  # a tag(that has class key) under tr tag
            link = 'http://www.ftoow.com/' + item['href'].strip()  # ftoow, itokoo
            name = item.string.strip()
            # find the albums before particular one (may downloaded already last time)
            if 'No.749' in name:  # check the end point manually and BE CAREFUL with the caps
                break
            url_title_dict.setdefault(link, name)
    return url_title_dict


def save_file(password):
    chrome.find_elements_by_class_name('down')[0].click()
    time.sleep(2)
    chrome.find_element_by_id('accessCode').send_keys(password)
    chrome.find_element_by_id('accessCode').submit()
    # chrome.find_element_by_xpath('//*[@id="submitBtn"]/a').click()
    # 隐形等待是设置了一个最长等待时间，如果在规定时间内网页加载完成，则执行下一步，否则一直等到时间截止，然后执行下一步。
    # 隐性等待对整个driver的周期都起作用，所以只要设置一次即可。
    # chrome.implicitly_wait(5)
    time.sleep(4)
    chrome.find_element_by_class_name('g-button-right').click()
    # locator = (By.CLASS_NAME, 'g-button-right')
    # WebDriverWait(chrome, 3).until(ec.presence_of_element_located(locator))
    time.sleep(4)  # //*[@id="fileTreeDialog"]/div[4]/a[2]
    # chrome.find_element_by_xpath('//*[@id="fileTreeDialog"]/div[4]/a[2]/span').click()
    chrome.find_elements_by_class_name('g-button-right')[-2].click()
    time.sleep(2)


def save_albums(url, name):
    # url is the album page url, something like this: http://www.ftoow.com/read.php?tid-32350.html
    chrome.get(url)

    # use find_elementS to judge the element exists or not
    download_button = chrome.find_elements_by_class_name('down')
    if len(download_button) != 0:
        get_password = chrome.find_elements_by_xpath('//a[@class="down"]/ancestor::span[2]/following-sibling::span')
        if len(get_password) != 0:
            password = get_password[0].text.strip()
        else:
            pw_soup = BeautifulSoup(chrome.page_source, 'html.parser')
            password = pw_soup.find('a', class_='down').nextSibling.strip()[-4:]
            # password = pw_soup.find_all('a', class_='down')[1].nextSibling.strip()[-4:]  # for itokoo.com
        if len(password) == 4:
            # target="_blank" means open the link in a new tab, remove it to let the link open within the tab
            js = 'document.getElementsByClassName("down")[0].target="";'
            chrome.execute_script(js)
            save_file(password)
            print(name + ' is saved.')
        else:
            print(name + ': get password failed, please check it by yourself.')
    else:
        print(name + ' is not free!!!')


def modify_dict(url, name):
    chrome.get(url)
    download_button = chrome.find_elements_by_class_name('down')
    if len(download_button) != 0:
        print('%s: %s' % (name, url))
    else:
        pass


all_album = get_page_url()
print(len(all_album))
for k, v in all_album.items():
    save_albums(k, v)
    # modify_dict(k, v)
#     print k, v


# test = 'http://www.itokoo.com/read-htm-tid-32252-fpage-2.html'
# chrome.get(test)
# t_soup = BeautifulSoup(chrome.page_source, 'html.parser')
# pw = t_soup.find_all('a', class_='down')[1].nextSibling.strip()[-4:]
# print pw


chrome.quit()




