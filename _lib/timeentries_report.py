"""
REPORTE DETALLADO
"""
import os
from _lib.f01_get_files_path import get_file_paths
import configparser
import requests
import json

def get_timeentries_report(workspace_id,project_id,dateRangeStart,dateRangeEnd,grupo_id = ""):

    #Obtiene la ruta de la librería
    library_path  = get_file_paths("_lib")

    # Lectura de la clave de la API
    config = configparser.ConfigParser()
    config.read(os.path.join(library_path, "config.ini")) 
    X_Api_Key = config.get('clockify', 'API_KEY')
    headers = { 'X-Api-Key': X_Api_Key, 'Content-Type': 'application/json'}

    #url
    url = f'https://reports.api.clockify.me/v1/workspaces/{workspace_id}/reports/detailed'
    i = 1
    continuar = True
    timeentries = []
    while continuar:
        data = {
            "dateRangeStart": f"{dateRangeStart}T00:00:00.000",
            "dateRangeEnd": f"{dateRangeEnd}T23:59:59.000",
            "detailedFilter": {
                "page": i,
                "pageSize": 1000
            },
            "projects":{
                "contains": "CONTAINS",
                "ids":[project_id]
            },
            "users": {
                "status": "ALL"
            },
            "exportType": "JSON"
        }

        if grupo_id!="":
            data["userGroups"] = {
                                    "contains":"CONTAINS",
                                    "ids": [grupo_id],
                                    "status": "ACTIVE"
                            }

        response = requests.post( url, headers=headers, data=json.dumps(data))
        userRecords = json.loads(response.content)

        if len(userRecords['timeentries']) > 0:
            for r in userRecords['timeentries']:
                timeentries.append(r)
            i+=1
        else:
            continuar = False

        
    return timeentries