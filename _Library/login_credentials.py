import pickle

"""
Inyectar usuarios administradores para el inicio de sesión
"""
admin = {
    "usernames": ["prueba1", "prueba2","1"],
    "passwords": ["admin11", "admin11","1"],
    "nombre": ["Usuario 1", "Usuario 2","Prueba"],
}

#Almacena las claves API en _Library
with open('_Library/login_credentials.pkl', 'wb') as f: 
    pickle.dump(admin, f) 
f.close()

with open('_Library/projects.pkl', 'rb') as file:
    projects = pickle.load(file)
file.close()

