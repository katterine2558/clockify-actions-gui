"""
CREATED BY: KATERINE ARIAS
"""
#Importa librerías
import configparser
import requests
import os
from _lib.f01_get_files_path import get_file_paths

def get_tasks(workspace_id, project_id):
    
    #Obtiene la ruta de la librería
    library_path  = get_file_paths("_lib")

    # URL para obtener los proyectos del workspace
    url_base = f'https://api.clockify.me/api/v1/workspaces/{workspace_id}/projects/{project_id}/tasks'

    # Lectura de la clave de la API
    config = configparser.ConfigParser()
    config.read(os.path.join(library_path, "config.ini")) 
    X_Api_Key = config.get('clockify', 'API_KEY')
    headers = { 'X-Api-Key': X_Api_Key, 'Content-Type': 'application/json'}

    continuar = True
    page = 1
    tareas, ids, status = [],[],[]
    while continuar:

        # Get al servidor
        data = {
                "page-size": 50,
                "page": page,
                "status": "ALL"
        }

        response = requests.get(url_base, headers=headers, params=data)
        decoded_content = response.content.decode('utf-8')
        decoded_content = decoded_content.replace("null","None")
        decoded_content = decoded_content.replace("true","True")
        decoded_content = decoded_content.replace("false","False")
        decoded_content = eval(decoded_content)

        if len(decoded_content) != 0:
            for decode in decoded_content:
                tareas.append(decode["name"])
                ids.append(decode["id"])
                status.append(decode["status"])

            page+= 1
        else: 
            continuar =  False

    return {"tareas": tareas, "id": ids, "status": status}