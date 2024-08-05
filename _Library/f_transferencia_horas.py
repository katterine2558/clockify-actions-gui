
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

def convertHour(hour):

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

def date_range_list(start_date:str, end_date:str):

    start_date = datetime.date(year=int(start_date.split('-')[0]),month=int(start_date.split('-')[1]),day=int(start_date.split('-')[2]))

    end_date = datetime.date(year=int(end_date.split('-')[0]),month=int(end_date.split('-')[1]),day=int(end_date.split('-')[2]))

    # Return list of datetime.date objects between start_date and end_date (inclusive).
    date_list = []
    curr_date = start_date
    while curr_date <= end_date:
        date_list.append(curr_date)
        curr_date += datetime.timedelta(days=1)
    return date_list

def getProjectTask(ID_workspace_origen: str, ID_workspace_destino: str, ID_project_origen: str,  ID_project_destino: str):

    library_path  = os.path.join(os.path.dirname(os.path.realpath(__file__)))

    task_origen, task_destino = [], []

    for i in range(2):

        if i == 0:
            workspaceId = ID_workspace_origen
            projectId = ID_project_origen
        else:
            workspaceId = ID_workspace_destino
            projectId = ID_project_destino

        # URL para obtener los proyectos del workspace
        url_base = f'https://api.clockify.me/api/v1/workspaces/{workspaceId}/projects/{projectId}/tasks'

        # Lectura de la clave de la API
        config = configparser.ConfigParser()
        config.read(os.path.join(library_path, "config.ini")) 
        X_Api_Key = config.get('clockify', 'API_KEY')

        # Get al servidor
        headers = { 'X-Api-Key': X_Api_Key}
        data = {
            "page-size": 200,
            "page": 1
            }
        response = requests.get(url_base, headers=headers, params=data)
        decoded_content = response.content.decode('utf-8')
        try:
            decoded_content = decoded_content.replace("null","None")
        except:
            pass
        try:
            decoded_content = decoded_content.replace("true","True")
        except:
            pass
        try:
            decoded_content = decoded_content.replace("false","False")
        except:
            pass

        decoded_content = eval(decoded_content)

        if i == 0:
            task_origen = decoded_content
        else:
            task_destino = decoded_content

    return task_origen, task_destino

def getRecords(start_date:str, end_date:str, ID_workspace_origen:str, ID_project_origen:str ):

    library_path  = os.path.join(os.path.dirname(os.path.realpath(__file__)))

    # URL para generar reporte
    url_base = f'https://reports.api.clockify.me/v1'
    url_report = f'/workspaces/{ID_workspace_origen}/reports/detailed'
    url = url_base  + url_report

    # Lectura de la clave de la API 
    config = configparser.ConfigParser()
    config.read(os.path.join(library_path, "config.ini"))
    X_Api_Key = config.get('clockify', 'API_KEY')
    # Post al servidor
    headers = {'content-type': 'application/json', 'X-Api-Key': X_Api_Key}
    data = {
    "dateRangeStart": f"{start_date}T00:00:00.000",
    "dateRangeEnd": f"{end_date}T23:59:59.000",
    "detailedFilter": {
        "page": 1,
        "pageSize": 1000
    },
    "projects":{
        "contains": "CONTAINS",
        "ids":[ID_project_origen]
    },
    "users": {
        "status": "ALL"
    },
    "exportType": "JSON"
    }

    response = requests.post( url, headers=headers, data=json.dumps(data))
    userRecords = json.loads(response.content)

    return userRecords

def deleteServer(start_date, end_date,ID_workspace_destino, ID_project_destino,ID_group):
    
    library_path  = os.path.join(os.path.dirname(os.path.realpath(__file__)))

    #Consulta los registros en el rango de tiempo
    url_base = f'https://reports.api.clockify.me/v1'
    url_report = f'/workspaces/{ID_workspace_destino}/reports/detailed'
    url = url_base  + url_report

    config = configparser.ConfigParser()
    config.read(os.path.join(library_path, "config.ini")) 
    X_Api_Key = config.get('clockify', 'API_KEY')
    # Post al servidor
    headers = {'content-type': 'application/json', 'X-Api-Key': X_Api_Key}
    data = {
    "dateRangeStart": f"{start_date}T00:00:00.000",
    "dateRangeEnd": f"{end_date}T23:59:59.000",
    "detailedFilter": {
        "page": 1,
        "pageSize": 1000
    },
    "projects":{
        "contains": "CONTAINS",
        "ids":[ID_project_destino]
    },
    "userGroups":{
        "ids":[ID_group]
    },
    "users": {
        "status": "ALL"
    },
    "exportType": "JSON"
    }

    response = requests.post( url, headers=headers, data=json.dumps(data))
    userRecords = json.loads(response.content)

    if len(userRecords["timeentries"]) > 0:
        for timeentry in userRecords["timeentries"]:
            
            #id timeentry
            id_timeentry = timeentry["_id"]

            #url delete
            url_delete = f"https://api.clockify.me/api/v1/workspaces/{ID_workspace_destino}/time-entries/{id_timeentry}"

            #Delete to server
            response = requests.delete( url_delete, headers=headers)

