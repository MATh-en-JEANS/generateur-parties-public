# Générateur de Parties

Ce projet contient une version publique et simplifiée d'un simulateur de partage de gâteau.  
Le script principal, `generateurParties.public.v1.0.py`, génère un gâteau aléatoire, crée des profils de joueurs, puis simule leurs décisions de dire `STOP` selon une stratégie commune.

## Idée du modèle

Le gâteau est représenté par une liste de goûts, par exemple `["V", "F", "C", "N"]`.

Chaque joueur reçoit :

- un dictionnaire de scores associé aux goûts ;
- un `scoreMax`, c'est-à-dire le meilleur score théorique qu'il pourrait atteindre ;
- un `scoreCible`, utilisé par la stratégie pour décider quand s'arrêter.

Pendant la partie :

- on parcourt le gâteau part par part ;
- chaque joueur encore en jeu cumule le score de la part courante ;
- certains joueurs peuvent dire `STOP` ;
- si plusieurs joueurs disent `STOP` en même temps, un seul est choisi aléatoirement.

En fin de simulation, le programme renvoie :

- le ratio moyen `score / scoreMax` ;
- la proportion moyenne de joueurs ayant atteint une part jugée équitable.

## Lancer le script

Prérequis :

- Python 3.10 ou plus récent.

Depuis le dossier du projet :

```bash
python generateurParties.public.v1.0.py
```

Le script propose deux modes :

- `P` : affiche une partie détaillée étape par étape ;
- `E` : lance plusieurs simulations et affiche des moyennes globales.

## Paramètres principaux

Au début du fichier, plusieurs variables globales peuvent être modifiées :

- `gouts` : liste des goûts utilisés dans le gâteau ;
- `longueur` : nombre de parts du gâteau ;
- `nbJoueur` : nombre de joueurs ;
- `rangeScore` : borne minimale et borne maximale des scores attribués aux goûts.

## Fonctions importantes

Quelques fonctions structurent le script :

- `genererGateau(...)` : construit un gâteau aléatoire ;
- `genererGouts(...)` : attribue des scores aux goûts pour un joueur ;
- `calculScoreMax(...)` : calcule le meilleur score théorique possible ;
- `strategies(...)` : décide si un joueur doit dire `STOP` ;
- `partie(...)` : lance une simulation complète ;
- `etudier_parties(...)` : répète plusieurs simulations pour obtenir des moyennes.

## Ce que j'ai corrigé dans cette version

Le fichier public contenait quelques points fragiles ou inachevés. Cette version corrige notamment :

- une erreur de syntaxe au début du fichier ;
- une simplification incomplète du gâteau dans `simplifieGateau` ;
- une logique de vérification du "reste du gâteau" pour le dernier joueur ;
- plusieurs cas limites sur les scores et les ratios ;
- l'ancien mode `E`, qui ne faisait presque rien dans la version publique.

J'ai aussi nettoyé les commentaires et docstrings pour qu'ils soient plus homogènes et plus lisibles.

## Conseils pour aller plus loin

Si tu veux continuer à faire évoluer le projet, voici les améliorations les plus utiles :

- ajouter des tests unitaires pour `calculScoreMax`, `genererGouts` et `partie` ;
- séparer la logique métier de l'affichage terminal ;
- ajouter plusieurs stratégies de joueurs et pouvoir les comparer ;
- permettre de fixer une graine aléatoire pour reproduire exactement une simulation ;
- exporter les résultats d'étude dans un fichier CSV pour faire des graphiques ensuite.

## Remarque

Le fichier `generateurParties.v6.0.py` semble être une version plus complète ou expérimentale du projet.  
Le fichier public est plus simple, plus lisible, et mieux adapté à une relecture ou à une présentation.
