"""
CREATED BY: KATERINE ARIAS
"""
#Importa librerías
import configparser
import requests
import re
import pickle
import os

def getProjectTask(workspace_name, project_name):
    
    library_path  = os.path.join(os.path.dirname(os.path.realpath(__file__)))

    #Abre la información de los workspaces
    with open(os.path.join(library_path, "workspaces.pkl"), 'rb') as file:
        workspaces = pickle.load(file)
    file.close()

    #Abre la información de los proyectos
    with open(os.path.join(library_path, "projects.pkl"), 'rb') as file:
        projects = pickle.load(file)
    file.close()

    #Obtiene el id del workspace
    for workspace in workspaces:

        if workspace["name"] == workspace_name:
            workspaceId = workspace["id"]
            break

    #obtiene el id del proyecto  
    for proj in projects[workspace_name]:
        if projects[workspace_name][proj]["name"] == project_name:
            projectId = projects[workspace_name][proj]["id"]
            break

    # URL para obtener los proyectos del workspace
    url_base = f'https://api.clockify.me/api/v1/workspaces/{workspaceId}/projects/{projectId}/tasks'

    # Lectura de la clave de la API
    config = configparser.ConfigParser()
    config.read(os.path.join(library_path, "config.ini")) 
    X_Api_Key = config.get('clockify', 'API_KEY')

    # Get al servidor
    headers = { 'X-Api-Key': X_Api_Key}
    data = {
            "page-size": 50,
            "page": 1,
        }
    response = requests.get(url_base, headers=headers, params=data)
    decoded_content = response.content.decode('utf-8')
    decoded_content = decoded_content.replace("null","None")
    decoded_content = decoded_content.replace("true","True")
    decoded_content = decoded_content.replace("false","False")
    decoded_content = eval(decoded_content)

    tareas = [decode["name" ]for decode in decoded_content]
    id_tareas = [decode["id" ]for decode in decoded_content]

    return {"Tareas":tareas, "ID":id_tareas}