import requests
from bs4 import BeautifulSoup
import json
import aiohttp
import asyncio
import pandas as pd

LINK = 'https://weedmaps.com/deliveries/bishop-boyz-2?page='
FIELDS = [
    {"name": "prod_info", "tag": "li", "attrs": {"data-test-id": "menu-item-list-item"}},
    {"name": "category", "tag": "div", "attrs": {"data-testid": "menu-item-category"}},
    {"name": "name", "tag": "div", "attrs": {"data-testid": "menu-item-title"}},
    {"name": "price", "tag": "div", "attrs": [
        {"class": "Text-sc-51fcf911-0 PriceText-sc-b03e0af1-1 dQtSPx jnRHpj"},
        {"class": "Text-sc-51fcf911-0 PriceText-sc-b03e0af1-1 dyeifY jnRHpj"}
    ]},
    {"name": "producer", "tag": "div", "attrs": {"data-testid": "menu-item-brand"}},
    {"name": "image", "tag": "img", "attrs": {"data-testid": "noscript-img"}},
    {"name": "description", "tag": "div", "attrs": {"class": "Text-sc-51fcf911-0 gqsyVp"}},
]

PAGE_AMOUNT = 15
PRODUCTS = []


async def gather_data():
    async with aiohttp.ClientSession() as session:
        tasks = []
        for page_number in range(1, PAGE_AMOUNT + 1):
            task = asyncio.create_task(get_page_products(page_number, session))
            tasks.append(task)
        await asyncio.gather(*tasks)


async def get_page_products(page_number: int, session):
    headers = {
        "User-Agent": "Mozilla / 5.0(Windows NT 10.0; Win64; x64) AppleWebKit "
                      "/ 537.36(KHTML, like Gecko) Chrome / 116.0 .5845 .686 YaBrowser / 23.9 .0 .0 Safari / 537.36"
    }
    async with session.get(url=f"{LINK}{page_number}", headers=headers) as response:
        page_to_scrape = await response.text()
        soup = BeautifulSoup(page_to_scrape, 'html.parser')
        product_tags = soup.findAll(FIELDS[0]["tag"], attrs=FIELDS[0]["attrs"])
        for product in product_tags:
            product_soup = BeautifulSoup(str(product), 'html.parser')
            current_product_json = dict()
            for field in FIELDS[1:]:
                if field["name"] == "price":
                    info = product_soup.find(field["tag"], attrs=field["attrs"][0])
                    if not info:
                        info = product_soup.find(field["tag"], attrs=field["attrs"][1])
                else:
                    info = product_soup.find(field["tag"], attrs=field["attrs"])
                if field["name"] == "image":
                    current_product_json[field["name"]] = info["src"].split('?')[0] if info and info["src"] else "-"
                else:
                    current_product_json[field["name"]] = info.text if info else "-"
            PRODUCTS.append(current_product_json)


def find_duplicates(products_info: list[dict]):
    df = pd.DataFrame(products_info)
    pd.set_option('display.max_columns', None)
    pd.set_option('display.expand_frame_repr', False)
    sorted_products = df.sort_values(by='price', ascending=False)
    unique_products = sorted_products.drop_duplicates(
        subset=['category', 'name', 'description', 'image', 'producer'],
        keep='first'
    )
    pd.reset_option('display.max_columns')
    pd.reset_option('display.expand_frame_repr')
    return unique_products.to_dict('records')


def create_products(create_serializer, list_serializer, category_ids):
    unique_products_info = get_unique_products_info()
    created_objects = []
    errors = []
    for product in unique_products_info:
        data = {
            "name": product["name"],
            "category": category_ids[product["category"]],
            "producer": product["producer"],
            "slug": "".join(
                [letter for letter in product["name"] if letter.isalpha() or letter.isdigit() or letter == ' '])
                    .replace(' ', '-').replace('--', '-')[:50],
            "description": product["description"],
            "price": product["price"].strip('$')
        }
        image_response = requests.get(url=product["image"])
        image_name = f"{data['slug']}.{product['image'].split('.')[-1]}"
        files = {'image': (image_name, image_response.content)}
        serializer = create_serializer(data=data, files=files)
        if serializer.is_valid():
            created_objects.append(serializer.save())
        else:
            errors.append(serializer.errors)
    response_data = {
        'created_objects': list_serializer(created_objects, many=True).data,
        'errors': errors,
    }
    return response_data


def create_categories(create_serializer, list_serializer):
    unique_products_info = get_unique_products_info()
    categories = list(set([product['category'] for product in unique_products_info]))
    created_objects = []
    errors = []
    for category in categories:
        data = {
            "name": category,
            "slug": category.replace('&', 'and').replace(' ', '-'),
        }
        serializer = create_serializer(data=data)
        if serializer.is_valid():
            created_objects.append(serializer.save())
        else:
            errors.append(serializer.errors)
    created_categories = list_serializer(created_objects, many=True).data["created_objects"]
    category_ids = {category["name"]: category["id"] for category in created_categories}
    return category_ids


def parse_products_info():
    asyncio.run(gather_data())
    unique_products_info = find_duplicates(PRODUCTS)
    with open('products/output.json', 'w') as output:
        output.write(json.dumps(unique_products_info))


def get_unique_products_info():
    return json.load(open('../output.json'))
