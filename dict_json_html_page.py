import json
from bs4 import BeautifulSoup

with open('index.html', encoding="utf-8") as file:
    src = file.read()

soup = BeautifulSoup(src, 'lxml')
all_produts_href = soup.find_all(class_='mzr-tc-group-item-href')

all_categories_dict = {}
for item in all_produts_href:
    item_text = item.text
    item_href = 'https://health-diet.ru' + item.get('href')

    all_categories_dict[item_text] = item_href

with open('all_categories_dict.json', 'w', encoding="utf-8") as file:
    json.dump(all_categories_dict, file, indent=4, ensure_ascii=False)