from bs4 import BeautifulSoup
import pickle
import codecs

from parser_01s.utils import read_config
from parser_01s.mod_parse import parse_shilco_sport_v2

config_parse = {}
# read data project
config_parse = read_config()
num_file_parse = 1  # number file parse
path_output = config_parse['path_output_file']
name_html = config_parse['name_html']
url_site = config_parse['url_site']
path_input_file = (
    path_output + 'html_' + name_html + '_' + str(num_file_parse) + '.parse')

rows_csv = []  # end data in csv file
path_output_file = path_input_file[:-6] + '.csv'  # name file csv

# read source code html for pages
sources_html_list = []
with open(path_input_file) as input_file:
    sources_html_list = input_file.read().split(';;;;;;;;;;;;;;;;;;;;')[:-1]
#write csv file
with open(path_output_file, 'w') as output_file:
    output_file.write(
        'артикул;наименование;описание;цена;размер;img;img;img;img;img;img;img;img;img;img\n')
    #get rows csv from function-parser
    rows_csv = parse_shilco_sport_v2(sources_html_list, url_site)
    for row in rows_csv:
        output_file.write(row + '\n')

