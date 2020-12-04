#! /usr/bin/env python3
# -*-coding: utf-8 -*

import scrapbook
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
        response = requests.get(url_category_page)
        response.encoding = 'utf-8'
        soup = BeautifulSoup(response.text, "lxml")

        for h3 in soup.findAll('h3'):  # balise 'h3' contient les urls des livres
            url_book = h3.find('a')['href'].replace('../../..', url_site + '/catalogue')
            data_category.append(scrapbook.scrap_book(url_book))
       
        next_page = soup.find('li', {"class": "next"})
        if next_page is not None:
            link_new_page = soup.find('li', {"class": "next"}).find('a')['href']
            url_category_page = url_category.replace('index.html','') + link_new_page

    return data_category


def main():
    url_category = "https://books.toscrape.com/catalogue/category/books/mystery_3/index.html"
    #url_category = "https://books.toscrape.com/catalogue/category/books/sequential-art_5/index.html"
    #url_category ="https://books.toscrape.com/catalogue/category/books/travel_2/index.html"
    #url_category = "https://books.toscrape.com/catalogue/category/books/historical-fiction_4/index.html"

    print(scrap_category(url_category))


if __name__ == "__main__":
    main()