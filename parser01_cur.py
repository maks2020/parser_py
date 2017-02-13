from bs4 import BeautifulSoup
import re

url_site = 'http://www.agat77.ru'
rows_csv = []
path_input_file = './result/figurki/output/html_figurki_1.parse'
path_output_file = path_input_file[:-6] + '.csv'

with open(path_input_file) as input_file:
    sources_html = input_file.read()
    sources_html_list = sources_html.split(';;;;;;;;;;;;;;;;;;;;')
    count = 1
    try:
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
            # print(row_in_csv)
            rows_csv.append(row_in_csv)
            with open(path_output_file, 'w') as output_file:
                output_file.write(
                    'артикул;наименование;описание;цена;размер;img;img;img;img;img;img;img;img;img;img\n')
                for row in rows_csv:
                    output_file.write(row + '\n')
                # with open('parser.log', 'a') as output_file:
                #     output_file.write(source + '\n' * 3 + '=' * 80 + '\n' *3)
            count += 1
    except:
        print('Exception in sourse: ' + str(sources_html_list.index(source)))
    print('Count: ' + str(count))
