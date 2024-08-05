"""
CREATED BY: KATERINE ARIAS
"""

#Importa librerías
import pickle
import os

def updateConfigIni(user_name):
    """
    Input args:
        user_name: Nombre de usuario que inicia sesión
    Output args:
    """
    library_path  = os.path.join(os.path.dirname(os.path.realpath(__file__)))

    #Abre el binario con las claves API
    with open(os.path.join(library_path, "APIKey.pkl"), 'rb') as file:
        APIKEY = pickle.load(file)
    file.close()

    #Encuentra la clave API del usuario que se loggeó
    api_key = APIKEY.loc[APIKEY["Correo"] == f'{user_name}@tucorreo.com'].iloc[0,1]
    
    #Abre el archivo config.ini y lo edita
    with open(os.path.join(library_path, "config.ini"),"r") as f:
        lines = f.read()
    f.close()
    lines = lines.split("\n")
    lines[-1] = f"API_KEY = {api_key}"

    with open(os.path.join(library_path, "config.ini"),"w") as f:
        f.write(lines[0])
        f.write("\n")
        f.write(lines[-1])
    f.close()

