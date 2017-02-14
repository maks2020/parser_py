import os
import re
import pickle

from bs4 import BeautifulSoup
from selenium import webdriver

from parser_01s.utils import get_html_make_file
from parser_01s.utils import read_file_in_list

config_parse = {}
with open('./result/kotmarkot_boys/config_kotmarkot_boys.pickle', 'rb') as input_file:
    config_parse = pickle.load(input_file)

name_html = config_parse['name_html']
catalog_results = config_parse['catalog_results']
path_html_url = config_parse['path_things_url_file']
path_output = config_parse['path_output_file']
num_file_parse = 1
start_index = 0

path_output_file = (path_output + 'html_' +
                    name_html + '_' + str(num_file_parse) + '.parse')

things_url_list = []
with open(path_html_url) as input_source:
    for item in input_source.readlines():
        things_url_list.append(item.rstrip())


get_html_make_file(read_file_in_list(path_html_url), path_output_file, 
                    start_index)
