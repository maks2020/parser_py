from bs4 import BeautifulSoup
import re

url_site = 'http://www.agat77.ru'
name_parse = 'figurki'
path_dir_source = './result/'
path_input_file = (path_dir_source + name_parse +
                   '/input/' + 'html_' + name_parse + '.txt')
path_output_file = (path_dir_source + name_parse +
                    '/input/' + 'thing_url_' + name_parse + '.txt')

def make_url_things_list(sources_html):
    soup = BeautifulSoup(sources_html, "lxml")
    things_list = soup.find_all('a', class_='catalog-list-title')
    url_things_list = []
    url_things_list = [(url_site + thing.get('href')) for thing in things_list 
                        if (url_site + thing.get('href')) not in url_things_list]
    return url_things_list


with open(path_input_file) as input_data:
    url_things_list = make_url_things_list(str(input_data.readlines()))
    with open(path_output_file, 'w') as output_url_list:
        count = 1
        for item in url_things_list:
            output_url_list.write(item + ' ' + '\n')
            count += 1
