from bs4 import BeautifulSoup
import requests
import csv
from os import path, system, name
from time import sleep

part_info = ('Name', 'Price', 'Availability', 'Link')


def clear() -> None:
    # for windows
    if name == 'nt':
        system('cls')

    # for mac and linux(here, os.name is 'posix')
    else:
        system('clear')


def show_parts(the_list: list) -> None:
    if len(the_list) == 0:
        print("Nothing to show!")
        return

    len0 = len(f'({len(the_list)}) ')
    len1 = len(part_info[0])
    len2 = len(part_info[1])
    len3 = len(part_info[2])
    len4 = len(part_info[3])

    # if len(the_list) > 1:
    index = 0
    while index < len(the_list):
        if len1 < len(the_list[index][0]):
            len1 = len(the_list[index][0])

        if len2 < len(f'{the_list[index][1]:,.2f}'):
            len2 = len(f'{the_list[index][1]:,.2f}')

        if len3 < len(the_list[index][2]):
            len3 = len(the_list[index][2])

        if len4 < len(the_list[index][3]):
            len4 = len(the_list[index][3])

        index += 1
    print(' ' * len0 + '+' + '-' * (len1 + len2 + len3 + len4 + 11) + '+')
    print(' ' * len0 + '| '
          + part_info[0] + ' ' * (len1 - len(part_info[0])) + ' | '
          + part_info[1] + ' ' * (len2 - len(part_info[1])) + ' | '
          + part_info[2] + ' ' * (len3 - len(part_info[2])) + ' | '
          + part_info[3] + ' ' * (len4 - len(part_info[3])) + ' |')
    print(' ' * len0 + '+' + '-' * (len1 + len2 + len3 + len4 + 11) + '+')

    for index, (name, price, availability, link) in enumerate(the_list):
        print(f'({index + 1}) ' + ' ' * (len0 - len(f'({index + 1}) ')), sep='', end='| ')
        print(name + ' ' * (len1 - len(name)), sep='', end=' | ')
        print(f'{price:,.2f}' + ' ' * (len2 - len(f'{price:,.2f}')), sep='', end=' | ')
        print(availability + ' ' * (len3 - len(availability)), sep='', end=' | ')
        print(link + ' ' * (len4 - len(link)), sep='', end=' |')
        print()
    print(' ' * len0 + '+' + '-' * (len1 + len2 + len3 + len4 + 11) + '+')


def price_cleaner(price: str) -> float:
    cleaned = ''.join(c for c in price if c.isdigit() or c == '.')
    return float(cleaned)


def results_from_uptodate(name: str) -> list:
    found_products = []
    try:
        content = requests.get(f'https://uptodate.store/?category=0&s={name}&post_type=products')
        soup = BeautifulSoup(content.text, 'lxml')
    except requests.exceptions.ConnectionError as e:
        print(f"there was an error while getting the page")
        raise e

    products = soup.find_all('div', {'class': "products"})
    for product in products:
        website_name_content = product.find('h3', {'class': "name"})
        website_name = website_name_content.text
        link = website_name_content.find('a')['href']
        price = price_cleaner(product.select('div.product-price > :last-child')[0].text)
        if product.find('div', {'class': "tag out-stock"}) is not None:
            availability = "Out of Stock"
        else:
            availability = "In Stock"
        found_products.append((website_name, price, availability, link))

    return found_products


def results_from_maximumhardware(name: str) -> list:
    found_products = []
    try:
        content = requests.get(
            f'https://maximumhardware.store/index.php?category_id=0&search={name}&submit_search=&route=product%2Fsearch',
            headers={
                'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Mobile Safari/537.36'}
        )
        soup = BeautifulSoup(content.text, 'lxml')
    except requests.exceptions.ConnectionError as e:
        print(f"there was an error while getting the page")
        raise e

    products = soup.find_all('div', {'class': "product-layout"})
    for product in products:
        website_name_content = product.find('h4')
        website_name = website_name_content.text.strip()
        link = website_name_content.find('a')['href']
        price = price_cleaner(str(product.find('span', {'class': "price-new"}).text).strip())
        if product.find('div', {'class': "label-stock label label-success"}) is not None:
            availability = "Out of Stock"
        else:
            availability = "In Stock"
        found_products.append((website_name, price, availability, link))

    return found_products


def search_for(name: str) -> list:
    found_products = []

    looping = True
    while looping:
        try:
            found_products.extend(results_from_uptodate(name))
            found_products.extend(results_from_maximumhardware(name))
            looping = False
        except requests.exceptions.ConnectionError:
            while True:
                choice = input('Do you want to try again? (y/n): ')
                if choice == 'y' or choice == 'Y':
                    break
                elif choice == 'n' or choice == 'N':
                    raise ConnectionError
                else:
                    pass

    return found_products


