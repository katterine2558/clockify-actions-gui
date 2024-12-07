"""
VENTANA PRINCIPAL
"""
#############################
#     IMPORTAR Y DECLARAR
#############################
import sys
import os
sys.path.append(os.getcwd())
from customtkinter import *
from PIL import Image, ImageTk
import tkinter
import pickle
import shutil
import subprocess
from _lib.f01_get_files_path import get_file_paths
from _lib.f02_verify_user import verify_user
from _lib.f03_create_project import open_create_project_window
from _lib.f04_create_task import open_create_task_window
from _lib.f05_delete_task import open_delete_task_window
from _lib.f06_upload_records import open_upload_records_window
from _lib.f07_delete_records import open_delete_records_window
from _lib.f08_transfer_hours import open_transfer_window

#Paths
images_path = get_file_paths("_images")

#############################
#     VENTANA DEL MENÚ
#############################
def open_menu_window():

    #Función para crear proyectos
    def crear_proyecto():
        open_create_project_window(menu_window,images_path)

    #Función para crear tareas
    def crear_tarea():
        open_create_task_window(menu_window,images_path)

    #Función para eliminar tareas
    def eliminar_tarea():
        open_delete_task_window(menu_window,images_path)

    #Función para subir registros
    def cargar_registros():
        open_upload_records_window(menu_window,images_path)

    #Función para eliminar registros
    def eliminar_registros():
        open_delete_records_window(menu_window,images_path)

    #Función para transferir horas
    def transferir_horas():
        open_transfer_window(menu_window,images_path)

    #Inicializa la ventana
    menu_window= CTk()
    #Geometría
    width = 450
    height = 440
    screen_width = menu_window.winfo_screenwidth()
    screen_height = menu_window.winfo_screenheight()
    x = (screen_width - width) // 2
    y = (screen_height - height) // 2
    menu_window.geometry(f'{width}x{height}+{x}+{y}')
    #Nombre de la ventana
    menu_window.title("Menú - Clockify")
    #Resizable
    menu_window.resizable(False,False)
    #Tema de la ventana
    set_appearance_mode("Dark")
    set_default_color_theme("dark-blue")
    #Ícono ventana
    menu_window.after(201, lambda :menu_window.iconbitmap(os.path.join(images_path, "logo.ico")))
    #Label de crear proyeco
    label_proyecto = CTkLabel(master=menu_window,text="Proyectos",fg_color="transparent",font=('Gothic A1',20))
    label_proyecto.place(x= 30,y=20)
    #Crear proyecto
    crear_proyecto_image = Image.open(os.path.join(images_path, "Crear_Proyecto.png"))
    crear_proyecto_image = crear_proyecto_image.resize((30, 30), Image.LANCZOS)
    crear_proyecto_image_tk = ImageTk.PhotoImage(crear_proyecto_image)
    btn_crear_proyecto = CTkButton(master=menu_window, 
                    text="Crear proyecto", 
                    image = crear_proyecto_image_tk,
                    width=180, 
                    height=40, 
                    compound="left",
                    font=('Gothic A1',15),
                    fg_color="#3A3A3A",
                    hover_color="#4C4C4C",
                    text_color="#E0E0E0",
                    corner_radius=5,
                    border_width=2,
                    border_color="#606060",
                    command=crear_proyecto)
    btn_crear_proyecto.place(x=30,y=60)
    #Label de tareas
    label_tareas = CTkLabel(master=menu_window,text="Tareas",fg_color="transparent",font=('Gothic A1',20))
    label_tareas.place(x= 30,y=120)
    # Crear tareas
    crear_tareas_image = Image.open(os.path.join(images_path, "Crear_Tarea.png"))
    crear_tareas_image = crear_tareas_image.resize((30, 30), Image.LANCZOS)
    crear_tareas_image_tk = ImageTk.PhotoImage(crear_tareas_image)
    btn_crear_tareas = CTkButton(master=menu_window, 
                    text="Crear tareas", 
                    image = crear_tareas_image_tk,
                    width=180, 
                    height=40, 
                    compound="left",
                    font=('Gothic A1',15),
                    fg_color="#3A3A3A",
                    hover_color="#4C4C4C",
                    text_color="#E0E0E0",
                    corner_radius=5,
                    border_width=2,
                    border_color="#606060",
                    command=crear_tarea)
    btn_crear_tareas.place(x=30,y=160)

    # Eliminar tareas
    eliminar_tareas_image = Image.open(os.path.join(images_path, "Eliminar_Tarea.png"))
    eliminar_tareas_image = eliminar_tareas_image.resize((30, 30), Image.LANCZOS)
    eliminar_tareas_image_tk = ImageTk.PhotoImage(eliminar_tareas_image)
    btn_eliminar_tareas = CTkButton(master=menu_window, 
                    text="Eliminar tareas", 
                    image = eliminar_tareas_image_tk,
                    width=180, 
                    height=40, 
                    compound="left",
                    font=('Gothic A1',15),
                    fg_color="#3A3A3A",
                    hover_color="#4C4C4C",
                    text_color="#E0E0E0",
                    corner_radius=5,
                    border_width=2,
                    border_color="#606060",
                    command=eliminar_tarea)
    btn_eliminar_tareas.place(x=230,y=160)

    #Label de registros
    label_registros = CTkLabel(master=menu_window,text="Registros",fg_color="transparent",font=('Gothic A1',20))
    label_registros.place(x= 30,y=220)

    # Cargar horas
    cargar_horas_image = Image.open(os.path.join(images_path, "Subir_horas.png"))
    cargar_horas_image = cargar_horas_image.resize((30, 30), Image.LANCZOS)
    cargar_horas_image_tk = ImageTk.PhotoImage(cargar_horas_image)
    btn_subir_horas = CTkButton(master=menu_window, 
                    text="Cargar registros", 
                    image = cargar_horas_image_tk,
                    width=180, 
                    height=40, 
                    compound="left",
                    font=('Gothic A1',15),
                    fg_color="#3A3A3A",
                    hover_color="#4C4C4C",
                    text_color="#E0E0E0",
                    corner_radius=5,
                    border_width=2,
                    border_color="#606060",
                    command=cargar_registros)
    btn_subir_horas.place(x=30,y=260)

    # eliminar horas
    eliminar_horas_image = Image.open(os.path.join(images_path, "Eliminar_horas.png"))
    eliminar_horas_image = eliminar_horas_image.resize((30, 30), Image.LANCZOS)
    eliminar_horas_image_tk = ImageTk.PhotoImage(eliminar_horas_image)
    btn_eliminar_horas = CTkButton(master=menu_window, 
                    text="Eliminar registros", 
                    image = eliminar_horas_image_tk,
                    width=180, 
                    height=40, 
                    compound="left",
                    font=('Gothic A1',15),
                    fg_color="#3A3A3A",
                    hover_color="#4C4C4C",
                    text_color="#E0E0E0",
                    corner_radius=5,
                    border_width=2,
                    border_color="#606060",
                    command=eliminar_registros)
    btn_eliminar_horas.place(x=230,y=260)

    #Label de transferencia
    label_transferencia = CTkLabel(master=menu_window,text="Transferencia de horas",fg_color="transparent",font=('Gothic A1',20))
    label_transferencia.place(x= 30,y=320)

    #botón de transferencia
    transferir_image = Image.open(os.path.join(images_path, "Transferencia_Horas.png"))
    transferir_image = transferir_image.resize((30, 30), Image.LANCZOS)
    transferir_image_tk = ImageTk.PhotoImage(transferir_image)
    btn_transferir = CTkButton(master=menu_window, 
                    text="Transferir horas", 
                    image = transferir_image_tk,
                    width=180, 
                    height=40, 
                    compound="left",
                    font=('Gothic A1',15),
                    fg_color="#3A3A3A",
                    hover_color="#4C4C4C",
                    text_color="#E0E0E0",
                    corner_radius=5,
                    border_width=2,
                    border_color="#606060",
                    command=transferir_horas)
    btn_transferir.place(x=30, y =360 )

    #Ejecuta la ventana
    menu_window.mainloop()

