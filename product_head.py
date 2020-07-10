import requests
import time
from selenium import webdriver
from pprint import pprint
import bs4
import site
import re
import constants


def scrape(product_type):
    browser = webdriver.Firefox()
    browser.minimize_window()

    filepath = 'scraped_data/' + product_type + constants.list_filename_suffix
    file = open(filepath, 'r')
    product_list = file.read().split('\n')
    file.close()

    browser.get(constants.base_url + '/product/' + product_list[0])
    time.sleep(5)
    page_content = browser.page_source
    soup = bs4.BeautifulSoup(page_content, 'html.parser')
    browser.quit()

    specs = soup.find('div', {'class': 'specs'})
    headers = specs.find_all('h3')

    headers_list = []
    for header in headers:
        headers_list.append(normalize(header.get_text()))

    data = '\n'.join(headers_list)
    filepath = 'scraped_data/' + product_type + constants.head_filename_suffix
    file = open(filepath, 'w')
    file.write(data)
    file.close()


def normalize(header):
    header = header.lower()
    header = remove_unwanted_characters(header, ['/', '#'])
    header = header.strip()
    header = re.sub(' +', ' ', header)
    header = header.replace(' ', '_')
    header = header.replace('-', '_')

    return header


def remove_unwanted_characters(text, characters_list):
    for charac in characters_list:
        text = text.replace(charac, '')
    return text
