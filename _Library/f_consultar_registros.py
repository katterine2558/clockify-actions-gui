"""
CREATED BY: KATERINE ARIAS
"""
#Importa librerías
import datetime
import pickle
import configparser
import requests
import json
import pytz
from customtkinter import *
import os


def f_consultar_registros(workspace, proyecto, email_user, fecha_inicio, fecha_fin):
    
    library_path  = os.path.join(os.path.dirname(os.path.realpath(__file__)))

    #Consulta el id del usuario
    with open(os.path.join(library_path, "users_data.pkl"),"rb") as f:
        users_data = pickle.load(f)
    f.close()

    for user in users_data[workspace]:
        if users_data[workspace][user]["email"] == email_user:
            userId = users_data[workspace][user]["id"]
            break

    #Obtiene el id del workspace
    with open(os.path.join(library_path, "workspaces.pkl"),"rb") as f:
        workspaces = pickle.load(f)
    f.close()
    workspaceId = next((item['id'] for item in workspaces if item['name'] == workspace), None)
    
    #Obtiene el id del proyecto
    with open(os.path.join(library_path, "projects.pkl"),"rb") as f:
        projects = pickle.load(f)
    f.close()
    projectId = next((project_data['id'] for project_id, project_data in projects[workspace].items() if project_data['name'] == proyecto), None)

    