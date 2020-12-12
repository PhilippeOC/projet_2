""" fonctions communes utilisées par les 3 programmes """
import csv
import requests


def requests_error(url: str):
    """ retourne la réponse à la requette si tout est correct """
    try:
        response = requests.get(url)
    except requests.exceptions.RequestException as err:
        print("Une erreur s'est produite:")
        raise SystemExit(err)
    else:
        if response.status_code == requests.codes.ok:
            return response
        else:
            print("Un problème est survenu !! \t status-code:", response.status_code)
            quit()


def record_csv(path: str, file_name: str, data_list: list):
    """ sauvegarde la liste des données dans un fichier csv """
    separator = '\t'
    quote = "'"
    with open(path + "/" + file_name + ".csv", 'w',
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
        for line in data_list:
            writer.writerow(line)
