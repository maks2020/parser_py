import re

url_first = 'http://www.azbukamoda.ru/catalog/muzhchinam/odezhda_1/futbolki_i_mayki/'
url_last = 'http://www.agat77.ru/catalog/busy/?&PAGEN_1=2&AJAX_PAGE=Y'

def url_list_make(url_first, url_last):
    """make list of url pages"""
    data_url = url_last.split('/') # last url in list
    for item in data_url:
        if re.search(r'[?]*&*[PAGE]*N_*[0-9]*=[0-9]*&*', item):
            p = re.search(r'[?]*&*[PAGE]*N_*[0-9]*=[0-9]*&*', item)
            str_01 = p.group()
            print(str_01[2:-1])
  # page_url_last_list = list(data_url.pop()) # take last element url PAGEN_1=XXX and convert in list
  # page_url_last_rev = reversed(page_url_last_list) # reverse list
  # num_page_rev = [] #define result list with last number page in reverse form 
  # for simb in page_url_last_rev: #passed on list  and get result last number page in format page
  #   if simb != '=':
  #     num_page_rev += simb
  #   else:
  #     break
  #   page_url_last_list.pop() #delete PAGEN_1=XXX from XXX
  # num_pages = int(''.join(reversed(num_page_rev))) #list-->string-->integer
  # urls_list = [] # add list for list urls
  # urls_list.append(url_first) # add url first page 
  # for num_page in range(2, num_pages + 1): # make list urls for scraped
  #   url_full = '/'.join(data_url) + '/' + ''.join(page_url_last_list) + \
  #   str(num_page) # concat url pages catalog 
  #   urls_list.append(url_full) #append url page in list
  # return urls_list
url_list_make(url_first, url_last)
