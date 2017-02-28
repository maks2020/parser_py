# models parsing for sites

import re
from bs4 import BeautifulSoup

def filling_str(string, len_str = 110):
    """filling string on full"""
    leght_str = len(string)
    if leght_str <= len_str:
        add_symb = len_str - len(string)
        add_str = '..' * add_symb
    else:
        while leght_str > len_str:
            leght_str = abs(leght_str - len_str)
        add_symb = len_str - leght_str
        add_str = '..' * add_symb
    return add_str


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
        # clear source from "; \n"
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
        # create dictionary item "color: size/height"
        thing_color_dict = {}
        for item in thing_data_list[1:]:
            thing_color_dict[item['0']] = ''
        for item in thing_data_list[1:]:
            thing_color_dict[item['0']] += item['1'] + '/' + item['2'] + ', '
        thing_color_size_height = ''
        for key in thing_color_dict:
            color_str = (key + ': ' + thing_color_dict[key][:-2] + '. ')
            thing_color_size_height += (key + ': ' + (filling_str(color_str)) +
                                        thing_color_dict[key][:-2] + '. ')
        # create sizes list
        thing_sizes = {}
        for item in thing_data_list[1:]:
            thing_sizes[item['1']] = ''
        sizes_list = list(thing_sizes.keys())
        sizes_list.sort(reverse=True)
        as_list = soup.select("a[data-zoom-image]")
        imgs_url_list = []
        # create list and string url images for .csv
        for item in as_list:
            imgs_url_list.append(url_site + item.get('data-zoom-image'))
        thing_data_list.append(imgs_url_list)  # add images in list data thing
        # create row csv for url images
        imgs_urls = ''
        for img_url in thing_data_list[-1]:
            imgs_urls += img_url + ';'
        # create row csv on sizes
        for size_thing in sizes_list:
            row_csv = (thing_data_list[0]['part_number'] + ' ' +
                       thing_data_list[0]['name_thing'] + ' ' + ';' +
                       thing_data_list[0]['part_number'] + ' ' +
                       thing_data_list[0]['name_thing'] + ' ' + ';' +
                       # thing_data_list[0]['description'] + ' ' +
                       thing_data_list[0]['description'] + filling_str(thing_data_list[0]['description']) + '. ' +
                       'Цвета, размер и рост доступные к заказу: ' + filling_str('Цвета, размер и рост доступные к заказу: ' + '. ') + '. ' +
                       #thing_color_size_height[:-1] + ';' +
                       thing_color_size_height + ';' +
                       thing_data_list[0]['price_thing'] + ';' +
                       # sizes_str[:-1] + ';' + imgs_urls)
                       size_thing + ';' + imgs_urls)
            # filling list rows_csv rows csv
            rows_csv.append(row_csv)
    return rows_csv


def parse_shilco_sport_v3(sources_html_list, url_site):
    """parser models for site shilco.ru"""
    data_prods_list = []
    for source in sources_html_list:
        thing_data_list = []  # define list for data things
        # clear source from "; \n"
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
        # create dictionary item "color: size/height"
        thing_color_dict = {}
        for item in thing_data_list[1:]:
            thing_color_dict[item['0']] = ''
        for item in thing_data_list[1:]:
            thing_color_dict[item['0']] += item['1'] + '/' + item['2'] + ', '
        thing_color_size_height = ''
        for key in thing_color_dict:
            thing_color_size_height += (key + ': ' + thing_color_dict[key][:-2] + '.' + '\r\n')
            # thing_color_size_height += (key + ': ' + (filling_str(color_str)) +
                                        # thing_color_dict[key][:-2] + '. ')
        # create sizes list
        thing_sizes = {}
        for item in thing_data_list[1:]:
            thing_sizes[item['1']] = ''
        sizes_list = list(thing_sizes.keys())
        sizes_list.sort(reverse=True)
        as_list = soup.select("a[data-zoom-image]")
        imgs_url_list = []
        # create list and string url images for .csv
        for item in as_list:
            imgs_url_list.append(url_site + item.get('data-zoom-image'))
        thing_data_list.append(imgs_url_list)  # add images in list data thing
        # create row csv for url images
        # imgs_urls = ''
        # for img_url in thing_data_list[-1]:
        #     imgs_urls += img_url + ';'
        # create row csv on sizes
        name_prod = (thing_data_list[0]['part_number'] + ' ' +
                       thing_data_list[0]['name_thing'])
        num_prod = (thing_data_list[0]['part_number'] + ' ' +
                       thing_data_list[0]['name_thing'])
        desc_prod = thing_data_list[0]['description']
        define_color = 'Цвета, размер и рост доступные к заказу:'
        price_thing = thing_data_list[0]['price_thing']
        data_prod = []
        data_prod.append(name_prod)
        data_prod.append(num_prod)
        data_prod.append(desc_prod)
        data_prod.append(define_color)
        data_prod.append(price_thing)
        data_prod.append(sizes_list)
        data_prod.append(thing_color_size_height)
        data_prod.append(thing_data_list[-1])
        data_prods_list.append(data_prod)
       
    return data_prods_list


