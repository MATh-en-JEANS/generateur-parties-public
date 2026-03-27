# Générateur de Parties

Ce dépôt contient une version publique et simplifiée du simulateur de partage de gâteau.

L'idée générale est la suivante :

- un gâteau est représenté par une suite de goûts ;
- chaque joueur a un score associé à chaque goût ;
- au fil de la partie, les joueurs accumulent un score temporaire ;
- les joueurs peuvent décider de dire `STOP` pour conserver la part en cours.

Cette version a surtout un objectif pédagogique : elle permet de lire le code, de comprendre le modèle et de lancer une simulation simple sans dépendances externes.

## À quoi sert le script

Le script `generateurParties.public.v1.0.py` permet de :

- générer un gâteau aléatoire ;
- générer aléatoirement les goûts des joueurs ;
- simuler une partie avec une stratégie commune ;
- afficher les étapes de la partie dans le terminal ;
- mesurer deux indicateurs simples en fin de partie.

Les deux valeurs renvoyées à la fin d'une simulation sont :

- le ratio moyen `score / scoreMax` ;
- la proportion de joueurs ayant atteint une part jugée équitable.

## Installation

Le script ne dépend d'aucune bibliothèque externe.

Prérequis :

- Python 3.10 ou plus récent.

## Lancement rapide

Depuis le dossier du projet, lance :

```bash
python generateurParties.public.v1.0.py
```

Le script affiche ensuite :

```text
Partie / Etude
(P/E) :
```

Dans cette version :

- `P` lance une partie affichée étape par étape ;
- `E` correspond à une partie laissée très simple dans cette version.

## Comment fonctionne le modèle

### 1. Le gâteau

Le gâteau est une liste de goûts, par exemple :

```python
['V', 'V', 'C', 'N', 'F']
```

Chaque lettre représente un goût.  
La variable `gouts` définit les goûts disponibles, et `longueur` définit la taille du gâteau.

### 2. Les joueurs

Chaque joueur possède :

- un identifiant ;
- un dictionnaire `gouts` associant un score à chaque goût ;
- un `scoreMax`, c'est-à-dire le meilleur score théorique qu'il pourrait atteindre ;
- un `scoreCible`, utilisé par la stratégie ;
- un `scorePartActuelle`, qui suit la valeur de la part en cours ;
- un booléen `stop`, qui indique si le joueur s'est déjà arrêté.

### 3. La partie

La simulation suit ce principe :

1. on génère un gâteau ;
2. on génère les joueurs et leurs goûts ;
3. on parcourt le gâteau part par part ;
4. à chaque étape, les joueurs encore en jeu mettent à jour leur score temporaire ;
5. selon la stratégie, certains peuvent dire `STOP` ;
6. si plusieurs joueurs disent `STOP`, un seul est choisi aléatoirement ;
7. la partie continue jusqu'à la fin du gâteau.

## Paramètres principaux

Au début du fichier generateurParties.public.v1.0.py, plusieurs paramètres peuvent être modifiés :

- `gouts` : la liste des goûts disponibles ;
- `longueur` : la longueur du gâteau ;
- `nbJoueur` : le nombre de joueurs ;
- `rangeScore` : l'intervalle des scores attribués aux goûts.

## Fonctions importantes

Voici les fonctions les plus utiles à connaître :

- `genererGateau(...)` : construit un gâteau aléatoire ;
- `genererGouts(...)` : attribue un score à chaque goût pour un joueur ;
- `calculScoreMax(...)` : calcule le meilleur score théorique atteignable ;
- `stopPartRestanteNegative(...)` : teste si la suite restante peut encore améliorer un score ;
- `strategies(...)` : décide si un joueur doit dire `STOP` ;
- `partie(...)` : exécute une simulation complète.

Les autres fonctions servent à l'affichage dans le terminal.

## Ce qui est simplifié dans cette version

Cette version a été pensée pour être montrable et compréhensible plus facilement.  
Elle simplifie donc plusieurs aspects :

- tous les joueurs utilisent la même stratégie ;
- l'affichage est très présent pour aider à suivre la simulation ;
- la partie "étude" est volontairement réduite ;
- le script reste volontairement simple et centré sur la simulation de base.

## Limites connues

Quelques points sont à garder en tête :

- l'affichage utilise des couleurs ANSI, ce qui dépend du terminal ;
- les noms de variables et de fonctions sont en français ;
- cette version privilégie la lisibilité à la généralisation.

## Pour aller plus loin

Si tu veux faire évoluer le projet, les pistes les plus naturelles sont :

- ajouter plusieurs stratégies de joueurs ;
- séparer encore plus la logique métier de l'affichage ;
- ajouter des tests unitaires ;
- exporter les résultats des simulations ;
- comparer plusieurs nombres de joueurs et plusieurs plages de scores.

## Résumé

Ce projet est une bonne porte d'entrée si tu veux :

- comprendre rapidement le fonctionnement du modèle ;
- lire un script de simulation sans dépendances ;
- montrer le projet à quelqu'un d'autre ;
- expérimenter ensuite tes propres variantes du modèle.

> Le README a été rédigé par Codex et relu par notre groupe 😁, le reste du code est 100% fait main par notre groupe. Passez une bonne journée
