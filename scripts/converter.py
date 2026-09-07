import re
import pandas as pd
from bs4 import BeautifulSoup
import requests

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/152.0.0.0 Safari/537.36'
}

main_page = [(requests.get('https://www.lafeltrinelli.it/classifica/libri/1day/sold?page=1', headers=headers)),
(requests.get('https://www.lafeltrinelli.it/classifica/libri/1day/sold?page=2', headers=headers)),
(requests.get('https://www.lafeltrinelli.it/classifica/libri/1day/sold?page=3', headers=headers))]

proceed = False

book_links = []

book_info = []

for main_link in main_page:
    if main_link.status_code == 200:
        soup = BeautifulSoup(main_link.text, 'html.parser')
        proceed = True

        for link in soup.find_all('li', class_="cc-product-list-item cc-product-list-item--ranking"):
            incomplete_link = link.find('a', class_="cc-img-link").get('href')
            href = 'https://www.lafeltrinelli.it'+incomplete_link
            book_links.append(href)

if proceed:
    for rank, url in enumerate(book_links, start=1):
        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            soup1 = BeautifulSoup(response.text, 'html.parser')

            title = None
            author = None
            stars = None
            reviews = None
            isbn_code = None
            price = None
            discount = None
            old_price = None


            book = soup1.find('div', class_="cc-content-interactions")
            price_info = soup1.find('div', {'id': 'buy-box'})

            if book:
                title_tag = book.find('span', class_="cc-title")
                title = title_tag.get_text(strip=True) if title_tag else None

                author_tag = book.find('span', class_="cc-author-name")
                author = author_tag.get_text(strip=True) if author_tag else None

                stars_tag = book.find('div', class_="cc-rating")
                stars = int(stars_tag["class"][1].replace('cc-rating--', '')) if stars_tag else 0

                reviews_tag = book.find('input', attrs={'name': 'num_review'})
                reviews = int(reviews_tag.get('value')) if reviews_tag else 0

                if reviews == 0:
                    stars = None

            isbn_tag = soup1.find('input', attrs={'id': "isKoboPlusEligible"})
            if isbn_tag:
                isbn_code = isbn_tag.get('data-ean') if isbn_tag else None

            if price_info:

                price_raw = price_info.find('div', class_="cc-content-price")

                if price_raw:
                    price_tag = price_raw.find('span', class_="cc-price")
                    price = re.sub(r'[^\d,.]', '', price_tag.get_text().replace(',', '.')) if price_tag else None

                    discount_tag = price_raw.find('span', class_="cc-discount")
                    discount = discount_tag.get_text(strip=True).replace('-', '').replace('%', '') if discount_tag else None

                    old_price_tag = price_raw.find('span', class_="cc-old-price")
                    old_price = re.sub(r'[^\d,.]', '', old_price_tag.get_text().replace(',', '.')) if old_price_tag else None

            book_info.append({
                'title': title,
                'rank': rank,
                'author': author,
                'stars': stars,
                'reviews': reviews,
                'isbn_code': isbn_code,
                'price': price,
                'discount': discount,
                'old_price': old_price
            })
else:
    print("Couldn't load main page.")

df = pd.DataFrame(book_info)
df.to_csv('feltrinelli_data.csv', index=False, encoding='utf-8')

print("Conversion done.") 