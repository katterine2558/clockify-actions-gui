"""
CREATED BY: KATERINE ARIAS
"""
#Importa librerías
import configparser
import requests
import os
from _lib.f01_get_files_path import get_file_paths

#Obtiene los usuarios de todos los workspaces
def get_workspace_users(workspaceId):

    #Obtiene la apikey de los usuarios
    lib_path = get_file_paths("_lib")

    # URL para obtener los workspaces
    url_base = f'https://api.clockify.me/api/v1/workspaces/{workspaceId}/users'
    # Lectura de la clave de la API - karias@pedelta.com.co - cada usuario tiene su clave API
    # Lectura de la clave de la API
    config = configparser.ConfigParser()
    config.read(os.path.join(lib_path, "config.ini")) 
    X_Api_Key = config.get('clockify', 'API_KEY')
    headers = { 'X-Api-Key': X_Api_Key, 'Content-Type': 'application/json'}
    
    users_data = {"email":[],"id":[]}

    i = 1
    continuar = True
    while continuar:
        data = {
            "status": "ACTIVE",
            "page-size": 5000,
            "page": i
        }
        response = requests.get(url_base, headers=headers, params=data)
        decoded_content = response.content.decode('utf-8')
        decoded_content = decoded_content.replace("null","None")
        decoded_content = decoded_content.replace("true","True")
        decoded_content = decoded_content.replace("false","False")

        #Usuarios
        users = eval(decoded_content)

        if len(users) > 0:
            for user in users:
                users_data["email"].append(user["email"])
                users_data["id"].append(user["id"])
            i+=1
        else:
            continuar = False

    return users_data

