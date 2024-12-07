"""
OBTIENE LA APIKEY DE TODOS LOS USUARIOS
"""

from _lib.f02_verify_user import googleSpreadSheetConnect

def users_apikey(file_key,sheet_name,token_path):

    #Conexión con el servicio de google
    workbook = googleSpreadSheetConnect(file_key,sheet_name,token_path)

    #Usuarios autorizados
    users = workbook.col_values(4)[1:]
    #Clave api
    apiKey = workbook.col_values(6)[1:]

    return {"users" : users , "apikey" : apiKey}