def adding_parts(the_list: list) -> None:
    searching = True
    while searching:
        part = input("Enter the product name you want to search for: ").strip()
        try:
            results = search_for(part)
        except ConnectionError:
            return None

        if len(results) == 0:
            print("nothing was found!")

        # showing the options
        print("\nChoose (multiple choices are seperated by a comma ',') :")
        show_parts(results)
        print('\n(0) for none (and search for something else)')
        print('(q) to quit choosing')

        have_chosen = False
        while not have_chosen:
            choice = input('>')
            print()
            # analyzing the input
            if choice == 'q' or choice == 'Q':
                clear()
                return None
            elif choice == '0':
                break
            else:
                numbers = choice.split(',')
                for number in numbers:
                    # check if numeric
                    number = number.strip()
                    if number.isnumeric():
                        # check if option is in the list
                        if int(number) <= len(results):
                            # check for duplicates
                            if results[int(number) - 1] not in the_list:
                                the_list.append(results[int(number) - 1])
                                print("part added to the list")
                                have_chosen = True
                                searching = False
                                continue
                            else:
                                print(f"sorry, choice number {number} already exists")
                        else:
                            print(f"sorry, option {number} is not available")
                    else:
                        print("you typed something wrong")

                    # this will execute if anything wrong happened
                    print("\ntry again from previous list!")
                    have_chosen = False
                    searching = True
                    break
    sleep(2)
    clear()


def removing_parts(the_list: list) -> None:
    print("\nChoose what to remove (multiple choices are seperated by a comma ',') :")
    show_parts(the_list)
    print('(q) to quit removing')
    have_chosen = False
    while not have_chosen:
        choice = input('>').strip()
        print()
        # analyzing the input
        if choice == 'q' or choice == 'Q':
            break
        else:
            numbers = choice.split(',')
            for number in numbers:
                # check if numeric
                number = number.strip()
                if number.isnumeric():
                    # check if option is in the list
                    if int(number) <= len(the_list):
                        the_list[int(number) - 1] = None
                        print(f"part ({number}) removed from the list")
                        have_chosen = True
                        continue
                    else:
                        print(f"sorry, option {number} is not available")
                else:
                    print("you typed something wrong")
                # this will execute if anything wrong happened
                print("\ntry again from previous list!")
                have_chosen = False
                break

        index = len(the_list) - 1
        while index >= 0:
            if the_list[index] is None:
                del the_list[index]
            index -= 1
    sleep(2)
    clear()


def write_to_csv(the_list: list) -> None:
    if len(the_list) != 0:
        with open("products.csv", 'w') as file:
            writer = csv.writer(file)
            writer.writerow(the_list)
            for part in pc_parts:
                writer.writerow(part)
        print('file exported successfully as "products.csv"')
    else:
        print("Sorry, won't make the file because there's nothing in the list")


def read_from_csv(the_list: list) -> None:
    file_name = "products.csv"
    if path.isfile(file_name):
        print('we found "products.csv" file exists here')
        while True:
            choice = input('Do you want to import from it (y/n): ').strip()
            if choice == 'y' or choice == 'Y':
                break
            elif choice == 'n' or choice == 'N':
                file_name = input("Enter the destination of the file you want to import: ").strip()
                break
            else:
                pass
    else:
        file_name = input("Enter the destination of the file you want to import: ").strip()

    with open(file_name, 'r') as file:
        reader = csv.reader(file)
        next(reader)
        for index, line in enumerate(reader):
            # check if it is just 4 columns
            if len(line) == 4:
                # check if the price column is really price
                try:
                    line[1] = float(line[1])
                except ValueError:
                    print(f"sorry, row {index + 1} is bad (price not numeric)")
                    print("so not added")
                    continue
                # check if the 3rd column is really the availability
                if not (line[2] == "Out of Stock" or line[2] == "In Stock"):
                    print(f"sorry, row {index + 1} is bad (in column 3)")
                    print("so not added")
                    continue
                line = tuple(line)
                # adding only new elements
                if line not in the_list:
                    the_list.append(line)
                    print(line[0] + ": added")
                else:
                    print(line[0] + ": already existed")
            else:
                print("sorry, the file is corrupted (not 4 columns)")


if __name__ == '__main__':
    pc_parts = []

    clear()
    while True:
        if len(pc_parts) == 0:
            print("\n****choose what you want to do!****\n")
            print("(1) adding parts to the list")
            print("(2) importing from a CSV file")
            print("\n(q) to exit the program")
            option = input('>').strip()
            clear()
            if option == '1':
                adding_parts(pc_parts)
            elif option == '2':
                read_from_csv(pc_parts)
            elif option == 'q' or option == 'Q':
                break
            else:
                print("sorry, you typed something wrong")
        else:
            print("\n****choose what you want to do!****\n")
            print("(1) adding parts to the list")
            print("(2) removing parts from the list")
            print("(3) show all chosen products")
            print("(4) exporting to a CSV file")
            print("(5) importing from a CSV file")
            print("\n(q) to exit the program")
            option = input('>').strip()
            clear()
            if option == '1':
                adding_parts(pc_parts)
            elif option == '2':
                removing_parts(pc_parts)
            elif option == '3':
                show_parts(pc_parts)
            elif option == '4':
                write_to_csv(pc_parts)
            elif option == '5':
                read_from_csv(pc_parts)
            elif option == 'q' or option == 'Q':
                break
            else:
                print("sorry, you typed something wrong")
