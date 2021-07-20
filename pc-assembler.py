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
        if product.find('div', {'class': "tag out-stock"}) is not None:
            availability = "Out of Stock"
        else:
            availability = "In Stock"
        found_products.append((website_name, price, availability, link))

    return found_products


def results_from_maximumhardware(name: str) -> list:
    found_products = []
    content = requests.get(
        f'https://maximumhardware.store/index.php?category_id=0&search={name}&submit_search=&route=product%2Fsearch',
        headers={
            'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Mobile Safari/537.36'}
    )

    soup = BeautifulSoup(content.text, 'lxml')
    products = soup.find_all('div', {'class': "product-layout"})
    for product in products:
        website_name_content = product.find('h4')
        website_name = website_name_content.text.strip()
        link = website_name_content.find('a')['href']
        price = str(product.find('div', {'class': "price"}).text).strip()
        if product.find('div', {'class': "label-stock label label-success"}) is not None:
            availability = "Out of Stock"
        else:
            availability = "In Stock"
        found_products.append((website_name, price, availability, link))

    return found_products


def search_for(name: str) -> list:
    found_products = []
    found_products.extend(results_from_uptodate(name))
    found_products.extend(results_from_maximumhardware(name))
    return found_products


def adding_parts(the_list: list) -> None:
    searching = True
    while searching:
        part = input("Enter the product name you want to search for: ")
        results = search_for(part)
        if len(results) == 0:
            print("nothing was found!")

        # showing the options
        print("choose (multiple choices are seperated by a comma ','):")
        for index, result in enumerate(results):
            print(f'({index + 1}) {result}')
        print('\n(0) for none (and search for something else)')
        print('(q) to quit choosing')

        have_chosen = False
        while not have_chosen:
            choice = input('>')
            print()
            # analyzing the input
            if choice == 'q' or choice == 'Q':
                searching = False
                break
            elif choice == '0':
                break
            else:
                numbers = choice.split(',')
                for number in numbers:
                    if number.isnumeric():
                        if int(number) < len(results) + 1:
                            the_list.append(results[int(number) - 1])
                            print("part added to the list")
                            have_chosen = True
                            searching = False
                            continue
                        else:
                            print(f"sorry, option {number} is not available")
                            have_chosen = False
                            searching = True
                            break
                    else:
                        print("you typed something wrong")
                        have_chosen = False
                        searching = True
                        break
                print("\ntry again from previous list!")


part_info = ('name', 'price', 'availability', 'link')
if __name__ == '__main__':
    pc_parts = []

    # choices
    # 1- adding parts to the list
    # 2- removing parts from the list
    # 3- show all chosen products
    #   1.show only in stock
    # 4- exporting to CSV file
    while True:
        if len(pc_parts) == 0:
            adding_parts(pc_parts)
        else:
            print("choose what you want to do!\n")
            print("(1) adding parts to the list")
            print("(2) removing parts from the list")
            print("(3) show all chosen products")
            print("(4) exporting to a CSV file")
            print("(q) to exit the program")
            option = input('>')
            if option == '1':
                adding_parts()
            elif option == '2':
                pass
            elif option == '3':
                pass
            elif option == '4':
                pass
            elif option == 'q' or option == 'Q':
                break
            else:
                print("sorry, you typed something wrong")
    print(pc_parts)
