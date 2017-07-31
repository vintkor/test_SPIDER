from bs4 import BeautifulSoup
from requests import request
import csv
from multiprocessing import Pool
import time


BASE_URL = 'http://www.strojmag.ua/'
URL = '/catalog/otdelochnye-materialy/stroitelnye_smesi/?PAGEN_1={}'
items = []
count = 0


def save_csv(items):
    print('================================ Saving ================================')
    print(items)
    with open('items.csv', 'w', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['link', 'title', 'price', 'image', 'description'])
        for item in items:
            writer.writerow([
                item['link'],
                item['title'],
                item['price'],
                item['image'],
                item['description']
            ])


def get_html(url):
    return request('get', url).text


def get_single_product_info(link):
    response = get_html(link)
    soup = BeautifulSoup(response, 'html.parser')
    try:
        product_name = soup.find('h1', {'class': 'product-title'}).text.strip()
    except:
        product_name = 'Product name is not find'

    try:
        product_image = soup.find('img', {'class': 'eshop_image_click'})['src']
    except:
        product_image = 'Product image is not find'

    try:
        product_price = soup.find('div', {'class': 'product-price-result'})\
            .find('nobr')\
            .text.strip()\
            .split('Розничная цена:')[1]\
            .split('грн.')[0].strip()
    except:
        product_price = 'Product price is not find'

    try:
        product_description = soup.find('div', {'class': 'description'}).text.strip()
    except:
        product_description = 'Product description is not find'

    print(product_name, product_image, product_price)

    items.append({
        'link': link,
        'title': product_name,
        'price': product_price,
        'image': product_image,
        'description': product_description
    })


def get_products_in_category(category_link, category_name):
    print('================================', category_name, '================================')
    response = get_html(category_link)
    soup = BeautifulSoup(response, 'html.parser')
    products = soup.find_all('div', {'class': 'eshop_list_item_row'})
    product__super_link = []

    for product in products:
        try:
            product_link = BASE_URL + product.find('a', {'class': 'name'})['href']
            product__super_link.append(product_link)
        except:
            product_link = 'Not find product link'

    with Pool(5) as p:
        p.map(get_single_product_info, product__super_link)

    # for product in products:
    #     try:
    #         product_link = BASE_URL + product.find('a', {'class': 'name'})['href']
    #         get_single_product_info(product_link, category_name)
    #     except:
    #         product_link = 'Not find product link'

    # try:
    #     pages = soup.find_all('a', {'class': 'pager_block'})
    # except:
    #     pages = None
    #
    # if pages:
    #     for page in pages:
    #         product_page_response = get_html(BASE_URL + page['href'])
    #         page_soup = BeautifulSoup(product_page_response, 'html.parser')
    #         products = page_soup.find_all('div', {'class': 'eshop_list_item_row'})
    #         for product in products:
    #             try:
    #                 product_link = BASE_URL + product.find('a', {'class': 'name'})['href']
    #                 get_single_product_info(product_link, category_name)
    #             except:
    #                 product_link = 'Not find product link'


def get_categories(nav_link):
    for item in nav_link:
        try:
            category_name = item.find('li').find('a').text
        except:
            category_name = '---'
        try:
            category_link = item.find('li').find('a')['href']
        except:
            category_link = '---'
        get_products_in_category(category_link, category_name)


def start():
    response = get_html(BASE_URL)
    soup = BeautifulSoup(response, 'html.parser')
    nav = soup.find_all('ul', {'class': 'menu_catalog_item_2'})
    get_categories(nav)


if __name__ == "__main__":
    print('=== START ===', time.strftime('%H-%M-%S'))
    # with Pool(200) as p:
    #     p.apply(start)
    get_products_in_category('http://www.strojmag.ua/katalog/ruchnoj_instrument/specodezhda', 'Гипсокартон, профиль')
    # get_single_product_info('http://www.strojmag.ua/katalog/krovelnye-materialy/evroshifer-ondulin/list-ondulin-2x095-m-krasnyj', 'Крепления')
    save_csv(items)
    print('=== FINISH ===', time.strftime('%H-%M-%S'))
