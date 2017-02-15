#http://www.shilco.ru/catalog/dlya_zhenshchin/?PAGEN_1=1

import re
from bs4 import BeautifulSoup
from selenium import webdriver
import os
import sys
import django
import pickle
import getpass

from parser_01s.utils import file_make_dict, read_config


def url_list_make(url_first, url_last_elem01, url_last_elem02, num_pages):
    """make list of url catalog pages"""
    urls_list = ['%s%s%s%s' % (url_first, url_last_elem01, str(num_page), url_last_elem02)
                 for num_page in range(1, int(num_pages))]
    # urls_list.append('http://kotmarkot.ru/catalog/20')
    return urls_list


def get_html_page(urls_list, url_login_page):
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
    #input and send login and password
    login_value = input('Input login for site: ')
    passwd_value = getpass.getpass('Input password for site: ')
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


def add_url_html_bd(dict_url_html):
    """add data in data base"""
    for key in dict_url_html:
        data_insert = Request_HTML(
            url_html=str(key), source_html=str(dict_url_html[key]))
        data_insert.save()

def login_in():
    url = input('Input url page login: ')
    PHANTOMJS_PATH = './phantomjs'
    # browser = webdriver.Firefox(path_geckodriver)
    browser = webdriver.PhantomJS(PHANTOMJS_PATH)
    browser.get(url)
    login_user = browser.find_element_by_id('USER_LOGIN')
    passwd_user = browser.find_element_by_id('USER_PASSWORD')
    submit_b = browser.find_element_by_id('Login')
    login_user.send_keys('Maxima')
    passwd_user.send_keys('qwerty')
    submit_b.click()


def project_base(name_project):
    projects_data = []
    config_parse = {}
    #open data file with name of projects
    try:
        with open('projects_data.pickle', 'rb') as r_file:
            projects_data = pickle.load(r_file)
    #if data file  projects not exist
    except FileNotFoundError:
        with open('projects_data.pickle', 'ab') as create_file:
            pickle.dump(projects_data, create_file)
        with open('projects_data.pickle', 'rb') as r_file:
            projects_data = pickle.load(r_file)
    if name_project in projects_data:
        config_parse = read_config(name_project)
    else:
        #input data for parse
        config_parse['name_html'] = name_project
        config_parse['url_site'] = input("Input url site aka http://example.com: ") #http://www.shilco.ru
        config_parse['url_first'] = input('Input url first page catalog aka http://example.com/catalog/: ') #http://www.shilco.ru/catalog/dlya_zhenshchin/
        config_parse['url_last_elem01'] = input('Input element url aka 11?page= : ') #?PAGEN_1=
        config_parse['url_last_elem02'] = ''
        config_parse['page_num'] = input('Input page count: ')
        config_parse['url_login'] = input('Input url login page: ')
        #input name parse in list data project
        projects_data.append(name_project)
        #write in file 
        with open('projects_data.pickle', 'wb') as output_file:
            pickle.dump(projects_data, output_file)
        #create path for input/output files
        config_parse['catalog_results'] = ('./result/' + '%s/' % name_html)
        config_parse['name_input_file'] = (catalog_results + 'input/')
        config_parse['cat_file_html'] = path_input_file + 'html_%s_catalog.parse' % name_html
        config_parse['path_output_file'] = (catalog_results + 'output/')
        config_parse['name_data_file'] = catalog_results + 'config_%s.pickle' % name_html
        #create structure directory
        create_dir(path_input_file, path_output_file)
        #write data parser in file
        with open(name_data_file, 'wb') as output_file:
            pickle.dump(config_parse, output_file)
    return config_parse

def create_dir(path_input_file, path_output_file):
    """create tree of dir for data of parser"""
    try:
        os.makedirs(path_input_file, mode=0o777, exist_ok=False)
    except:
        ...
    try:
        os.makedirs(path_output_file, mode=0o777, exist_ok=False)
    except:
        ...

config_parse = {}
name_project = input('Input name project: ')
#try is project in base if not add his and new data
config_parse = project_base(name_project) 
# name_project = name_html it's bug 
name_html = config_parse['name_html']
url_site = config_parse['url_site']
url_first = config_parse['url_first']
url_last_elem01 = config_parse['url_last_elem01']
url_last_elem02 = config_parse['url_last_elem02']
page_num = config_parse['page_num']
catalog_results = config_parse['catalog_results']
path_input_file = config_parse['name_input_file']
cat_file_html = config_parse['cat_file_html']
path_output_file = config_parse['path_output_file']
name_data_file = config_parse['name_data_file']
url_login = config_parse['url_login']

# get url list and html source
sources_html = get_html_page(url_list_make(url_first, url_last_elem01,
                            url_last_elem02, page_num), url_login)
#make output file with html source get above
file_make_dict(sources_html, cat_file_html)
#done 
print(
    ('Done process get html from internet. See new file - html_%s.txt' % name_html))

# if __name__ == '__main__':
#   print ("Starting add data in BD script...")
#   os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'parser_01s.settings')
#   django.setup()
#   from parser_01s.models import Request_HTML
#   add_url_html_bd(sources_url_html)
