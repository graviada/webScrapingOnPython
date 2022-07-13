from bs4 import BeautifulSoup

with open('blank/index.html', encoding='utf-8') as file:
    src = file.read()
# print(src)

# Преобразование html-кода в дерево объектов Python
# lxml - парсер
soup = BeautifulSoup(src, "lxml")

# Информация о теге title
# title = soup.title
# print(title)
# # Для получения содержимого тега
# print(title.text)
# # или
# print(title.string)

# Методы .find(), .find_all()
# # .find() забирает данные из первого попавшегося искомого элемента
# page_h1 = soup.find("h1")
# print(page_h1)
# # .find_all() забирает данные со всех подходящих элементов и сохраняет их в список
# page_all_h1 = soup.find_all("h1")
# print(page_all_h1)
#
# for item in page_all_h1:
#     print(item.text)

# # Получаем имя пользователя class="user__name"
# user_name = soup.find("div", class_="user__name")
# print(user_name.text.strip())
#
# # Двойной поиск
# user_name = soup.find("div", class_="user__name").find("span").text
# print(user_name)

# # Передача данных с помощью словаря
# user_name = soup.find("div", {"class": "user__name"}).find("span").text
# print(user_name)
#
# find_all_spans = soup.find("div", {"class" : "user__info"}).find_all("span")
# print(find_all_spans)

all_a = soup.find_all("a")
# print(all_a)

for item in all_a:
    item_text = item.text
    item_url = item.get("href")
    print(f"{item_text}: {item_url}")

# .find_parent(), .find_parents() - идем вверх кода
post_div = soup.find(class_="post__text").find_parent()
print(post_div)