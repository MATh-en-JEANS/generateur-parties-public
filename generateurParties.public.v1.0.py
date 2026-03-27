from random import randint, choice, randrange
from typing import List, Dict

# Ce fichier est la version publique du code. Pour faciliter la compréhension, tous les joueurs utilisent la même stratégie et quelques parties ont été simplifiées.

'''
Ce fichier permet de générer et de simuler une partie.
Le gâteau et les scores associés aux goûts sont générés aléatoirement.
Les "joueurs" décident de dire STOP en fonction des stratégies à implémenter lors de leur création et dans la fonction "strategies()".
La simulation est en quatre étapes :
    Étape 1 : On génère un gâteau aléatoire en fonction des goûts et de la longueur fournis.
    Étape 2 : On génère les goûts des joueurs en fonction des goûts, du score minimum et du score maximum.
    Étape 3 : Valeur de gâteau par valeur de gâteau, les joueurs ont l'opportunité de dire STOP.
    Étape 4 : On affiche le ratio du score obtenu par rapport au score maximal possible (score/scoreMax), et le pourcentage de joueurs ayant atteint une part équitable (scoreMax/nbJoueur).
'''

gouts = ['V', 'C', 'N', 'F']        # Les goûts utilisés dans le gâteau (privilégiez des lettres pour plus de clarté).
longueur = 100                      # Taille (nombre de valeurs) du gâteau
nbJoueur = 4                        # Nombre de joueurs dans la partie
rangeScore = [-5, 10]               # Le score minimum et le score maximum pouvant être associés à un goût

class Joueur:
    '''
    La classe Joueur permet de représenter les joueurs d'une partie.
    '''
    __slots__ = ('id', 'gouts', 'scoreMax', 'scoreCible', 'score', 'scorePartActuelle', 'stop')
    def __init__(self, id : int, gouts : dict, scoreMax : int, scoreCible : float) -> None:
        self.id = id
        self.gouts = gouts
        self.scoreMax = scoreMax
        self.score = 0
        self.scorePartActuelle = 0
        self.scoreCible = scoreCible
        self.stop = False

#### ---- AFFICHAGE ---- ####

def printGateau(gateau : List[str]) -> dict[str, str]:
    '''
    Affiche le gâteau. Chaque part est affichée par un |. Les goûts sont différenciés par leur couleur (ne fonctionne que pour moins de 10 goûts)

    :param gateau: La liste représentant le gâteau à afficher
    :return: Renvoie le dictionnaire associatif entre les goûts et leur couleur, permettant de garder une cohérence
    '''
    # La liste des couleurs
    listCouleur = [
        '\033[31m', '\033[32m', '\033[33m', '\033[34m', '\033[35m',
        '\033[36m', '\033[37m', '\033[38m', '\033[39m', '\033[30m'
        ]
    # Un dictionnaire permettant d'associer un goût à l'indice de sa couleur
    listGoutsTrouve = {}
    # L'indice à associer
    index = 0
    # Pour chaque part de gâteau
    for part in gateau:
        # Si la part est un goût qui n'a pas encore été associé à un indice
        if not(part in listGoutsTrouve):
            # On l'associe
            listGoutsTrouve[part] = listCouleur[index%10]
            index += 1
        # Puis on affiche la part avec sa couleur
        print(listGoutsTrouve[part], end='')
        print('|', end='')
    # On rétablit le terminal à ses couleurs normales
    print("\033[0m")

    return listGoutsTrouve

