"""
SUBE REGISTROS A WORKSPACES
"""
#Importa librerías
from _lib.hours_processing import convertir_a_formato_completo, convert24HFormat, convertUTCHour
from _lib.get_projects import get_projects
from _lib.users_apikey import users_apikey
from _lib.get_tasks import get_tasks
from _lib.f01_get_files_path import get_file_paths
from _lib.get_workspace_users import get_workspace_users
from _lib.progress_window import create_progress_window
import requests
import json
from customtkinter import *
import os
import tkinter
from datetime import datetime
import time

def upload_timeentries(records,workspace_id):

    #Crea la ventana de progreso
    ventana_progreso, barra_progreso, texto_progreso = create_progress_window("Cargando registros...","Subir_horas.ico",f"0/{len(records['Proyecto'])}")

    #Obtiene los proyectos del workspace
    projects =  get_projects(workspace_id)

    #Obtiene la ruta de documentos
    documents_path = os.path.expanduser("~\\Documents")

    #Obtiene la apikey de los usuarios
    lib_path = get_file_paths("_lib")
    file_key = "1asbaD2XMx7GIKrcE9I9a9VyLi-1zloTh0M-dhjHwLEc"
    sheet_name = 'Respuestas de formulario 1'
    token_path = os.path.join(lib_path, "api_account.json")
    apikey_object = users_apikey(file_key,sheet_name,token_path)

    #Obtiene los usuarios dle workspace
    workspace_users = get_workspace_users(workspace_id)

    # URL para subir registro
    url_base = f'https://api.clockify.me/api/v1/workspaces/{workspace_id}/time-entries'

    #variables para logs
    logs = []
    cont = 1
    exitos = 0

    #Itera por los registros
    for i in range(len(records["Proyecto"])):

        #Obtiene los usuarios del workspace y verifica que exista en el workspacwe
        if records["Correo electrónico"][i] not in workspace_users["email"]:
            logs.append(f'{records["Correo electrónico"][i]} no pertenece al workspace.')
            #Actualiza la barra de progreso
            barra_progreso.set(cont / len(records['Proyecto']))  # Actualizar progreso
            texto_progreso.set(f"{cont}/{len(records['Proyecto'])}")
            ventana_progreso.update_idletasks()  # Forzar actualización de la ventana
            cont+=1
            continue

        #Obtiene la apikey del usuario
        if records["Correo electrónico"][i] not in apikey_object["users"]:
            #Escribe el log
            logs.append(f'{records["Correo electrónico"][i]} no tiene registrada la apikey.')
            #Actualiza la barra de progreso
            barra_progreso.set(cont / len(records['Proyecto']))  # Actualizar progreso
            texto_progreso.set(f"{cont}/{len(records['Proyecto'])}")
            ventana_progreso.update_idletasks()  # Forzar actualización de la ventana
            cont+=1
            continue
        else:
            index_user = apikey_object["users"].index(records["Correo electrónico"][i])
            X_Api_Key = apikey_object["apikey"][index_user]

        #Obtiene el id del proyecto
        project_id = ""
        for p in projects:
            if p["name"] == records["Proyecto"][i]:
                project_id = p["id"]
                break
        
        if project_id == "":
            logs.append(f"El proyecto {records['Proyecto'][i]} no existe en el workspace.")
            #Actualiza la barra de progreso
            barra_progreso.set(cont / len(records['Proyecto']))  # Actualizar progreso
            texto_progreso.set(f"{cont}/{len(records['Proyecto'])}")
            ventana_progreso.update_idletasks()  # Forzar actualización de la ventana
            cont+=1
            continue
        
        #Verifica si la tarea viene vacia
        if records["Tarea"][i] == "":
            logs.append(f"El registro del usuario {records['Correo electrónico'][i]} del {records['Fecha de inicio'][i]} a las {records['Hora de inicio'][i]} no tiene tarea asignada.")
            #Actualiza la barra de progreso
            barra_progreso.set(cont / len(records['Proyecto']))  # Actualizar progreso
            texto_progreso.set(f"{cont}/{len(records['Proyecto'])}")
            ventana_progreso.update_idletasks()  # Forzar actualización de la ventana
            cont+=1
            continue

        #Obtiene el id de las tareas
        tareas = get_tasks(workspace_id,project_id)
        task_id = ""
        for j in range(len(tareas["tareas"])):
            if tareas["tareas"][j] == records["Tarea"][i]:
                task_id = tareas["id"][j]
                break

        if task_id == "":
            logs.append(f"La tarea {records['Tarea'][i]} no existe en el proyecto {records['Proyecto'][i]}.")
            #Actualiza la barra de progreso
            barra_progreso.set(cont / len(records['Proyecto']))  # Actualizar progreso
            texto_progreso.set(f"{cont}/{len(records['Proyecto'])}")
            ventana_progreso.update_idletasks()  # Forzar actualización de la ventana
            cont+=1
            continue

        #Descripción
        descripcion = records["Descripción"][i]

        #Fecha inicial de tarea
        fecha_inicial  = datetime.strptime(records["Fecha de inicio"][i], "%d/%m/%Y")
        fecha_inicial = fecha_inicial.strftime("%Y-%m-%d")
        #Fecha final de tarea
        fecha_final = datetime.strptime(records["Fecha de finalización"][i], "%d/%m/%Y")
        fecha_final = fecha_final.strftime("%Y-%m-%d")
        #Hora de inicio
        hora_inicio = convertir_a_formato_completo(records["Hora de inicio"][i])
        hora_inicio = convert24HFormat(hora_inicio)
        hora_inicio = convertUTCHour(f"{fecha_inicial}T{hora_inicio}")
        #Hora final
        hora_finalizacion = convertir_a_formato_completo(records["Hora de finalización"][i])
        hora_finalizacion = convert24HFormat(hora_finalizacion)
        hora_finalizacion = convertUTCHour(f"{fecha_final}T{hora_finalizacion}")


        #Data
        data = {
            "start": f"{hora_inicio}Z",
            "description": descripcion,
            "projectId": project_id,
            "taskId": task_id,
            "end": f"{hora_finalizacion}Z"
        }

        headers = {'content-type': 'application/json', 'X-Api-Key': X_Api_Key}

        # Post al servidor
        response = requests.post( url_base, headers=headers,data=json.dumps(data))

        #Actualiza la barra de progreso
        barra_progreso.set(cont / len(records['Proyecto']))  # Actualizar progreso
        texto_progreso.set(f"{cont}/{len(records['Proyecto'])}")
        ventana_progreso.update_idletasks()  # Forzar actualización de la ventana
        cont+=1

        if response.status_code != 201:
            logs.append(f"El registro de {records['Correo electrónico'][i]} del {['Fecha de inicio'][i]}  a las {records['Hora de inicio'][i]} correspondiente al proyecto {records['Proyecto'][i]} no fue subida.")
        else:
            exitos+=1
    
    ventana_progreso.destroy()
    time.sleep(1)

    #Crea la ruta de logs
    try:
        os.makedirs(f'{documents_path}\\logs_clockify\\subir_registros\\')
    except OSError:
        pass

    #Escribe los logs
    fecha_hora_actual = datetime.now()
    estampa = fecha_hora_actual.strftime("%Y_%m_%d_%H_%M_%S")

    if len(logs) != 0:

        with open(f'{documents_path}\\logs_clockify\\subir_registros\\{estampa}.txt',"w") as f:
            for line in logs:
                f.write(line + '\n')

        tkinter.messagebox.showinfo("Info",f"Se subieron {exitos} de {len(records['Proyecto'])} registros.")
    else:
        tkinter.messagebox.showinfo("Info",f'Se subieron todos los registros con éxito.')
    return