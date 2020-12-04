#! /usr/bin/env python3
# -*-coding: utf-8 -*

import os
import csv
import scrapcategory
import requests
from bs4 import BeautifulSoup


def scrap_all():
    """ Sauvegarde l'ensenmble des données de tous les livres du site dans un
    fichier csv au nom de la catégorie """

    data = []
    a_list = []

    url_site = "https://books.toscrape.com"

    os.makedirs("data", exist_ok=True)
    directory = os.path.dirname(__file__)  # wd
    path_to_file = directory + "/" + "data"
   
    response = requests.get(url_site)
    response.encoding = 'utf-8'
    soup = BeautifulSoup(response.text, "lxml")

    url_nav = soup.find('ul', {"class": "nav nav-list"})
    
    a_list = url_nav.findAll('a')
    a_list = a_list[1:len(url_nav.findAll('a'))]  # supprime l'item "Books" de la liste
    # a_list = a_list[:2] sous liste de 2 element pour diminuer la durée des tests
    
    for cat in a_list:
        cat_data = cat.text.replace('\n', '').strip()  # nom categorie

        os.makedirs(path_to_file + '/' + cat_data, exist_ok=True)  # creation dossier data/nom catégorie
        os.makedirs(path_to_file + '/' + cat_data + '/' + cat_data + "_image", exist_ok=True) # creation dossier image catégorie
        
        data = scrapcategory.scrap_category(url_site + '/' + cat['href'])  # datas d'une categorie livre
        
        # sauvegarde dans le fichier cat_data.csv
        csv_file(cat_data, path_to_file, data)
        
        # Téléchargement de l'image
        img_file(cat_data, path_to_file, data)
       

def csv_file(cat_data: str, path_to_file: str, data: list):
    cat_data = path_to_file + "/" + cat_data + "/" + cat_data + ".csv"
    with open(cat_data, 'w', encoding="utf-8", newline='') as csvfile:
        order = ["title",
                 "product_description",
                 "universal_product_code (upc)",
                 "price_including_tax",
                 "price_excluding_tax",
                 "number_available",
                 "review_rating",
                 "product_page_url",
                 "image_url"] 
        writer = csv.DictWriter(csvfile, dialect='excel-tab', fieldnames= order)
        writer.writeheader()
        for line in data:
            writer.writerow(line)


def img_file(cat_data: str, path_to_file: str, data: list):
    cat_image = path_to_file + '/' + cat_data + '/' + cat_data + "_image" 
    
    for line in data:
        image_url = line["image_url"]
        image_title = line["title"].replace(':','_').replace(' ', '_') + '.jpg'
        file_name = cat_image + '/' + image_title
        print(file_name)
        resp_image = requests.get(image_url)
        with open(file_name, 'wb') as picfile:
            picfile.write(resp_image.content)


def main():
    scrap_all()


if __name__ == "__main__":
    main()
