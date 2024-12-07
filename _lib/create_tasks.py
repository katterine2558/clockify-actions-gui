"""
CREA LAS TAREAS DE LOS PROYECTOS VIA API
"""
import configparser
import tkinter.messagebox
import requests
from datetime import datetime
from _lib.f01_get_files_path import get_file_paths
from _lib.progress_window import create_progress_window
import os
import json
import tkinter
import time

def create_task(workspace_id,project_id,list_task):

    #Crea la ventana de progreso
    ventana_progreso, barra_progreso, texto_progreso = create_progress_window("Creando tareas...","Crear_Tarea.ico",f"0/{len(list_task)}")

    #Obtiene la ruta de la librería
    library_path  = get_file_paths("_lib")

    #Obtiene la ruta de documentos
    documents_path = os.path.expanduser("~\\Documents")

    config = configparser.ConfigParser()
    config.read(os.path.join(library_path, "config.ini")) 
    X_Api_Key = config.get('clockify', 'API_KEY')
    headers = { 'X-Api-Key': X_Api_Key, 'Content-Type': 'application/json'}
    
    url = f"https://api.clockify.me/api/v1/workspaces/{workspace_id}/projects/{project_id}/tasks"

    #Crea las tareas
    exitos = 0
    logs = []
    cont = 1
    for task in list_task:

        data = {
            "name": task
        }
   
        #post to server
        response = requests.post( url, headers=headers, data = json.dumps(data))

        if response.status_code == 201:
            exitos += 1
        else:
            logs.append(f"{task} no pudo ser creada.")
        
        barra_progreso.set(cont / len(list_task))  # Actualizar progreso
        texto_progreso.set(f"{cont}/{len(list_task)}")
        ventana_progreso.update_idletasks()  # Forzar actualización de la ventana

        cont+=1

    ventana_progreso.destroy()
    time.sleep(1)

    #Crea la ruta de logs
    try:
        os.makedirs(f'{documents_path}\\logs_clockify\\crear_tareas\\')
    except OSError:
        pass

    #Escribe los logs
    fecha_hora_actual = datetime.now()
    estampa = fecha_hora_actual.strftime("%Y_%m_%d_%H_%M_%S")

    if len(logs) != 0:

        with open(f'{documents_path}\\logs_clockify\\crear_tareas\\{estampa}.txt',"w") as f:
            for line in logs:
                f.write(line + '\n')

        tkinter.messagebox.showinfo("Info",f'Se crearon {exitos} de {len(list_task)} tareas.')
    else:
        tkinter.messagebox.showinfo("Info",f'Se crearon todas las tareas con éxito.')
            
    return
    


