"""
OBTIENE LOS PROYECTOS DE UN WORKSPACE
"""
#Importa librerías
import configparser
import requests
import os
from _lib.f01_get_files_path import get_file_paths

def get_projects(workspaceId):

    library_path  = get_file_paths("_lib")

    # URL para obtener los proyectos del workspace
    url_base = f'https://api.clockify.me/api/v1/workspaces/{workspaceId}/projects'

    # Lectura de la clave de la API
    config = configparser.ConfigParser()
    config.read(os.path.join(library_path, "config.ini")) 
    X_Api_Key = config.get('clockify', 'API_KEY')

    #Inicializa para almacenar proyectos
    projects = []

    # Get al servidor
    headers = { 'X-Api-Key': X_Api_Key}
    continuar = True
    i = 1
    while continuar:
        data = {
                "page-size": 200,
                "page": i,
                "archived": False
            }
        
        response = requests.get(url_base, headers=headers, params=data)
        decoded_content = response.content.decode('utf-8')
        decoded_content = decoded_content.replace("null","None")
        decoded_content = decoded_content.replace("true","True")
        decoded_content = decoded_content.replace("false","False")
        decoded_content = eval(decoded_content)

        if len(decoded_content) > 0:

            for d in decoded_content:
                projects.append(d)

            i+=1
        else:
            continuar = False

    return projects

