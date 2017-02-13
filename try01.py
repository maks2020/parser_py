import os
import re
import codecs
import math
from parser_01s.utils import write_file_csv

path_files = './result/figurki/input/'
path_files_output = './result/figurki/output/'
codec_file = 'cp1251'
method_rec = 'w'

files_list = os.listdir(path_files)
ext_files = re.compile(r'csv')

for file_name in files_list:
    rows_csv = []
    if ext_files.search(file_name):
        path_file = path_files + file_name
        file_name_new = path_files_output + file_name[:-4] + '_opt.csv'
        input_file = codecs.open(path_file, 'r', codec_file)
        read_file_data = input_file.readlines()
        row_list = []
        try:
            for data in read_file_data:
                row_list = data.split(';')
                if row_list[3] and row_list[3] != 'цена':
                    row_list[3] = str(math.ceil(
                        (int(
                            re.search(r'[0-9]+', row_list[3].replace(' ', ''))
                            .group())) * 0.46))
                    print(row_list[0], row_list[3])
                row_csv = ''
                for item_row in row_list:
                    row_csv += item_row + ';'
                rows_csv.append(row_csv[:-1])
                write_file_csv(file_name_new, rows_csv, method_rec, codec_file)
        except:
            print(file_name, row_list, row_list[3])