def printGoutsJoueur(listJoueur : List[Joueur], dicCouleursGouts : dict[str, str]) -> None:
    '''
    Permet d'afficher le tableau d'association entre goûts et score
    
    :param listJoueur : La liste des objets Joueur
    :param dicCouleurGouts : Le dictionnaire d'association entre goûts et couleurs
    '''

    def grosseLigne(tailleHorizontale : int) -> None:
        '''
        Affiche les lignes de début et de fin de tableau
        '''
        for _ in range(tailleHorizontale-1):
            print("#", end='')
        print("#")

    def ligneSeparation(tailleHorizontale : int, tailleMax : int) -> None:
        '''
        Affiche les lignes de séparation pour les lignes du tableau
        '''
        print("#", end='')
        for i in range(tailleHorizontale-2):
            if (i>=5 and (i-5)%(tailleMax+3)==0):
                print("+", end='')
            else:
                print("-", end='')
        print("#")

    def tailleCaseCalcul(listJoueur : List[Joueur]) -> int:
        '''
        Permet de calculer la taille des cases nécessaires
        '''
        dicGoutJ1 = listJoueur[0].gouts
        tailleMax = len("J\\G")
        # On regarde d'abord avec les goûts
        for gout in dicGoutJ1:
            if len(gout)>tailleMax:
                tailleMax = len(gout)

        # Puis pour chaque joueur, pour les scores de goûts
        for joueur in listJoueur:
            dicGouts = joueur.gouts
            for gout in dicGouts:
                if len(str(dicGouts[gout])) > tailleMax:
                    tailleMax = len(str(dicGouts[gout]))

        return tailleMax

    def afficherLigneGouts(idJoueur : int, dicGouts : dict, tailleCase : int) -> None:
        ''''
        S'occupe d'afficher les lignes correspondant aux scores des goûts
        '''
        # On affiche tout d'abord l'id du joueur
        print("#\033[32m", end='')
        printCase(idJoueur, tailleCase)
        print("\033[0m|", end='')

        # Puis, on affiche les goûts
        for i, gout in enumerate(dicGouts):
            printCase(dicGouts[gout], tailleCase)

            if i != len(dicGouts)-1:
                print("|", end='')
            else:
                print("#")

    # On regarde quelle taille doivent avoir les cases horizontalement
    tailleMax = tailleCaseCalcul(listJoueur)

    # On récupère la longueur horizontale
    nbGout = len(listJoueur[0].gouts)
    tailleHorizontale = 7 + nbGout*(tailleMax+3)

    # On affiche la 1ère ligne
    grosseLigne(tailleHorizontale)

    # La taille (horizontale) des cellules du tableau
    tailleCase = tailleMax+2

    # On affiche la 1ère ligne, présentant les goûts
    print("# J\\G |", end='')
    for i, gout in enumerate(listJoueur[0].gouts):
        print(dicCouleursGouts[gout], end='')
        printCase(gout, tailleCase)
        print("\033[0m", end='')

        # On affiche la fin, | s'il y en a après, # sinon
        if i ==len(listJoueur[0].gouts)-1:
            print("#")
        else:
            print("|", end='')

    # On affiche la ligne de séparation
    ligneSeparation(tailleHorizontale, tailleMax)

    # On affiche pour chaque joueur ses goûts
    for i, joueur in enumerate(listJoueur):
        afficherLigneGouts(i, joueur.gouts, tailleCase)

        if i!=len(listJoueur)-1:
            ligneSeparation(tailleHorizontale, tailleMax)

    grosseLigne(tailleHorizontale)

def printScore(listJoueur : list) -> None:
    '''
    Affiche les scores des joueurs
    
    :param listJoueur : La liste des objets joueur
    '''
    def printLong(tailleCase):
        for i in range(3*tailleCase+4):
            print("#", end='')
        print("#")

    def printDebut(tailleCase):
        print("#", end='')
        printCase("ID Joueur", tailleCase)
        print("|", end='')
        printCase("Score", tailleCase)
        print("|", end='')
        printCase("Ratio", tailleCase)
        print("#")

    def printInter():
        print("#", end='')
        for i in range(11):
            print("-", end='')
        print("+", end='')
        for j in range(11):
            print("-", end='')
        print("+", end='')
        for j in range(11):
            print("-", end='')
        print("#")

    tailleCase = 11

    printLong(tailleCase)
    printDebut(tailleCase)
    printInter()

    for i, joueur in enumerate(listJoueur):
        print("#", end ='')
        id = joueur.id
        printCase(id, tailleCase)
        print("|", end='')

        printCase(joueur.score, tailleCase)
        print("|", end='')
        ratio = str((joueur.score/joueur.scoreMax)*100)[:4]+" %"
        printCase(ratio, tailleCase)
        print("#")
        if i < len(listJoueur)-1:
            printInter()
        else:
            printLong(tailleCase)

