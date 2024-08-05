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
from _Library.getProjectTask import getProjectTask

def get_workspace_id(workspace):

    library_path  = os.path.join(os.path.dirname(os.path.realpath(__file__)))

    #Obtiene el id del workspace
    with open(os.path.join(library_path, "workspaces.pkl"), 'rb') as file:
        workspaces = pickle.load(file)

    for w in workspaces:
        if w["name"] == workspace:
            workspaceId = w["id"]
    
    return workspaceId

def get_project_id(workspace,project):

    library_path  = os.path.join(os.path.dirname(os.path.realpath(__file__)))

    #Obtiene el id del proyecto
    with open(os.path.join(library_path, "projects.pkl"),'rb') as file:
        projects = pickle.load(file)

    for i in projects[workspace]:
        if projects[workspace][i]["name"] == project:
            projectId = projects[workspace][i]["id"]
            break
    
    return projectId

def get_user_apikey(email):

    library_path  = os.path.join(os.path.dirname(os.path.realpath(__file__)))

    #Obtiene la información de apikey
    with open(os.path.join(library_path, "APIKEY.pkl"), 'rb') as file:
        APIKEY = pickle.load(file)

    line = APIKEY.loc[APIKEY['Correo'] == email]

    return line.iloc[0,1]

def convertUTCHour(hour):

    timezone = pytz.timezone('America/Bogota')

    fecha = hour.split('T')[0]
    hora = hour.split('T')[1]

    anio = int(fecha.split('-')[0])
    mes = int(fecha.split('-')[1])
    dia = int(fecha.split('-')[2])

    h = int(hora.split(':')[0])
    m = int(hora.split(':')[1])

    original_time = datetime.datetime(anio, mes, dia, h, m)  # change this to sample datetime to test different values

    local_timezone_datetime = timezone.localize(original_time, False)  # change False to True if DST is enabled on the timezone

    converted_datetime = local_timezone_datetime.astimezone(pytz.utc)

    anio = converted_datetime.year
    mes = converted_datetime.month
    if mes < 10:
        mes = f'0{mes}'
    dia = converted_datetime.day
    if dia < 10:
        dia  = f'0{dia}'

    h =  converted_datetime.hour
    m = converted_datetime.minute

    if h < 10:
        h = f'0{h}'
    if m < 10:
        m = f'0{m}'


    hora = f'{anio}-{mes}-{dia}T{h}:{m}:00'


    return hora

def get_task_id(workspace,proyecto,tarea):

    task = getProjectTask(workspace,proyecto)

    taskId = task["ID"][task["Tareas"].index(tarea)]

    return taskId


def f_subir_registro(workspace:str,proyecto:str,email:str,tarea:str,fecha:str,hora:str,duracion:float, descripcion:str):
    
    library_path  = os.path.join(os.path.dirname(os.path.realpath(__file__)))

    #ID del workspace
    workspaceId = get_workspace_id(workspace)

    #ID del proyecto
    projectId = get_project_id(workspace,proyecto)

    #Obtiene apikey del usuario
    X_Api_Key = get_user_apikey(email)
    headers = {'content-type': 'application/json','X-Api-Key': X_Api_Key}

    #Fecha y hora inicial
    fecha_inicio = f"{fecha}T{hora}:00"
    fecha_inicio = convertUTCHour(fecha_inicio)

    #Fecha y hora final
    fecha_hora_inicial  = datetime.datetime.strptime(fecha_inicio, "%Y-%m-%dT%H:%M:%S")
    delta_tiempo = datetime.timedelta(hours=duracion)
    fecha_hora_resultante = fecha_hora_inicial + delta_tiempo
    fecha_fin = fecha_hora_resultante.strftime("%Y-%m-%dT%H:%M:%S")

    #Inicializa data
    data = {
        "start": f"{fecha_inicio}Z",
        "end": f"{fecha_fin}Z",
        "projectId": projectId
    }

    #Tarea
    if tarea != "":
        taskId = get_task_id(workspace,proyecto,tarea)
        data["taskId"] = taskId

    #Descripción
    if descripcion != "":
        data["description"] = descripcion


    # URL para subir registro
    url_base = f'https://api.clockify.me/api/v1/workspaces/{workspaceId}/time-entries'

    # Post al servidor
    response = requests.post( url_base, headers=headers,data=json.dumps(data))

    if response.status_code == 201:
        #Crea un log de exito
        with open(os.path.join(library_path, "exitoSubirRegistro.log"),"w") as f:
            f.write("Exito")
        f.close()
    else:
        #Crea un log de falla
        with open(os.path.join(library_path, "fallaSubirRegistro.log"),"w") as f:
            f.write("Falla")
        f.close()

    

    