"""
MÓDULO DE TRANSFERIR HORAS
"""
import os
from customtkinter import *
from _lib.get_workspaces import get_workspaces
from _lib.get_projects import get_projects
import tkinter
from datetime import datetime
from _lib.transfer_records import transfer_records

def open_transfer_window(menu_window, images_path):

    # Crear una nueva ventana
    transfer_window = CTkToplevel(menu_window)
    # Geometría
    width = 240
    height = 430
    screen_width = transfer_window.winfo_screenwidth()
    screen_height = transfer_window.winfo_screenheight()
    x = (screen_width - width) // 2
    y = (screen_height - height) // 2
    transfer_window.geometry(f'{width}x{height}+{x}+{y}')
    # Nombre de la ventana
    transfer_window.title("Transferencia Horas")
    # Ícono ventana
    transfer_window.after(201, lambda: transfer_window.iconbitmap(os.path.join(images_path, "Transferencia_Horas.ico")))
    # Resizable
    transfer_window.resizable(False, False)
    transfer_window.grab_set()  # Esto hace que la ventana sea modal
    transfer_window.transient(menu_window)  # Para que esté asociada a la ventana principal
    transfer_window.focus_force()  # Enfoca la ventana modal

    def click_transfer_records():

        #Verifica que el proyecto no esté vacío
        if project_dropdown.get() == "":
            tkinter.messagebox.showerror("Error","El proyecto no puede estar vacío.")
            return

        #verifica que las fechas no estén vacías
        if date_start.get() == "" or date_end == "":
            tkinter.messagebox.showerror("Error","Las fechas no pueden estar vacías.")
            return
        
        #verifica que las fechas estén en el formato correcto
        try:
           datetime.strptime(date_start.get(), '%Y-%m-%d')
           datetime.strptime(date_end.get(), '%Y-%m-%d')
        except ValueError:
            date_start.delete(0, "end")  
            date_end.delete(0, "end")  
            tkinter.messagebox.showerror("Error","Las fechas no están correctamente definidas.")
            return

        #Verifica si la fecha inicial es menor a la fecha final
        if datetime.strptime(date_start.get(), '%Y-%m-%d') > datetime.strptime(date_end.get(), '%Y-%m-%d'):
            date_start.delete(0, "end")  
            date_end.delete(0, "end")  
            tkinter.messagebox.showerror("Error","La fecha de inicio no puede ser mayor a la fecha de finalización.")
            return

        #Obtiene los workspaces
        workspace_origen = workspace_1.get()
        workspace_destino = workspace_2.get()

        #Obtiene los proyectos
        decoded_content = get_workspaces()

        #ID de los workspaces
        for workspace in decoded_content:

            if workspace["name"] == workspace_origen:
                workspace_id_origen = workspace["id"]

            if workspace["name"] == workspace_destino:
                workspace_id_destino = workspace["id"]

        transfer_records(workspace_id_origen,workspace_id_destino,project_dropdown.get(),date_start.get(),date_end.get())


    # Lista de workspaces
    workspaces = populate_origin_workspace()

    #Label workspace origen
    label_origen_workspace = CTkLabel(master=transfer_window,text="Workspace origen:",fg_color="transparent",font=('Gothic A1',15))
    label_origen_workspace.place(x= 30,y=20)

    # Dropdown del espacio de trabajo origen
    workspace_1 = CTkOptionMenu(
        master=transfer_window,
        hover=True,
        corner_radius=3,
        fg_color="gray25",
        button_color="gray50",
        font=('Gothic A1', 12),
        dropdown_font=('Gothic A1', 12),
        dynamic_resizing=False,
        width=180,
        height=22,
        values=workspaces,
        command=lambda _: update_workspace_2(workspace_1, workspace_2, workspaces)
    )
    workspace_1.place(x=30, y=50)
    workspace_1.set(workspaces[0])

    #Label workspace origen
    label_destino_workspace = CTkLabel(master=transfer_window,text="Workspace destino:",fg_color="transparent",font=('Gothic A1',15))
    label_destino_workspace.place(x= 30,y=90)

    # Dropdown del espacio de trabajo destino
    workspace_2 = CTkOptionMenu(
        master=transfer_window,
        values=[""],
        hover=True,
        corner_radius=3,
        fg_color="gray25",
        button_color="gray50",
        font=('Gothic A1', 12),
        dropdown_font=('Gothic A1', 12),
        dynamic_resizing=False,
        width=180,
        height=22,
        command=lambda _: update_project(workspace_1, workspace_2,project_dropdown)
    )
    workspace_2.place(x=30, y=120)

    #Seleccionar proyecto
    label_project_workspace = CTkLabel(master=transfer_window,text="Proyecto:",fg_color="transparent",font=('Gothic A1',15))
    label_project_workspace.place(x= 30,y=160)

    # Dropdown del proyecto entre los dos workspaces
    project_dropdown = CTkOptionMenu(
        master=transfer_window,
        values=[""],
        hover=True,
        corner_radius=3,
        fg_color="gray25",
        button_color="gray50",
        font=('Gothic A1', 12),
        dropdown_font=('Gothic A1', 12),
        dynamic_resizing=False,
        width=180,
        height=22
    )
    project_dropdown.place(x=30, y=190)

    #Label workspace origen
    label_date_start = CTkLabel(master=transfer_window,text="Fecha de inicio:",fg_color="transparent",font=('Gothic A1',15))
    label_date_start.place(x= 30,y=230)

    #Fecha de inicio
    date_start = CTkEntry(master=transfer_window, width=90, font=('Gothic A1', 12), placeholder_text="aaaa-mm-dd")
    date_start.place(x=30, y=260)

    #Label workspace final
    label_date_end = CTkLabel(master=transfer_window,text="Fecha de finalización:",fg_color="transparent",font=('Gothic A1',15))
    label_date_end.place(x= 30,y=300)

    #Fecha de finalización
    date_end = CTkEntry(master=transfer_window, width=90, font=('Gothic A1', 12), placeholder_text="aaaa-mm-dd")
    date_end.place(x=30, y=330)

    # Botón transferior
    transfer_button = CTkButton(
        master=transfer_window,
        text="Transferir",
        width=100,
        height=30,
        command=click_transfer_records
    )
    transfer_button.place(x=70, y=380)

    #Actualiza el workspace destino
    update_workspace_2(workspace_1, workspace_2, workspaces) 
    #Actualice proyecto
    update_project(workspace_1, workspace_2,project_dropdown)