def printCase(chose : str | list, tailleCase : int) -> None:
    '''
    Cette fonction sert à l'affichage. S'il y a besoin d'afficher une donnée dans une case, alors on la met au milieu

    :param chose: La donnée à afficher dans la case
    :param tailleCase: La taille de la case dans laquelle afficher la donnée
    '''
    # S'il y a la possibilité d'avoir des couleurs, la taille devra être calculée avant
    if isinstance(chose, str):
        choseTaille = len(enleveCouleur(chose))
    else:
        choseTaille = len(str(chose))

    chose = str(chose)
    positionMilieu = (tailleCase-choseTaille)//2
    for i in range(positionMilieu):
        print(" ", end='')
    print(chose, end='')
    for i in range(positionMilieu+choseTaille, tailleCase):
        print(" ", end='')

def plusLong(listJoueur : list, listGouts : list):
    '''
    Permet de déterminer la taille des cases du tableau des étapes

    :param gateau: Le gâteau. Il sert à calculer la longueur de la plus grande part simplifiée théorique
    :param listJoueur: La liste des joueurs
    :param listGouts: La liste des goûts
    '''

    tailleMax = 15 # Une taille minimale de 15 permet de bien lire et surtout d'afficher les parts à chaque tour
    for joueur in listJoueur:
        if len(str(joueur.id))>tailleMax:
            tailleMax = len(str(joueur.id))

    for gout in listGouts:
        if len(gout)>tailleMax:
            tailleMax =len(gout)

    return tailleMax+2 # Prend en compte les espaces sur les côtés

def enleveCouleur(part : str) -> str:
    '''
    Pour l'affichage, permet d'enlever la partie couleur d'une chaîne de caractères

    :param part: Le string à modifier
    :return: Donne le string sans couleur
    '''
    novPart = []
    i = 0
    while i < len(part):
        # Si part[i] est le début d'une couleur
        if part[i] == '\033' and i + 1 < len(part) and part[i+1] == '[':
            # Alors on la saute
            while i < len(part) and part[i] != 'm':
                i += 1
            i += 1
        # Sinon, on l'ajoute à la nouvelle partie
        else:
            novPart.append(part[i])
            i += 1

    # On renvoie la nouvelle part
    return ''.join(novPart)

def simplifiePart(anciennePart: str, ajout: str, dictAssociatifGoutsCouleurs: dict) -> str:
    '''
    Permet d'ajouter la nouvelle part à la part actuelle (version simplifiée)
    Ex : 3N2C + C = 3N3C
    Chaque ensemble nombre+goût est coloré selon dictAssociatifGoutsCouleurs.

    :param anciennePart: L'ancienne part (peut contenir des codes couleur ANSI)
    :param ajout: La nouvelle part à ajouter (ex: "C")
    :param dictAssociatifGoutsCouleurs: Dictionnaire associant chaque goût à une couleur ANSI
    :return: La nouvelle part simplifiée, avec chaque segment coloré
    '''

    # On enlève les couleurs pour travailler sur le texte brut
    anciennePart_sans_couleur = enleveCouleur(anciennePart)

    # Cas particulier : si l'ancienne part est vide
    if not anciennePart_sans_couleur:
        couleur = dictAssociatifGoutsCouleurs.get(ajout, "")
        return f"{couleur}1{ajout}\033[0m"

    # On récupère le dernier goût
    dernierGout = anciennePart_sans_couleur[-1]

    if dernierGout == ajout:
        # On extrait le nombre avant le dernier goût
        i = len(anciennePart_sans_couleur) - 2
        nombre = ""
        while i >= 0 and anciennePart_sans_couleur[i].isdigit():
            nombre = anciennePart_sans_couleur[i] + nombre
            i -= 1
        # On incrémente le nombre
        if nombre:
            nombre = str(int(nombre) + 1)
            # On reconstruit la chaîne
            debut = anciennePart_sans_couleur[:i+1]
            # On réapplique les couleurs à chaque segment
            result = []
            i = 0
            while i < len(debut):
                if i < len(debut) and debut[i].isdigit():
                    j = i
                    while j < len(debut) and debut[j].isdigit():
                        j += 1
                    if j < len(debut):
                        gout = debut[j]
                        couleur = dictAssociatifGoutsCouleurs.get(gout, "")
                        result.append(f"{couleur}{debut[i:j+1]}\033[0m")
                        i = j + 1
                    else:
                        break
                else:
                    i += 1
            # On ajoute le dernier segment incrémenté
            couleur = dictAssociatifGoutsCouleurs.get(dernierGout, "")
            result.append(f"{couleur}{nombre}{dernierGout}\033[0m")
            return "".join(result)
        else:
            # Cas où il n'y a pas de nombre (ex: "N" + "N" -> "2N")
            couleur = dictAssociatifGoutsCouleurs.get(dernierGout, "")
            return f"{couleur}2{dernierGout}\033[0m"
    else:
        # On ajoute le nouveau goût avec 1, en colorant chaque segment
        result = []
        i = 0
        while i < len(anciennePart_sans_couleur):
            if i < len(anciennePart_sans_couleur) and anciennePart_sans_couleur[i].isdigit():
                j = i
                while j < len(anciennePart_sans_couleur) and anciennePart_sans_couleur[j].isdigit():
                    j += 1
                if j < len(anciennePart_sans_couleur):
                    gout = anciennePart_sans_couleur[j]
                    couleur = dictAssociatifGoutsCouleurs.get(gout, "")
                    result.append(f"{couleur}{anciennePart_sans_couleur[i:j+1]}\033[0m")
                    i = j + 1
                else:
                    break
            else:
                i += 1
        # On ajoute le nouvel ajout
        couleur = dictAssociatifGoutsCouleurs.get(ajout, "")
        result.append(f"{couleur}1{ajout}\033[0m")
        return "".join(result)

