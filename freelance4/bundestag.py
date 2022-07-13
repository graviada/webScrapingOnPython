import requests
import json
from bs4 import BeautifulSoup


def get_bundestag_members():
    # headers = {
    #     "user-agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36"
    # }
    #
    # persons_url_list = []
    # for i in range(0, 720, 20):
    #     url = f"https://www.bundestag.de/ajax/filterlist/en/members/863330-863330?limit=20&noFilterSet=true&offset={i}"
    #     response = requests.get(url, headers=headers)
    #
    #     result = response.content
    #     soup = BeautifulSoup(result, "lxml")
    #
    #     persons_url = soup.find_all("a", class_="bt-open-in-overlay")
    #     for person in persons_url:
    #         person_url = person.get("href")
    #         persons_url_list.append(person_url)
    #     # print(persons_url_list)
    #
    # with open('persons_url_list.txt', 'a') as file:
    #     for line in persons_url_list:
    #         file.write(f'{line}\n')

    # Нужны имя, партия и ссылки на социальные сети
    with open('persons_url_list.txt') as file:
        lines = [line.strip() for line in file.readlines()]
        data_dict = []
        count = 0

        for line in lines:
            query = requests.get(line)
            result = query.content

            soup = BeautifulSoup(result, 'lxml')
            person = soup.find("div", class_="col-xs-8 col-md-9 bt-biografie-name").find("h3").text

            # print(person)

            person_name_pol_party = person.strip().split(",")
            person_name = person_name_pol_party[0]
            person_pol_party = person_name_pol_party[1].strip()

            social_networks = soup.find("ul", class_="bt-linkliste").find_all("a")
            social_networks_url = []
            for url in social_networks:
                social_networks_url.append(url.get("href"))

            data = {
                'person_name': person_name,
                'political_party': person_pol_party,
                'social_network_name': social_networks_url
            }
            count += 1
            print(f'#{count}: {line} is done!')

            data_dict.append(data)

            with open('data.json', 'w') as json_file:
                json.dump(data_dict, json_file, indent=4)


def main():
    get_bundestag_members()


if __name__ == '__main__':
    main()
