#! /usr/bin/env python3
# -*-coding: utf-8 -*

import scrapbook
import csv
import os
import argparse
import requests
from bs4 import BeautifulSoup


def scrap_category(url_category: str) -> list:
    """ retourne toutes les données des livres d'une catérorie
    dans la liste data_category """

    url_site = "https://books.toscrape.com"
    next_page = ""
    url_category_page = url_category
    data_category = []
  
    while next_page is not None:
        try:
            response = requests.get(url_category_page)
        except requests.ConnectionError:
            print("Erreur de connexion: veuillez vérifier l'url")
            break
        except requests.exceptions.RequestException:
            print("Une erreur s'est produite.")
            break
        else:
            if response.status_code == requests.codes.ok:
                response.encoding = 'utf-8'
                soup = BeautifulSoup(response.text, "lxml")

                for h3 in soup.findAll('h3'):  # balise 'h3' contient les urls des livres
                    url_book = h3.find('a')['href'].replace('../../..', url_site + '/catalogue')
                    data_category.append(scrapbook.scrap_book(url_book))
        
                next_page = soup.find('li', {"class": "next"})
                if next_page is not None:
                    link_new_page = soup.find('li', {"class": "next"}).find('a')['href']
                    url_category_page = url_category.replace('index.html','') + link_new_page
            else:
                print("Un problème est survenu !!", response.status_code)
                quit()
    return data_category


def record_file(data_category: list, file_name: str):
    """ sauvegarde les données d'une categorie dans le dossier data_category
        si l'opton -s est activée. Nom du fichier : défini par l'utilisateur"""
    separator = '\t'
    quote = "'"
    os.makedirs("data_category", exist_ok=True)

    with open(os.path.dirname(__file__) + "/" +
              "data_category" + "/" + file_name + '.csv', 'w',
              encoding="utf-8", newline='') as csvfile:
        fieldorder = ["title",
                      "product_description",
                      "universal_product_code (upc)",
                      "price_including_tax",
                      "price_excluding_tax",
                      "number_available",
                      "review_rating",
                      "product_page_url",
                      "image_url"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldorder,
                                delimiter=separator,
                                quotechar=quote)
        writer.writeheader()
        for line in data_category:
            writer.writerow(line)


def main():
    # url_category = "https://books.toscrape.com/catalogue/category/books/sequential-art_5/index.html"
    # url_category = "https://books.toscrape.com/catalogue/category/books/sequential-art_5/index.html"
    # url_category = "https://books.toscrape.com/catalogue/category/books/travel_2/index.html"
    # url_category = "https://books.toscrape.com/catalogue/category/books/historical-fiction_4/index.html"
    # print(scrap_category(url_category))

    parser = argparse.ArgumentParser(description='execute le programme scrapcategory.py')
    parser.add_argument('url_category',
                        help="Entrez l'url d'une catégorie entre quotes",
                        type=str)
    parser.add_argument('-s', '--save', type=str,
                        help="taper '-s' ou '--save' puis son 'nom' pour enregistrer la catégorie")
    args = parser.parse_args()
    args = parser.parse_args()
    data_category = scrap_category(args.url_category)
    if args.save:
        record_file(data_category, args.save)
    else:
        print(data_category)


if __name__ == "__main__":
    main()