"""
OBTIENE LOS GRUPOS DEL WORKSPACE
"""

#Importa librerías
import configparser
import requests
import os
from _lib.f01_get_files_path import get_file_paths

def get_groups(workspace_id):

    #Obtiene la ruta de la librería
    library_path  = get_file_paths("_lib")

    # URL para obtener los proyectos del workspace
    url_base = f'https://api.clockify.me/api/v1/workspaces/{workspace_id}/user-groups'

    # Lectura de la clave de la API
    config = configparser.ConfigParser()
    config.read(os.path.join(library_path, "config.ini")) 
    X_Api_Key = config.get('clockify', 'API_KEY')
    headers = { 'X-Api-Key': X_Api_Key, 'Content-Type': 'application/json'}

    # Get al servidor
    data = {
            "page-size": 50,
            "page": 1
    }

    response = requests.get(url_base, headers=headers, params=data)
    decoded_content = response.content.decode('utf-8')
    decoded_content = decoded_content.replace("null","None")
    decoded_content = decoded_content.replace("true","True")
    decoded_content = decoded_content.replace("false","False")
    decoded_content = eval(decoded_content)

    return decoded_content
