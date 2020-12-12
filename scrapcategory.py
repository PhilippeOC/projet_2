import constants as csts
import scrapbook
import utilities as utils

import argparse
from bs4 import BeautifulSoup
import os


def scrap_category(url_category: str) -> list:
    """ retourne toutes les données des livres d'une catérorie """

    next_page = True
    url_category_page = url_category
    data_category = []

    while next_page:
        response = utils.requests_error(url_category_page)
        response.encoding = 'utf-8'
        soup = BeautifulSoup(response.text, "lxml")

        for h3 in soup.findAll('h3'):  # balise 'h3' contient les urls des livres
            url_book = h3.find('a')['href'].replace('../../..', csts.URL_SITE + '/catalogue')
            data_category.append(scrapbook.scrap_book(url_book))

        next_page = soup.find('li', {"class": "next"})
        if next_page:
            link_new_page = soup.find('li', {"class": "next"}).find('a')['href']
            url_category_page = url_category.replace('index.html', '') + link_new_page
    return data_category


def category_name(url_category: str) -> str:
    """ retourne le nom de la catégorie """
    response = utils.requests_error(url_category)
    response.encoding = 'utf-8'
    return BeautifulSoup(response.text, "lxml").find('h1').text


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
        utils.record_csv(csts.PATH_CAT, category_name(args.url_category), data_category)
    else:
        print(data_category)


if __name__ == "__main__":
    main()