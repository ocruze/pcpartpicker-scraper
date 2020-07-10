import requests
import time
from selenium import webdriver
from pprint import pprint
import bs4
import site

base_url = 'https://pcpartpicker.com'
max_page = -1
list_filename_suffix = '-list.csv'


def scrape(product_type):

    browser = webdriver.Firefox()
    browser.minimize_window()

    browser.get(base_url + '/products/' + product_type + '/#page=' + str(1))
    time.sleep(5)
    page_content = browser.page_source
    soup = bs4.BeautifulSoup(page_content, 'html.parser')

    pages = soup.find('section', {'id': 'module-pagination'}).find_all('a')
    max_page = pages[len(pages) - 1].get_text()
    max_page = int(max_page)
    print('Scraping product type: ' + product_type)
    print('Number of pages to be scraped: ' + str(max_page))

    products_list_scraped = []
    for page in range(1, 3):
        browser.get(base_url + '/products/' +
                    product_type + '/#page=' + str(page))
        time.sleep(5)
        print('Scraping page: ' + str(page))
        page_content = browser.page_source
        soup = bs4.BeautifulSoup(page_content, 'html.parser')
        products_list_scraped += scrape_products_list(soup)

    csv = '\n'.join(products_list_scraped)

    browser.quit()

    csv_file = open('scraped_data/' + product_type + list_filename_suffix, 'w')
    csv_file.write(csv)
    csv_file.close()


def scrape_products_list(soup):
    table = soup.find('table', {'id': 'paginated_table'})
    products_list = table.find('tbody').find_all('tr')

    product_codes = []

    for product in products_list:
        a = product.find('td', {'class': 'td__name'}).find('a')
        link = a['href']

        product_codes.append(link.split('/')[2])
    return product_codes


def remove_element(element):
    if (element is not None):
        element.decompose()
