import requests
from bs4 import BeautifulSoup
import json


def liste_liens(page):
    # Construit l'URL de la page en ajoutant l'adresse de base du wiki
    adresse = "https://iceandfire.fandom.com/wiki/" + page

    # Envoie une requête GET pour récupérer le contenu HTML de la page
    r = requests.get(adresse)

    # Parse le contenu HTML à l'aide de BeautifulSoup
    soup = BeautifulSoup(r.content, 'html.parser')

    # Trouve la balise 'main' qui contient le contenu principal de la page
    main = soup.find('main')

    # Initialise la liste des liens
    liens = []

    # Parcourt toutes les balises 'a' (liens) dans le contenu principal de la page
    for a in main.find_all('a'):
        # Récupère la valeur de l'attribut 'href' (l'URL cible du lien)
        href = a.get('href')

        # Vérifie si le lien est interne au wiki (commence par '/wiki/')
        if href and href.startswith('/wiki/'):
            # Enlève le préfixe "/wiki/" et conserve uniquement le nom de la page cible
            lien = href[6:]

            # Filtre les liens indésirables contenant des ':' ou des '=' et élimine les liens vers la page elle-même
            if ':' not in lien and '=' not in lien and lien != page:
                # Ajoute le lien à la liste des liens
                liens.append(lien)

    # Retourne la liste des liens trouvés
    return liens


# print(liste_liens("Larence_Snow"))


def svg_disco(data, filename):
    # Ouvre le fichier en mode écriture
    with open(filename, 'w') as f:
        # Parcourt les éléments du dictionnaire 'data'
        for key, value in data.items():
            # Convertit la liste de valeurs en une chaîne de caractères séparée par des virgules
            value_str = ', '.join(value)

            # Écrit la clé et la chaîne de valeurs dans le fichier, séparées par un deux-points et un espace
            f.write(f'{key}: {value_str}\n')


# my_dict = {'key1': ['1', '2', '3'], 'key2': ['a', 'b', 'c']}
# svg_disco(my_dict, 'my_file.txt')


# Question 4 :


def chg_dico(filename):
    dico = {}
    key = ""
    value = []

    with open(filename, 'r') as f:
        # Lire chaque ligne du fichier
        for line in f:
            # Diviser la ligne en clé et valeur
            if ': ' in line:
                try:
                    key, value_str = line.strip().split(': ')
                    # Convertir la chaîne de caractères séparée par des virgules en une liste de valeurs
                    value = value_str.split(', ')
                    # Ajouter la paire clé-valeur au dictionnaire
                except ValueError:
                    key = line.strip().split(': ')[0]
                    value = []

            dico[key] = value

    return dico


# print(chg_dico("wiki.txt"))


def save_wiki():
    # initialisation de la liste de liens à visiter
    links_to_visit = ["Petyr_Baelish"]
    # initialisation du dictionnaire de liens visités
    visited_links = {"Petyr_Baelish": []}

    # tant qu'il reste des liens à visiter
    while links_to_visit:
        # récupération du premier lien de la liste
        link = links_to_visit.pop(0)

        # récupération des liens pointés par le lien courant
        links = liste_liens(link)

        # ajout des liens pointés à la liste de liens à visiter si ils ne sont pas déjà visités
        for l in links:
            if l not in visited_links:
                visited_links[l] = []
                links_to_visit.append(l)

        # ajout des liens pointés par le lien courant à la liste des liens visités
        visited_links[link] = links

    # sauvegarde du dictionnaire dans un fichier
    svg_disco(visited_links, "wiki.txt")


# save_wiki()

# Question 5 :


def plus_court_chemin(graph, depart, arrivee):
    # Initialisation
    file = [(depart, [depart])]
    visites = set()
    paths = []

    # Parcours en largeur
    while file:
        # Retirer un noeud de la file
        (node, chemin) = file.pop(0)

        # Si on est à la page d'arrivée
        if node == arrivee:
            paths.append((chemin, len(chemin)))

        # Si le noeud n'a pas déjà été visité
        if node not in visites:
            # Marquer le noeud comme visité
            visites.add(node)

            # Ajouter ses voisins à la file
            for voisin in graph.get(node, []):
                if voisin not in visites:
                    file.append((voisin, chemin + [voisin]))

    # Trier les chemins par longueur croissante
    paths = sorted(paths, key=lambda x: x[1])

    # Retourner les chemins et leurs longueurs
    return paths.__getitem__(0)[0]


print("PCC: ", plus_court_chemin(chg_dico("wiki.txt"), "Dorne", "Rhaego"))


# Question 6


def poids_voyelles(page):
    # Compte le nombre de caractères de la chaîne, en comptant les voyelles deux fois
    voyelles = 'aeiouyAEIOUY'
    poids = sum(2 if lettre in voyelles else 1 for lettre in page)
    return poids


