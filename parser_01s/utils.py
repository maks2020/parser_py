import codecs
import timeit
from bs4 import BeautifulSoup
from selenium import webdriver
import pickle
import getpass


def get_html_wout_login(urls_list, file_name, index_item=0):
    """get html code from source and make output file"""
    # path_geckodriver='/Users/mas/Desktop/my_python/py3x/parser01/env/bin'
    with open(file_name, 'w') as output_file:
        count = 1
        slice_urls_list = urls_list[index_item:]
        buffer_list = []
        PHANTOMJS_PATH = './phantomjs'
        # browser = webdriver.Firefox(path_geckodriver)
        browser = webdriver.PhantomJS(PHANTOMJS_PATH)
        for url_full in slice_urls_list:
            print(str(index_item + 1), ' ', url_full.rstrip())
            browser.get(url_full)
            buffer_list.append(browser.page_source)
            if count == 10:
                count = 1
                print("Process write from buffer...")
                for item in buffer_list:
                    output_file.write(str(item) + ';;;;;;;;;;;;;;;;;;;;')
                buffer_list = []
                print("End write")
            if slice_urls_list.index(url_full) == (len(slice_urls_list) - 1):
                print("End urls. Process write from buffer...")
                for item in buffer_list:
                    output_file.write(str(item) + ';;;;;;;;;;;;;;;;;;;;')
                print('End write')
            count += 1
            index_item += 1


def get_html_with_login(urls_list, file_name, url_login_page, index_item=0):
    """get html code from source and make output file with login"""
    # path_geckodriver='/Users/mas/Desktop/my_python/py3x/parser01/env/bin'
    with open(file_name, 'w') as output_file:
        count = 1
        slice_urls_list = urls_list[index_item:]
        buffer_list = []
        # path_geckodriver='/Users/mas/Desktop/my_python/py3x/parser01/env/bin/'
        PHANTOMJS_PATH = './phantomjs'
        # browser = webdriver.Firefox(path_geckodriver)
        browser = webdriver.PhantomJS(PHANTOMJS_PATH)
        #get page with login and password input
        browser.get(url_login_page)
        #search form input login, password, button input
        login_user = browser.find_element_by_id('USER_LOGIN')
        passwd_user = browser.find_element_by_id('USER_PASSWORD')
        submit_b = browser.find_element_by_id('Login')
        #input and send login and password
        login_value = input('Input login for site: ')
        passwd_value = getpass.getpass('Input password for site: ')
        login_user.send_keys(login_value)
        passwd_user.send_keys(passwd_value)
        #click on button submit
        submit_b.click()
        #get html pages code on list url
        for url_full in slice_urls_list:
            print(str(index_item + 1), ' ', url_full.rstrip())
            # PHANTOMJS_PATH = './phantomjs'
            # # browser = webdriver.Firefox(path_geckodriver)
            # browser = webdriver.PhantomJS(PHANTOMJS_PATH)
            browser.get(url_full)
            buffer_list.append(browser.page_source)
            if count == 10:
                count = 1
                print("Process write from buffer...")
                for item in buffer_list:
                    output_file.write(str(item) + ';;;;;;;;;;;;;;;;;;;;')
                buffer_list = []
                print("End write")
            if slice_urls_list.index(url_full) == (len(slice_urls_list) - 1):
                print("End urls. Process write from buffer...")
                for item in buffer_list:
                    output_file.write(str(item) + ';;;;;;;;;;;;;;;;;;;;')
                print('End write')
            count += 1
            index_item += 1


def read_file_in_list(file_name):
    with open(file_name) as input_file:
        return input_file.readlines()


def write_file_csv(file_name, rows_csv_list, method_rec, codec_text):
    with codecs.open(file_name, method_rec, codec_text) as output_file:
        for row in rows_csv_list:
            output_file.write(row)

def file_make_dict(data, path_file):
    """make data file from dictionary"""
    with open(path_file, 'w') as output_file:
        for item in data:
            output_file.write(data[item])

def read_config(name_html_in = ''):
    """try and read exist config file"""
    if name_html_in == '':
        name_html = input('Input name project: ')
    else:
        name_html = name_html_in
    name_data_file  = './result/%s/config_%s.pickle' % (name_html, name_html)
    config_parse = {}
    with open(name_data_file, 'rb') as input_file:
        return pickle.load(input_file)

def get_html_page_auth(urls_list, url_login_page):
    """get html source from web site"""
    source_html = []
    url_html = []
    source_html_dict = []
    # path_geckodriver='/Users/mas/Desktop/my_python/py3x/parser01/env/bin/'
    PHANTOMJS_PATH = './phantomjs'
    # browser = webdriver.Firefox(path_geckodriver)
    browser = webdriver.PhantomJS(PHANTOMJS_PATH)
    #get page with login and password input
    browser.get(url_login_page)
    #search form input login, password, button input
    login_user = browser.find_element_by_id('USER_LOGIN')
    passwd_user = browser.find_element_by_id('USER_PASSWORD')
    submit_b = browser.find_element_by_id('Login')
    #input login and password
    login_value = input('Input login for site: ')
    passwd_value = getpass.getpass('Input password for site: ')
    #and send...
    login_user.send_keys(login_value)
    passwd_user.send_keys(passwd_value)
    #click on button submit
    submit_b.click()
    #get html pages code on list url
    for url_full in urls_list:
        print(url_full)
        browser.get(url_full)
        source_html.append(browser.page_source)
        url_html.append(url_full)
        source_html_dict = dict(zip(url_html, source_html))
    return source_html_dict


def get_html_page_wout_auth(urls_list):
    """get html source from web site"""
    source_html = []
    url_html = []
    source_html_dict = []
    # path_geckodriver='/Users/mas/Desktop/my_python/py3x/parser01/env/bin/'
    PHANTOMJS_PATH = './phantomjs'
    # browser = webdriver.Firefox(path_geckodriver)
    browser = webdriver.PhantomJS(PHANTOMJS_PATH)
    #get html pages code on list url
    for url_full in urls_list:
        print(url_full)
        browser.get(url_full)
        source_html.append(browser.page_source)
        url_html.append(url_full)
        source_html_dict = dict(zip(url_html, source_html))
    return source_html_dict

