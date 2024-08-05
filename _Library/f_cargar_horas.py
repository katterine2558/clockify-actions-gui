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

def convert24HFormat(str1):

    if 'AM' in str1:
        if int(str1.split(':')[0])<=9:
            hora =  str1.split(':')[0]
            hora = f'0{hora}'
        elif int(str1.split(':')[0])== 12:
            hora = '00'
        else:
            hora =  str1.split(':')[0]

    else:
        if int(str1.split(':')[0])==12:
            hora = str1.split(':')[0]
        else:
            if int(str1.split(':')[0])>=1: 
                hora = int(str1.split(':')[0])+12  
            else:
                hora = str1.split(':')[0]

    minutos = str1.split(':')[1]
    segundos = str1.split(' ')[0].split(':')[2]
    hora = f'{hora}:{minutos}:{segundos}'

    return hora

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

def f_cargar_horas(dataframe:object, workspace_origen:str,workspace_destino:str, project_name:str):

    library_path  = os.path.join(os.path.dirname(os.path.realpath(__file__)))

    #ruta para almacenar logs
    ruta_documentos = os.path.expanduser("~\\Documents")

    #Abre la información de los workspaces
    with open(os.path.join(library_path, "workspaces.pkl"), 'rb') as file:
        workspaces = pickle.load(file)
    file.close()

    #Abre la información de los proyectos
    with open(os.path.join(library_path, "projects.pkl"), 'rb') as file:
        projects = pickle.load(file)
    file.close()

    #Abre información de API
    with open(os.path.join(library_path, "APIKey.pkl"), 'rb') as file:
        APIKEY = pickle.load(file)
    file.close()

    #inicializa el registro de logs
    logs=[]

    #Inicializa el contador de exitos y fracasos
    exitos, fracasos = 0,0

    #Tareas del proyecto
    taskProject = getProjectTask(workspace_destino,project_name)

    #ID del workspace de destino
    for w in workspaces:
        if w["name"] == workspace_destino:
            workspaceId = w["id"]
            break

    #ID del proyecto
    for proj in projects[workspace_destino]:
        if projects[workspace_destino][proj]["name"] == project_name:
            projectId = projects[workspace_destino][proj]["id"]
            break

    #URL de conexión
    url_base = f'https://api.clockify.me/api/v1'
    url_post = f'/workspaces/{workspaceId}/time-entries'
    url = url_base  + url_post

    #itera por los usuarios
    for i in range(len(dataframe)):

        #Verifica si el usuario tiene clave API
        if dataframe.iloc[i,6] in APIKEY["Correo"].values:

            #Clave api del usuario
            x_api_key = APIKEY.loc[APIKEY['Correo'] == dataframe.iloc[i,6]].iloc[0,1]

        else:
            logs.append(f"El usuario {dataframe.iloc[i,6]} no tiene clave API.\n")
            fracasos+=1
            continue

        #Verifica si la tarea existe
        if dataframe.iloc[i,3] in taskProject["Tareas"]:
            taskId = taskProject["ID"][taskProject["Tareas"].index(dataframe.iloc[i,3])]
        else:
            logs.append(f"La tarea {dataframe.iloc[i,3]} del usuario {dataframe.iloc[i,6]} no existe. \n")
            fracasos+=1
            continue

        #Descripcion
        descripcion = dataframe.iloc[i,2]

        # Convertir hora en formato 24 horas
        sdate = dataframe.iloc[i,9].split('/')
        edate = dataframe.iloc[i,11].split('/')
        hIni = dataframe.iloc[i,10].split(' ')
        horaIni = f"{hIni[0]}:00 {hIni[1]}"
        hEnd = dataframe.iloc[i,12].split(' ')
        horaEnd = f"{hEnd[0]}:00 {hEnd[1]}"

        horaI = convert24HFormat(horaIni)
        horaE = convert24HFormat(horaEnd)

        #Convierte la hora colombiana a la del servidor
        start_date = f'{sdate[2]}-{sdate[1]}-{sdate[0]}T{horaI}'
        end_date = f'{edate[2]}-{edate[1]}-{edate[0]}T{horaE}' #Fecha fin de tarea
        start_date = convertUTCHour(start_date)
        end_date = convertUTCHour(end_date)

        data = {
            "start": f"{start_date}Z",
            "description": descripcion,
            "projectId": projectId,
            "taskId": taskId,
            "end": f"{end_date}Z"
        }
            
        headers = {'content-type': 'application/json', 'X-Api-Key': x_api_key}

        response = requests.post( url, headers=headers, data=json.dumps(data))
        if response.status_code == 201:
            exitos+=1
        else:
            logs.append(f"[{start_date}] El usuario {dataframe.iloc[i,6]} no pertenece al workspace.\n")
            fracasos+=1

    #Escribe los logs en documentos
    with open(f"{ruta_documentos}\CargarHoras.log","w") as f:
        for line in logs:
            f.write(line)
    f.close()

    #Guarda exitos y fracasos
    contadores = {"exitos": exitos, "fracasos": fracasos}
    with open(os.path.join(library_path, "contadores_cargarHoras.pkl"), 'wb') as f: 
        pickle.dump(contadores, f) 
    f.close()
        


        