def parse_kotmarkot(sources_html_list):
    rows_csv = []
    for source in sources_html_list:
        soup = BeautifulSoup(source, "lxml")
        imgs_list = soup.select('.imagezoom-thumbs a')
        imgs_str = []
        for img in imgs_list:
            imgs_soup = BeautifulSoup(str(img), "lxml")
            imgs_str.append(imgs_soup.a['data-zoom-image'])
        while len(imgs_str) < 10:
            imgs_str.append('')
        img_str = ';'.join(imgs_str)
        thing_props_list = soup.select('.field__item')
        try:
            if not thing_props_list[1].find('a'):
                thing_props_list.insert(1, '<div></div>')
        except:
            ...
        try:
            if thing_props_list[2].find('a'):
                thing_props_list.insert(2, '<div></div>')
        except:
            ...
        try:
            if re.search(r'[0-9]+', str(thing_props_list[8])):
                thing_props_list.insert(8, '<div></div>')
        except:
            ...
        try:
            thing_props = BeautifulSoup(
                str(thing_props_list[-1]), "lxml").get_text()
            if not (re.match(r'[0-9]+', thing_props)):
                thing_props_list.insert(9, str(thing_props_list.pop()).strip())
        except:
            ...
        size_thing_list = []
        for size in thing_props_list[10:]:
            size_soup = BeautifulSoup(str(size), 'lxml')
            size_thing_list.append(size_soup.div.get_text())
        size_thing = '<div>' + ','.join(size_thing_list) + '</div>'
        thing_props_list[10:] = ''
        thing_props_list.append(size_thing)
        prop_str = ''
        index = 1
        for prop in thing_props_list:
            prop_soup = BeautifulSoup(str(prop), "lxml")
            try:
                prop_str += prop_soup.div.get_text().strip() + ';'
            except:
                print(index, prop)
            index += 1
        rows_csv.append((img_str + prop_str))
    return rows_csv


def parse_agat_77(sources_html_list):
    rows_csv = []
    for source in sources_html_list:
        soup = BeautifulSoup(source, "lxml")
        div_src_img = soup.find(
            class_={'d-item-gallery', 'info-block-content'})
        div_src_img = soup.find(
            class_={'d-item-gallery', 'info-block-content'})
        if div_src_img:
            link_img001_main = url_site + \
                str(div_src_img.contents[1]['href'])
        else:
            link_img001_main = ''
        if div_src_img and len(div_src_img.contents) >= 4:
            link_img002_second = url_site + \
                str(div_src_img.contents[3].a['href'])
        else:
            link_img002_second = ''
        if soup.find(class_={'d-item-descr'}):
            desc_busy = soup.find(
                class_={'d-item-descr'}).get_text(separator=u" ", strip=True)
        else:
            desc_busy = ''
        if soup.find(class_={'d-item-text'}):
            descr_material = soup.find(
                class_={'d-item-text'}).get_text(separator=u" ", strip=True)
        else:
            descr_material = ''
        desc_product = '%s %s' % (desc_busy, descr_material)
        if soup.find('h1'):
            name_product = soup.find('h1').get_text(
                separator=u" ", strip=True) + '.'
        else:
            name_product = 'None'
        if soup.find(class_={'d-item-price'}):
            desc_price = soup.find(
                class_={'d-item-price'}).get_text(separator=u" ", strip=True)
        else:
            desc_price = 'None'
        row_in_csv = '%s;%s;%s;%s;%s;%s;%s;' % (
            name_product, name_product, desc_product, desc_price, '', link_img001_main, link_img002_second)
        rows_csv.append(row_in_csv)
    return rows_csv
