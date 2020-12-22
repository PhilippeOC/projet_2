import constants as csts
import scrapcategory
import utilities as utils

from bs4 import BeautifulSoup
import os


def scrap_all():
    """
    - Sauvegarde l'ensenmble des données de tous les livres dans un
    fichier csv au nom de la catégorie.
    - Sauvegarde des images de couverture.
    """
    
    data = []
    a_list = []
   
    response = utils.requests_error(csts.URL_SITE)
    response.encoding = 'utf-8'
    soup = BeautifulSoup(response.text, "lxml")

    a_list = soup.find('ul', {"class": "nav nav-list"}).findAll('a')  # scrap les balises <a> du menu des catégories
    a_list = a_list[1:len(a_list)]  # supprime l'item "Books" de la liste

    os.makedirs(csts.PATH_DATA, exist_ok=True) 
    os.makedirs(csts.PATH_DATA_CSV, exist_ok=True)
    os.makedirs(csts.PATH_DATA_IMG, exist_ok=True)
    
    for num_cat, cat in enumerate(a_list):
        data = scrapcategory.scrap_category(csts.URL_SITE + '/' + cat['href'])  # données d'une categorie de livres
        print("Catégorie en cours:", data[0])
        
        # sauvegarde des images de la catégorie
        for num_img, img in enumerate(data[1:]):
            resp_image = utils.requests_error(img["image_url"])
            img_name = "cat_" + str(num_cat + 1) + "_image_" + str(num_img + 1) + ".jpg"
            img["image_url"] = os.path.join("data/img", img_name)
            with open(os.path.join(csts.PATH_DATA_IMG, img_name), 'wb') as picfile:
                picfile.write(resp_image.content)
        
        utils.record_csv(csts.PATH_DATA_CSV, data[0], data[1:])


def main():
    scrap_all()


if __name__ == "__main__":
    main()
