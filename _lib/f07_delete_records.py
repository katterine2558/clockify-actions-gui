"""
MÓDULO DE ELIMINAR TAREAS
"""
import os
import tkinter.messagebox
import csv
from customtkinter import * 
from _lib.get_workspaces import get_workspaces
from _lib.delete_timeentries import delete_timeentries
import tkinter

def open_delete_records_window(menu_window, images_path):

    # Crear una nueva ventana
    window = CTkToplevel(menu_window)
    # Geometría
    width = 300
    height = 220
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    x = (screen_width - width) // 2
    y = (screen_height - height) // 2
    window.geometry(f'{width}x{height}+{x}+{y}')
    window.title("Eliminar horas")
    window.after(201, lambda: window.iconbitmap(os.path.join(images_path, "Eliminar_horas.ico")))
    window.resizable(False, False)
    window.grab_set()
    window.transient(menu_window)
    window.focus_force()

    datos = {}
    workspace_id = ""

    #Función para adjuntar archivo con las tareas
    def open_file_dialog(browse_entry):

        nonlocal datos

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
            
            #Verifica si el archivo está vacio
            if os.stat(file_path).st_size == 0:
                browse_entry.configure(state=NORMAL)  # Habilita el campo para insertar el texto
                browse_entry.delete(0, "end")  # Limpia el contenido actual del campo
                browse_entry.configure(state=DISABLED)
                tkinter.messagebox.showerror("Error", "El archivo está vacío o no está en el formato correcto.")
            else:


                # Leer el contenido del archivo .txt
                with open(file_path, encoding='utf-8') as archivo:
                    lector = csv.DictReader(archivo, delimiter='\t')

                    # Verificar si el archivo tiene encabezados y datos
                    if lector.fieldnames is None:
                        tkinter.messagebox.showerror("Error", "El archivo no contiene encabezados o está mal formateado.")
                    else:
                        # Inicializar listas vacías para cada encabezado
                        for encabezado in lector.fieldnames:
                            datos[encabezado] = []
                        # Rellenar el diccionario con los datos
                        for fila in lector:
                            for encabezado, valor in fila.items():
                                datos[encabezado].append(valor)

    def click_delete_records():

        nonlocal workspace_id

        if datos == {}:
            tkinter.messagebox.showerror("Error","Adjuntar un archivo válido.")
            return
        else:
            if "Proyecto" not in list(datos.keys()) or "Descripción" not in list(datos.keys()) or "Tarea" not in list(datos.keys()) or "Correo electrónico" not in list(datos.keys()) or "Fecha de inicio" not in list(datos.keys()) or "Hora de inicio" not in list(datos.keys()) or "Fecha de finalización" not in list(datos.keys()) or "Hora de finalización" not in list(datos.keys()):
                
                datos == {}
                tkinter.messagebox.showerror("Error","Registros inválidos. Hace falta información.")
    
                return
            else:
                for w in workspaces_object:
                    if w["name"] == selected_workspace.get():
                        workspace_id = w["id"]
                        break

                delete_timeentries(datos,workspace_id)

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
        values=workspaces
    )
    workspace_menu.place(x=35, y=50)
    workspace_menu.set(workspaces[0]) 

    #Label para examinar el archivo
    label_browse = CTkLabel(master=window, text="Buscar archivo:", fg_color="transparent", font=('Gothic A1', 15))
    label_browse.place(x=35, y=85)

    # Campo de entrada para el nombre del archivo
    browse_entry = CTkEntry(master=window, width=140, font=('Gothic A1', 12), placeholder_text="Archivo",state=DISABLED)
    browse_entry.place(x=35, y=115)

    # Botón para buscar archivo
    browse_button = CTkButton(
        master=window,
        text="Examinar",
        width=80,
        height=22,
        command= lambda: open_file_dialog(browse_entry)  
    )
    browse_button.place(x=190, y=115)

    # Botón eliminar tarea
    delete_button = CTkButton(
        master=window,
        text="Eliminar",
        width=100,
        height=30,
        command=click_delete_records
    )
    delete_button.place(x=100, y=165)

# Función para obtener la lista de workspaces
def populate_workspace():
    decoded_content = get_workspaces()
    workspaces_list = [d["name"] for d in decoded_content]
    return workspaces_list, decoded_content