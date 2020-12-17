import constants as csts
import scrapbook
import utilities as utils

import argparse
from bs4 import BeautifulSoup
import os


def scrap_category(url_category: str) -> list:
    """ retourne la liste de toutes les données des livres de la catérorie
    dont l'url est entrée en paramètre """

    next_page = True
    url_category_page = url_category
    data_category = []

    while next_page:
        response = utils.requests_error(url_category_page)
        response.encoding = 'utf-8'
        soup = BeautifulSoup(response.text, "lxml")

        if url_category_page == url_category:
            data_category.append(soup.find('h1').text)  # enregistre le nom de la catégorie

        for h3 in soup.findAll('h3'):  # balise 'h3' contient les urls des livres
            url_book = h3.find('a')['href'].replace('../../..', csts.URL_SITE + '/catalogue')
            data_category.append(scrapbook.scrap_book(url_book))

        next_page = soup.find('li', {"class": "next"})
        if next_page:
            url_category_page = url_category.replace('index.html', '') + soup.find('li', {"class": "next"}).find('a')['href']
    return data_category


def main():
    parser = argparse.ArgumentParser(description='execute le programme scrapcategory.py')
    parser.add_argument('url_category',
                        help="Entrer l'url d'une catégorie entre quotes",
                        type=str)
    parser.add_argument('-s', '--save', action='store_true',
                        help="taper '-s' ou '--save' pour sauvegarder les données d'une catégorie")
    args = parser.parse_args()
    data_category = scrap_category(args.url_category)
   
    if args.save:
        os.makedirs(csts.PATH_CAT, exist_ok=True)
        utils.record_csv(csts.PATH_CAT, data_category[0], data_category[1:])
    else:
        print(data_category)


if __name__ == "__main__":
    main()