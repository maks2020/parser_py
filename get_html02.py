import os
import re
from bs4 import BeautifulSoup
from selenium import webdriver

from parser_01s.utils import get_html_make_file
from parser_01s.utils import read_file_in_list

path_html_url = './result/figurki/input/thing_url_figurki.txt'
name_parse = 'figurki'
path_dir_source = './result/'
num_file_parse = 1
start_index = 0

path_input_file = (path_dir_source + name_parse +
                   '/input/' + 'thing_url_' + name_parse + '.txt')
path_dir_output = (path_dir_source + name_parse +
                   '/output/')
path_output_file = (path_dir_output + 'html_' +
                    name_parse + '_' + str(num_file_parse) + '.parse')

things_url_list = []
with open(path_html_url) as input_source:
    for item in input_source.readlines():
        things_url_list.append(item.rstrip())


try:
    os.makedirs(path_dir_output, mode=0o777, exist_ok=False)
except:
    ...
get_html_make_file(read_file_in_list(path_html_url), path_output_file, 
                    start_index)
