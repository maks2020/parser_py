from bs4 import BeautifulSoup
import re
import pickle
import codecs

from parser_01s.utils import read_config

config_parse = {}
# read data project
config_parse = read_config('shilco_womens')

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
    sources_html_list = input_file.read().split(';;;;;;;;;;;;;;;;;;;;')
    # print(len(sources_html_list))
    count = 0
for source in sources_html_list:
    thing_data_list = []  # define list for data things
    # source_ed = source.replace(';', '')
    # soup = BeautifulSoup(source_ed, "lxml")
    soup = BeautifulSoup(sources_html_list[1].replace(';', ''), "lxml")
    # add common data for thing
    common_data = {}
    try:
        common_data['part_number'] = soup.select(
            ".display_properties li font")[0].get_text(strip=True)
    except:
        common_data['part_number'] = ''
    try:
        common_data['name_thing'] = soup.select(
            ".dop_info p")[0].get_text(strip=True)
    except:
        common_data['name_thing'] = ''
    #common_data['name_thing'] = soup.h1.get_text(strip=True)
    #desc = re.compile(r'(span)* p* [А-Яа-я0-9%]+')
    try:
        common_data['description'] = soup.find(
            "span", class_="description").get_text(strip=True).replace('\n', '')
    except:
        ...
    # print(soup.find(desc))
    # print(common_data['part_number']   ,soup.find("span", class_="description").get_text(strip=True))
    thing_data_list.append(common_data)
    # get list contents from tag <script> for every page
    scripts_list = soup.find_all('script')
    scripts_text = []
    for script_item in scripts_list:
        scrp_soup = BeautifulSoup(str(script_item), 'lxml')
        scripts_text.append(scrp_soup.get_text(separator=u"", strip=True))
    # get text data color, size, man's height from content of tag <script> and
    # add it's in the list
    for text in scripts_text:
        regex_str = re.compile(r"arSKU = [{['0-9:А-Яа-я,A-Za-z#{ ._}/?=&-}]+")
        # search path text for regex
        if regex_str.search(text):
            vals_list = regex_str.search(
                text).group()[9:-2].replace("{'0':", ";;;;{'0':").split(';;;;')
            vals_list = vals_list[1:]
            data_thing_for_color = {}
            keys_list_temp = []
            values_list_temp = []
            # delete symbols "{}'" and elements and split. Build dictionary from
            # lists
            for val in vals_list:
                vars_list = val.replace('{', '').replace('}', '').replace(
                    "'", "")[:-1].split(',')
                vars_list.remove(vars_list[5])
                for var in vars_list:
                    var = var.split(':')
                    keys_list_temp.append(var[0])  # add keys
                    values_list_temp.append(var[1])  # add values of keys
                data_thing_for_color = dict(zip(keys_list_temp, values_list_temp))
                thing_data_list.append(data_thing_for_color)
    # find url images and create list
    as_list = soup.select("a[data-zoom-image]")
    imgs_url_list = []
    for item in as_list:
        imgs_url_list.append(url_site + item.get('data-zoom-image'))
    thing_data_list.append(imgs_url_list)  # add images in list data thing
    count += 1
    # print(thing_data_list[0]['part_number'],
    #     thing_data_list[0]['name_thing'],
    #     thing_data_list[1]['0'],
    #     thing_data_list[1]['PRICE'],
    #     thing_data_list[1]['1'],
    #     thing_data_list[1]['2'],
    #     sep=' | ', end='')
    # print(thing_data_list[-1])
    #generate row csv for url images
    imgs_urls = ''
    for img_url in thing_data_list[-1]:
        imgs_urls += img_url + ';'
    
    for item in thing_data_list[1:-1]:
        try:
            row_csv = (thing_data_list[0]['part_number'] + ' ' +
                       thing_data_list[0]['name_thing'] + ' ' +
                       item['0'] + ';' + #color
                       thing_data_list[0]['part_number'] + ' ' +
                       thing_data_list[0]['name_thing'] + ' ' +
                       item['0'] + ';' + #color
                       thing_data_list[0]['description'] + ';' +
                       item['PRICE'] + ';' +
                       item['1'] + ';' + 
                       imgs_urls)
            rows_csv.append(row_csv)
        except:
            ...
#=========
with open(path_output_file, 'w') as output_file:
    output_file.write(
        'артикул;наименование;описание;цена;размер;img;img;img;img;img;img;img;img;img;img\n')
    for row in rows_csv:
        output_file.write(row + '\n')
# =========
    # with open('parser.log', 'a') as output_file:
    #     output_file.write(source + '\n' * 3 + '=' * 80 + '\n' *3)
# count += 1

    #     print('Exception in sourse: ' + str(sources_html_list.index(source)))
    # print('Count: ' + str(count))