def pcc_voyelles(source, cible):
    # Charge les données de wiki.txt dans un dictionnaire
    with open('wiki.txt') as f:
        data = {line.split(':')[0]: line.strip().split(':')[1].split(', ') for line in f}

    # Initialise les dictionnaires de distance et de prédécesseurs pour chaque page
    dist = {page: float('inf') for page in data}
    prev = {page: None for page in data}
    dist[source] = 0

    # Crée un ensemble de toutes les pages pour suivre les pages non visitées
    pages = set(data.keys())

    # Boucle principale de l'algorithme de Dijkstra
    while pages:
        # Trouve la page non visitée avec la distance minimale
        current = min(pages, key=lambda page: dist[page])

        # Si la distance minimale est infinie, il n'y a pas de chemin possible
        if dist[current] == float('inf'):
            break

        # Retire la page courante de l'ensemble des pages non visitées
        pages.remove(current)

        # Parcourt les liens de la page courante
        for link in data[current]:
            # Ignore les pages déjà visitées
            if link not in pages:
                continue

            # Calcule la distance alternative en utilisant la fonction poids_voyelles
            alt = dist[current] + poids_voyelles(link)

            # Met à jour la distance et le prédécesseur si la distance alternative est plus courte
            if alt < dist[link]:
                dist[link] = alt
                prev[link] = current

    # Reconstitue le chemin à partir des prédécesseurs
    chemin = []
    page = cible
    while page is not None:
        chemin.append(page)
        page = prev[page]
    chemin.reverse()

    # Retourne le chemin s'il est valide, sinon retourne None
    return chemin if chemin[0] == source else None


print("PPC (voyelles):", pcc_voyelles('Dorne', 'Rhaego'))


# Question 7 -----------


def get_family(page, fam_type):
    fam_list = []
    # send a GET request to the URL of the webpage
    url = "https://iceandfire.fandom.com/wiki/" + page
    response = requests.get(url)

    # parse the HTML content of the webpage
    soup = BeautifulSoup(response.content, "html.parser")

    # find all the HTML tags with a specific class name
    class_name = "pi-item pi-group pi-border-color pi-collapse pi-collapse-open"
    tags = soup.find_all(class_=class_name)

    # iterate through the tags and print their text content if they contain an h2 tag with inner text "Family"
    try:
        for tag in tags:
            if tag.find("h2", string="Family"):
                fam_tag = tag

        for lien in fam_tag.find("h3", string=fam_type).parent.find_all("a"):
            href = lien.get('href')
            fam_list.append(href[6:])

    except AttributeError:
        return []
    except UnboundLocalError:
        return []

    return fam_list


def save_family():
    # Use chg_disco method to get character data
    character_data = chg_dico("wiki.txt")

    # Initialize the character graph
    character_graph = {}

    # pour chaque personnage, on appelle la fonction get_family pour ses voisins
    for character, related_characters in character_data.items():
        # la valeur associée à chaque personnage est un autre dictionnaire
        character_graph[character] = {
            "Siblings": [],
            "Lover": [],
            "Children": [],
            "Father": [],
            "Mother": [],
            "Spouse": []
        }
        # en utilisant relationship_type comme clé pour ce dictionnaire imbriqué, on accéde à la valeur associée à ce
        # type de relation
        for relationship_type in character_graph[character].keys():
            # get_family retourne une list
            character_graph[character][relationship_type] = get_family(character, relationship_type)

    # Sauvegarder le graph sous fromat JSON
    with open("character_graph.json", "w") as file:
        json.dump(character_graph, file)


# save_family()

# Question 8 -------------------


def inceste_couple():
    # Charger le graphe des personnages
    with open("character_graph.json", "r") as file:
        character_graph = json.load(file)

    # Liste pour stocker les couples incestueux
    couples_inc = []

    # Parcourir tous les personnages du graphe
    for character in character_graph:
        # Vérifier si le personnage a des amants ou des conjoints
        lovers_and_spouses = character_graph[character]["Lover"] + character_graph[character]["Spouse"]

        # Parcourir tous les amants et les conjoints
        for partner in lovers_and_spouses:
            # Créez un ensemble pour vérifier rapidement si le partenaire appartient à l'une des relations incestueuses
            incestuous_relationships = set(character_graph[character]["Siblings"] +
                                           character_graph[character]["Children"] +
                                           character_graph[character]["Father"] +
                                           character_graph[character]["Mother"])

            # Vérifier les conditions d'inceste
            if partner in incestuous_relationships:
                # Ajouter le couple à la liste des couples incestueux (en évitant les doublons :("Character_A",
                # "Character_B") ou ("Character_B", "Character_A"))
                couple = tuple(sorted([character, partner]))
                if couple not in couples_inc:
                    couples_inc.append(couple)

    # retourne la liste des couples incestueux
    return couples_inc


# print("couple_incestueux:", inceste_couple())


# Question 9 -------------------


def descendant_graph():
    # Charger le graphe des personnages
    with open("character_graph.json", "r") as file:
        character_graph = json.load(file)

    # Créer un nouveau graphe pour stocker les relations de descendance
    descendance_graph = {}

    # Fonction récursive pour trouver les descendants d'un personnage
    def find_descendants(current_character, current_descendants):
        if current_character not in character_graph:  # Ajouter cette vérification
            return

        for child in character_graph[current_character]["Children"]:
            if child not in current_descendants:
                current_descendants.add(child)
                find_descendants(child, current_descendants)

    # Parcourir le graphe des personnages pour trouver les relations de descendance
    for character in character_graph:
        descendants = set()
        find_descendants(character, descendants)
        descendance_graph[character] = {"Descendants": list(descendants)}  # Modifier cette ligne

    # Sauvegarder le graphe de descendance dans un fichier
    with open("descendance_graph.json", "w") as file:
        json.dump(descendance_graph, file)

# descendant_graph()