def simplifieGateau(gateau  : list) -> str:
    '''
    Permet de simplifier le gâteau par un compte des goûts
    Ex : NNNCCVVVVNN -> 3N2C4V2N

    :param gateau: Le gâteau à simplifier
    :type gateau: list
    '''
    nombre = 0
    dernierePart = gateau[0]
    gateauSimplifie = ""
    # Pour chaque partie du gâteau
    for part in gateau:
        # Si la part est la même, alors on augmente son nombre
        if part == dernierePart:
            nombre += 1

        # Sinon, on l'enregistre
        else:
            gateauSimplifie += str(nombre) + dernierePart
            dernierePart = part
            nombre = 1

    return gateauSimplifie

def printSeparation(tailleCase : int, nbJoueur : int) -> None:
    '''
    Affiche une séparation entre chaque ligne en fonction du nombre de joueurs
    '''
    print("#", end='')
    # On met une séparation pour chaque case (nbJoueur + case de la part)
    for i in range(nbJoueur+1):
        # Pour la taille des cases
        for j in range(tailleCase):
            print("-", end='')
        if i < nbJoueur:
            print("+", end='')
        else:
            print("#")

def printEtape(listJoueur : list, listStop : list, partActuelleOriginal : str, tailleCase : int, nbJoueur : int) -> None:
    '''
    Affiche chaque étape de la partie. C'est-à-dire la part en jeu et les scores.
    
    :param listJoueur : La liste des objets Joueur représentant les joueurs
    :param listStop : La liste des joueurs s'étant arrêtés
    :param partActuelleOriginal : La part en jeu ayant encore les couleurs
    :param tailleCase : La taille des cellules du tableau
    :param nbJoueur : Le nombre de joueurs (et donc le nombre de cellules)
    :return: None
    '''
    # On affiche d'abord la séparation
    printSeparation(tailleCase, nbJoueur)

    # Si la part actuelle est plus grande que la case, on la réduit
    partSimple = enleveCouleur(partActuelleOriginal)
    vraiTaille = len(partSimple)
    if vraiTaille>(tailleCase - 2):
            partActuelle = "..." + partSimple[-(tailleCase-5):]
    else:
        partActuelle = partActuelleOriginal

    print("#", end='')
    printCase(partActuelle, tailleCase)
    print("|", end='')
    listIdRestant = []

    # Pour chaque joueur
    for i, joueur in enumerate(listJoueur):
        # S'ils ont dit Stop par le passé, on remplace leur score par '/'
        if joueur.stop:
            printCase("/", tailleCase)
            if i < len(listJoueur)-1:
                print("|", end='')

        # Sinon, on affiche leur score
        else:
            # S'ils ont dit Stop, alors on affiche leur score en rouge
            if i in listStop:
                print("\033[31m", end='')
                printCase(joueur.scorePartActuelle, tailleCase)
                print("\033[0m", end='')

            # Sinon, on affiche juste leur score
            else:
                printCase(joueur.scorePartActuelle, tailleCase)

            # En fonction de si l'on est au bout du tableau ou non
            if i < len(listJoueur)-1:
                print("|", end='')
    print("#")

