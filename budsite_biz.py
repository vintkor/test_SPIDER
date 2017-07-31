from bs4 import BeautifulSoup
from requests import request
import csv
from multiprocessing import Pool
from datetime import datetime
from random import randint


base_url = 'https://budsite.biz/'
url = 'g13693777-vodostochnye-sistemy'
filename = 'vodostochnye-sistemy.csv'
total_page = 11
count_pools = 10

with open(filename, 'w', encoding='utf-8') as file:
    start_writer = csv.writer(file)
    start_writer.writerow([
        'Название_позиции', 'Ключевые_слова', 'Описание', 'Тип_товара', 'Цена', 'Валюта',
        'Единица_измерения', 'Ссылка_изображения', 'Наличие', 'Идентификатор_товара'
    ])


def get_html(url_):
    return request('get', url_).text


def start_parse(base_url_, url_):
    product_links = []
    for page in range(1, total_page+1):
        print('-'*60, 'start_parse page -', page, '-'*60)
        html = get_html(base_url_ + url_ + '/page_{}'.format(page))
        soup = BeautifulSoup(html, 'html.parser')
        products = soup.find_all('li', {'class': 'js-rtb-partner'})
        for product in products:
            product_links.append(product.find('a', {'class': 'b-product-gallery__image-link'})['href'])
    return product_links


def get_single_product(product_link):
    print(product_link)
    html = get_html(product_link)
    soup = BeautifulSoup(html, 'html.parser')
    try:
        title = soup.find('div', {'class': 'b-breadcrumb__current'}).text.strip()
    except:
        title = 'Title not found'

    try:
        category = soup.find_all('div', {'class': 'b-breadcrumb__item'})[-1].find('a', {'class': 'b-breadcrumb__link '}).text.strip()
    except:
        category = 'Category not found'

    try:
        price = soup.find('p', {'class': 'b-product-cost__price'}).find('span', {'itemprop': 'price'}).text.strip()
    except:
        price = ''

    try:
        currency = soup.find('p', {'class': 'b-product-cost__price'}).find('span', {'class': 'notranslate'})['content']
    except:
        currency = ''

    try:
        description = soup.find('div', {'data-qaid': 'product_description'})
        for a in description.find_all('a'):
            a.replace_with(' ---')
    except:
        description = ''

    try:
        image = soup.find('div', {'class': 'b-product-view__zoom-box'})['data-imagezoom-url']
    except:
        image = ''

    with open(filename, 'a', encoding='utf-8') as new_file:
        end_writer = csv.writer(new_file)
        end_writer.writerow([
            title, category, description, 'u', price, currency,
            'шт', image, '+', randint(0, 1000000000)
        ])


if __name__ == '__main__':
    time_start = datetime.now()
    links = start_parse(base_url, url)
    with Pool(count_pools) as p:
        p.map(get_single_product, links)
    # get_single_product('https://budsite.biz/p347436652-derevyannaya-trehsektsionnaya-cherdachnaya.html')
    time_end = datetime.now()
    print('-'*60, str(time_end - time_start), '-'*60)