def postServer(records_workspace_origen, ID_workspace_destino, ID_project_destino, task_destino, APIKEY,logs,logs_generales,exitos, fracasos):

    #URL POST
    url_POST = f'https://api.clockify.me/api/v1/workspaces/{ID_workspace_destino}/time-entries'

    #Itera por registro
    for timeentry in records_workspace_origen["timeentries"]:

        #Extrae los parámetros necesarios para hacer post o delete en el servidor
        start_date = timeentry['timeInterval']['start'].split('-05:00')[0]
        end_date = timeentry['timeInterval']['end'].split('-05:00')[0] 
        task_name =  timeentry['taskName']
        user_email = timeentry["userEmail"]
        if not timeentry["description"]:
            description="Default"
        else:
            description = timeentry["description"]

        #Modifica las horas. El servidor está en GMT
        start_date = convertHour(start_date)
        end_date = convertHour(end_date)

        #Verifica si el usuario tiene registrada clave api
        try:
            api_key =  APIKEY["Key"][APIKEY["correo"].index(user_email)]    
        except ValueError:
            fracasos +=1
            temp_value = start_date.split("T")[0]
            duracion = timeentry["timeInterval"]["duration"] / 3600 
            logs.append(f"[{temp_value}] El usuario: {user_email} no tiene registrada clave API. No se migró el registro con duración de {duracion} horas.\n")
            logs_generales.append(f"[{temp_value}] El usuario: {user_email} no tiene registrada clave API. No se migró el registro con duración de {duracion} horas.\n")
            continue

        #Verifica si el nombre de la tarea coincide en ambos workspaces
        task_id = next((item['id'] for item in task_destino if item['name'] == task_name), None) 

        if task_id is None:
            fracasos +=1
            temp_value = start_date.split("T")[0]
            duracion = timeentry["timeInterval"]["duration"] / 3600 
            logs.append(f"[{temp_value}] No se migró el registro de {user_email} con duración de {duracion} horas dado que la tarea no coincide en el workspace de destino.\n")
            logs_generales.append(f"[{temp_value}] No se migró el registro de {user_email} con duración de {duracion} horas dado que la tarea no coincide en el workspace de destino.\n")
            continue
        
        #Hace el post al servidor
        data = {
                "start": f"{start_date}Z",
                "description": description,
                "projectId": ID_project_destino,
                "taskId": task_id,
                "end": f"{end_date}Z"
                }
        
        headers = {'content-type': 'application/json', 'X-Api-Key': api_key}
        response = requests.post( url_POST, headers=headers, data=json.dumps(data))

        if response.status_code == 201:
            exitos +=1
        else:
            fracasos +=1
            if response.status_code == 403:
                temp_value = start_date.split("T")[0]
                duracion = timeentry["timeInterval"]["duration"] / 3600 
                logs.append(f"[{temp_value}] No se migró el registro de {user_email} con duración de {duracion} horas dado que no pertenece al workspace de destino. \n")
                logs_generales.append(f"[{temp_value}] No se migró el registro de {user_email} con duración de {duracion} horas dado que no pertenece al workspace de destino. \n")
            elif response.status_code == 400:
                temp_value = start_date.split("T")[0]
                duracion = timeentry["timeInterval"]["duration"] / 3600 
                logs.append(f"[{temp_value}] No se migró el registro de {user_email} con duración de {duracion} horas dado no tiene grupo asignado. \n")
                logs_generales.append(f"[{temp_value}] No se migró el registro de {user_email} con duración de {duracion} horas dado no tiene grupo asignado. \n")

    return logs, logs_generales, exitos, fracasos


