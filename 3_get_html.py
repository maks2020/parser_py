import os
import re
import pickle

from bs4 import BeautifulSoup
from selenium import webdriver

from parser_01s.utils import get_html_with_login
from parser_01s.utils import read_file_in_list
from parser_01s.utils import read_config

# read config from directory of parse
config_parse = {}
config_parse = read_config()

# define variable from dictionary configuration
name_html = config_parse['name_html']
catalog_results = config_parse['catalog_results']
path_html_url = config_parse['path_things_url_file']
path_output = config_parse['path_output_file']
url_login = config_parse['url_login']
num_file_parse = 1
start_index = 0

# define path for the source get from the site
path_output_file = (path_output + 'html_' +
                    name_html + '_' + str(num_file_parse) + '.parse')

get_html_with_login(read_file_in_list(path_html_url), path_output_file,
                    url_login, start_index)
