"""
CREATED BY: KATERINE ARIAS
"""
#Importa librerías
import configparser
import requests
import re
import pickle
import os

#Obtiene los usuarios de todos los workspaces
def getWorkspaceUsers():

    library_path  = os.path.join(os.path.dirname(os.path.realpath(__file__)))

    #Abre el archivo de workspaces
    with open(os.path.join(library_path, "workspaces.pkl"), 'rb') as file:
        workspaces = pickle.load(file)
    file.close()

    #Inicializa el diccionario para almacenar
    users_data = {workspace["name"]: {} for workspace in workspaces}

    #Itera sobre cada workspace
    for workspace in workspaces:

       #Id del workspace
        workspaceId = workspace['id']

        # URL para obtener los workspaces
        url_base = f'https://api.clockify.me/api/v1/workspaces/{workspaceId}/users'
        # Lectura de la clave API
        config = configparser.ConfigParser()
        config.read(os.path.join(library_path, "config.ini")) 
        X_Api_Key = config.get('clockify', 'API_KEY')
        # Get al servidor
        headers = { 'X-Api-Key': X_Api_Key}
        continuar = True
        i = 1
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
                j=0
                for user in users:
                    users_data[workspace["name"]][j] = user
                    j+=1
                i+=1
            else:
                continuar = False

    #Almacena los proyectos de los workspaces
    with open(os.path.join(library_path, "users_data.pkl"), 'wb') as f: 
        pickle.dump(users_data, f) 
    f.close()
