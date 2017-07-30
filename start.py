from bs4 import BeautifulSoup
from requests import request
import csv
from multiprocessing import Pool


BASE_URL = 'http://www.strojmag.ua/'
URL = '/catalog/otdelochnye-materialy/stroitelnye_smesi/?PAGEN_1={}'
items = []


def save_csv(items):
    with open('items.csv', 'w', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['title', 'price', 'image', 'link'])
        for item in items:
            writer.writerow([item['title'], item['price'], item['image'], item['link']])


def get_html(url):
    return request('get', url).text


def get_products_in_category(category_link, category_name):
    response = get_html(category_link)
    soup = BeautifulSoup(response, 'html.parser')
    products = soup.find_all('div', {'class': 'eshop_list_item_row'})
    pages = soup.find_all('a', {'class': 'pager_block'})
    for page in pages:
        print(page['href'])

    for product in products:
        try:
            product_link = BASE_URL + product.find('a', {'class': 'name'})['href']
        except:
            product_link = 'Not find product link'
        # print(product_link)


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
    # with Pool(70) as p:
    #     p.apply(start)
    get_products_in_category('http://www.strojmag.ua/katalog/gipsokarton-i-komplektujuschie', 'Гипсокартон, профиль')
