import requests
import time
from selenium import webdriver
from pprint import pprint
import bs4
import site

url = "https://pcpartpicker.com/products/cpu/#page="
url = 'https://pcpartpicker.com/products/video-card/#page='
max_page = -1
csv_delimiter = ','


def scrape():

    browser = webdriver.Firefox()
    # browser.minimize_window()

    browser.get(url + str(1))
    time.sleep(5)
    page_content = browser.page_source
    soup = bs4.BeautifulSoup(page_content, 'html.parser')

    pages = soup.find('section', {'id': 'module-pagination'}).find_all('a')
    max_page = pages[len(pages) - 1].get_text()
    max_page = int(max_page)
    print('Number of pages to be scraped: ' + str(max_page))

    products_list_scraped = []
    for page in range(1, 6):
        browser.get(url + str(page))
        time.sleep(5)
        print('Scraping page: ' + str(page))
        page_content = browser.page_source
        soup = bs4.BeautifulSoup(page_content, 'html.parser')
        products_list_scraped += scrape_data(soup)

    csv = '\n'.join(products_list_scraped)

    browser.quit()

    csv_file = open('scraped_data/video-card.csv', 'w')
    csv_file.write(csv)
    csv_file.close()


def scrape_data(soup):
    table = soup.find('table', {'id': 'paginated_table'})
    products_list = table.find('tbody').find_all('tr')

    products_list_scraped = []

    for product in products_list:
        product_specs = product.find_all('td')
        product_specs.pop(0)  # removing the checkbox
        product_specs_array = []

        for spec in product_specs:
            remove_element(spec.find('div', {'class': 'td__rating'}))
            remove_element(spec.find('h6'))
            remove_element(spec.find('button'))

            product_specs_array.append(spec.get_text().strip())

        products_list_scraped.append(csv_delimiter.join(product_specs_array))
    return products_list_scraped


def remove_element(element):
    if (element is not None):
        element.decompose()


if __name__ == '__main__':
    scrape()
