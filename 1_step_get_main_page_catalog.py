import re
from bs4 import BeautifulSoup
from selenium import webdriver
import os
import sys
import django
import pickle

from parser_01s.utils import file_make_dict

def url_list_make(url_first, url_last_elem01, url_last_elem02, num_pages):
    """make list of url catalog pages"""
    urls_list = ['%s%s%s%s' % (url_first, url_last_elem01, str(num_page), url_last_elem02)
                 for num_page in range(1, int(num_pages) + 1)]
    urls_list.append('http://kotmarkot.ru/catalog/20')
    return urls_list


def get_html_page(urls_list):
    """get html source from web site"""
    source_html = []
    url_html = []
    source_html_dict = []
    # path_geckodriver='/Users/mas/Desktop/my_python/py3x/parser01/env/bin/'
    PHANTOMJS_PATH = './phantomjs'
    for url_full in urls_list:
        print(url_full)
        # browser = webdriver.Firefox(path_geckodriver)
        browser = webdriver.PhantomJS(PHANTOMJS_PATH)
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

config_parse = {}
name_html = config_parse['name_html'] = input('Input name project: ')
url_site = config_parse['url_site'] = input("Input url site aka http://example.com: ")
url_first = config_parse['url_first'] = input('Input url first page catalog aka http://example.com/catalog/: ')
url_last_elem01 = config_parse['url_last_elem01'] = input('Input element url aka 11?page= : ') 
url_last_elem02 = config_parse['url_last_elem02'] = ''
page_num = config_parse['page_num'] = input('Input page count: ')
catalog_results = config_parse['catalog_results'] = ('./result/' + '%s/' % name_html)
path_input_file = config_parse['name_input_file'] = (catalog_results + 'input/')
cat_file_html = config_parse['cat_file_html'] = path_input_file + 'html_%s_catalog.parse' % name_html
path_output_file = config_parse['path_output_file'] = (catalog_results + 'output/')
name_data_file = config_parse['name_data_file'] = catalog_results + 'config_%s.pickle' % name_html

try:
    os.makedirs(path_input_file, mode=0o777, exist_ok=False)
except:
    ...

try:
    os.makedirs(path_output_file, mode=0o777, exist_ok=False)
except:
    ...

sources_html = get_html_page(url_list_make(url_first, url_last_elem01,
                                           url_last_elem02, page_num))
#make output file with html source
file_make_dict(sources_html, cat_file_html)

with open(name_data_file, 'wb') as output_file:
    pickle.dump(config_parse, output_file)

print(
    ('Done process get html from internet. See new file - html_%s.txt' % name_html))


# if __name__ == '__main__':
#   print ("Starting add data in BD script...")
#   os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'parser_01s.settings')
#   django.setup()
#   from parser_01s.models import Request_HTML
#   add_url_html_bd(sources_url_html)
