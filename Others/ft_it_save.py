# -*- coding:utf-8 -*-

# from selenium import webdriver
import time
from bs4 import BeautifulSoup
import re
from pprint import pprint
import requests


# chrome_options = webdriver.ChromeOptions()
# chrome_options.add_argument('user-data-dir=C:\\Users\\Administrator\\AppData\\Local\\Google\\Chrome\\User Data')
# chrome_options.add_argument('disable-infobars')
# chrome = webdriver.Chrome(chrome_options=chrome_options)


# get album link and name from index, no use any more
def get_page_url():
    url_title_dict = {}
    # 222-Xiuren, 223-MyGirl, 224-Tukmo(Bololi), 225-MiStar, 226-IMiss
    # 227-MFStar, 228-FEILIN, 229-UXing, 230-YouWu, 231-MiiTao, 232-TASTE
    # 15-Ugirls, 18-Rosi, 13-Disi, 39-Ligui, 209-TouTiao, 239-QingDouKe

    main_url = 'http://www.ftoow.com/thread.php?fid-222-page-'
    # main_url = 'http://www.itokoo.com/thread-htm-fid-15-page-'
    # temp = 'http://www.ftoow.com/thread.php?fid-61-type-82-page-'
    for i in range(1, 2):  # 3 means get 2 pages
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


# get links from txt file, return link and password pairs
def get_links_from_txt(txt_file, start):
    pairs = []
    with open(txt_file) as f:
        for line in f.readlines():
            line = line.rstrip('\n')
            if len(line) == 0:
                continue
            link = line[start-1:36]
            password = line[-4:]
            pair = [link, password]
            pairs.append(pair)
    f.close()
    return pairs


# get link from txt, open it and save the file to my pan.baidu.com
# can use other tool to do this work (batch save files quickly), no use any more
def save_file2():
    pairs = get_links_from_txt('test.txt', 5)
    for pair in pairs:
        print(pair)
        link = pair[0]
        password = pair[1]
        chrome.get(link)
        time.sleep(2)
        chrome.find_element_by_id('ali93J1').send_keys(password)
        chrome.find_element_by_id('ali93J1').submit()
        time.sleep(2)
        print(chrome.find_element_by_class_name('tip-msg').text)
        time.sleep(2)


# just for save_albums function's usage, not used separately
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


# open the url, find the link and password, save it. no use anymore
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


# all_album = get_page_url()
# print(len(all_album))
# for k, v in all_album.items():
#     save_albums(k, v)
#     modify_dict(k, v)
#     print k, v


# test = 'http://www.itokoo.com/read-htm-tid-32252-fpage-2.html'
# chrome.get(test)
# t_soup = BeautifulSoup(chrome.page_source, 'html.parser')
# pw = t_soup.find_all('a', class_='down')[1].nextSibling.strip()[-4:]
# print pw

# save_file2()
# pprint(get_page_url())
# chrome.quit()


# get page content use requests.get function and return the content
def get_page_content(url):
    return requests.get(url).content


# get album index(name actually) and link from the forum
def get_album_index(forum, fid, start=1, end=2):
    album_index = []
    # 222-Xiuren, 223-MyGirl, 224-Tukmo(Bololi), 225-MiStar, 226-IMiss
    # 227-MFStar, 228-FEILIN, 229-UXing, 230-YouWu, 231-MiiTao, 232-TASTE
    # 15-Ugirls, 18-Rosi, 13-Disi, 39-Ligui, 209-TouTiao, 239-QingDouKe

    # 127-FEILIN

    for i in range(start, end):  # 3 means get 2 pages
        if forum == 1:
            main_url = 'http://www.itokoo.com/thread.php?fid='
            index_page_url = main_url + str(fid) + '&page=' + str(i)
        else:
            main_url = 'http://www.ftoow.com/thread.php?fid-'
            index_page_url = main_url + str(fid) + '-page-' + str(i) + '.html'
        response = get_page_content(index_page_url).decode('gbk')
        soup = BeautifulSoup(response, 'html.parser')
        if i == 1:
            contents = soup.find('tr', class_='tr4').find_next_siblings('tr')  # siblings(trs after first tr)
        else:
            contents = soup.find('table', class_='z').find_all('tr')  # children(trs under table)
        for content in contents:  # a content is a tr
            item = content.find('a', class_='subject_t')  # a tag(that has class key) under tr tag
            if forum == 1:
                link = 'http://www.itokoo.com/' + item['href'].strip()
            else:
                link = 'http://www.ftoow.com/' + item['href'].strip()
            name = item.string.strip()
            # find the albums before particular one (may downloaded already last time)
            if 'No.749' in name:  # check the end point manually and BE CAREFUL with the caps
                break
            pair = [name, link]
            album_index.append(pair)
    return album_index


# get the download link and password of every album
def get_link_and_pw(forum, fid, start=1, end=2):
    album_index = get_album_index(forum, fid, start, end)
    down_link = []
    for link_and_pw_pair in album_index:
        album_link = link_and_pw_pair[1]
        # print(album_link)
        name = link_and_pw_pair[0]
        print("Now finding %s's download link" % name)
        response = get_page_content(album_link).decode('gbk')
        pattern = re.compile('https://pan.baidu.com/s/(.*?)".*?密码(.*?)</div>', re.S)  # itokoo&some ftoow
        # pattern2 = re.compile('https://pan.baidu.com/s/(.*?)".*?"color:#333333 ">(.*?)</span>', re.S)  # most ftoow
        if forum == 1:
            link_and_pw = re.findall(pattern, response)
            if len(link_and_pw) == 0:
                # print('This album is NOT free!!!')
                down_link.append(name + '↓↓↓\n' + 'This album is NOT free!!!')
            else:
                link = 'https://pan.baidu.com/s/' + link_and_pw[0][0]
                password = link_and_pw[0][1].strip()[-4:]
                # print(link, password)
                down_link.append(name + '↓↓↓\n' + link+'---'+password)
        else:
            soup = BeautifulSoup(response, 'html.parser')
            link_and_pw = soup.find('a', class_='down')
            if link_and_pw is None:
                down_link.append(name + '↓↓↓\n' + 'This album is NOT free!!!')
            else:
                link = link_and_pw['href']
                password = link_and_pw.nextSibling.strip()[-4:]
                if '：' in password:
                    password = link_and_pw.parent.parent.next_sibling.text
                down_link.append(name + '↓↓↓\n' + link+'---'+password)
    return down_link


# save contents in list to txt file
def write_file(path, data):
    f = open(path, 'w')
    for down_link in data:
        f.write(down_link)
        f.write('\n')
    f.close()


def main(forum, fid, start=1, end=2):
    data = get_link_and_pw(forum, fid, start, end)
    write_file('test.txt', data)

main(2, 209)

# print(get_album_index(1, 127))
# get_link_and_pw(2, 209)

