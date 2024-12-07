"""
OBTIENE LOS WORKSPACES
"""
#Importa librerías
import configparser
import requests
import os
from _lib.f01_get_files_path import get_file_paths

# Obtiene los workspaces de Clockify
def get_workspaces():

    """
    Input args:
    Output args:
    """
    library_path  = get_file_paths("_lib")

    # URL para obtener los workspaces
    url_base = f'https://api.clockify.me/api/v1/workspaces'
    # Lectura de la clave de la API - karias@pedelta.com.co - cada usuario tiene su clave API
    config = configparser.ConfigParser()
    config.read(os.path.join(library_path, "config.ini")) 
    X_Api_Key = config.get('clockify', 'API_KEY')
    # Get al servidor
    headers = { 'X-Api-Key': X_Api_Key}
    response = requests.get(url_base, headers=headers)
    decoded_content = response.content.decode('utf-8')

    try:
        decoded_content = decoded_content.replace("null","None")
    except:
        pass
    try:
        decoded_content = decoded_content.replace("true","True")
    except:
        pass
    try:
        decoded_content = decoded_content.replace("false","False")
    except:
        pass

    decoded_content = eval(decoded_content)

    return decoded_content