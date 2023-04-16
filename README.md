# Ice-and-Fire-Wiki-Crawler
Ce projet est un web crawler pour le wiki d'A Song of Ice and Fire (https://iceandfire.fandom.com). L'objectif est d'explorer les pages de ce wiki pour en extraire des informations sur les personnages et les relations entre eux. Le projet utilise la bibliothèque Requests pour effectuer des requêtes HTTP et BeautifulSoup pour analyser le contenu HTML des pages.

# Fonctionnalités : 
Le projet offre les fonctionnalités suivantes :

* Récupération des liens entre les pages de personnages.
* Sauvegarde des liens et des relations entre les personnages dans un fichier texte et un fichier JSON.
* Calcul du plus court chemin entre deux personnages en utilisant l'algorithme de Dijkstra.
* Implémentation d'une version modifiée de l'algorithme de Dijkstra pour prendre en compte le poids des voyelles dans les noms de pages.
* Extraction des informations sur la famille des personnages (parents, conjoints, enfants, etc.).
* Détection des couples incestueux.
* Construction d'un graphe de descendance pour chaque personnage.
# Utilisation :
Le projet peut être utilisé pour explorer les relations complexes entre les personnages d'A Song of Ice and Fire et analyser les liens familiaux et les alliances politiques. Il peut également servir de base pour des projets futurs impliquant l'analyse de réseaux sociaux ou l'étude de la structure narrative de la série.