# Popular dropdown workspace origen
def populate_origin_workspace():
    # Lista de los workspaces
    decoded_content = get_workspaces()
    workspaces = [d["name"] for d in decoded_content]
    return workspaces

# Función para actualizar las opciones de workspace_2
def update_workspace_2(workspace_1,workspace_2,workspaces):
    selected_workspace = workspace_1.get()
    available_workspaces = [ws for ws in workspaces if ws != selected_workspace]
    workspace_2.configure(values=available_workspaces)
    workspace_2.set(available_workspaces[0] if available_workspaces else "")

# Función para actualizar las opciones de proyecto
def update_project(workspace_1,workspace_2,project_dropdown):

    #Obtiene los workspaces
    workspace_origen = workspace_1.get()
    workspace_destino = workspace_2.get()

    #Obtiene los proyectos
    decoded_content = get_workspaces()

    #ID de los workspaces
    for workspace in decoded_content:

        if workspace["name"] == workspace_origen:
            workspace_id_origen = workspace["id"]

        if workspace["name"] == workspace_destino:
            workspace_id_destino = workspace["id"]

    #Obtiene los proyectos de workspace de origen
    projects_origen = get_projects(workspace_id_origen)
    projects_origen = [proj["name"] for proj in projects_origen]
    
    #Obtiene los proyectos de workspace de destino
    projects_destino = get_projects(workspace_id_destino)
    projects_destino = [proj["name"] for proj in projects_destino]

    #Proyectos en común
    elementos_comunes = list(set(projects_origen).intersection(projects_destino))

    #Configura el dropdown
    project_dropdown.configure(values=elementos_comunes)
    project_dropdown.set(elementos_comunes[0] if elementos_comunes else "")
    