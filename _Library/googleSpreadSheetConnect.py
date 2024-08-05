"""
CREATED BY: KATERINE ARIAS
"""
#Importa librerías
import gspread

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
    

