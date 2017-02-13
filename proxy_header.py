# from browsermobproxy import Server
# from selenium import webdriver
# BROWSERMOB_PROXY_PATH = '/Users/mas/Desktop/my_python/py3x/parser01/env/bin/browsermob-proxy/bin/browsermob-proxy.bat'
# url = 'http://www.taofli.ru'

# server = Server(BROWSERMOB_PROXY_PATH)
# server.start()
# proxy = server.create_proxy()
# PHANTOMJS_PATH = './phantomjs'
# browser = webdriver.PhantomJS(PHANTOMJS_PATH)
# #browser.set_proxy(proxy.selenium_proxy())
# proxy_address = "--proxy=127.0.0.1:8080" # % proxy.port
# service_args = [ proxy_address, '--ignore-ssl-errors=yes', ] #so that i can do https connections
# browser = webdriver.PhantomJS(PHANTOMJS_PATH, service_args=service_args)
# proxy.new_har(url, options={'captureHeaders': True})
# browser.get(url)
# file_info = open("file_info.har", "w") # returns a HAR JSON blob
# file_info.write(str(proxy.har))
# file_info.close()
# browser.quit()
# server.stop()

def proxyFirefox(ref_har, url, path_browsermob_proxy="/Users/mas/Desktop/my_python/py3x/parser01/env/bin/browsermob-proxy/bin/browsermob-proxy.bat", path_geckodriver='/Users/mas/Desktop/my_python/py3x/parser01/env/bin'):
  from browsermobproxy import Server

  server = Server(path_browsermob_proxy)
  server.start()
  proxy = server.create_proxy()

  from selenium import webdriver
  PATH_GECKO_DRIVER = path_geckodriver
  profile  = webdriver.FirefoxProfile(PATH_GECKO_DRIVER)
  profile.set_proxy(proxy.selenium_proxy())
  driver = webdriver.Firefox(firefox_profile=profile)
  proxy.new_har(ref_har, options={'captureHeaders': True})
  driver.get(url)

  
  import json
  file_info = open("file_info.json", "w") # returns a HAR JSON blob
  # file_info.write(str(proxy.har))
  json.dump(str(proxy.har), file_info)
  file_info.close()
  driver.quit()
  server.stop()

link_t= 'http://www.taofli.ru'
name_har = 'taofli'
proxyFirefox(name_har, link_t)


