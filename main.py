from bs4 import BeautifulSoup
import requests
import pandas as pd

BOOK = input('Please enter the genre you want to find books/prices for: ')
SRVICE_ENDPOINT = 'https://www.audible.com/search'
PARAMETERS = {
    'keywords': BOOK,
    'ref': '',
    'override': 'a_hp_t1_header_search',
    'k': BOOK
}
header = {
    "Accept-Language": "en-US,en;q=0.9,ar;q=0.8",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36"
}

response = requests.get(url=SRVICE_ENDPOINT, params=PARAMETERS, headers=header)
# print(response.text)
soup = BeautifulSoup(response.content, 'html.parser')
prices = soup.find_all(class_="bc-text bc-size-base bc-color-base", name="span")
prices_list = []
product_list = []
for counter in range(len(prices)):
    if '$' in prices[counter].get_text():
        prices_list.append(float(prices[counter].get_text().strip().replace('$', '')))

for counter in range(1, len(prices)+1):
    try:
        product_list.append(soup.select_one(f'#product-list-a11y-skiplink-target > span > ul > li:nth-child({counter}) > div > div.bc-col-responsive.bc-spacing-top-none.bc-col-8 > div > div.bc-col-responsive.bc-col-6 > div > div > span > ul > li:nth-child(1) > h3 > a').get_text())
    except AttributeError:
        break
# soup = BeautifulSoup(response, "html.parser")
df = pd.DataFrame(data=list(zip(product_list, prices_list)), columns=('Product Name', 'Price in $'))

print(df)