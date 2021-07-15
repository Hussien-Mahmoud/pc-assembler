def results_from_uptodate(name: str) -> list:


def results_from_maximumhardware(name: str) -> list:


def search_for(name: str) -> list:
    found_products = []
    found_products.extend(results_from_uptodate(name))
    found_products.extend(results_from_maximumhardware(name))


pc_parts = []
if __name__ == '__main__':
    print('')

    part = input("Enter the product name you want to search for: ")
    pc_parts.append(part)

    results = search_for(part)

    # print("we found:")
    # for result in results:
    # 	print(f'{result} for ...')

    # save in a csv file
