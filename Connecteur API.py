# Importation des bibliothèques nécessaires
import requests
import json
from datetime import datetime
import time
import os
from tqdm import tqdm

# Token d'authentification pour l'API et définition de l'header de la requête http
token = "caf8058b-b7ec-4df2-85e3-a673b5466e97"
headers = {"Content-Type": "application/json", "Authorization": f"lucca application={token}"}

# Chemin d'accès pour stocker les fichiers JSON crées
folder_path="your\\path"

# Fonction pour calculer l'âge à partir de la date de naissance
def get_age(birthDate):
    today = datetime.now()  # Date d'aujourd'hui
    age = today.year - birthDate.year - ((today.month, today.day) < (birthDate.month, birthDate.day))
    return age  # Retourne l'âge calculé

# Fonction pour récupérer la liste des utilisateurs en fonction de leur statut (actif ou inactif)
def get_user_list(statut="active", headers=headers):
    url = "https://reflect2-sandbox.ilucca-demo.net/api/v3/users/"
    if statut == "active":
        response = requests.request("GET", url, headers=headers)  # Requête pour les utilisateurs actifs
    else:
        querystring = {"dtContractEnd": "notequal,null"}  # Paramètre pour obtenir les utilisateurs inactifs
        response = requests.request("GET", url, headers=headers, params=querystring)
    
    # Vérification de la réponse de l'API
    if response.status_code == 200:
        file = json.loads(response.text)  # Conversion de la réponse JSON en dictionnaire
        data = file.get("data")
        items = data.get("items")
        return items  # Retourne la liste des utilisateurs
    else:
        print(f"Error : {response.status_code} : {response.text}  ")

# Fonction pour récupérer la liste des départements
def get_dpt_list(headers=headers):
    url_dpt = "https://reflect2-sandbox.ilucca-demo.net/api/v3/departments/"
    response = requests.request("GET", url_dpt, headers=headers)  # Requête pour les départements
    if response.status_code == 200:
        file = json.loads(response.text)  # Conversion de la réponse JSON en dictionnaire
        data = file.get("data")
        items = data.get("items")
        return items  # Retourne la liste des départements
    else:
        print(f"Error : {response.status_code} : {response.text}  ")

# Fonction pour créer un dictionnaire JSON avec les détails d'un employé
def employee_json(item_data):
    id = item_data.get("id")
    lastName = item_data.get("lastName")
    firstName = item_data.get("firstName")
    gender = item_data.get("gender")
    mail = item_data.get("mail")
    nationality = item_data.get("nationality") and item_data["nationality"].get("name")
    birthDate = item_data.get("birthDate")
    # Formate la date de naissance et calcule l'âge si la date est disponible
    if birthDate:
        date = datetime.strptime(birthDate, "%Y-%m-%dT%H:%M:%S")
        formatted_birthDate = date.strftime("%d/%m/%Y")
        age = get_age(date)
    else:
        formatted_birthDate = None
        age = None
    address = item_data.get("address")
    jobTitle = item_data.get("jobTitle")
    departement = item_data.get("department") and item_data["department"].get("name")
    
    # Création du dictionnaire avec les informations de l'employé
    employee_data = {
        id: {
            "firstName": firstName,
            "lastName": lastName,
            "gender": gender,
            "mail": mail,
            "nationality": nationality,
            "birthDate": formatted_birthDate,
            "age": age,
            "address": address,
            "jobTitle": jobTitle,
            "departement": departement,
        }
    }
    return employee_data

# Fonction pour créer un dictionnaire JSON avec les détails d'un contrat
def contract_json(item_data):
    id = item_data.get("id")
    lastName = item_data.get("lastName")
    firstName = item_data.get("firstName")
    jobTitle = item_data.get("jobTitle")
    departement = item_data.get("department") and item_data["department"].get("name")
    dtContractStart = item_data.get("dtContractStart")
    dtContractEnd = item_data.get("dtContractEnd")
    appData = item_data.get("applicationData")
    
    # Extraction des informations de rémunération et de temps de travail si disponibles
    if appData:
        remuneration = appData.get("theoreticalRemuneration") and appData["theoreticalRemuneration"].get("value")
        workedTime = appData.get("fullTimeEquivalent") and appData["fullTimeEquivalent"].get("value")
    else :
        remuneration = None
        workedTime = None
    legalEntity = item_data.get("legalEntity") and item_data["legalEntity"].get("name")
    
    # Création du dictionnaire avec les informations du contrat
    contract_data = {
        id: {
            "firstName": firstName,
            "lastName": lastName,
            "jobTitle": jobTitle,
            "departement": departement,
            "dtContractStart": dtContractStart,
            "dtContractEnd": dtContractEnd,
            "remuneration": remuneration,
            "workedTime": workedTime,
            "legalEntity": legalEntity,
        }
    }
    return contract_data

