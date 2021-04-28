import time

from selenium import webdriver

chromedriver = r"G:\mayur photo\mini project\chromedriver.exe"
driver = webdriver.Chrome(chromedriver)

driver.get('http://127.0.0.1:8000/')

time.sleep(4)
driver.find_elements_by_name('userid')[0].clear()
driver.find_elements_by_name('userid')[0].send_keys('robo')
driver.find_elements_by_name('password')[0].clear()
driver.find_elements_by_name('password')[0].send_keys('robo')
time.sleep(1)
driver.find_elements_by_name('submit')[0].click()

time.sleep(4)
driver.find_elements_by_name('gggg')[0].click()
time.sleep(4)
driver.get('http://www.google.com/')
driver.close()