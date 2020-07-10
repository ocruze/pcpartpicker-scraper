import requests
import time
from selenium import webdriver
from pprint import pprint
import bs4
import site

base_url = 'https://pcpartpicker.com'
max_page = -1
product_type_filename_suffix = '.csv'


def scrape(product_type):
    browser = webdriver.Firefox()
    browser.minimize_window()

    browser.get(base_url + '/product/' + product_type + '/#page=' + str(1))
    time.sleep(5)
    page_content = browser.page_source
    soup = bs4.BeautifulSoup(page_content, 'html.parser')

    


if __name__ == '__main__':
    product_types = ['cpu', 'video-card', 'memory']

    for product_type in product_types:
        scrape(product_type)
