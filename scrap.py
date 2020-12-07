#! /usr/bin/env python3
# -*-coding: utf-8 -*

import os
import csv
import scrapcategory
import requests
from bs4 import BeautifulSoup


def scrap_all():
    """
    - Sauvegarde l'ensenmble des données de tous les livres dans un
    fichier csv au nom de la catégorie.
    - Sauvegarde des images de couverture
    """

    data = []
    a_list = []  
    url_site = "https://books.toscrape.com"

    os.makedirs("data", exist_ok=True)
    path = os.path.dirname(__file__) + "/" + "data"  # path du répertoire d'enregistrement
   
    response = requests.get(url_site)
    response.encoding = 'utf-8'
    soup = BeautifulSoup(response.text, "lxml")

    url_nav = soup.find('ul', {"class": "nav nav-list"})   
    a_list = url_nav.findAll('a')
    a_list = a_list[1:len(url_nav.findAll('a'))]  # supprime l'item "Books" de la liste
    a_list = a_list[:1]  # sous-liste pour diminuer la durée des tests
    for cat in a_list:
        cat_name = cat.text.replace('\n', '').strip()  # nom categorie
        path_data = path + '/' + cat_name  # chemin du dossier au nom de la catégorie

        os.makedirs(path_data, exist_ok=True)  # creation dossier nom catégorie
        os.makedirs(path_data + '/' + cat_name + "_image", exist_ok=True)  # creation du sous-dossier image catégorie

        data = scrapcategory.scrap_category(url_site + '/' + cat['href'])  # datas d'une categorie livre
        
        # sauvegarde dans le fichier cat_name.csv
        record_file(cat_name, path_data, data)


def record_file(cat_name: str, path_data: str, data: list):
    """ Enregistrement des données dans le fichier 'categorie.csv'
        et téléchargement des images dans le sous dossier 'categorie_image' """
    print(cat_name)
    cat_image = path_data + '/' + cat_name + "_image"
    csv_data = path_data + "/" + cat_name + ".csv"
  
    separator = '\t'
    quote = "'"
    with open(csv_data, 'w', encoding="utf-8", newline='') as csvfile:
        fieldorder = ["title",
                      "product_description",
                      "universal_product_code (upc)",
                      "price_including_tax",
                      "price_excluding_tax",
                      "number_available",
                      "review_rating",
                      "product_page_url",
                      "image_url",
                      "image"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldorder,
                                delimiter=separator,
                                quotechar=quote)
        writer.writeheader()
        i = 1
        for line in data:
            # telechargement de l'image
            image_url = line["image_url"]
            file_name = cat_image + '/' + 'image_' + str(i) + '.jpg'
            line["image"] = "data" + '/' + cat_name + '/' + cat_name + "_image" + '/' + 'image_' + str(i) + '.jpg'
            resp_image = requests.get(image_url)
            with open(file_name, 'wb') as picfile:
                picfile.write(resp_image.content)
            writer.writerow(line)
            i += 1


def main():
    scrap_all()


if __name__ == "__main__":
    main()