def f_transferencia_horas(home_window: object, workspace_origen:str, workspace_destino:str, proyecto:str, fecha_inicio:str, fecha_fin:str):

    library_path  = os.path.join(os.path.dirname(os.path.realpath(__file__)))

    #ruta para almacenar logs
    ruta_documentos = os.path.expanduser("~\\Documents")

    #abre proyectos y workspaces
    with open(os.path.join(library_path, "projects.pkl"), 'rb') as file:
        projects = pickle.load(file)
    file.close()

    #Abre los workspaces
    with open(os.path.join(library_path, "workspaces.pkl"), 'rb') as file:
        workspaces = pickle.load(file)
    file.close()

    #Abre los grupos
    with open(os.path.join(library_path, "groups.pkl"), 'rb') as file:
        groups = pickle.load(file)
    file.close()

    #Abre la clave API para todos los usuarios
    with open(os.path.join(library_path, "APIKey.pkl"), 'rb') as file:
        APIKEY = pickle.load(file)
    file.close()

    APIKEY = {"correo":list(APIKEY.iloc[:,0]),
            "Key": list(APIKEY.iloc[:,1])}
    
    #Inicia la lista de logs generales
    logs_generales = []

    #ID del workspace de origen
    ID_workspace_origen = next((item['id'] for item in workspaces if item['name'] == workspace_origen), None)

    #ID del workspace de destomp
    ID_workspace_destino = next((item['id'] for item in workspaces if item['name'] == workspace_destino), None)

    #ID del proyecto en el workspace de origen
    ID_project_origen = next((project_data['id'] for project_id, project_data in projects[workspace_origen].items() if project_data['name'] == proyecto), None)

    #ID del proyecto en el workspace de destino
    ID_project_destino = next((project_data['id'] for project_id, project_data in projects[workspace_destino].items() if project_data['name'] == proyecto), None)

    #Inicializa el contador de exitos y fracasos
    exitos, fracasos = 0,0

    #Rango de días
    dateList = date_range_list(fecha_inicio,fecha_fin)

    #Obtiene la tarea del proyecto para ambos workspaces
    task_origen, task_destino = getProjectTask(ID_workspace_origen, ID_workspace_destino, ID_project_origen,  ID_project_destino)

    #Obtiene el id del grupo de usuarios para borrar registros
    ID_group = next((item['id'] for item in groups[workspace_destino] if item['name'] == "NOMBRE_GRUPO"), None)

    #Intenta crear la carpeta de logs
    try:
        os.mkdir(f"{ruta_documentos}\TransferenciaHoras_log")
    except OSError:
        pass

    #Extrae la información diaria
    for date in dateList:

        #inicializa el registro de logs. Se generará un log por cada día
        logs=[]

        #Arregla las fechas
        if date.month <=9:
            month = f'0{date.month}'
        else:
            month = date.month
        
        if date.day <=9:
            day = f'0{date.day}'
        else:
            day = date.day

        start_date = f'{date.year}-{month}-{day}'
        end_date = f'{date.year}-{month}-{day}'

        print(start_date)

        #Obtiene los registros para la fecha y el proyecto específico en el workspace de origen
        records = getRecords(start_date, end_date, ID_workspace_origen, ID_project_origen)

        #Elimina todos los registros posibles de los usuarios en el rango de fecha
        deleteServer(start_date, end_date,ID_workspace_destino, ID_project_destino,ID_group)

        #POST al servidor
        logs, logs_generales, exitos, fracasos = postServer(records, ID_workspace_destino, ID_project_destino, task_destino, APIKEY,logs,logs_generales,exitos, fracasos)

        #Escribe los logs en documentos
        with open(f"{ruta_documentos}\TransferenciaHoras_log\{start_date}.log","w") as f:
            for line in logs:
                f.write(line)
        f.close()

    #Escribe los logs en documentos
    with open(f"{ruta_documentos}\TransferenciaHoras_log\generales.log","w") as f:
        for line in logs_generales:
            f.write(line)
    f.close()

    #Guarda exitos y fracasos
    contadores = {"exitos": exitos, "fracasos": fracasos}
    with open(os.path.join(library_path, "contadores.pkl"), 'wb') as f: 
        pickle.dump(contadores, f) 
    f.close()

    