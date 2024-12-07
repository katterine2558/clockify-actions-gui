
"""
TRANSFIERE HORAS DE AMBOS WORKSPACES
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
from _lib.get_projects import get_projects
from _lib.timeentries_report import get_timeentries_report
from _lib.get_groups import get_groups
from _lib.f01_get_files_path import get_file_paths
from _lib.users_apikey import users_apikey
from _lib.get_workspace_users import get_workspace_users
from _lib.get_tasks import get_tasks
from _lib.progress_window import create_progress_window
import pytz
from datetime import datetime
import time
import tkinter

def transfer_records(workspace_origen_id, workspace_destino_id, project, fecha_inicio, fecha_fin):
    #Obtiene la ruta de documentos
    documents_path = os.path.expanduser("~\\Documents")

    #Obtiene el ID del proyecto en el workspace de origen y en el workspace de destino
    projects = get_projects(workspace_origen_id)
    for proj in projects:
        if proj["name"] == project:
            project_id_origen = proj["id"]
            break
    projects = get_projects(workspace_destino_id)
    for proj in projects:
        if proj["name"] == project:
            project_id_destino = proj["id"]
            break

    #Obtiene las tareas en el workspace de destino y de origen
    task_origen = get_tasks(workspace_origen_id,project_id_origen)
    task_destino = get_tasks(workspace_destino_id,project_id_destino)

    #Obtiene todos los registros del workspace de origen
    records_origen = get_timeentries_report(workspace_origen_id,project_id_origen,fecha_inicio,fecha_fin)

    #Obtiene el id del grupo de pedelta
    groups = get_groups(workspace_destino_id) 
    for group in groups:
        if group["name"] == "Pedelta":
            group_id = group["id"]
            break

    #### Elimina todos los registros de los usuarios de pedelta en el workspace de destino ####
    records_destino = get_timeentries_report(workspace_destino_id,project_id_destino,fecha_inicio,fecha_fin,group_id)

    #Obtiene los apikeys de los usuarios
    lib_path = get_file_paths("_lib")
    file_key = "1asbaD2XMx7GIKrcE9I9a9VyLi-1zloTh0M-dhjHwLEc"
    sheet_name = 'Respuestas de formulario 1'
    token_path = os.path.join(lib_path, "api_account.json")
    apikey_object = users_apikey(file_key,sheet_name,token_path)

    #Obtiene los usuarios del workspace de destino y origen
    workspace_users_destino = get_workspace_users(workspace_destino_id)

    #Elimina los registros 
    for r in records_destino:

        try:
            X_Api_Key = apikey_object["apikey"][apikey_object["users"].index(r["userEmail"])]
            headers = {'content-type': 'application/json', 'X-Api-Key': X_Api_Key}
            url = f"https://api.clockify.me/api/v1/workspaces/{workspace_destino_id}/time-entries/{r['_id']}"
            response = requests.delete( url, headers=headers)
        except:
            pass
    #Crea la ventana de progreso
    ventana_progreso, barra_progreso, texto_progreso = create_progress_window("Transfiriendo registros...","Transferencia_Horas.ico",f"0/{len(records_origen)}")

    #variables para logs
    logs = []
    cont = 1
    exitos = 0

    url_base = f'https://api.clockify.me/api/v1/workspaces/{workspace_destino_id}/time-entries'

    #Sube los registros
    for r in records_origen:

        #Obtiene las fechas y las horas 
        date_obj = datetime.fromisoformat(r['timeInterval']['start'])
        date_obj_gmt = date_obj.astimezone(pytz.UTC)
        date_start = date_obj_gmt.strftime('%Y-%m-%dT%H:%M:%S') + 'Z'

        date_obj = datetime.fromisoformat(r['timeInterval']['end'])
        date_obj_gmt = date_obj.astimezone(pytz.UTC)
        date_end = date_obj_gmt.strftime('%Y-%m-%dT%H:%M:%S') + 'Z'

        #Obtiene los usuarios del workspace y verifica que exista en el workspacwe
        if r["userEmail"] not in workspace_users_destino["email"]:
            logs.append(f"{r['userEmail']} no pertenece al workspace.")
            #Actualiza la barra de progreso
            barra_progreso.set(cont / len(records_origen))  # Actualizar progreso
            texto_progreso.set(f"{cont}/{len(records_origen)}")
            ventana_progreso.update_idletasks()  # Forzar actualización de la ventana
            cont+=1
            continue

        #Obtiene la apikey del usuario
        if r["userEmail"] not in apikey_object["users"]:
            #Escribe el log
            logs.append(f'{r["userEmail"]} no tiene registrada la apikey.')
            #Actualiza la barra de progreso
            barra_progreso.set(cont / len(records_origen))  # Actualizar progreso
            texto_progreso.set(f"{cont}/{len(records_origen)}")
            ventana_progreso.update_idletasks()  # Forzar actualización de la ventana
            cont+=1
            continue
        else:
            index_user = apikey_object["users"].index(r["userEmail"])
            X_Api_Key = apikey_object["apikey"][index_user]

        #Verificz que la tarea no sea vacía
        if r["taskId"] == "":
            logs.append(f"El registro del usuario {r['userEmail']} del {date_start.split('T')[0]} a las {r['timeInterval']['start'].split('T')[1].split('-05:00')[0]} no tiene tarea asignada.")
            #Actualiza la barra de progreso
            barra_progreso.set(cont / len(records_origen))  # Actualizar progreso
            texto_progreso.set(f"{cont}/{len(records_origen)}")
            ventana_progreso.update_idletasks()  # Forzar actualización de la ventana
            cont+=1
            continue

        # Encuentra el ID de la tarea equivalente en el workspace de destino
        name_task_origen = task_origen["tareas"][task_origen["id"].index(r["taskId"])]

        if name_task_origen not in task_destino['tareas']:
            logs.append(f"La tarea del registro del usuario {r['userEmail']} del {date_start.split('T')[0]} a las {r['timeInterval']['start'].split('T')[1].split('-05:00')[0]} existe en el workspace de destino.")
            #Actualiza la barra de progreso
            barra_progreso.set(cont / len(records_origen))  # Actualizar progreso
            texto_progreso.set(f"{cont}/{len(records_origen)}")
            ventana_progreso.update_idletasks()  # Forzar actualización de la ventana
            cont+=1
            continue
        else:
            task_id_destino = task_destino["id"][task_destino['tareas'].index(name_task_origen)]
        
        data = {
                "start": date_start,
                "description": r['description'],
                "projectId": project_id_destino,
                "taskId": task_id_destino,
                "end": date_end
                }
        
        headers = {'content-type': 'application/json', 'X-Api-Key': X_Api_Key}

        # Post al servidor
        response = requests.post( url_base, headers=headers,data=json.dumps(data))

        #Actualiza la barra de progreso
        barra_progreso.set(cont / len(records_origen))  # Actualizar progreso
        texto_progreso.set(f"{cont}/{len(records_origen)}")
        ventana_progreso.update_idletasks()  # Forzar actualización de la ventana
        cont+=1

        if response.status_code != 201:
            logs.append(f"El registro de {r['userEmail']} del {date_start.split('T')[0]} a las {r['timeInterval']['start'].split('T')[1].split('-05:00')[0]} no fue migrada.")
        else:
            exitos+=1
    
    ventana_progreso.destroy()
    time.sleep(1)

    #Crea la ruta de logs
    try:
        os.makedirs(f'{documents_path}\\logs_clockify\\transferencia_horas\\')
    except OSError:
        pass

    #Escribe los logs
    fecha_hora_actual = datetime.now()
    estampa = fecha_hora_actual.strftime("%Y_%m_%d_%H_%M_%S")

    if len(logs) != 0:

        with open(f'{documents_path}\\logs_clockify\\transferencia_horas\\{estampa}.txt',"w") as f:
            for line in logs:
                f.write(line + '\n')

        tkinter.messagebox.showinfo("Info",f"Se subieron {exitos} de {len(records_origen)} registros.")
    else:
        tkinter.messagebox.showinfo("Info",f'Se subieron todos los registros con éxito.')
    return
