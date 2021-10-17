import requests
from bs4 import BeautifulSoup
import csv
import lxml

headers = {
		'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36',
		'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9'
	}


# ----------------------------------Сбор ссылок на карочки товаров в TXT------------------------------------------ #
def get_links_cards():
	
	cards_list_url = []

	for i in range(1, 21, 1):
		url = f'https://www.proudmom.ru/collection/all?page={i}'
		print(url)

		req = requests.get(url, headers)
		result = req.content

		soup = BeautifulSoup(result, 'lxml')
		cards = soup.find_all(class_='cont_it_crt')

		for card in cards:
			card_page_url = card.get('href')
			cards_list_url.append('https://www.proudmom.ru' + card_page_url)

	# print(cards_list_url)

	with open('cards_list_url.txt', 'a') as file:
		for line in cards_list_url:
			file.write(f'{line}\n')


# ---------------------Сбор необходимых данных из карточек и сохранение их в CSV------------------------------------- #
def get_data_from_cards():
	with open('cards_list_url.txt') as file:

		lines = [line.strip() for line in file.readlines()]

		data_dict = []

		count = 0

		for line in lines:
			req = requests.get(line, headers)
			result = req.content

			soup = BeautifulSoup(result, 'lxml')
			article_brand_production = soup.find(class_='desc_text_prod').text
			article_brand_production_tech = article_brand_production.strip().split('\n')
			article_product = article_brand_production_tech[0].strip().split(': ')

			article = article_product[1]
			name_product = soup.find(class_='content_product_description').find('form').find('h1').text
			price = soup.find(class_='content_product_description').find('form').find('div', class_='block_price_product').text.strip()
			product_info = []
			product_info_p = soup.find(class_='body_product_tabs_info').find(class_='item_tabs_1').find_all('p')
			for item in product_info_p:
				product_info.append(item.text)
			size = []
			size_option = soup.find(class_='block_size_product').find('select').find_all('option')
			for item in size_option:
				size.append(item.text)
			photo_url = []
			photo_url_soup = soup.find('div', class_='product_description').find('div', class_='galery_product_description').find('div', class_='block_img_galery_product_description').find('div', class_='img_galery_product_description').find_all('a')
			for item in photo_url_soup:
				photo_url.append(item.get('href'))
			product_url = line

			data = {
				'Ссылка на товар': product_url,
				'Артикул': article,
				'Наименование': name_product,
				'Цена': price,
				'Описание': product_info,
				'Размер': size,
				'Фото': photo_url
			}

			count += 1
			print(f'{count}: {line} is done!')

			data_dict.append(data)

			with open('data.csv', 'w', newline='', encoding='utf-8-sig') as file:
				writer = csv.writer(file, delimiter=';')
				writer.writerow(['Ссылка на товар', 'Артикул', 'Наименование', 'Цена', 'Описание', 'Размер', 'Фото'])
				for item in data_dict:
					writer.writerow([item['Ссылка на товар'], item['Артикул'], item['Наименование'], item['Цена'], item['Описание'], item['Размер'], item['Фото']])


# ---------------------------------------------Вызов функций-------------------------------------------------------- #
get_links_cards()
get_data_from_cards()
