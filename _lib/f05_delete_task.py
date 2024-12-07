"""
MÓDULO DE ELIMINAR TAREAS
"""
import os
import tkinter.messagebox
from customtkinter import * 
from _lib.get_workspaces import get_workspaces
from _lib.get_projects import get_projects
from _lib.delete_task import delete_task
import tkinter

def open_delete_task_window(menu_window, images_path):
    # Crear una nueva ventana
    window = CTkToplevel(menu_window)
    # Geometría
    width = 300
    height = 340
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    x = (screen_width - width) // 2
    y = (screen_height - height) // 2
    window.geometry(f'{width}x{height}+{x}+{y}')
    window.title("Eliminar tareas")
    window.after(201, lambda: window.iconbitmap(os.path.join(images_path, "Eliminar_Tarea.ico")))
    window.resizable(False, False)
    window.grab_set()
    window.transient(menu_window)
    window.focus_force()

    # Variables para almacenar datos del archivo y IDs
    file_content = ""
    workspace_id = ""
    project_id = ""
    project_object = []  # Para almacenar los proyectos con sus IDs

    # Función para actualizar el dropdown de proyectos al seleccionar un workspace
    def update_project_dropdown(workspace_name, workspace_object, filter_text=""):

        nonlocal workspace_id, project_object

        all_projects, project_object = get_projects_for_workspace(workspace_name,workspace_object)
        # Filtrar los proyectos que contengan el texto ingresado
        filtered_projects = [p for p in all_projects if filter_text.lower() in p.lower()]
        project_menu.configure(values=filtered_projects)
        if filtered_projects:
            project_menu.set(filtered_projects[0])  # Seleccionar el primer proyecto por defecto
        else:
            project_menu.set("No hay proyectos")

        # Obtener el ID del workspace seleccionado
        for w in workspace_object:
            if w["name"] == workspace_name:
                workspace_id = w["id"]
                break

    #Función para adjuntar archivo con las tareas
    def open_file_dialog(browse_entry):

        nonlocal file_content

        #ruta del archivo
        file_path = filedialog.askopenfilename()
        #extensión del archivo
        file_extension = os.path.splitext(file_path)[1]
        #nombre del archivo
        file_name = os.path.basename(file_path)  # Obtiene solo el nombre del archivo

        if file_extension != ".txt":
            tkinter.messagebox.showerror("Error","Formato de archivo no válido.")
            return
        else:
            browse_entry.configure(state=NORMAL)  # Habilita el campo para insertar el texto
            browse_entry.delete(0, "end")  # Limpia el contenido actual del campo
            browse_entry.insert(0, file_name)  # Inserta la ruta del archivo en el campo
            browse_entry.configure(state=DISABLED)  # Desactiva nuevamente el campo para que no se edite

            # Leer el contenido del archivo .txt
            with open(file_path, 'r', encoding='utf-8') as file:
                file_content = file.read()

            # Convertir el contenido a una lista
            if file_content.strip():  # Verifica que el contenido no esté vacío
                file_content = file_content.splitlines()  # Convierte el contenido a una lista, incluso si es una sola línea
            else:
                tkinter.messagebox.showerror("Error", "El archivo está vacío o no está en el formato correcto.")
                file_content = ""  # Reiniciar el contenido si no cumple con el formato

    # Función para obtener el ID del proyecto seleccionado
    def get_selected_project_id():
        nonlocal project_id
        selected_project_name = selected_project.get()
        for p in project_object:
            if p["name"] == selected_project_name:
                project_id = p["id"]
                break
    
    # Función para el botón eliminar tareas
    def click_delete_task():
        
        #Obtiene el ID del proyecto
        get_selected_project_id()  

        if file_content == "":
            tkinter.messagebox.showerror("Error","Adjuntar un archivo válido.")
            return
        else:
            delete_task(workspace_id,project_id,file_content)

        

    # Obtener y mostrar la lista de workspaces
    workspaces, workspaces_object = populate_workspace()

    # Label seleccionar workspace
    label_workspace = CTkLabel(master=window, text="Seleccione workspace:", fg_color="transparent", font=('Gothic A1', 15))
    label_workspace.place(x=35, y=20)

    # Dropdown seleccionar workspace
    selected_workspace = StringVar(window)
    workspace_menu = CTkOptionMenu(
        master=window,
        variable=selected_workspace,
        hover=True,
        corner_radius=3,
        fg_color="gray25",
        button_color="gray50",
        font=('Gothic A1', 12),
        dropdown_font=('Gothic A1', 12),
        dynamic_resizing=False,
        width=200,
        height=22,
        values=workspaces,
        command=lambda _: update_project_dropdown(selected_workspace.get(),workspaces_object)
    )
    workspace_menu.place(x=35, y=50)
    workspace_menu.set(workspaces[0]) 

    # Label seleccionar proyecto
    label_project = CTkLabel(master=window, text="Seleccione proyecto:", fg_color="transparent", font=('Gothic A1', 15))
    label_project.place(x=35, y=90)

    # Campo de entrada para filtrar proyectos
    project_filter_entry = CTkEntry(master=window, width=140, font=('Gothic A1', 12), placeholder_text="Filtrar proyectos")
    project_filter_entry.place(x=35, y=120)

    # Botón para aplicar el filtro
    filter_button = CTkButton(
        master=window,
        text="Filtrar",
        width=80,
        height=22,
        command=lambda: update_project_dropdown(selected_workspace.get(), workspaces_object,project_filter_entry.get())
    )
    filter_button.place(x=190, y=120)

    # Dropdown para los proyectos (inicialmente vacío)
    selected_project = StringVar(window)
    project_menu = CTkOptionMenu(
        master=window,
        variable=selected_project,
        hover=True,
        corner_radius=3,
        fg_color="gray25",
        button_color="gray50",
        font=('Gothic A1', 12),
        dropdown_font=('Gothic A1', 12),
        dynamic_resizing=False,
        width=200,
        height=22,
        values=["Selecciona un workspace"]
    )
    project_menu.place(x=35, y=160)

    #Label para examinar el archivo
    label_browse = CTkLabel(master=window, text="Buscar archivo:", fg_color="transparent", font=('Gothic A1', 15))
    label_browse.place(x=35, y=200)

    # Campo de entrada para el nombre del archivo
    browse_entry = CTkEntry(master=window, width=140, font=('Gothic A1', 12), placeholder_text="Archivo",state=DISABLED)
    browse_entry.place(x=35, y=230)

    # Botón para buscar archivo
    browse_button = CTkButton(
        master=window,
        text="Examinar",
        width=80,
        height=22,
        command= lambda: open_file_dialog(browse_entry)  
    )
    browse_button.place(x=190, y=230)

    # Botón eliminar tarea
    delete_button = CTkButton(
        master=window,
        text="Eliminar",
        width=100,
        height=30,
        command=click_delete_task
    )
    delete_button.place(x=100, y=280)

    # Llamar a update_project_dropdown inicialmente para cargar los proyectos del primer workspace
    update_project_dropdown(workspaces[0],workspaces_object)

# Función para obtener la lista de workspaces
def populate_workspace():
    decoded_content = get_workspaces()
    workspaces_list = [d["name"] for d in decoded_content]
    return workspaces_list, decoded_content

# Función para obtener los proyectos del workspace seleccionado
def get_projects_for_workspace(workspace_name,workspace_object):
    for w in workspace_object:
        if w["name"] == workspace_name:
            workspace_id = w["id"]
            break

    decoded_content = get_projects(workspace_id)  
    projects_list = [p["name"] for p in decoded_content]
    return projects_list, decoded_content
