from bs4 import BeautifulSoup
import re
import pickle

config_parse = {}
with open('./result/kotmarkot_boys/config_kotmarkot_boys.pickle', 'rb') as input_file:
    config_parse = pickle.load(input_file)

num_file_parse = 1
path_output = config_parse['path_output_file']
name_html = config_parse['name_html']
path_input_file = (path_output + 'html_' + name_html + '_' + str(num_file_parse) + '.parse')

rows_csv = []
path_output_file = path_input_file[:-6] + '.csv'

with open(path_input_file) as input_file:
    sources_html = input_file.read()
    sources_html_list = sources_html.split(';;;;;;;;;;;;;;;;;;;;')
    count = 1
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
            thing_props = BeautifulSoup(str(thing_props_list[-1]), "lxml").get_text()
            if not (re.match(r'[0-9]+', thing_props)):
                thing_props_list.insert(9, str(thing_props_list.pop()).strip()) 
        except:
            ...
        # try:
        #     print(thing_props_list[9])
        # except:
        #     ...

        size_thing_list = []
        for size in thing_props_list[10:]:
            size_soup = BeautifulSoup(str(size), 'lxml')
            size_thing_list.append(size_soup.div.get_text())
        size_thing ='<div>' + ','.join(size_thing_list) + '</div>'
        thing_props_list[10:] = ''
        thing_props_list.append(size_thing)
        print(thing_props_list)


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
with open(path_output_file, 'w') as output_file:
    # output_file.write(
    #     'артикул;наименование;описание;цена;размер;img;img;img;img;img;img;img;img;img;img\n')
    for row in rows_csv:
        output_file.write(row + '\n')
    # with open('parser.log', 'a') as output_file:
    #     output_file.write(source + '\n' * 3 + '=' * 80 + '\n' *3)
count += 1

    #     print('Exception in sourse: ' + str(sources_html_list.index(source)))
    # print('Count: ' + str(count))