# Función click en login
def login_click():
    successful_login = verify_user(main_window, user_entry.get(), password_entry.get())
    if successful_login == 1:

        main_window.destroy()  # Destruye la ventana de login
        open_menu_window()  # Abre la nueva ventana
    
#############################
#     VENTANA DE LOGIN
#############################
#Inicializa la ventana
main_window= CTk()
#Geometría
width = 300
height = 200
screen_width = main_window.winfo_screenwidth()
screen_height = main_window.winfo_screenheight()
x = (screen_width - width) // 2
y = (screen_height - height) // 2
main_window.geometry(f'{width}x{height}+{x}+{y}')
#Nombre de la ventana
main_window.title("Login - Clockify")
#Resizable
main_window.resizable(False,False)
#Tema de la ventana
set_appearance_mode("Dark")
set_default_color_theme("dark-blue")
#Ícono ventana
main_window.after(201, lambda :main_window.iconbitmap(os.path.join(images_path, "logo.ico")))
#Label de iniciar sesión
login_label = CTkLabel(master=main_window,text="Iniciar sesión",fg_color="transparent",font=('Gothic A1',20))
login_label.place(x= 90,y=20)
#Input usuario
user_entry=CTkEntry(master=main_window, width=120, placeholder_text='Username')
user_entry.place(x= (300 - 120) / 2 ,y=65)
#Input password
password_entry=CTkEntry(master=main_window, width=120, placeholder_text='Password', show="*")
password_entry.place(x= (300 - 120) / 2 ,y=105)
#Botón de iniciar sesión
conectar= CTkButton(master=main_window, text="Login", width=70, height=30, compound="left",font=('Gothic A1',15), command=login_click) 
conectar.place(x= (300 - 70) / 2 ,y=155)
#Ejecuta la ventana
main_window.mainloop()