import product_details
import product_head
import products_list

product_types = ['cpu', 'video-card', 'memory']
product_types = ['cpu']

for product_type in product_types:
    """ products_list.scrape(product_type)
    product_head.scrape(product_type) """
    product_details.scrape(product_type)