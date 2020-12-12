import constants as csts
import utilities as utils

import argparse
from bs4 import BeautifulSoup
import os
import re


def scrap_book(url_book: str) -> dict:
    """ retourne les données d'un livre : title, product_description,
    universal_product_code (upc), price_including_tax, price_excluding_tax,
    number_available, review_rating, product_page_url, image_url """

    book_data = {}
    response = utils.requests_error(url_book)
    response.encoding = 'utf-8'
    soup = BeautifulSoup(response.text, "lxml")

    # titre du livre
    book_data["title"] = soup.find('h1').text

    # description du livre
    description = soup.find(attrs={'name': 'description'})
    book_data["product_description"] = description.attrs["content"].strip()

    # infos du tableau
    book_data["universal_product_code (upc)"] = soup.findAll('td')[0].text
    book_data["price_excluding_tax"] = soup.findAll('td')[2].text
    book_data["price_including_tax"] = soup.findAll('td')[3].text
    book_data["number_available"] = soup.findAll('td')[5].text
    book_data["review_rating"] = soup.findAll('td')[6].text

    # url du produit
    book_data["product_page_url"] = url_book

    # url de l'image
    book_data["image_url"] = soup.find("img")["src"].replace('../..', csts.URL_SITE)
    return book_data


def main():
    parser = argparse.ArgumentParser(description='execute le programme scrapbook.py')
    parser.add_argument('url_book',
                        help="Entrez l'url d'un livre entre quotes",
                        type=str)
    parser.add_argument('-s', '--save', action='store_true',
                        help="taper '-s' ou '--save' pour sauvegarder les données du livre")
    args = parser.parse_args()
    data_list = [scrap_book(args.url_book)]
    
    if args.save:
        os.makedirs(csts.PATH_BOOk, exist_ok=True)
        utils.record_csv(csts.PATH_BOOk,
                         re.sub(r"[^A-Za-z0-9 '_]", '',  # supprime la ponctuation et les caractères spéciaux
                                data_list[0]['title']),
                         data_list)
    else:
        print(data_list[0])


if __name__ == "__main__":
    main()   