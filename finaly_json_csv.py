import json, requests, csv, time, random
from bs4 import BeautifulSoup

headers = {
    'Accept': '*/*',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36'
}

with open('all_categories_dict.json', encoding="utf-8") as file:
    all_categories = json.load(file)

iteration_count = int(len(all_categories)) - 1
count = 0
print(f'Всего итераций: {iteration_count}')

for category_name, category_href in all_categories.items():

    rep = [',', ' ', '-', "'"]
    for item in rep:
        if item in category_name:
            category_name = category_name.replace(item, '_')

    req = requests.get(url=category_href, headers=headers)
    src = req.text

    with open(f'data/{count}_{category_name}.html', 'w', encoding="utf-8") as file:
        file.write(src)

    with open(f'data/{count}_{category_name}.html', encoding="utf-8") as file:
        src = file.read()

    soup = BeautifulSoup(src, 'lxml')

    #Проверка страницы на наличие таблицы с продуктами
    alert_block = soup.find(class_='uk-alert uk-alert-danger uk-h1 uk-text-center mzr-block mzr-grid-3-column-margin-top')
    if alert_block is not None:
        continue

    #Собираем заголовки таблицы
    table_head = soup.find(class_='uk-table mzr-tc-group-table uk-table-hover uk-table-striped uk-table-condensed').find('tr').find_all('th')
    product = table_head[0].text
    calories = table_head[1].text
    proteins = table_head[2].text
    fats = table_head[3].text
    carbohydrates = table_head[4].text

    with open(f'data/{count}_{category_name}.csv', 'w', newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(
            (
                product,
                calories,
                proteins,
                fats,
                carbohydrates
            )
        )

    #Собираем заголовки таблицы
    product_data = soup.find(class_='uk-table mzr-tc-group-table uk-table-hover uk-table-striped uk-table-condensed').find('tbody').find_all('tr')

    product_info = []

    for item in product_data:
        product_tds = item.find_all('td')

        title = product_tds[0].find("a").text
        calories = product_tds[1].text
        proteins = product_tds[2].text
        fats = product_tds[3].text
        carbohydrates = product_tds[4].text

        product_info.append(
            {
                'Title' : title,
                'Calorise' : calories,
                'Proteins' : proteins,
                'Fats' : fats,
                'Carbohydrates' : carbohydrates
            }
        )

        with open(f'data/{count}_{category_name}.csv', 'a', newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(
                (
                    title,
                    calories,
                    proteins,
                    fats,
                    carbohydrates
                )
            )
    with open(f'data/{count}_{category_name}.json', 'a', newline="", encoding="utf-8") as file:
        json.dump(product_info, file, indent=4, ensure_ascii=False)


    count += 1
    print(f'# Итерация {count}.{category_name} записана...')
    iteration_count = iteration_count - 1

    if iteration_count == 0:
        print("Работа завершена")
        break

    print(f'Осталось итераций: {iteration_count}')
    time.sleep(random.randrange(2, 4))