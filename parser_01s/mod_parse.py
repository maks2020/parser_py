# models parsing for sites

import re
from bs4 import BeautifulSoup


def parse_shilco_sport_v1(sources_html_list, url_site):
    """parser models for site shilco.ru"""
    rows_csv = []
    for source in sources_html_list:
        thing_data_list = []  # define list for data things
        source_ed = source.replace(';', '')
        soup = BeautifulSoup(source_ed, "lxml")
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
        try:
            common_data['description'] = soup.find(
                "span", class_="description").get_text(strip=True).replace('\n', '')
        except:
            ...
        try:
            common_data['price_thing'] = soup.select(
                ".price")[0].get_text(strip=True)
        except:
            ...
        print(soup.select(".price"))
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
            regex_str = re.compile(
                r"arSKU = [{['0-9:А-Яа-я,A-Za-z#{ ._}/?=&-}]+")
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
                    data_thing_for_color = dict(
                        zip(keys_list_temp, values_list_temp))
                    thing_data_list.append(data_thing_for_color)
        # find url images and create list
        as_list = soup.select("a[data-zoom-image]")
        imgs_url_list = []
        for item in as_list:
            imgs_url_list.append(url_site + item.get('data-zoom-image'))
        thing_data_list.append(imgs_url_list)  # add images in list data thing
        # create row csv for url images
        imgs_urls = ''
        for img_url in thing_data_list[-1]:
            imgs_urls += img_url + ';'
        for item in thing_data_list[1:-1]:
            try:
                row_csv = (thing_data_list[0]['part_number'] + ' ' +
                           thing_data_list[0]['name_thing'] + ' ' +
                           item['0'] + ';' +  # color
                           thing_data_list[0]['part_number'] + ' ' +
                           thing_data_list[0]['name_thing'] + ' ' +
                           item['0'] + ';' +  # color
                           thing_data_list[0]['description'] + ';' +
                           thing_data_list[0]['price_thing'] + ';' +
                           item['1'] + ';' +
                           imgs_urls)
                print(row_csv)
                rows_csv.append(row_csv)
            except:
                ...
    return rows_csv


def parse_shilco_sport_v2(sources_html_list, url_site):
    """parser models for site shilco.ru"""
    rows_csv = []
    for source in sources_html_list:
        thing_data_list = []  # define list for data things
        #clear source from "; \n"
        source_ed = source.replace(';', '').replace('\n', '')
        soup = BeautifulSoup(source_ed, "lxml")
        # soup = BeautifulSoup(sources_html_list[10].replace(';', ''), "lxml")
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
        try:
            common_data['description'] = soup.find(
                "span", class_="description").get_text(strip=True).replace('\n', '')
            if '-->' in common_data['description']:
                common_data['description'] = common_data[
                    'description'].split('-->')[1]
        except:
            common_data['description'] = ''
        try:
            common_data['price_thing'] = soup.select(
                ".price")[0].get_text(strip=True)
        except:
            common_data['price_thing'] = ''
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
            regex_str = re.compile(
                r"arSKU = [{['0-9:А-Яа-я,A-Za-z#{ ._}/?=&-}]+")
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
                    data_thing_for_color = dict(
                        zip(keys_list_temp, values_list_temp))
                    thing_data_list.append(data_thing_for_color)
        #create dictionary item "color: size/height"
        thing_color_dict = {}
        for item in thing_data_list[1:]:
            thing_color_dict[item['0']] = ''
        for item in thing_data_list[1:]:
            thing_color_dict[item['0']] += item['1'] + '/' + item['2'] + ', '
        thing_color_size_height = ''
        for key in thing_color_dict:
            thing_color_size_height += (key + ': ' +
                                        thing_color_dict[key][:-2]) + '. '
        # create sizes list
        thing_sizes = {}
        for item in thing_data_list[1:]:
            thing_sizes[item['1']] = ''
        sizes_list = list(thing_sizes.keys())
        sizes_list.sort(reverse=True)
        as_list = soup.select("a[data-zoom-image]")
        imgs_url_list = []
        #create list and string url images for .csv
        for item in as_list:
            imgs_url_list.append(url_site + item.get('data-zoom-image'))
        thing_data_list.append(imgs_url_list)  # add images in list data thing
        # create row csv for url images
        imgs_urls = ''
        for img_url in thing_data_list[-1]:
            imgs_urls += img_url + ';'
        #create row csv on sizes
        for size_thing in sizes_list:
            row_csv = (thing_data_list[0]['part_number'] + ' ' +
                       thing_data_list[0]['name_thing'] + ' ' + ';' +
                       thing_data_list[0]['part_number'] + ' ' +
                       thing_data_list[0]['name_thing'] + ' ' + ';' +
                       thing_data_list[0]['description'] + ' ' +
                       'Цвета, размер и рост доступные к заказу: ' +
                       thing_color_size_height[:-1] + ';' +
                       thing_data_list[0]['price_thing'] + ';' +
                       # sizes_str[:-1] + ';' + imgs_urls)
                       size_thing + ';' + imgs_urls)
            #filling list rows_csv rows csv
            rows_csv.append(row_csv)
    return rows_csv
