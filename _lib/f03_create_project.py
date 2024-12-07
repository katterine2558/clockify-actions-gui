"""
MÓDULO DE CREAR PROYECTO
"""
import os
from customtkinter import * 
from _lib.get_workspaces import get_workspaces
from _lib.create_project import create_project
import tkinter

def open_create_project_window(menu_window, images_path):

    # Crear una nueva ventana
    window = CTkToplevel(menu_window)
    # Geometría
    width =230
    height = 220
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    x = (screen_width - width) // 2
    y = (screen_height - height) // 2
    window.geometry(f'{width}x{height}+{x}+{y}')
    # Nombre de la ventana
    window.title("Crear proyecto")
    # Ícono ventana
    window.after(201, lambda: window.iconbitmap(os.path.join(images_path, "Crear_Proyecto.ico")))
    # Resizable
    window.resizable(False, False)
    window.grab_set()  # Esto hace que la ventana sea modal
    window.transient(menu_window)  # Para que esté asociada a la ventana principal
    window.focus_force()  # Enfoca la ventana modal

    # Lista de workspaces
    workspaces, decoded_content = populate_workspace()

    #Label seleccionar workspace
    label_workspace = CTkLabel(master=window,text="Seleccione workspace:",fg_color="transparent",font=('Gothic A1',15))
    label_workspace.place(x= 35,y=20)

    #Dropdown seleccionar workspace
    workspace_1 = CTkOptionMenu(
        master=window,
        hover=True,
        corner_radius=3,
        fg_color="gray25",
        button_color="gray50",
        font=('Gothic A1', 12),
        dropdown_font=('Gothic A1', 12),
        dynamic_resizing=False,
        width=160,
        height=22,
        values=workspaces
    )
    workspace_1.place(x=35, y=50)
    workspace_1.set(workspaces[0])

    #Label nombre proyecto
    crear_label = CTkLabel(master=window,text="Nombre del proyecto:",fg_color="transparent",font=('Gothic A1',15))
    crear_label.place(x= 35,y=90)
    #entrada nombre proyecto
    nombre_proyecto=CTkEntry(master=window, width=160, placeholder_text='')
    nombre_proyecto.place(x= 35 ,y=120)
    #Botón de crear proyecto
    crear= CTkButton(master=window, text="Crear", width=70, height=30, compound="left",font=('Gothic A1',15), command=lambda: click_create_project(nombre_proyecto.get(), workspace_1.get(), window,decoded_content) ) 
    crear.place(x= 80 ,y=170)

def click_create_project(project_name,workspace_name, window,workspaces_objets):

    if project_name == "":
        tkinter.messagebox.showerror(title="Error", message="Nombre del proyecto inválido.")
        return

    #Obtiene el ID del workspace
    for w in workspaces_objets:
        if w["name"] == workspace_name:
            workspace_id = w["id"]
            break
    
    # Intenta crear el proyecto
    if create_project(project_name, workspace_id):
        window.destroy() 
    
# Popular workspaces
def populate_workspace():
    # Lista de los workspaces
    decoded_content = get_workspaces()
    workspaces_list = [d["name"] for d in decoded_content]
    return workspaces_list, decoded_content



