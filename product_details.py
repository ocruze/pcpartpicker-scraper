import requests
import time
from selenium import webdriver
from pprint import pprint
import bs4
import site
import constants
import re


def scrape(product_type):
    browser = webdriver.Firefox()
    browser.minimize_window()

    filepath = constants.dir_scrape_data + '/' + product_type + constants.list_filename_suffix
    file = open(filepath, 'r')
    product_list = file.read().split('\n')
    file.close()

    filepath = constants.dir_scrape_data + '/' + product_type + constants.head_filename_suffix
    file = open(filepath, 'r')
    headers = file.read().split('\n')
    file.close()

    product_details_list = [constants.csv_delimiter.join(headers)]

    for product_id in product_list:
        browser.get(constants.base_url + '/product/' + product_id)
        time.sleep(5)
        page_content = browser.page_source
        soup = bs4.BeautifulSoup(page_content, 'html.parser')

        product_details_list.append(constants.csv_delimiter.join(scrape_details(soup, product_id)))

    browser.quit()

    data = '\n'.join(product_details_list)
    filepath = constants.dir_scrape_data + '/' + \
        product_type + constants.specs_filename_suffix
    file = open(filepath, 'w')
    file.write(data)
    file.close()


def scrape_details(soup, product_id):
    specs = soup.find('div', {'class': 'specs'})
    specs = specs.find_all('div', {'class': 'group__content'})

    details = []
    for spec in specs:
        text = ''
        ul = spec.find('ul')
        if ul:
            li = ul.find_all('li')
            bulleted_line = ''
            for l in li:
                bulleted_line += l.get_text()
            text = bulleted_line
        else:
            text = spec.find('p').get_text()
        details.append(normalize_text(text))

    return details


def normalize_text(text):
    text = text.strip()
    text = re.sub(' +', ' ', text)
    text = text.replace('\n', '')

    return text
