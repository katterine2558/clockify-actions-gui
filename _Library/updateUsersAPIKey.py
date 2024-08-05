"""
CREATED BY: KATERINE ARIAS
"""

#Importa librerías
import gspread
import pandas as pd
from _Library.googleSpreadSheetConnect import *
import pickle
import os

"""
"""

def getAPIRecords(sheet:object):
    """
    Input args:
        sheet: Hoja como objeto
    Output args:
        dataframe: DataFrame con los registros de los usuarios
    """

    email_list = sheet.col_values(2)[1:]
    apiKey_list = sheet.col_values(6)[1:]

    df = pd.DataFrame({
        "Correo": email_list,
        "APIKEY": apiKey_list
    })

    return df

def updateUserAPIKeys(file_key: str ,sheet_name: str,token_path: str):

    library_path  = os.path.join(os.path.dirname(os.path.realpath(__file__)))

    #Conexión con el servicio de google
    workbook = googleSpreadSheetConnect(file_key,sheet_name,token_path)

    # Registros de clave api en forma de DataFrame
    df = getAPIRecords(workbook)
    #Almacena las claves API en _Library
    with open(os.path.join(library_path, "APIKey.pkl"), 'wb') as f: 
        pickle.dump(df, f) 
    f.close()
    