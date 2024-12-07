"""
ELIMINA LAS TAREAS DE LOS PROYECTOS VIA API
"""
import configparser
import tkinter.messagebox
import requests
from datetime import datetime
from _lib.f01_get_files_path import get_file_paths
from _lib.progress_window import create_progress_window
from _lib.get_tasks import get_tasks
import os
import json
import tkinter
import time

def delete_task(workspace_id,project_id,list_task):

    #Crea la ventana de progreso
    ventana_progreso, barra_progreso, texto_progreso = create_progress_window("Eliminando tareas...","Eliminar_Tarea.ico",f"0/{len(list_task)}")

    #Obtiene las tareas del proyecto
    task_object = get_tasks(workspace_id,project_id)

    #Obtiene la ruta de la librería
    library_path  = get_file_paths("_lib")

    #Header
    config = configparser.ConfigParser()
    config.read(os.path.join(library_path, "config.ini")) 
    X_Api_Key = config.get('clockify', 'API_KEY')
    headers = { 'X-Api-Key': X_Api_Key, 'Content-Type': 'application/json'}

    #Obtiene la ruta de documentos
    documents_path = os.path.expanduser("~\\Documents")

    #Itera por cada tareas para eliminar (primero debe cambiar el estado)
    exitos = 0
    cont = 1
    logs = []
    for task in list_task:

        if task in task_object["tareas"]:
            task_id = task_object["id"][task_object["tareas"].index(task)]
            url = f'https://api.clockify.me/api/v1/workspaces/{workspace_id}/projects/{project_id}/tasks/{task_id}'
            #PUT
            data = {
                "name" : task,
                "status": "DONE"
            }
            #Delete to server
            response = requests.put( url, headers=headers,data=json.dumps(data))
            if response.status_code == 200:
                response = requests.delete(url, headers=headers)
                if response.status_code == 200:
                    exitos+=1
            else:
                logs.append(f'La tarea {task} no existe en el proyecto, por lo tanto, no fue borrada.')
        else:
            logs.append(f'La tarea {task} no existe en el proyecto, por lo tanto, no fue borrada.')

        barra_progreso.set(cont / len(list_task))  # Actualizar progreso
        texto_progreso.set(f"{cont}/{len(list_task)}")
        ventana_progreso.update_idletasks()  # Forzar actualización de la ventana
        cont+=1

    #Crea la ruta de logs
    try:
        os.makedirs(f'{documents_path}\\logs_clockify\\eliminar_tareas\\')
    except OSError:
        pass
    
    ventana_progreso.destroy()
    time.sleep(2)

    #Escribe los logs
    fecha_hora_actual = datetime.now()
    estampa = fecha_hora_actual.strftime("%Y_%m_%d_%H_%M_%S")

    if len(logs) != 0:

        with open(f'{documents_path}\\logs_clockify\\eliminar_tareas\\{estampa}.txt',"w") as f:
            for line in logs:
                f.write(line + '\n')

        tkinter.messagebox.showinfo("Info",f'Se eliminaron {exitos} de {len(list_task)} tareas.')
    else:
        tkinter.messagebox.showinfo("Info",f'Se eliminaron todas las tareas con éxito.')
            
    return
    


