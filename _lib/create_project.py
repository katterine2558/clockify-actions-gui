"""
CREA PROYECTO VIA API
"""
import configparser
import requests
from _lib.f01_get_files_path import get_file_paths
import os
import json
import tkinter

def create_project(projectName, workspaceId):

    library_path  = get_file_paths("_lib")

    config = configparser.ConfigParser()
    config.read(os.path.join(library_path, "config.ini")) 
    X_Api_Key = config.get('clockify', 'API_KEY')
    headers = { 'X-Api-Key': X_Api_Key, 'Content-Type': 'application/json'}

    url = f"https://api.clockify.me/api/v1/workspaces/{workspaceId}/projects"

    data = {
        "isPublic": True,
        "name": projectName
    }
   
    #post to server
    response = requests.post( url, headers=headers, data = json.dumps(data))

    if response.status_code == 201:
        tkinter.messagebox.showinfo(title="Éxito", message="Proyecto creado con éxito")
        return True  
    else:
        tkinter.messagebox.showerror(title="Error", message="El proyecto ya existe.")
        return False 

