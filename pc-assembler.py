from bs4 import BeautifulSoup
import requests


def results_from_uptodate(name: str) -> list:
    found_products = []
    content = requests.get(f'https://uptodate.store/?category=0&s={name}&post_type=products').text
    soup = BeautifulSoup(content, 'lxml')
    products = soup.find_all('div', {'class': "products"})
    for product in products:
        website_name_content = product.find('h3', {'class': "name"})
        website_name = website_name_content.text
        link = website_name_content.find('a')['href']
        price = product.find('div', {'class': "product-price"}).text
        if product.find('div', {'class': "tag out-stock"}) != None:
            availability = "Out of Stock"
        else:
            availability = "In Stock"
        found_products.append((website_name, price, availability, link))

    return found_products


def results_from_maximumhardware(name: str) -> list:
    found_products = []
    content = requests.get(
        f'https://maximumhardware.store/index.php?category_id=0&search={name}&submit_search=&route=product%2Fsearch',
        headers={'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Mobile Safari/537.36'}
    )
    # print(content)
    # print(content.headers)
    # print(content.text)
    # with open("page.html", 'w') as html_file:
    #     print(str(content.text), file=html_file)

    soup = BeautifulSoup(content.text, 'lxml')
    print(soup)
    products = soup.find_all('div', {'class': "product-layout"})
    for product in products:
        website_name_content = product.find('h4')
        website_name = website_name_content.text.strip()
        link = website_name_content.find('a')['href']
        price = str(product.find('div', {'class': "price"}).text).strip()

        print(price)
        if product.find('div', {'class': "label-stock label label-success"}) is not None:
            availability = "Out of Stock"
        else:
            availability = "In Stock"
        found_products.append((website_name, price, availability, link))

    return found_products
    # return [('i3 10100', '1900', 'out of stock', "www.somewebsite2.com")]


def search_for(name: str) -> list:
    found_products = []
    found_products.extend(results_from_uptodate(name))
    found_products.extend(results_from_maximumhardware(name))
    return found_products


part_info = ('name', 'price', 'availability', 'link')
pc_parts = []
if __name__ == '__main__':
    print('')

    # choices
    # 1- adding parts to the list
    # 2- removing parts from the list
    # 3- show all chosen products
    #   1.show only in stock
    # 4- exporting to CSV file

    # (1) adding parts to the list
    part = input("Enter the product name you want to search for: ")

    results = search_for(part)

    print("choose:")
    for index, result in enumerate(results):
        print(f'({index + 1}) {result}')
    print('(0) for none')
    choice = int(input('>'))
    # todo type check
    if choice != 0:
        pc_parts.append(results[choice - 1])
    print(pc_parts)

