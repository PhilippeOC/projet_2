#! /usr/bin/env python3
# -*-coding: utf-8 -*

import requests
from bs4 import BeautifulSoup


def scrap_book(url_book: str) -> dict:
    """ retourne les données d'un livre : title, product_description,
    universal_product_code (upc), price_including_tax, price_excluding_tax,
    number_available, review_rating, product_page_url, image_url """

    url_site = "https://books.toscrape.com/"
    book_data = {}
    
    response = requests.get(url_book)
    response.encoding = 'utf-8'
    soup = BeautifulSoup(response.text, "lxml")

    # titre du livre
    book_data["title"] = soup.find('h1').text

    # description du livre
    description = soup.find(attrs={'name': 'description'})
    book_data["product_description"] = description.attrs["content"].strip()

    # infos du tableau
    td_list = soup.findAll('td')
    book_data["universal_product_code (upc)"] = td_list[0].text
    
    # book_data["product type"] = td_list[1].text
    book_data["price_excluding_tax"] = td_list[2].text
    book_data["price_including_tax"] = td_list[3].text
    # book_data["tax"] = td_list[4].text
    book_data["number_available"] = td_list[5].text

    book_data["review_rating"] = td_list[6].text

    # url du produit
    book_data["product_page_url"] = url_book

    # url de l'image
    image = soup.find("img")
    url_image = image["src"].replace('../..', url_site)
    book_data["image_url"] = url_image
    return book_data


def main():
    # url_book = "https://books.toscrape.com/catalogue/a-summer-in-europe_458/index.html"
    url_book = "https://books.toscrape.com/catalogue/its-only-the-himalayas_981/index.html"  
    print(scrap_book(url_book))


if __name__ == "__main__":
    main()   