def grandeLigne(tailleCase : int, nbJoueur : int) -> None:
    '''
    Sert à afficher les grandes lignes dépendant du nombre de joueurs
    
    :param tailleCase : La taille des cellules
    :param nbJoueur : Le nombre de joueurs (donc de cases)
    '''
    nbJoueur += 1   # On affiche aussi la case pour la part
    tailleCase += 1 # On prend en compte les lignes de séparations verticales
    for i in range((tailleCase*nbJoueur)):
        print("#", end='')
    print("#")

def premLigne(tailleCase : int, listJoueur : list) -> None:
    '''
    Affiche la première ligne de la partie
    
    :param tailleCase : la taille de la case
    :param listJoueur : la liste des joueurs
    '''
    print("# Parts \\ Joueurs |", end='')
    for i, joueur in enumerate(listJoueur):
        printCase(joueur.id, tailleCase)
        if i < len(listJoueur)-1:
            print("|", end='')
        else:
            print("#")

def printScoreMax(tailleCase : int, listJoueur : list) -> None:
    '''
    Affiche le score max
    
    :param tailleCase : La taille des cases
    :param listJoueur : La liste des joueurs, pour en récupérer le nombre et les scores max
    '''
    print("#\033[32m", end='')
    printCase("Score Max :", tailleCase)
    print("\033[0m|", end='')
    for i, joueur in enumerate(listJoueur):
        print("\033[32m", end='')
        printCase(joueur.scoreMax, tailleCase)
        print("\033[0m", end='')
        if i < len(listJoueur)-1:
            print("|", end='')
        else:
            print("#")

def printScoreCible(tailleCase : int, listJoueur : list) -> None:
    '''
    Affiche le score ciblé
    
    :param tailleCase : La taille des cellules
    :param listJoueur : 
    '''
    print("#\033[31m", end='')
    printCase("Score Cible :", tailleCase)
    print("\033[0m|", end='')
    for i, joueur in enumerate(listJoueur):
        print("\033[31m", end='')
        printCase(joueur.scoreCible, tailleCase)
        print("\033[0m", end='')
        if i < len(listJoueur)-1:
            print("|", end='')
        else:
            print("#")


#### ---- Parties ---- ####

def genererGouts(listGouts: list, scoreMin: int, scoreMax: int) -> dict:
    '''
    Génère un dictionnaire associant à chaque goût un score aléatoire dans [scoreMin, scoreMax],
    en garantissant qu'au moins un goût a un score strictement positif.

    :param listGouts: Liste des goûts (str).
    :param scoreMin: Score minimal possible (inclus).
    :param scoreMax: Score maximal possible (inclus).
    :return: Dictionnaire {goût: score}.
    :raises ValueError: Si scoreMax < 1.
    '''
    if scoreMax < 1:
        raise ValueError("Le score maximal doit être au moins 1 pour garantir un goût positif.")

    dicScore = {}
    positif = False

    for gout in listGouts:
        dicScore[gout] = randint(scoreMin, scoreMax)
        while(dicScore[gout]==0):
            dicScore[gout] = randint(scoreMin, scoreMax)
        if dicScore[gout]>0:
            positif = True
    
    if not positif:
        goutRand = choice(listGouts)
        dicScore[goutRand] = 0-dicScore[goutRand]

    return dicScore

def genererGateau(nbLongueur: int, listGouts: list, v) -> list:
    '''
    Génère un gâteau (liste) de longueur donnée, contenant tous les goûts possibles au moins une fois,
    sauf si la longueur est insuffisante.

    :param nbLongueur: Longueur souhaitée pour le gâteau.
    :param listGouts: Liste des goûts disponibles.
    :return: Liste représentant le gâteau.
    :raises ValueError: Si la liste des goûts est vide ou si la longueur est inférieure à 1.
    '''
    if not listGouts:
        raise ValueError("La liste des goûts est vide.")
    if nbLongueur < 1:
        raise ValueError("Le gâteau doit avoir au moins 1 valeur.")

    # Si la longueur est insuffisante pour tous les goûts, retourne un gâteau aléatoire
    if nbLongueur < len(listGouts):
        return [choice(listGouts) for _ in range(nbLongueur)]

    # Sinon, génère un gâteau contenant tous les goûts
    while True:
        gateau = []
        gouts_presents = set()
        gouts_restants = listGouts.copy()

        # Ajoute le premier goût
        gout = choice(gouts_restants)
        gateau.append(gout)
        gouts_presents.add(gout)
        gouts_restants.remove(gout)

        # Remplit le reste du gâteau
        for _ in range(1, nbLongueur):
            prob_changement = max(round(v * nbLongueur), 6)
            if randrange(prob_changement) == 0 and gouts_restants:
                gout = choice(gouts_restants)
                gouts_presents.add(gout)
                gouts_restants.remove(gout)
            else:
                gout = choice(listGouts)
            gateau.append(gout)

        # Vérifie si tous les goûts sont présents
        if all(g in gateau for g in listGouts):
            return gateau

