"""
OBTIENE LOS REGISTROS DE UN USUARIO
"""

from _lib.f01_get_files_path import get_file_paths
import configparser
import os
import requests

def get_user_records(workspace_id,user_id,descripcion,date_start,date_end,project_id,task_id):

    #Obtiene la ruta de la librería
    library_path  = get_file_paths("_lib")

    # URL para obtener los proyectos del workspace
    url_base = f'https://api.clockify.me/api/v1/workspaces/{workspace_id}/user/{user_id}/time-entries'

    # Lectura de la clave de la API
    config = configparser.ConfigParser()
    config.read(os.path.join(library_path, "config.ini")) 
    X_Api_Key = config.get('clockify', 'API_KEY')
    headers = { 'X-Api-Key': X_Api_Key, 'Content-Type': 'application/json'}

    # Get al servidor
    data = {
            "start": f'{date_start}T00:00:00Z',
            "end": f'{date_end}T23:59:00Z',
            "project": project_id,
            "task": task_id,
            "description" : descripcion
        }   

    response = requests.get(url_base, headers=headers, params=data)
    decoded_content = response.content.decode('utf-8')
    decoded_content = decoded_content.replace("null","None")
    decoded_content = decoded_content.replace("true","True")
    decoded_content = decoded_content.replace("false","False")
    decoded_content = eval(decoded_content)

    return decoded_content