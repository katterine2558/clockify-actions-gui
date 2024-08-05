"""
CREATED BY: KATERINE ARIAS
"""
#Importa librerías
import configparser
import requests
import re
import pickle
import os

def getProjects():

    library_path  = os.path.join(os.path.dirname(os.path.realpath(__file__)))

    #Abre la información de los workspaces
    with open(os.path.join(library_path, "workspaces.pkl"), 'rb') as file:
        workspaces = pickle.load(file)
    file.close()

    #inicializa el diccionario
    workspacesProjects = {workspace["name"]: {} for workspace in workspaces}

    #Itera sobre cada workspace
    for workspace in workspaces:

        #Id del workspace
        workspaceId = workspace['id']
        #Nombre del workspace
        nameWorkspace = workspace['name']
        
        # URL para obtener los proyectos del workspace
        url_base = f'https://api.clockify.me/api/v1/workspaces/{workspaceId}/projects'

        # Lectura de la clave de la API
        config = configparser.ConfigParser()
        config.read(os.path.join(library_path, "config.ini")) 
        X_Api_Key = config.get('clockify', 'API_KEY')

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

                if i == 1:
                    for j in range(len(decoded_content)):
                        workspacesProjects[nameWorkspace][j] = decoded_content[j]
                else:
                    cons_id = len(workspacesProjects[nameWorkspace])
                    for j in range(cons_id,len(decoded_content)+cons_id): 
                        workspacesProjects[nameWorkspace][j] = decoded_content[j-cons_id]

                i+=1

            else:

                continuar = False

    #Almacena los proyectos de los workspaces
    with open(os.path.join(library_path, "projects.pkl"), 'wb') as f: 
        pickle.dump(workspacesProjects, f) 
    f.close()