def calculScoreMax(gateau: list, gouts: dict) -> int:
    '''
    Calcule le score maximal qu'un joueur peut obtenir en additionnant les parts consécutives de même signe,
    puis en appliquant l'algorithme de Kadane sur les sous-séquences obtenues.

    :param gateau: Liste représentant les parts du gâteau.
    :param gouts: Dictionnaire associant chaque part à son score pour le joueur.
    :return: Score maximal possible.
    '''
    if not gateau:
        return 0

    # 1. Calcul des sous-séquences de même signe
    sous_sequences = []
    current_sum = 0
    current_signe = (gouts[gateau[0]] > 0)

    for part in gateau:
        signe = (gouts[part] > 0)
        if signe == current_signe:
            current_sum += gouts[part]
        else:
            sous_sequences.append(current_sum)
            current_sum = gouts[part]
            current_signe = signe
    sous_sequences.append(current_sum)  # Ajoute la dernière sous-séquence

    # 2. Algorithme de Kadane sur les sous-séquences
    max_actuel = max_global = sous_sequences[0]
    for val in sous_sequences[1:]:
        max_actuel = max(val, max_actuel + val)
        max_global = max(max_global, max_actuel)

    return max_global

def stopPartRestanteNegative(partRestante : list , gouts : list) -> bool:
    '''
    Permet de déterminer si une part a une chance d'augmenter le score
    
    :param partRestante: La part à tester
    :param gouts: Les scores associés aux goûts, propres aux joueurs
    :return: False si la part peut augmenter le score, True sinon
    :rtype: bool
    '''
    score = 0
    # On ajoute chaque partie au score
    for element in partRestante:
        score += gouts[element]
        # Si à un moment il est positif, alors on return False
        if score > 0:
            return False
    return True

def strategies(joueur: Joueur, nbJoueur : int, gateau : list, positionActuelle : int, nbJoueurFinit : int, v : float, choixStratégie : int) -> bool:
    '''
    La fonction renvoie True si, d'après les stratégies du joueur, le joueur doit dire STOP.
    La stratégie actuelle est de dire STOP si l'on n'est pas le dernier joueur et que :
        - Il ne sera pas possible d'obtenir un score aussi grand que celui actuel si un joueur venait à dire STOP maintenant
        - Le ratio "d'équité" est atteint (ex : 25% du score Max si 4 joueurs)
    '''
    
    # Règle 3
    if choixStratégie == 1:
        if nbJoueur == nbJoueurFinit + 1: # SI on est le dernier
            return stopPartRestanteNegative(gateau[positionActuelle:], joueur.gouts)
        
    # Règle 1
    if joueur.scorePartActuelle >= joueur.scoreCible:
        return True
    return False

