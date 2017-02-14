from bs4 import BeautifulSoup
import re
import pickle

config_parse = {}
with open('./result/kotmorkot_girl/config_kotmorkot_girl.pickle', 'rb') as input_file:
    config_parse = pickle.load(input_file)
url_site = config_parse['url_site']
url_first = config_parse['url_first']
name_html = config_parse['name_html']
catalog_results = config_parse['catalog_results']
cat_file_html = config_parse['cat_file_html']
path_things_url_file = config_parse['path_things_url_file'] = config_parse['path_output_file'] + 'thing_url_' + name_html + '.txt'
name_data_file = config_parse['name_data_file']


def make_url_things_list(sources_html):
    soup = BeautifulSoup(sources_html, "lxml")
    # things_list = soup.find_all('a', class_='catalog-list-title')
    things_list = soup.select('.images a')
    url_things_list = []
    # url_things_list = [(url_site + thing.get('href')) for thing in things_list 
                        # (url_site + thing.get('href')) not in url_things_list]
    for thing in things_list:
        if (url_site + thing.get('href')) not in url_things_list:
            url_things_list.append((url_site + thing.get('href')))
        else:
            pass
    return url_things_list


with open(cat_file_html) as input_data:
    url_things_list = make_url_things_list(str(input_data.readlines()))
    with open(path_things_url_file, 'w') as output_file:
        count = 1
        for item in url_things_list:
            output_file.write(item + ' ' + '\n')
            count += 1

with open(name_data_file, 'wb') as output_file:
    pickle.dump(config_parse, output_file)


