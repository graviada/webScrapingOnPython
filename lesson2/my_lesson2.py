import requests
from bs4 import BeautifulSoup
import json
import csv

# url = "https://health-diet.ru/table_calorie/?utm_source=leftMenu&utm_medium=table_calorie"
#
headers = {
    "Accept": "*/*",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36"
}
# request = requests.get(url, headers=headers)
#
# src = request.text
# # print(src)
#
# with open("index.html", "w", encoding="utf-8") as file:
#     file.write(src)

with open("index.html", encoding="utf-8") as file:
    src = file.read()

soup = BeautifulSoup(src, "lxml")

# # Получаем все ссылки на категории товаров
# product_categories_dict = {}
# product_categories = soup.find_all(class_="mzr-tc-group-item-href")
# for item in product_categories:
#     item_text = item.text
#     item_href = "https://health-diet.ru" + item.get("href")
#     print(f"{item.text}: {item_href}")
#
#     product_categories_dict[item_text] = item_href
#
# # Сохраним словарь в JSON-файл
# with open("product_categories.json", "w", encoding="utf-8") as file:
#     json.dump(product_categories_dict, file, indent=4, ensure_ascii=False)

with open("data/product_categories.json", encoding="utf-8") as file:
    product_categories = json.load(file)

# print(product_categories)

# Собрать данные в каждой категории о товарах и их химическом составе, записать в файл
count = 0
# Количество страниц категорий
iteration_count = int(len(product_categories)) - 1
print(f"Всего итераций: {iteration_count}")

for category_name, category_href in product_categories.items():
    rep = [",", " ", "'", "-"]

    for item in rep:
        if item in category_name:
            category_name = category_name.replace(item, "_")

    # print(category_name)

    req = requests.get(url=category_href, headers=headers)
    src = req.text

    with open(f"data/{count}_{category_name}.html", "w", encoding="utf-8") as file:
        file.write(src)

    with open(f"data/{count}_{category_name}.html", encoding="utf-8") as file:
        src = file.read()

    soup = BeautifulSoup(src, "lxml")

    # Проверка категории на пустоту
    alert_block = soup.find(class_="uk-alert-danger")
    if alert_block is not None:
        continue

    # Собираем заголовки таблицы
    table_headers = soup.find("thead").find_all("th")
    # print(table_headers)
    product = table_headers[0].text
    calories = table_headers[1].text
    proteins = table_headers[2].text
    fats = table_headers[3].text
    carbohydrates = table_headers[4].text

    # Начинаем запись данных в таблицу
    with open(f"data/{count}_{category_name}.csv", "w", encoding="utf-8", newline='') as file:
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

    # Собираем данные продуктов
    products_data = soup.find("tbody").find_all("tr")

    products_info = []
    for item in products_data:
        products_tds = item.find_all("td")

        title = products_tds[0].find("a").text
        calories = products_tds[1].text
        proteins = products_tds[2].text
        fats = products_tds[3].text
        carbohydrates = products_tds[4].text

        products_info.append(
            {
                "Title": title,
                "Calories": calories,
                "Proteins": proteins,
                "Fats": fats,
                "Carbohydrates": carbohydrates
            }
        )

        with open(f"data/{count}_{category_name}.csv", "a", encoding="utf-8", newline='') as file:
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

    with open(f"data/{count}_{category_name}.json", "w", encoding="utf-8") as file:
        json.dump(products_info, file, indent=4, ensure_ascii=False)

    count += 1

    print(f"# Итерация {count}. {category_name} записан...")
    iteration_count = iteration_count - 1

    if iteration_count == 0:
        print("Работа завершена")
        break

    print(f"Осталось итераций: {iteration_count}")