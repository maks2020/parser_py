import re
from bs4 import BeautifulSoup
from selenium import webdriver
import os
import sys
import django
import pickle
from parser_01s.utils import file_make_dict

# # url_catalog = '/catalog/muzhchinam/odezhda_1/svitery_dzhempery/'
# url_catalog = '/catalog/muzhchinam/odezhda_1/palto/'
# url_full = config_parse['url_site'] + url_catalog
# PHANTOMJS_PATH = './phantomjs'
# browser = webdriver.PhantomJS(PHANTOMJS_PATH)
# browser.get(url_full)
# source_html = browser.page_source
# soup = BeautifulSoup(source_html, "lxml")
# things_list = soup.find_all('a', ['class': 'text_fader'])
# url_things_list = []
# for thing in things_list:
#   url_thing = config_parse['url_site'] + thing.get('href')
#   url_things_list.append(url_thing)
# sources_html_list = []
# for url in url_things_list:
#   browser.get(url)
#   sources_html_list.append(browser.page_source)
# with open('sources_html_list02.pickle', 'wb') as output_file:
#   pickle.dump(sources_html_list, output_file)

# work version
# config_parse['url_site'] = input('Введите адрес сайта: ')
# config_parse['url_first'] = input('Вставьте адрес первой страницы каталога: ')
# url_last = input('Вставьте адрес последней страницы каталога: ')
# count_page = input('Сколько страниц нужно обойти: ')
# name_file = input('На выходе вы получите файл csv. Введите желаемое имя файла без расширения: ')
# print('Process...')
# name_file_input = name_file + '.pickle'
# name_data_file = name_file + '.data'
# with open(name_data_file, 'wb') as output_file:
#   pickle.dump(config_parse['url_site'], output_file)
#   pickle.dump(name_file, output_file)

config_parse = {}
config_parse['url_site'] = 'http://www.agat77.ru'
config_parse['url_first'] = 'http://www.agat77.ru/catalog/figurki/'
config_parse['url_last_elem01'] = '?&PAGEN_1='
config_parse['url_last_elem02'] = '&AJAX_PAGE=Y'
config_parse['page_num'] = 8
config_parse['name_html'] = config_parse['url_first'].split('/')[-2]
print(config_parse['name_html'])
config_parse['catalog_results'] = './result/' + \
    '%s/input/' % config_parse['name_html']
config_parse['name_output_file'] = config_parse[
    'catalog_results'] + 'html_%s.txt' % config_parse['name_html']


try:
    os.makedirs(config_parse['catalog_results'], mode=0o777, exist_ok=False)
except:
    ...

# with open(name_data_file, 'wb') as output_file:
#     pickle.dump(config_parse['url_site'], output_file)
#     pickle.dump(name_file, output_file)


def url_list_make(url_first, url_last_elem01, url_last_elem02, num_pages):
    """make list of url pages"""
    # urls_list = []  # define list for list urls
    # for num_page in range(1, num_pages + 1):  # make list urls for scraped
    # num_page = 0
    # url_str =
    # urls_list.append(url_full)  # append url page in list
    urls_list = ['%s%s%s%s' % (config_parse['url_first'], config_parse['url_last_elem01'],
                               str(num_page), config_parse['url_last_elem02'])
                 for num_page in range(1, num_pages + 1)]
    return urls_list


def get_html_page(urls_list):
    """get html source from web site"""
    source_html = []
    url_html = []
    source_html_dict = []
    for url_full in urls_list:
        print(url_full)
        PHANTOMJS_PATH = './phantomjs'
        browser = webdriver.PhantomJS(PHANTOMJS_PATH)
        browser.get(url_full)
        source_html.append(browser.page_source)
        url_html.append(url_full)
        source_html_dict = dict(zip(url_html, source_html))
    return source_html_dict


def add_url_html_bd(dict_url_html):
    """add data in basedata"""
    for key in dict_url_html:
        data_insert = Request_HTML(
            url_html=str(key), source_html=str(dict_url_html[key]))
        data_insert.save()

sources_html = get_html_page(url_list_make(config_parse['url_first'], config_parse['url_last_elem01'],
                                           config_parse['url_last_elem02'], config_parse['page_num']))
# make outpat file with html source
file_make_dict(sources_html, config_parse['name_output_file'])
print(
    ('Done process get html from internet. See new file - html_%s.txt' % config_parse['name_html']))


# if __name__ == '__main__':
#   print ("Starting add data in BD script...")
#   os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'parser_01s.settings')
#   django.setup()
#   from parser_01s.models import Request_HTML
#   add_url_html_bd(sources_url_html)
