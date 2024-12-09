# Connecteur API Lucca

## Objectif
Le but de ce script python est de récupérer les informations employés, contrats et départements à partir de Lucca en utilisant l'API fournie, pour pouvoir les stocker en local sous le format JSON.
L'URL de l'API : https://reflect2-sandbox.ilucca-demo.net


## Fonctions
Pour cela, plusieurs fonctions sont définies :
- get_age(birthDate: str) : 
    à partir d'une date de naissance fournie, renvoie l'âge actuel de cette personne
- get_user_list(statut="active": str, headers=headers: dict): 
    récupère la liste des employés (actifs si statut="active", passés sinon) à partir de l'API à l'aide d'une reqûete HTTP et qui renvoie cette liste si il l'obtient,une erreur sinon
- get_dpt_list(statut="active": str, headers=headers: dict): 
    fonction qui récupère la liste des départements à partir de l'API à l'aide d'une reqûete HTTP et qui renvoie cette liste s'il l'obtient, une erreur sinon
- employee_json(item_data: dict): 
    à partir du dictionnaire des données de chaque employé fournie par l'API, renvoie un dictionnaire bien rangé des informations pertinentes de chaque employé
- contract_json(item_data: dict):
    à partir du dictionnaire des données de chaque employé fournie par l'API, renvoie un dictionnaire bien rangé des informations pertinentes de chaque contrat de travail
- dpt_json(item_data: dict):
    à partir du dictionnaire des données de chaque département fournie par l'API, renvoie un dictionnaire bien rangé des informations pertinentes de chaque département
- create_jsons(items: dict, headers=headers: dict, folder_path=folder_path: str):
    à partir de la liste des employés fournie par l'API, pour chaque employé récupère les informations avec une requête HTTP à l'API, éxecute les fonctions employee_json et contract_json pour récupérer les informations, les combiner et créer les fichiers json correspondants
- create_dpt_json(items: dict, headers=headers: dict, folder_path=folder_path):  
    à partir de la liste des départements fournie par l'API, pour chaque département récupère les informations avec une requête HTTP à l'API, éxecute la fonction dpt_json pour récupérer les informations, les combiner et créer le fichier json correspondant
- main():
    Exécute les fonctions pour récupérer les informations employé et département et créer les fichiers json correspondant

## Installation
Pour pouvoir exécuter ce script, il est nécessaire d'avoir les bibliothèques python suivantes : requests, json, datetime, time, os, tqdm

## Utilisation
Avant l'exécution, il faut entrer le chemin d'accès au dossier où les fichiers json seront enregistrés.
Lors de l'éxecution du script, la fonction main est appelé et le code s'exécute.

## Contact
Bastien Chevalier : bastien.chevalier@telecom-sudparis.eu