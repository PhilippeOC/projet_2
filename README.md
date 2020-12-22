#### Projet 2 : Utilisez les bases de Python pour l'analyse de marché.
#### Réalisation d'un "scrapeur" sur le site Books to Scrape  https://books.toscrape.com/

#### Composition :
Le projet est composé de cinq fichiers
- scrapbook.py: programme qui permet de télécharger les données concernant un livre et de les enregistrer dans un fichier csv. 
- scrapcategory.py: programme qui permet de télécharger les données concernant une catégorie de livres et de les enregistrer dans un fichier csv.
- scrap.py: programme qui permet de télécharger les données de tous les livres du site "Books to Scrape" et de les enregistrer dans un fichier csv. Il permet également de télécharger et d'enregistrer les images de couverture des livres dans un fichier spécifique.

- utilities.py: ce fichier contient des fonctions communes nécessaires pour assurer le fonctionnement des trois programmes précédents.
- constants.py: contient les constantes des programmes.

#### Installation : 
1. Télécharger depuis GitHub les cinq fichiers cités. 
2. Créer un environnement virtuel avec la commande: python -m venv <environment_name>
3. Activer cet environnement avec la commande: 
        - sous Windows PowerShell: <environment_name>\Scripts\Activate.ps1
        - sous Linux:              source <environment_name>/bin/activate
4. Installer, dans cet environnement, les packages:
        - requests          commande: pip install requests
        - lxml              commande: pip install lxml
        - BeautifulSoup     commande: pip install beautifulsoup4

#### Exécution :
- Pour lancer le programme scrapbook.py: 
        * pour afficher à l'écran les donneés d'un livre, taper en ligne de commande: python scrapbook.py "url du livre"
        * pour enregistrer les donneés d'un livre, taper en ligne de commande: python scrapbook.py "url du livre" -s
        (Le nom du fichier est le titre du livre, sans la ponctuation.)
        * pour afficher l'aide, utiliser la commande:  python scrapbook.py -h
- Pour lancer le programme scrapcategory.py: 
        * pour afficher à l'écran les donneés d'une catégorie, taper en ligne de commande: python scrapcategory.py "url de la catégorie"
        * pour enregistrer les donneés d'une catégorie, taper en ligne de commande: python scrapcategory.py "url de la catégorie" -s 
         (Le nom du fichier est le nom de la catégorie, sans la ponctuation.)
        * pour afficher l'aide, utiliser la commande:  python scrapcategory.py -h
- Pour lancer le programme scrap.py taper la commande: python scrap.py 

* Remarque: la tabulation est utilisée comme séparateur dans les fichiers csv





