# coding: utf-8


import os
import csv
import argparse
import requests
from bs4 import BeautifulSoup


def scrap_book(url_book: str) -> dict:
    """ retourne les données d'un livre : title, product_description,
    universal_product_code (upc), price_including_tax, price_excluding_tax,
    number_available, review_rating, product_page_url, image_url """

    url_site = "https://books.toscrape.com/"
    book_data = {}
    
    soup = BeautifulSoup(ok_all(url_book).text, "lxml")

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
    """else:
        print("Un problème est survenu !!")"""


def ok_all(url_book: str):
    """ retourne la réponse à la requette si tout est correct"""
    try:
        response = requests.get(url_book)
        response.encoding = 'utf-8'
        # print(type(response))
    except requests.ConnectionError:
        print("Erreur de connexion: veuillez vérifier l'url")
        quit()
    except requests.exceptions.RequestException:
        print("Une erreur s'est produite.")
        quit()
    else:
        if response.status_code == requests.codes.ok:
            return response
        else:
            print("Un problème est survenu !!", response.status_code)
            quit()


def record_file(data: dict):
    """ sauvegarde les données d'un livre dans le dossier data_book
        si l'opton -s est activée. Nom du fichier : titre du livre.csv """
    separator = '\t'
    quote = "'"
    os.makedirs("data_book", exist_ok=True)

    with open(os.path.dirname(__file__) + "/" +
              "data_book" + "/" + data['title'] + '.csv', 'w',
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
        writer.writerow(data)


def main():
    #url_book = "https://books.toscrape.com/catalogue/its-only-the-himalayas_981/index.html"
    #print(scrap_book(url_book))
    parser = argparse.ArgumentParser(description='execute le programme scrapbook.py')
    parser.add_argument('url_book',
                        help="Entrez l'url d'un livre entre quotes",
                        type=str)
    parser.add_argument('-s', '--save', action='store_true',
                        help="taper '-s' ou '--save' pour sauvegarder les données du livre")
    args = parser.parse_args()
    data = scrap_book(args.url_book)
    if args.save:
        record_file(data)
    else:
        print(data)


if __name__ == "__main__":
    main()   