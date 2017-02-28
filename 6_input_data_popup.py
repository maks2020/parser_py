from selenium import webdriver
from bs4 import BeautifulSoup
import getpass
import time
import math

from parser_01s.mod_parse import parse_shilco_sport_v3
from parser_01s.utils import read_config

def get_html_with_login_2(data_prod_list):
    """get html code from source and make output file with login"""
    # # path_geckodriver='./parser01/env/bin'
    print(len(data_prod_list))
    start_pos = input('Input number start position: ')
    url_login_page = 'http://example.ru/'
    path_geckodriver='./parser01/env/bin/chromedriver'
    # # PHANTOMJS_PATH = './phantomjs'
    # # browser = webdriver.Firefox(path_geckodriver)
    browser = webdriver.Chrome(path_geckodriver)
    # # browser = webdriver.PhantomJS(PHANTOMJS_PATH)
    # get page with login and password input
    browser.get(url_login_page)
    # search form input login, password, button input
    login_user = browser.find_element_by_id('id_username')
    passwd_user = browser.find_element_by_id('id_password')
    submit_b = browser.find_element_by_xpath(
        '//*[@id="login-form"]/div[3]/span/input')
    # input and send login and password
    login_value = input('Input login for site: ')
    passwd_value = getpass.getpass('Input password for site: ')
    login_user.send_keys(login_value)
    passwd_user.send_keys(passwd_value)
    url_get = input('Inter url catalog: ')
    time.sleep(1)
    # click on button submit
    submit_b.submit()
    browser.get(url_get)
    print("=== Login OK ===")
    time.sleep(10)
    for count_data, data_prod in enumerate(data_prods_list[int(start_pos) - 1:]):
        # data_prod = data_prods_list[5]
        name_prod = data_prod[0]
        num_prod = data_prod[1]
        desc_prod = data_prod[2].replace('&nbsp', ' ')
        define_color = data_prod[3]
        try:
            price_thing = math.ceil(int(data_prod[4][:-5].replace(' ', '')) * 1.15)
        except:
            price_thing = 0
        sizes_list = data_prod[5]
        print(sizes_list)
        thing_color_size_height = data_prod[6]
        img_url_list= data_prod[7]
        print(img_url_list)
        submit_trigger_popup = browser.find_element_by_xpath('//*[@id="tabs-1"]/form/div[18]/a')
        # submit_trigger_popup = browser.find_element_by_link_text('Добавить новый ряд')
        submit_trigger_popup.click()
        time.sleep(3)
        for handle in browser.window_handles:
            browser.switch_to_window(handle)
        lead = browser.find_elements_by_tag_name('iframe')[1]
        # print(lead)
        browser.switch_to_frame(lead)
        # source_html = browser.page_source
        # soup = BeautifulSoup(source_html, 'lxml')
        # print(soup.prettify())
        el_body = browser.find_element_by_id('tinymce')
        el_body.send_keys(thing_color_size_height)
        browser.switch_to_default_content()
        for handle in browser.window_handles:
            browser.switch_to_window(handle)
        field_prod_name = browser.find_element_by_css_selector('form#row_form > div.formBox > div.i-text > input#id_name')
        field_prod_desc_1 = browser.find_element_by_css_selector('form#row_form > div.formBox > div.i-text > input#id_field2')
        field_prod_name.send_keys(name_prod)
        field_prod_desc_1.send_keys(desc_prod)
        if len(sizes_list) > 1:
            items = len(sizes_list)
            submit_add_size = browser.find_element_by_xpath('//*[@id="row_form"]/div[11]/a')
            for item in range(1, items):
                submit_add_size.click()
            for index, size in enumerate(sizes_list):
                field_prod_path_num = browser.find_element_by_xpath('//*[@id="id_item_set-%s-article"]' % index)
                field_prod_size = browser.find_element_by_xpath('//*[@id="id_item_set-%s-size"]' % index)
                field_prod_price = browser.find_element_by_xpath('//*[@id="id_item_set-%s-price"]' % index)
                field_prod_path_num.send_keys(num_prod)
                field_prod_size.send_keys(size)
                field_prod_price.send_keys(price_thing)
        else:
            for index, size in enumerate(sizes_list):
                field_prod_path_num = browser.find_element_by_xpath('//*[@id="id_item_set-%s-article"]' % index)
                field_prod_size = browser.find_element_by_xpath('//*[@id="id_item_set-%s-size"]' % index)
                field_prod_price = browser.find_element_by_xpath('//*[@id="id_item_set-%s-price"]' % index)
                field_prod_path_num.send_keys(num_prod)
                field_prod_size.send_keys(size)
                field_prod_price.send_keys(price_thing)
        submit_save_data = browser.find_element_by_xpath('//*[@id="row_form"]/div[13]/span/input')
        # submit_save_data = browser.find_element_by_xpath('//*[@id="row_form"]/div[14]/span/input')
        submit_save_data.click()
        browser.switch_to_default_content()
        time.sleep(3)
        # try:
        submit_popup_img_list = browser.find_elements_by_class_name('ico-video')
        # submit_popup_img_list[int(start_pos) - 1 + count_data].click()//*[@id="row31492975"]/td[6]/a
        #submit_popup_img_list[-1].click()
        submit_popup_img_list[0].click()
        time.sleep(3)
        for handle in browser.window_handles:
            browser.switch_to_window(handle)
        url_img_fields_list = browser.find_elements_by_xpath('//*[@id="images_url"]/input')
        if len(img_url_list) > len(url_img_fields_list):
            add_field_url = browser.find_element_by_xpath('//*[@id="image_form"]/div[7]/a')
            diff_len = len(img_url_list) - len(url_img_fields_list)
            for item in range(1, diff_len):
                add_field_url.click()
        url_img_fields_list = browser.find_elements_by_xpath('//*[@id="images_url"]/input')
        for url, field in zip(img_url_list, url_img_fields_list):
            field.send_keys(url)
        time.sleep(1)
        submit_add_url_img = browser.find_element_by_xpath('//*[@id="image_form"]/div[9]/span/input')
        submit_add_url_img.click()
        time.sleep(1)
    print('=== Done ===')

config_parse = {}
# read data project
config_parse = read_config()
num_file_parse = 1 # number file parse
path_output = config_parse['path_output_file']
name_html = config_parse['name_html']
url_site = config_parse['url_site']
path_input_file = (
    path_output + 'html_' + name_html + '_' + str(num_file_parse) + '.parse')

# read source code html for pages
sources_html_list = []
with open(path_input_file) as input_file:
    sources_html_list = input_file.read().split(';;;;;;;;;;;;;;;;;;;;')[:-1]

data_prods_list = parse_shilco_sport_v3(sources_html_list, url_site)
get_html_with_login_2(data_prods_list)


