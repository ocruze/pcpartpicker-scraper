import requests
import time
from selenium import webdriver
from pprint import pprint
import bs4
import site


base_url = 'https://pcpartpicker.com'
head_filename_suffix = '-head.csv'
list_filename_suffix = '-list.csv'


def scrape(product_type):
    browser = webdriver.Firefox()
    browser.minimize_window()

    filepath = 'scraped_data/' + product_type + list_filename_suffix
    file = open(filepath, 'r')
    product_list = file.read().split('\n')
    file.close()

    browser.get(base_url + '/product/' + product_list[0])
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
    filepath = 'scraped_data/' + product_type + head_filename_suffix
    file = open(filepath, 'w')
    file.write(data)
    file.close()

def normalize(header):
    header = header.lower()
    header = remove_unwanted_characters(header, ['/', '#'])
    header = header.strip()
    header = header.replace(' ', '_')

    return header

def remove_unwanted_characters(text, characters_list):
    for charac in characters_list:
        text = text.replace(charac, '')
    return text