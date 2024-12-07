"""
VERIFICA EL USUARIO Y LA CONTRASEÑA
"""
import tkinter
import gspread
from _lib.f01_get_files_path import get_file_paths
import os

def verify_user(main_window,username,password):

    bool_admin = check_admin_users(username)

    if bool_admin != 1:
        tkinter.messagebox.showerror("Error", "Usuario incorrecto")
        return 0
    
    if password != "admin":
        tkinter.messagebox.showerror("Error", "Contraseña incorrecta")
        return 0

    return 1
    
def check_admin_users(username):

    lib_path = get_file_paths("_lib")
    file_key = "1I49RKQmi7h7YoQAh4EOTeqhdTJM-xAYH8pbR8lctcLU"
    sheet_name = 'admin'
    token_path = os.path.join(lib_path, "api_admin.json")

    #Conexión con el servicio de google
    workbook = googleSpreadSheetConnect(file_key,sheet_name,token_path)

    #Usuarios autorizados
    users = workbook.col_values(1)
    #Clave api
    apiKey = workbook.col_values(2)

    if username in users:
        idx_user = users.index(username)
        with open(os.path.join(lib_path, "config.ini"),"r") as f:
            lines = f.readlines()

        lines[1] = f"API_KEY = {apiKey[idx_user]}"

        with open(os.path.join(lib_path, "config.ini"), "w") as f:
            f.writelines(lines)
        
        return 1
    else:
        return 0

#%% Conecta a la hoja de Google Spreadsheet
def googleSpreadSheetConnect(file_key:str,sheet_name:str,token_path:str):
    """
    Input args:
        file_key: Código genérico del archivo (se encuentra en la url)
        sheet_name: Nombre de la hoja
        token_path: Ruta del token para conectarse a la API
    Output args:
        sheet: Hoja como objeto
    """

    #Conecta con google spreadsheet
    service = gspread.service_account(token_path)

    #Obtiene la hoja
    workbook = service.open_by_key(file_key)
    sheet = workbook.worksheet(sheet_name)

    return sheet
    

