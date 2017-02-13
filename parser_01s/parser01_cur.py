from bs4 import BeautifulSoup
import pickle
import os
import sys
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'
sys.path.append('../')

url_site = 'http://www.azbukamoda.ru'
rows_csv = []
# with open('sources_html_list.pickle', 'rb') as input_file:
with open('sources_html_list02.pickle', 'rb') as input_file:
  sources_html_list = pickle.load(input_file) 
  for source in sources_html_list:
    soup = BeautifulSoup(source, "lxml")
    img_src = soup.select('a[data-bigimagesrc]')
    path_number = soup.h1.string
    url_imgs_list = []
    for src in img_src:
      url_img = src.get('data-bigimagesrc')
      url_imgs_list.append(url_site + url_img)
      url_string = ''
    for url in url_imgs_list:
      url_string += '; ' + url
    path_number += url_string
    rows_csv.append(path_number)
    print(rows_csv)
with open('url02.csv','w') as output_file:
  for row in rows_csv:
    output_file.write(row + '\n')