# Fonction pour créer un dictionnaire JSON avec les détails d'un département
def dpt_json(item_data):
    id = item_data.get("id")
    name = item_data.get("name")
    treeStructureName = item_data.get("treeStructureName")
    splitted = treeStructureName.split("/")
    structureName = splitted[0]
    
    # Obtention du nom de l'entité parente si elle existe
    if len(splitted) > 2:
        parent = splitted[len(splitted) - 2]
    else:
        parent = None
    
    currentUsersCount = item_data.get("currentUsersCount")
    
    # Création du dictionnaire avec les informations du département
    dpt_data = {
        id: {
            "name": name,
            "structureName": structureName,
            "parent_department": parent,
            "currentUsersCount": currentUsersCount,
        }
    }
    return dpt_data

# Fonction pour créer et sauvegarder les JSON des employés et des contrats
def create_jsons(items, headers=headers,folder_path=folder_path):
    print("Création des fichiers employés et contrats")
    combined_data1 = {}
    combined_data2 = {}
    
    # Parcours de chaque élément de la liste des utilisateurs
    for elt in tqdm(items, total=len(items)):
        url_item = elt.get("url")
        response_item = requests.request("GET", url_item, headers=headers)
        
        # Gestion des limites de débit (status 429)
        while response_item.status_code == 429:
            time.sleep(1)
            response_item = requests.request("GET", url_item, headers=headers)
        
        if response_item.status_code == 200:
            item_file = json.loads(response_item.text)
            item_data = item_file.get("data")
            employee_data = employee_json(item_data)
            contract_data = contract_json(item_data)
            combined_data1.update(employee_data)
            combined_data2.update(contract_data)
    
    # Sauvegarde des informations des employés et des contrats dans des fichiers JSON
    file_employee_name = "employees.json"
    employee_file=os.path.join(folder_path,file_employee_name)
    with open(employee_file, "w", encoding="utf-8") as json_file:
        json.dump(combined_data1, json_file, indent=4, ensure_ascii=False)
    
    file_contracts_name = "contracts.json"
    contracts_file=os.path.join(folder_path,file_contracts_name)
    with open(contracts_file, "w", encoding="utf-8") as json_file:
        json.dump(combined_data2, json_file, indent=4, ensure_ascii=False)
    print("Le fichier des employés et celui des contrats ont été créés avec succès")

# Fonction pour créer et sauvegarder le JSON des départements
def create_dpt_json(items, headers=headers,folder_path=folder_path):
    print("Création du fichier départements")
    combined_data = {}
    
    # Parcours de chaque département pour obtenir ses détails
    for elt in tqdm(items, total=len(items)):
        dpt_elt_url = elt.get("url")
        response_item = requests.request("GET", dpt_elt_url, headers=headers)
        
        # Gestion des limites de débit (status 429)
        while response_item.status_code == 429:
            time.sleep(1)
            response_item = requests.request("GET", dpt_elt_url, headers=headers)
        
        if response_item.status_code == 200:
            item_file = json.loads(response_item.text)
            item_data = item_file.get("data")
            dpt_data = dpt_json(item_data)
            combined_data.update(dpt_data)
        else:
            print(f"Error : {response_item.status_code} : {response_item.text}  ")

    
    # Sauvegarde des informations des départements dans un fichier JSON
    file_dpt_name = "departments.json"
    dpt_file=os.path.join(folder_path,file_dpt_name)
    with open(dpt_file, "w", encoding="utf-8") as json_file:
        json.dump(combined_data, json_file, indent=4, ensure_ascii=False)
    print("Le fichier des départements des entreprises a été créé avec succès")

# Fonction principale pour exécuter les tâches de récupération et de création de fichiers JSON
def main():
    start_time = time.time()  # Temps de début
    print("Début de l'extraction")
    items1 = get_user_list("active")  # Récupère les utilisateurs actifs
    items2 = get_user_list("inactive")  # Récupère les utilisateurs inactifs
    items = items1 + items2  # Combine les deux listes
    create_jsons(items)  # Créer les fichiers des employés et des contrats
    dpt_items = get_dpt_list()  # Récupère la liste des départements
    create_dpt_json(dpt_items)  # Crée le fichier JSON des départements
    end_time = time.time()  # Temps de fin
    duration = int(end_time - start_time)
    print(f"Importation terminée avec succès en {duration} s !")

main()  # Exécute la fonction principale
