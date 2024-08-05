"""
CREATED BY: KATERINE ARIAS
"""
#Importa librerías
import configparser
import requests
import re
import pickle
import os

def getGroups():
    
    library_path  = os.path.join(os.path.dirname(os.path.realpath(__file__)))

    #Get workspaces
    with open(os.path.join(library_path, "workspaces.pkl"), 'rb') as file:
        workspaces = pickle.load(file)
    file.close()

    #itera sobrre workspaces
    groups = {

    }
    
    for w in workspaces:

        # URL para obtener los proyectos del workspace
        url_base = f'https://api.clockify.me/api/v1/workspaces/{w["id"]}/user-groups'

        # Lectura de la clave de la API
        config = configparser.ConfigParser()
        config.read(os.path.join(library_path, "config.ini")) 
        X_Api_Key = config.get('clockify', 'API_KEY')

        # Get al servidor
        headers = { 'X-Api-Key': X_Api_Key}

        response = requests.get(url_base, headers=headers)
        decoded_content = response.content.decode('utf-8')
        decoded_content = decoded_content.replace("null","None")
        decoded_content = decoded_content.replace("true","True")
        decoded_content = decoded_content.replace("false","False")
        decoded_content = eval(decoded_content)

        #Almacena los grupos
        groups[w["name"]] = decoded_content

    #Almacena los grupos de los workspaces
    with open(os.path.join(library_path, "groups.pkl"), 'wb') as f: 
        pickle.dump(groups, f) 
    f.close()