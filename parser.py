import csv

import requests
import json
from bs4 import BeautifulSoup
from fake_useragent import UserAgent

ua = UserAgent()
user_agent = ua.random

headers = {'user-agent': user_agent}


def get_data_json():
    """
    Сбор ссылок на карочки товаров в TXT
    """
    data = {}
    for i in range(1, 17, 1):
        url = f'https://www.proudmom.ru/collection/brands?page={i}'
        req = requests.get(url=url, headers=headers)
        result = req.content

        soup = BeautifulSoup(result, 'lxml')
        cards = soup.find_all("form", action="/cart_items")

        print(url)
        print(f'Кол-во карточек: {len(cards)}')

        for card in cards:
            product_id = card.get('data-product-id')
            urlj = f'https://www.proudmom.ru/products_by_id/{product_id}.json'

            data_json = requests.get(urlj)
            data[product_id] = data_json.json()

    with open('data.json', 'w') as file:
        json.dump(data, file, indent=4, ensure_ascii=False)


def get_data_and_sav_csv():
    """
    Сбор необходимых данных и сохранение их в CSV
    """
    with open('data.json') as file:
        data = json.load(file)

    data_dict = []
    count = 1

    for key in data.keys():
        data_sku = data[key]["products"][0]
        data_sku_var = data_sku["variants"]

        product_url = f"https://www.proudmom.ru{data_sku['url']}"
        article = data_sku_var[0]["sku"] + f"-{count}"
        name_product = data_sku["title"]
        price = float(data_sku_var[0]["price"]) * 0.8

        size_list = [data_sku_var[i]["title"] + "; " for i in range(
            len(data_sku_var)
        )]
        size = ""
        for item in size_list:
            size += item

        img_l = [data_sku["images"][i]["original_url"] + "; " for i in range(
            len(data_sku["images"])
        )]
        photo_url = ""
        for url in img_l:
            photo_url += url

        try:
            response = requests.get(url=product_url, headers=headers)
            content = response.content
            soup = BeautifulSoup(content, 'lxml')

            try:
                div_breadcrumb = soup.find_all(
                    class_="breadcrumb-link bttn-underline"
                )
                albom = div_breadcrumb[1].text.strip()
            except Exception:
                albom = "Новинки"
            try:
                div_info = soup.find(class_="accordion-item__container")
                product_info = div_info.text.strip()
            except Exception as error:
                print(error)
                product_info = "Нет данных"

        except Exception as error:
            print(error)
            continue

        data_temp = {
            'Рубрика': 'Для женщин',
            'Подрубрика': 'Женские блузки, кофты',
            'Альбом': albom,
            'Артикул': article,
            'Наименование': name_product,
            'Вес': '',
            'Цена': price,
            'Цена2': '',
            'Изображения': photo_url,
            'Описание': product_info,
            'Стоимость доставки': '',
            'Ссылка на товар': product_url,
            'Seo заголовок': '',
            'Seo описание': '',
            'Ключевые слова': '',
            'Показ': '',
            'Порядок отображения': '',
            'Ярлык': '',
            'Ряд по количеству': '',
            'Параметр: Размер': size,
            'Ряд3: Количество': '',
        }

        data_dict.append(data_temp)

        with open(
            'data_final.csv', 'w', newline='', encoding='utf-8-sig'
        ) as file:
            writer = csv.writer(file, delimiter=';')
            writer.writerow([
                'Рубрика',
                'Подрубрика',
                'Альбом',
                'Артикул',
                'Название',
                'Вес',
                'Цена',
                'Цена2',
                'Изображения',
                'Описание',
                'Стоимость доставки',
                'Ссылка на товар',
                'Seo заголовок',
                'Seo описание',
                'Ключевые слова',
                'Показ',
                'Порядок отображения',
                'Ярлык',
                'Ряд по количеству',
                'Параметр: Размер',
                'Ряд3: Количество'
            ])
            for item in data_dict:
                writer.writerow([
                    item['Рубрика'],
                    item['Подрубрика'],
                    item['Альбом'],
                    item['Артикул'],
                    item['Наименование'],
                    item['Вес'],
                    item['Цена'],
                    item['Цена2'],
                    item['Изображения'],
                    item['Описание'],
                    item['Стоимость доставки'],
                    item['Ссылка на товар'],
                    item['Seo заголовок'],
                    item['Seo описание'],
                    item['Ключевые слова'],
                    item['Показ'],
                    item['Порядок отображения'],
                    item['Ярлык'],
                    item['Ряд по количеству'],
                    item['Параметр: Размер'],
                    item['Ряд3: Количество']
                ])

        print(f'{count}: {key} is done!')
        count += 1


def main():
    # get_data_json()
    get_data_and_sav_csv()


if __name__ == '__main__':
    main()
