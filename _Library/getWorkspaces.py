"""
CREATED BY: KATERINE ARIAS
"""
#Importa librerías
import configparser
import requests
import re
import pickle
import os

# Obtiene los workspaces de Clockify
def getWorkspaces():
    """
    Input args:
    Output args:
    """
    library_path  = os.path.join(os.path.dirname(os.path.realpath(__file__)))

    # URL para obtener los workspaces
    url_base = f'https://api.clockify.me/api/v1/workspaces'
    # Lectura de la clave de la API
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


    # #Convierte el texto obtenido por el servidor a una cadena de string
    # pattern = r'(\{\"id\"[^}]*\})'
    # matches = re.findall(pattern, decoded_content[1:-1])
    # workspaces = [match for match in matches]
    # for i in range(len(workspaces)):
    #     workspaces[i] = eval(f"{workspaces[i]}" + "}")

    #Almacena lso workspaces en _Library
    with open(os.path.join(library_path, "workspaces.pkl"), 'wb') as f: 
        pickle.dump(decoded_content, f) 
    f.close()