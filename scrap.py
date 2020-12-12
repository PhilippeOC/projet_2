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
    #a_list = a_list[:1]  # TD sous-liste pour diminuer la durée des tests

    os.makedirs(csts.PATH_DATA, exist_ok=True) 
    os.makedirs(csts.PATH_DATA + "/csv", exist_ok=True)
    os.makedirs(csts.PATH_DATA + "/img", exist_ok=True)
    
    num_img = 1
    for cat in a_list:
        cat_name = cat.text.replace('\n', '').strip()  # nom de la categorie
        print("Catégorie en cours:", cat_name)
        data = scrapcategory.scrap_category(csts.URL_SITE + '/' + cat['href'])  # données d'une categorie de livres
        for img in data:
            resp_image = utils.requests_error(img["image_url"])
            img["image_url"] = "data/img/image_" + str(num_img) + ".jpg"
            # sauvegarde des images de la catégorie
            with open(csts.PATH_DATA + "/img/image_" + str(num_img) + ".jpg", 'wb') as picfile:
                picfile.write(resp_image.content)
            num_img += 1
        
        utils.record_csv(csts.PATH_DATA + "/csv", cat_name, data)


def main():
    scrap_all()


if __name__ == "__main__":
    main()