def partie(longueur : int, gouts : list, nbJoueur : int=4, rangeScore : list=[-5, 10], affichage : bool=False, v : float=1, choixStratégie : int=1):
    # v sert en vue de test
    # On génère le gâteau
    gateau = genererGateau(longueur, gouts, 1)

    if affichage:
        print("\033[32mÉtape 1 : Générer le gâteau\033[0m")
        dicAssociatifGoutCouleur = printGateau(gateau)

    # On génère les joueurs
    listJoueur = []
    for i in range(nbJoueur):
        goutsJoueur = genererGouts(gouts, rangeScore[0], rangeScore[1])
        scoreMaxJoueur = calculScoreMax(gateau, goutsJoueur)
        scoreCibleJoueur = scoreMaxJoueur*v
        listJoueur.append(Joueur(i, goutsJoueur, scoreMaxJoueur, scoreCibleJoueur))

    # On affiche le tableau des scores
    if affichage:
        print("\n\033[32mÉtape 2 : Générer les goûts des joueurs\033[0m")
        printGoutsJoueur(listJoueur, dicAssociatifGoutCouleur) # type: ignore

        # Il faudra afficher les étapes
        tailleCase = plusLong(listJoueur, gouts)
        print("\n\033[32mÉtape 3 : Effectuer la partie\033[0m", flush = True)
        partActuelleSimplifie = ""
        grandeLigne(tailleCase, nbJoueur)
        premLigne(tailleCase, listJoueur)
        printSeparation(tailleCase, nbJoueur)
        printScoreMax(tailleCase, listJoueur)
        printSeparation(tailleCase, nbJoueur)
        printScoreCible(tailleCase, listJoueur)

    joueurFini = 0

    # La partie commence
    for i, part in enumerate(gateau):
        stop = False # Permet de tester s'il y a des STOP
        # Pour chaque étape, on ajoute la part actuelle aux joueurs et on récupère les IDs des joueurs disant STOP, pour plus tard les choisir aléatoirement
        listIdJoueurStop = []
        for j, joueur in enumerate(listJoueur):
            # On ne prend en compte que les joueurs qui n'ont pas déjà dit Stop
            if not joueur.stop:
                joueur.scorePartActuelle += joueur.gouts[part]
                if strategies(joueur, nbJoueur, gateau, i, joueurFini, v, choixStratégie):
                    listIdJoueurStop.append(joueur.id)
                    stop = True

        if affichage:
            # On affiche l'étape actuelle
            partActuelleSimplifie = simplifiePart(partActuelleSimplifie, part, dicAssociatifGoutCouleur) # type: ignore
            printEtape(listJoueur, listIdJoueurStop, partActuelleSimplifie, tailleCase, nbJoueur) # type: ignore

        # S'il y en a qui s'arrête
        if stop:
            if affichage:
                # On supprime la part simplifiée
                partActuelleSimplifie = ""

            # On récupère l'ID du joueur qui s'arrêtera
            idStop = choice(listIdJoueurStop)

            # On dit au joueur désigné qu'il a gagné le pile ou face
            listJoueur[idStop].stop = True
            listJoueur[idStop].score = listJoueur[idStop].scorePartActuelle
            joueurFini += 1
            
            # On réinitialise les parts
            for joueur in listJoueur:
                joueur.scorePartActuelle = 0

    # Lorsque l'on arrive au bout du gâteau, on attribue la part aléatoirement (s'il reste un joueur et qu'il s'agit d'une part positive)
    if nbJoueur>joueurFini:
        # On récupère la liste des joueurs pour qui cette part est positive (sinon il perdrait encore plus)
        listePositif = []
        for i, joueur in enumerate(listJoueur):
            if (not joueur.stop) and (joueur.scorePartActuelle>0):
                listePositif.append(i)

        # S'il y en a, alors on en prend un
        if len(listePositif)>0:
            idChanceux = choice(listePositif)
            listJoueur[idChanceux].stop = True
            listJoueur[idChanceux].score = listJoueur[idChanceux].scorePartActuelle

    if affichage:
        grandeLigne(tailleCase, nbJoueur) # type: ignore
        # Puis, on affiche les scores
        print("\n\033[32mÉtape 4 : Afficher les scores finaux\033[0m")
        printScore(listJoueur)

    # Calcul de la moyenne des scores
    total = 0
    for joueur in listJoueur:
        ratio = joueur.score/joueur.scoreMax
        total += ratio
    
    # On regarde les joueurs ayant atteint leur objectif
    equitable = 0
    for joueur in listJoueur:
        if joueur.score > joueur.scoreMax/nbJoueur:
            equitable += 1

    return total/nbJoueur, equitable/nbJoueur

if __name__=='__main__':
    print("Partie / Etude")
    choix = input("(P/E) : ").strip()

    # Partie
    if choix == 'P':
        '''On génère une partie aléatoire en affichant les étapes'''
        print(partie(longueur, gouts, nbJoueur, rangeScore, True, v=(1/nbJoueur), choixStratégie=1))

    # Etude
    if choix == 'E':
        '''Cette partie permet de faire des tests.'''
