import codecs
import timeit
from bs4 import BeautifulSoup
from selenium import webdriver
import pickle


def get_html_make_file(urls_list, file_name, index_item=0):
    """get html code from source and make output file"""
    # path_geckodriver='/Users/mas/Desktop/my_python/py3x/parser01/env/bin'
    with open(file_name, 'w') as output_file:
        count = 1
        slice_urls_list = urls_list[index_item:]
        buffer_list = []
        for url_full in slice_urls_list:
            print(str(index_item + 1), ' ', url_full.rstrip())
            PHANTOMJS_PATH = './phantomjs'
            # browser = webdriver.Firefox(path_geckodriver)
            browser = webdriver.PhantomJS(PHANTOMJS_PATH)
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


def write_file_csv(file_name, content_file, method_rec, codec_text):
    with codecs.open(file_name, method_rec, codec_text) as output_file:
        for row in content_file:
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

