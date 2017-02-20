import os
import re
import codecs
import math
import pickle

from parser_01s.utils import write_file_csv
#========
# path_files = './result/figurki/input/'
# path_files_output = './result/figurki/output/'
# codec_file = 'cp1251'
# method_rec = 'w'

# files_list = os.listdir(path_files)
# ext_files = re.compile(r'csv')

# for file_name in files_list:
#     rows_csv = []
#     if ext_files.search(file_name):
#         path_file = path_files + file_name
#         file_name_new = path_files_output + file_name[:-4] + '_opt.csv'
#         input_file = codecs.open(path_file, 'r', codec_file)
#         read_file_data = input_file.readlines()
#         row_list = []
#         try:
#             for data in read_file_data:
#                 row_list = data.split(';')
#                 if row_list[3] and row_list[3] != 'цена':
#                     row_list[3] = str(math.ceil(
#                         (int(
#                             re.search(r'[0-9]+', row_list[3].replace(' ', ''))
#                             .group())) * 0.46))
#                     print(row_list[0], row_list[3])
#                 row_csv = ''
#                 for item_row in row_list:
#                     row_csv += item_row + ';'
#                 rows_csv.append(row_csv[:-1])
#                 write_file_csv(file_name_new, rows_csv, method_rec, codec_file)
#         except:
#             print(file_name, row_list, row_list[3])
#=====
from parser_01s.utils import read_config

config_parse = read_config()
num_file_parse = 1
name_html = config_parse['name_html']
path_html_url = config_parse['path_things_url_file']
path_output = config_parse['path_output_file']
# path_parse_file = (path_input + 'html_' +
                    # name_html + '_' + str(num_file_parse) + '.parse')
path_output_file = (path_output + 'html_' +
                    name_html + '_filt_url_' + '.txt')

# source_html = []
# with open(path_parse_file, 'r') as input_file:
#     source_html = input_file.read().split(';;;;;;;;;;;;;;;;;;;;')

things_url_list = []
with open(path_html_url) as input_source:
    for item in input_source.readlines():
        things_url_list.append(item.rstrip())

# dict_url_html = dict(zip(things_url_list, source_html))
key_url = re.compile(r'//[.a-z]+/[a-z]+/[_*a-z]+/[_*a-z0-9]+/')

url_fil = []
# html_filter = []
for url in things_url_list:
    if key_url.search(url):
        url_fil.append(url)

with open(path_output_file, 'w') as output_file:
    for url in url_fil:
        output_file.write(url + '\n')


