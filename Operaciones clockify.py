#importa libreria
import sys
import os
sys.path.append(os.getcwd())
from customtkinter import *
from PIL import Image, ImageTk
import tkinter
import pickle
import shutil
from _Library.updateUsersAPIKey import updateUserAPIKeys
from _Library.getWorkspaces import getWorkspaces
from _Library.updateConfig import updateConfigIni
from _Library.getProjects import getProjects
from _Library.getGroups import getGroups
from datetime import datetime, date
import copy
import re
from _Library.f_transferencia_horas import f_transferencia_horas
from _Library.getWorkspaceUsers import getWorkspaceUsers
from _Library.getProjectTask import getProjectTask
from _Library.f_subir_registro import f_subir_registro
from tkinter import filedialog
import pandas as pd
from _Library.f_cargar_horas import f_cargar_horas
from _Library.f_consultar_registros import f_consultar_registros

library_path  = os.path.join(os.path.dirname(os.path.realpath(__file__)), "_Library")

#%% ---------------------------------------------------
#%%                    HOME WINDOW
#%% ---------------------------------------------------

#%% ---------------- HOME WINDOW: MOSTRAR VENTANA HOME ---------------
def show_home_window():

    #Declaración de variables globales
    global home_window
    global TransferenciaHoras_button, Frame_Transferencia_Horas, Workspace1_variable, Workspace2_variable, workspace_origen, workspace_destino, proyecto, fecha_inicio, fecha_fin, OptionMenu1_Transferencia_Horas, OptionMenu2_Transferencia_Horas, OptionMenu3_Transferencia_Horas, Entry1_Transferencia_Horas, Entry2_Transferencia_Horas, TransferirBoton_Transferencia_Horas, Project3_variable, TransferirBoton_Transferencia_Horas, contador_verificaciones

    global CargarHoras_button, Frame_Cargar_Horas, workspace_origen_menu2, Workspace1_variable_menu2, OptionMenu1_Cargar_Horas, workspace_destino_menu2, Workspace2_variable_menu2, OptionMenu2_Cargar_Horas,proyecto_menu2 ,Project3_variable_menu2,OptionMenu3_Cargar_Horas, TextBox1_Cargar_Horas, CargarArchivo_Cargar_Horas, archivo_horas, CargarHoras_Cargar_Horas, archivo

    global AgregarRegistro_button, Frame_Añadir_Registro_Individual, workspace_menu3,Workspace_menu3_variable, OptionMenu1_Añadir_Registro_Individual, proyecto_menu3, Proyectos_menu3_variable, OptionMenu2_Añadir_Registro_Individual, usuario_menu3, Usuarios_menu3_variable, OptionMenu3_Añadir_Registro_Individual, email_menu3, tarea_menu3, Tareas_menu3_variable, OptionMenu4_Añadir_Registro_Individual, fecha_menu3, Entry1_Añadir_Registro_Individual, hora_menu3, Hora_menu3_variable, OptionMenu5_Añadir_Registro_Individual, descripcion_menu3, Entry2_Añadir_Registro_Individual, duracion_menu3, Entry3_Añadir_Registro_Individual, SubirRegistro_Añadir_Registro_Individual

    global workspaces_name, projects_name, users_data

    #Carga workspaces, proyectos y usuarios
    with open(os.path.join(library_path, "workspaces.pkl"), 'rb') as file:
        workspaces = pickle.load(file)
    file.close()
    with open(os.path.join(library_path, "projects.pkl"), 'rb') as file:
        projects = pickle.load(file)
    file.close()
    with open(os.path.join(library_path, "users_data.pkl"), 'rb') as file:
        users_data = pickle.load(file)
    file.close()

    #Inicializa vatiable
    lista_workspace_destino,lista_workspace_destino_menu2 = [],[]

    #Lista horas
    lista_horas =["00:00","00:15","00:30","00:45","01:00","01:15","01:30","01:45","02:00","02:15","02:30","02:45","03:00","03:15","03:30","03:45","04:00","04:15","04:30","04:45","05:00","05:15","05:30","05:45","06:00","06:15","06:30","06:45","07:00","07:15","07:30","07:45","08:00","08:15","08:30","08:45","09:00","09:15","09:30","09:45","10:00","10:15","10:30","10:45","11:00","11:15","11:30","11:45","12:00","12:15","12:30","12:45","13:00","13:15","13:30","13:45","14:00","14:15","14:30","14:45","15:00","15:15","15:30","15:45","16:00","16:15","16:30","16:45","17:00","17:15","17:30","17:45","18:00","18:15","18:30","18:45","19:00","19:15","19:30","19:45","20:00","20:15","20:30","20:45","21:00","21:15","21:30","21:45","22:00","22:15","22:30","22:45","23:00","23:15","23:30","23:45"]

    #Inicializa la ventana
    home_window = CTkToplevel()

    #Geometría
    width = 700
    height = 500
    screen_width = home_window.winfo_screenwidth()
    screen_height = home_window.winfo_screenheight()
    x = (screen_width - width) // 2
    y = (screen_height - height) // 2
    home_window.geometry(f"{width}x{height}+{x}+{y}")
    #Nombre de la ventana
    home_window.title("Operaciones: Clockify")
    #Resizable
    home_window.resizable(False,False)
    #Grid
    home_window.grid_rowconfigure(0, weight=1)
    home_window.grid_columnconfigure(1, weight=1)

    #Load icon and images
    home_window.after(201, lambda :home_window.iconbitmap(os.path.join(images_path, "logo.ico")))
    logo_pedelta2 = CTkImage(Image.open(os.path.join(images_path, "Pedelta.png")), size=(150, 60))
    logo_reporteDetallado = CTkImage(Image.open(os.path.join(images_path, "Reporte_Detallado.png")), size=(30, 30))
    logo_reporteDiligenciamiento = CTkImage(Image.open(os.path.join(images_path, "Reporte_Diligenciamiento.png")), size=(30, 30))
    logo_transferenciaHoras = CTkImage(Image.open(os.path.join(images_path, "Transferencia_Horas.png")), size=(30, 30))
    logo_CargarHoras = CTkImage(Image.open(os.path.join(images_path, "Agregar_RegistrosMasivos.png")), size=(30, 30))
    logo_AgregarRegistro = CTkImage(Image.open(os.path.join(images_path, "Anadir_Registro.png")), size=(30, 30))

    #%% ---------------- FRAME DE NAVEGACIÓN ---------------
    navigation_frame = CTkFrame(master=home_window, corner_radius=0)
    navigation_frame.grid(row=0, column=0, sticky="nsew")
    navigation_frame.grid_rowconfigure(10, weight=1)
    
    navigation_frame_label = CTkLabel(master=navigation_frame, text="     ", image=logo_pedelta2, compound="right",font=('Gothic A1',13))
    navigation_frame_label.grid(row=0, column=0, padx=10, pady=1)

    blank_space1 = CTkLabel(master=navigation_frame,text=f"¡Hola, {name_user}!",font=('Gothic A1',13))
    blank_space1.grid(row=1, column=0, padx=10, pady=1)

    blank_space2 = CTkLabel(master=navigation_frame,text="")
    blank_space2.grid(row=2, column=0, padx=10, pady=1)

    TransferenciaHoras_button = CTkButton(master= navigation_frame, corner_radius=0, height=40, border_spacing=10, text="Transferencia Horas",
                                                   fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
                                                   image=logo_transferenciaHoras, anchor="w",font=('Gothic A1',13),command=seleccionar_frame_transferencia_horas)
    TransferenciaHoras_button.grid(row=5, column=0, sticky="ew")

    CargarHoras_button = CTkButton(master= navigation_frame, corner_radius=0, height=40, border_spacing=10, text="Cargar Horas",
                                                   fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
                                                   image=logo_CargarHoras, anchor="w",font=('Gothic A1',13),command=seleccionar_frame_cargar_horas)
    CargarHoras_button.grid(row=6, column=0, sticky="ew")

    AgregarRegistro_button = CTkButton(master= navigation_frame, corner_radius=0, height=40, border_spacing=10, text="Subir Registro",
                                                   fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
                                                   image=logo_AgregarRegistro, anchor="w",font=('Gothic A1',13),command=seleccionar_frame_agregar_registros)
    AgregarRegistro_button.grid(row=7, column=0, sticky="ew")

    ############################################################################
    # CONFIGURACIÓN DE TRANSFERENCIA DE HORAS - TH
    ############################################################################
    #Creación de frame de transferencia de horas
    Frame_Transferencia_Horas = CTkFrame(master=home_window,corner_radius=0,fg_color="transparent")
    Frame_Transferencia_Horas.grid_columnconfigure(0, weight=1)

    #Creación del header de transferencia de horas
    Header_Transferencia_Horas = CTkLabel(master=Frame_Transferencia_Horas,text="TRANSFERIR HORAS ENTRE WORKSPACES",font=('Gothic A1',20,"bold") )
    Header_Transferencia_Horas.place(x=40,y=50)

    #Label de selección de workspace origen
    Label1_Transferencia_Horas = CTkLabel(master=Frame_Transferencia_Horas,text="Seleccionar workspace de origen: ",font=('Gothic A1',13,) )
    Label1_Transferencia_Horas.place(x=40,y=140)

    #Label de selección de workspace destino
    Label2_Transferencia_Horas = CTkLabel(master=Frame_Transferencia_Horas,text="Seleccionar workspace de destino: ",font=('Gothic A1',13,) )
    Label2_Transferencia_Horas.place(x=40,y=200)

    #Label de selección de proyecto
    Label3_Transferencia_Horas = CTkLabel(master=Frame_Transferencia_Horas,text="Seleccionar proyecto: ",font=('Gothic A1',13,) )
    Label3_Transferencia_Horas.place(x=40,y=260)

    #Label de selección de fecha inicio
    Label4_Transferencia_Horas = CTkLabel(master=Frame_Transferencia_Horas,text="Fecha inicio: ",font=('Gothic A1',13,) )
    Label4_Transferencia_Horas.place(x=40,y=320)

    #Label de selección de fecha fin
    Label5_Transferencia_Horas = CTkLabel(master=Frame_Transferencia_Horas,text="Fecha fin: ",font=('Gothic A1',13,) )
    Label5_Transferencia_Horas.place(x=40,y=380)

    #Extra el nombre de proyectos y workspaces
    workspaces_name = extraer_workspaces(workspaces)
    projects_name = extraer_proyectos(projects)

    #Option menu para workspace de origen
    workspace_origen = ""
    Workspace1_variable = StringVar()
    Workspace1_variable.set("")
    OptionMenu1_Transferencia_Horas = CTkOptionMenu(master=Frame_Transferencia_Horas,variable=Workspace1_variable, values= workspaces_name,hover=True,corner_radius=3,fg_color="gray25",button_color="gray50",font=('Gothic A1',12),dropdown_font=('Gothic A1',12),command=mostrar_workspace_destino,dynamic_resizing=False,width=180,height=22)
    OptionMenu1_Transferencia_Horas.place(x=260,y=145)
    Workspace1_variable.trace_add("write",obtener_workspace_origen)

    #Option menu para workspace de destino
    workspace_destino = ""
    Workspace2_variable = StringVar()
    Workspace2_variable.set("")
    OptionMenu2_Transferencia_Horas = CTkOptionMenu(master=Frame_Transferencia_Horas,variable=Workspace2_variable, values="",hover=True,corner_radius=3,fg_color="gray25",button_color="gray50",font=('Gothic A1',12),dropdown_font=('Gothic A1',12),command= mostrar_proyecto ,dynamic_resizing=False,width=180,height=22)
    OptionMenu2_Transferencia_Horas.place(x=260,y=205)
    Workspace2_variable.trace_add("write",obtener_workspace_destino)

    #Option menu para proyectos que sean comun entre workspace de origen y workspace de destino
    proyecto = ""
    Project3_variable = StringVar()
    Project3_variable.set("")
    OptionMenu3_Transferencia_Horas = CTkOptionMenu(master=Frame_Transferencia_Horas,variable=Project3_variable, values="",hover=True,corner_radius=3,fg_color="gray25",button_color="gray50",font=('Gothic A1',12),dropdown_font=('Gothic A1',12),dynamic_resizing=False,width=180,height=22)
    OptionMenu3_Transferencia_Horas.place(x=190,y=265)
    Project3_variable.trace_add("write",obtener_proyecto)

    #Entry para fecha de inicio
    fecha_inicio = ""
    Entry1_Transferencia_Horas=CTkEntry(master=Frame_Transferencia_Horas, width=100, placeholder_text='aaaa-mm-dd')
    Entry1_Transferencia_Horas.place(x=135, y=320)
    Entry1_Transferencia_Horas.bind("<Leave>", lambda event: verificar_fecha_inicio())

    #Entry para fecha fin
    fecha_fin = ""
    Entry2_Transferencia_Horas=CTkEntry(master=Frame_Transferencia_Horas, width=100, placeholder_text='aaaa-mm-dd')
    Entry2_Transferencia_Horas.place(x=135, y=380)
    Entry2_Transferencia_Horas.bind("<Leave>", lambda event: verificar_fecha_fin())

    #Boton de transferencia de horas
    TransferirBoton_Transferencia_Horas = CTkButton(master= Frame_Transferencia_Horas, text="Transferir", width=80, height=30, compound="left",font=('Gothic A1',15),command=transferir_horas,state=tkinter.DISABLED)
    TransferirBoton_Transferencia_Horas.place(x=200,y=440)

    #Habilitar botón de transferir
    OptionMenu1_Transferencia_Horas.bind("<Leave>", lambda event: habilitar_boton_transferir_horas())
    OptionMenu2_Transferencia_Horas.bind("<Leave>", lambda event: habilitar_boton_transferir_horas())
    OptionMenu3_Transferencia_Horas.bind("<Leave>", lambda event: habilitar_boton_transferir_horas())
    Entry1_Transferencia_Horas.bind("<Leave>", lambda event: habilitar_boton_transferir_horas())
    Entry2_Transferencia_Horas.bind("<Leave>", lambda event: habilitar_boton_transferir_horas())

    
    ############################################################################
    # CONFIGURACIÓN DE CARGAR HORAS - CH
    ############################################################################
    #Creación de frame de cargar horas
    Frame_Cargar_Horas = CTkFrame(master=home_window,corner_radius=0,fg_color="transparent")
    Frame_Cargar_Horas.grid_columnconfigure(0, weight=1)

    #Creación del header de cargar horas
    Header_Cargar_Horas = CTkLabel(master=Frame_Cargar_Horas,text="CARGAR HORAS",font=('Gothic A1',20,"bold") )
    Header_Cargar_Horas.place(x=170,y=60)

    #Label de selección de workspace origen
    Label1_Cargar_Horas = CTkLabel(master=Frame_Cargar_Horas,text="Seleccionar workspace de origen: ",font=('Gothic A1',13,) )
    Label1_Cargar_Horas.place(x=40,y=140)

    #Label de selección de workspace destino
    Label2_Cargar_Horas = CTkLabel(master=Frame_Cargar_Horas,text="Seleccionar workspace de destino: ",font=('Gothic A1',13,) )
    Label2_Cargar_Horas.place(x=40,y=200)
    
    #Label de selección de proyecto
    Label3_Cargar_Horas = CTkLabel(master=Frame_Cargar_Horas,text="Seleccionar proyecto: ",font=('Gothic A1',13,) )
    Label3_Cargar_Horas.place(x=40,y=260)

    #Label nombre archivo seleccionado
    Label4_Cargar_Horas = CTkLabel(master=Frame_Cargar_Horas,text="Archivo: ",font=('Gothic A1',13,) )
    Label4_Cargar_Horas.place(x=40,y=320)

    #Option menu para workspace de origen
    workspace_origen_menu2 = ""
    Workspace1_variable_menu2 = StringVar()
    Workspace1_variable_menu2.set("")
    OptionMenu1_Cargar_Horas = CTkOptionMenu(master=Frame_Cargar_Horas,variable=Workspace1_variable_menu2, values= workspaces_name,hover=True,corner_radius=3,fg_color="gray25",button_color="gray50",font=('Gothic A1',12),dropdown_font=('Gothic A1',12),command=mostrar_workspace_destino_menu2,dynamic_resizing=False,width=180,height=22)
    OptionMenu1_Cargar_Horas.place(x=260,y=145)
    Workspace1_variable_menu2.trace_add("write",obtener_workspace_origen_menu2)

     #Option menu para workspace de destino
    workspace_destino_menu2 = ""
    Workspace2_variable_menu2 = StringVar()
    Workspace2_variable_menu2.set("")
    OptionMenu2_Cargar_Horas = CTkOptionMenu(master=Frame_Cargar_Horas,variable=Workspace2_variable_menu2, values="",hover=True,corner_radius=3,fg_color="gray25",button_color="gray50",font=('Gothic A1',12),dropdown_font=('Gothic A1',12),command= mostrar_proyecto_menu2 ,dynamic_resizing=False,width=180,height=22)
    OptionMenu2_Cargar_Horas.place(x=260,y=205)
    Workspace2_variable_menu2.trace_add("write",obtener_workspace_destino_menu2)

    #Option menu para proyectos que sean comun entre workspace de origen y workspace de destino
    proyecto_menu2 = ""
    Project3_variable_menu2 = StringVar()
    Project3_variable_menu2.set("")
    OptionMenu3_Cargar_Horas = CTkOptionMenu(master=Frame_Cargar_Horas,variable=Project3_variable_menu2, values="",hover=True,corner_radius=3,fg_color="gray25",button_color="gray50",font=('Gothic A1',12),dropdown_font=('Gothic A1',12),dynamic_resizing=False,width=180,height=22)
    OptionMenu3_Cargar_Horas.place(x=190,y=265)
    Project3_variable_menu2.trace_add("write",obtener_proyecto_menu2)

    #Text box para nombre de archivo
    TextBox1_Cargar_Horas = CTkTextbox(master=Frame_Cargar_Horas,font=('Gothic A1',12), text_color=("gray10", "gray90"),width=180,height=10,state=DISABLED,activate_scrollbars=False)
    TextBox1_Cargar_Horas.place(x=105,y=320)

    #Boton examinar
    CargarArchivo_Cargar_Horas = CTkButton(master= Frame_Cargar_Horas, text="Examinar", width=80, height=30, compound="left",font=('Gothic A1',12),command=cargar_archivo)
    CargarArchivo_Cargar_Horas.place(x=320,y=320)

    #Boton cargar horas
    CargarHoras_Cargar_Horas = CTkButton(master= Frame_Cargar_Horas, text="Cargar Horas", width=80, height=30, compound="left",font=('Gothic A1',12),state=tkinter.DISABLED, command=cargar_horas)
    CargarHoras_Cargar_Horas.place(x=200,y=400)
    
    #Habilitar botón de cargar horas
    OptionMenu1_Cargar_Horas.bind("<Leave>", lambda event: habilitar_boton_cargar_horas())

    OptionMenu2_Cargar_Horas.bind("<Leave>", lambda event: habilitar_boton_cargar_horas())

    OptionMenu3_Cargar_Horas.bind("<Leave>", lambda event: habilitar_boton_cargar_horas())
   

    ############################################################################
    # CONFIGURACIÓN DE AÑADIR REGISTRO INDIVIDUAL - ARI
    ############################################################################
    #Creación de frame de añadir registro individual
    Frame_Añadir_Registro_Individual = CTkFrame(master=home_window,corner_radius=0,fg_color="transparent")
    Frame_Añadir_Registro_Individual.grid_columnconfigure(0, weight=1)

    #Creación del header de transferencia de horas
    Header_Añadir_Registro_Individual = CTkLabel(master=Frame_Añadir_Registro_Individual,text="SUBIR REGISTRO A USUARIO",font=('Gothic A1',20,"bold") )
    Header_Añadir_Registro_Individual.place(x=110,y=50)

    #Label de selección de workspace
    Label1_Añadir_Registro_Individual = CTkLabel(master=Frame_Añadir_Registro_Individual,text="Seleccionar workspace: ",font=('Gothic A1',13,) )
    Label1_Añadir_Registro_Individual.place(x=40,y=120)

    #Label de selección de proyecto
    Label2_Añadir_Registro_Individual = CTkLabel(master=Frame_Añadir_Registro_Individual,text="Seleccionar proyecto: ",font=('Gothic A1',13,) )
    Label2_Añadir_Registro_Individual.place(x=290,y=120)

    #Label de selección de usuario
    Label3_Añadir_Registro_Individual = CTkLabel(master=Frame_Añadir_Registro_Individual,text="Seleccionar usuario: ",font=('Gothic A1',13,) )
    Label3_Añadir_Registro_Individual.place(x=40,y=190)

    #Label de selección de tarea
    Label4_Añadir_Registro_Individual = CTkLabel(master=Frame_Añadir_Registro_Individual,text="Seleccionar tarea: ",font=('Gothic A1',13,) )
    Label4_Añadir_Registro_Individual.place(x=290,y=190)

    #Label de ingresar fecha y hora
    Label5_Añadir_Registro_Individual = CTkLabel(master=Frame_Añadir_Registro_Individual,text="Ingresar fecha: ",font=('Gothic A1',13,) )
    Label5_Añadir_Registro_Individual.place(x=40,y=260)

    #Label de ingresar hora
    Label6_Añadir_Registro_Individual = CTkLabel(master=Frame_Añadir_Registro_Individual,text="Seleccionar hora: ",font=('Gothic A1',13,) )
    Label6_Añadir_Registro_Individual.place(x=290,y=260)

    #Label de ingresar duración
    Label7_Añadir_Registro_Individual = CTkLabel(master=Frame_Añadir_Registro_Individual,text="Ingresar duración (decimal): ",font=('Gothic A1',13,) )
    Label7_Añadir_Registro_Individual.place(x=40,y=335)

    #Label de ingresar descripción
    Label8_Añadir_Registro_Individual = CTkLabel(master=Frame_Añadir_Registro_Individual,text="Ingresar descripción: ",font=('Gothic A1',13,) )
    Label8_Añadir_Registro_Individual.place(x=290,y=335)

    #Option menu para workspace
    workspace_menu3 = ""
    Workspace_menu3_variable = StringVar()
    Workspace_menu3_variable.set("")
    OptionMenu1_Añadir_Registro_Individual = CTkOptionMenu(master=Frame_Añadir_Registro_Individual,variable=Workspace_menu3_variable, values= workspaces_name,hover=True,corner_radius=3,fg_color="gray25",button_color="gray50",font=('Gothic A1',12),dropdown_font=('Gothic A1',12),dynamic_resizing=False,width=170,height=22,command=proyectos_menu3)
    OptionMenu1_Añadir_Registro_Individual.place(x=40,y=155)
    Workspace_menu3_variable.trace_add("write",obtener_workspace_menu3)

    #Option menu para proyectos
    proyecto_menu3 = ""
    Proyectos_menu3_variable = StringVar()
    Proyectos_menu3_variable.set("")
    OptionMenu2_Añadir_Registro_Individual = CTkOptionMenu(master=Frame_Añadir_Registro_Individual,variable=Proyectos_menu3_variable, values= "",hover=True,corner_radius=3,fg_color="gray25",button_color="gray50",font=('Gothic A1',12),dropdown_font=('Gothic A1',12),dynamic_resizing=False,width=170,height=22,command=usuarios_menu3)
    OptionMenu2_Añadir_Registro_Individual.place(x=290,y=155)
    Proyectos_menu3_variable.trace_add("write",obtener_proyecto_menu3)

    #Option menu para usuarios 
    usuario_menu3 = ""
    email_menu3 = ""
    Usuarios_menu3_variable = StringVar()
    Usuarios_menu3_variable.set("")
    OptionMenu3_Añadir_Registro_Individual = CTkOptionMenu(master=Frame_Añadir_Registro_Individual,variable=Usuarios_menu3_variable, values= "",hover=True,corner_radius=3,fg_color="gray25",button_color="gray50",font=('Gothic A1',12),dropdown_font=('Gothic A1',12),dynamic_resizing=False,width=170,height=22,command=mostrar_tareas_proyecto)
    OptionMenu3_Añadir_Registro_Individual.place(x=40,y=225)
    Usuarios_menu3_variable.trace_add("write",obtener_usuario_menu3)

    #Option menu para tareas 
    tarea_menu3 = ""
    Tareas_menu3_variable = StringVar()
    Tareas_menu3_variable.set("")
    OptionMenu4_Añadir_Registro_Individual = CTkOptionMenu(master=Frame_Añadir_Registro_Individual,variable=Tareas_menu3_variable, values= "",hover=True,corner_radius=3,fg_color="gray25",button_color="gray50",font=('Gothic A1',12),dropdown_font=('Gothic A1',12),dynamic_resizing=False,width=170,height=22)
    OptionMenu4_Añadir_Registro_Individual.place(x=290,y=225)
    Tareas_menu3_variable.trace_add("write",obtener_tarea)

    #Entry de fecha
    fecha_menu3 = ""
    Entry1_Añadir_Registro_Individual=CTkEntry(master=Frame_Añadir_Registro_Individual, width=100, placeholder_text='aaaa-mm-dd')
    Entry1_Añadir_Registro_Individual.place(x=40, y=295)
    Entry1_Añadir_Registro_Individual.bind("<Leave>", lambda event: verificar_fecha_tarea())

    #Option menu para horas
    hora_menu3 = ""
    Hora_menu3_variable = StringVar()
    Hora_menu3_variable.set("00:00")
    OptionMenu5_Añadir_Registro_Individual = CTkOptionMenu(master=Frame_Añadir_Registro_Individual,variable=Hora_menu3_variable, values=lista_horas,hover=True,corner_radius=3,fg_color="gray25",button_color="gray50",font=('Gothic A1',12),dropdown_font=('Gothic A1',12),dynamic_resizing=False,width=90,height=22)
    OptionMenu5_Añadir_Registro_Individual.place(x=290,y=295)
    Hora_menu3_variable.trace_add("write",obtener_hora)

    #Entry de duración
    duracion_menu3 = ""
    Entry3_Añadir_Registro_Individual=CTkEntry(master=Frame_Añadir_Registro_Individual, width=150, placeholder_text='Duración')
    Entry3_Añadir_Registro_Individual.place(x=40, y=370)
    Entry3_Añadir_Registro_Individual.bind("<Leave>", lambda event: verificar_duracion_tarea())

    #Entry de descripción
    descripcion_menu3 = ""
    Entry2_Añadir_Registro_Individual=CTkEntry(master=Frame_Añadir_Registro_Individual, width=150, placeholder_text='Descripción')
    Entry2_Añadir_Registro_Individual.place(x=290, y=370)
    Entry2_Añadir_Registro_Individual.bind("<Leave>", lambda event: obtener_descripcion())

    #Boton de subir registro
    SubirRegistro_Añadir_Registro_Individual = CTkButton(master= Frame_Añadir_Registro_Individual, text="Subir Registro", width=80, height=30, compound="left",font=('Gothic A1',15),command=subir_registro,state=tkinter.DISABLED)
    SubirRegistro_Añadir_Registro_Individual.place(x=200,y=430)

    #Habilitar botón de subir registro
    OptionMenu1_Añadir_Registro_Individual.bind("<Leave>", lambda event: habilitar_boton_subir_registro())
    OptionMenu2_Añadir_Registro_Individual.bind("<Leave>", lambda event: habilitar_boton_subir_registro())
    OptionMenu3_Añadir_Registro_Individual.bind("<Leave>", lambda event: habilitar_boton_subir_registro())
    Entry1_Añadir_Registro_Individual.bind("<Leave>", lambda event: habilitar_boton_subir_registro())
    OptionMenu5_Añadir_Registro_Individual.bind("<Leave>", lambda event: habilitar_boton_subir_registro())
    Entry3_Añadir_Registro_Individual.bind("<Leave>", lambda event: habilitar_boton_subir_registro())

    #Selección por defecto
    seleccionar_frame("Transferencia Horas")

#%% -------------- GENERAL: GENERAR VENTANA DE ALERTA ------------------
def generar_ventana_alerta(mensaje_alerta:str,titulo_alerta:str,nombre_ico:str,x_place_text:int,y_place_text:int,x_place_button:int,y_place_button:int,command:list):

    #Creación de ventana
    alerta = CTkToplevel()
    #Nombre de la ventana
    alerta.title(titulo_alerta)
    #Resizable
    alerta.resizable(False,False)
    alerta.transient(home_window)
    alerta.grab_set()
    #icono
    alerta.after(201, lambda :alerta.iconbitmap(os.path.join(images_path,nombre_ico )))
    #Geometría
    width = 400
    height = 100
    screen_width = alerta.winfo_screenwidth()
    screen_height = alerta.winfo_screenheight()
    x = (screen_width - width) // 2
    y = (screen_height - height) // 2
    alerta.geometry(f"{width}x{height}+{x}+{y}")
    #Label de aviso
    Label1_window_alert1 = CTkLabel(master=alerta,text=mensaje_alerta,font=('Gothic A1',13))
    Label1_window_alert1.place(x=x_place_text,y=y_place_text)
    #Botón de ok
    OKBoton_window_alert1 = CTkButton(master= alerta, text="OK", width=40, height=20, compound="left",font=('Gothic A1',15), command=alerta.destroy)
    OKBoton_window_alert1.place(x=x_place_button,y=y_place_button)
    for line in command:
        try:
            eval(line)
        except SyntaxError:
            pass

#%% -------------- MAIN WINDOW: SELECCIÓN DE FRAME PARA NAVEGACIÓN ------------------
def seleccionar_frame(name):
        
        # set button color for selected button
        TransferenciaHoras_button.configure(fg_color=("gray75", "gray25") if name == "Transferencia Horas" else "transparent")
        CargarHoras_button.configure(fg_color=("gray75", "gray25") if name == "Cargar Horas" else "transparent")
        AgregarRegistro_button.configure(fg_color=("gray75", "gray25") if name == "Añadir Registro Individual" else "transparent")


        if name == "Transferencia Horas":
            Frame_Transferencia_Horas.grid(row=0, column=1, sticky="nsew")
        else:
            Frame_Transferencia_Horas.grid_forget()

        if name == "Cargar Horas":
            Frame_Cargar_Horas.grid(row=0, column=1, sticky="nsew")
        else:
            Frame_Cargar_Horas.grid_forget()

        if name == "Añadir Registro Individual":
            Frame_Añadir_Registro_Individual.grid(row=0, column=1, sticky="nsew")
        else:
            Frame_Añadir_Registro_Individual.grid_forget()

#%% -------------- MAIN WINDOW: SELECCIÓN DE FRAME DE TRANSFERENCIA HORAS -----------------
def seleccionar_frame_transferencia_horas():
    seleccionar_frame("Transferencia Horas")

#%% -------------- MAIN WINDOW: SELECCIÓN DE FRAME DE CARGAR HORAS -----------------
def seleccionar_frame_cargar_horas():
    seleccionar_frame("Cargar Horas")

#%% -------------- MAIN WINDOW: SELECCIÓN DE FRAME DE AGREGAR REGISTROS -----------------
def seleccionar_frame_agregar_registros():
    seleccionar_frame("Añadir Registro Individual")

#%% -------------- FRAME TRANSFERENCIA HORAS: EXTRAER WORKSPACES --------------
def extraer_workspaces(workspaces):
    name_workspaces = []
    for i in range(len(workspaces)):
        name_workspaces.append(workspaces[i]["name"])

    return name_workspaces

#%% -------------- FRAME TRANSFERENCIA HORAS: EXTRAER PROYECTOS --------------
def extraer_proyectos(projects):
    projects_name = {}
    for workspace in list(projects.keys()):
        projects_name[workspace]=[]
        for proj in projects[workspace]:
            projects_name[workspace].append(projects[workspace][proj]["name"])

    return projects_name

#%% -------------- FRAME TRANSFERENCIA HORAS: OBTENER WORKSPACE DE ORIGEN --------------
def obtener_workspace_origen(*args):
    global workspace_origen
    workspace_origen = Workspace1_variable.get()

#%% -------------- FRAME TRANSFERENCIA HORAS: OBTENER PROYECTO --------------
def obtener_proyecto(*args):
    global proyecto
    proyecto = Project3_variable.get()

#%% -------------- FRAME TRANSFERENCIA HORAS: OBTENER WORKSPACE DE DESTINO --------------
def obtener_workspace_destino(*args):
    global workspace_destino
    workspace_destino = Workspace2_variable.get()
    
#%% -------------- FRAME TRANSFERENCIA HORAS: MOSTRAR WORKSPACE DE DESTINO --------------    
def mostrar_workspace_destino(*args):

    global Workspace2_variable, OptionMenu2_Transferencia_Horas
    lista_workspace_destino = [nombre for nombre in workspaces_name if nombre != workspace_origen]
    Workspace2_variable.set("")
    OptionMenu2_Transferencia_Horas.configure(values=lista_workspace_destino)

    Project3_variable.set("")
    OptionMenu3_Transferencia_Horas.configure(values="")

#%% -------------- FRAME TRANSFERENCIA HORAS: MOSTRAR PROYECTO --------------
def mostrar_proyecto(*args):
    global Project3_variable, OptionMenu3_Transferencia_Horas

    elementos_comunes = [elemento for elemento in projects_name[workspace_origen] if elemento in projects_name[workspace_destino]]

    #Crea la ventana de alerta
    if len(elementos_comunes)==0:

        mensaje_alerta = "No hay proyectos en común entre estos dos workspaces.\nPor favor selecciona otro(s) workspace(s)."
        titulo_alerta = "Error: Selección proyecto"
        nombre_ico = "Error.ico"
        x_place_button, y_place_button =180, 65
        x_place_text, y_place_text =38, 20
        command = [f"Project3_variable.set(\"\")", f"OptionMenu3_Transferencia_Horas.configure(values=\"\")"]
        generar_ventana_alerta(mensaje_alerta,titulo_alerta,nombre_ico,x_place_text, y_place_text,x_place_button, y_place_button,command)
        
    else:

        Project3_variable.set("")
        OptionMenu3_Transferencia_Horas.configure(values=elementos_comunes)

#%% -------------- FRAME TRANSFERENCIA HORAS: HABILITAR BOTÓN TRANSFERIR HORAS --------------
def habilitar_boton_transferir_horas():

    global fecha_inicio, fecha_fin, TransferirBoton_Transferencia_Horas

    fecha_inicio = Entry1_Transferencia_Horas.get()
    fecha_fin = Entry2_Transferencia_Horas.get()

    if workspace_origen and workspace_destino and proyecto and fecha_inicio and fecha_fin:
        TransferirBoton_Transferencia_Horas.configure(state=tkinter.NORMAL)
    else:
        TransferirBoton_Transferencia_Horas.configure(state=tkinter.DISABLED)

#%% -------------- FRAME TRANSFERENCIA HORAS: VERIFICAR FECHA DE INICIO --------------
def verificar_fecha_inicio():
    
    global fecha_inicio

    fecha_inicio = Entry1_Transferencia_Horas.get()

    if re.match(r"^\d{4}-\d{2}-\d{2}$", fecha_inicio):
        try:
            datetime.strptime(fecha_inicio, '%Y-%m-%d')
        except ValueError:
            mensaje_alerta = "El mes debe estar entre 1 y 12.\nEl día debe estar entre 1 y 31."
            titulo_alerta = "Error: Fecha de inicio"
            nombre_ico = "Error.ico"
            x_place_button, y_place_button =180, 65
            x_place_text, y_place_text =110, 20
            command = [f"Entry1_Transferencia_Horas.delete(0,\"end\")"]
            generar_ventana_alerta(mensaje_alerta,titulo_alerta,nombre_ico,x_place_text, y_place_text,x_place_button, y_place_button,command)
    elif fecha_inicio == "":
        pass
    else:
        mensaje_alerta = "Se espera el formato de fecha aaaa-mm-dd.\nPor ejemplo: 2022-12-19."
        titulo_alerta = "Error: Fecha de inicio"
        nombre_ico = "Error.ico"
        x_place_button, y_place_button =180, 65
        x_place_text, y_place_text =70, 20
        command = [f"Entry1_Transferencia_Horas.delete(0,\"end\")"]
        generar_ventana_alerta(mensaje_alerta,titulo_alerta,nombre_ico,x_place_text, y_place_text,x_place_button, y_place_button,command)

#%% -------------- FRAME TRANSFERENCIA HORAS: VERIFICAR FECHA FIN --------------
def verificar_fecha_fin():
    
    global fecha_fin

    fecha_fin = Entry2_Transferencia_Horas.get()

    if re.match(r"^\d{4}-\d{2}-\d{2}$", fecha_fin):
        try:
            datetime.strptime(fecha_fin, '%Y-%m-%d')
        except ValueError:
            mensaje_alerta = "El mes debe estar entre 1 y 12.\nEl día debe estar entre 1 y 31."
            titulo_alerta = "Error: Fecha fin"
            nombre_ico = "Error.ico"
            x_place_button, y_place_button =180, 65
            x_place_text, y_place_text =110, 20
            command = [f"Entry2_Transferencia_Horas.delete(0,\"end\")"]
            generar_ventana_alerta(mensaje_alerta,titulo_alerta,nombre_ico,x_place_text, y_place_text,x_place_button, y_place_button,command)
            fecha_fin = ""
    elif fecha_fin == "":
        pass
    else:
        mensaje_alerta = "Se espera el formato de fecha aaaa-mm-dd.\nPor ejemplo: 2022-12-19."
        titulo_alerta = "Error: Fecha fin"
        nombre_ico = "Error.ico"
        x_place_button, y_place_button =180, 65
        x_place_text, y_place_text =70, 20
        command = [f"Entry2_Transferencia_Horas.delete(0,\"end\")"]
        generar_ventana_alerta(mensaje_alerta,titulo_alerta,nombre_ico,x_place_text, y_place_text,x_place_button, y_place_button,command)
        fecha_fin = ""

    if fecha_fin != "" and fecha_inicio !="":

        if (datetime.strptime(fecha_fin, "%Y-%m-%d") - datetime.strptime(fecha_inicio, "%Y-%m-%d")).days < 0:
            mensaje_alerta = "La fecha fin debe ser mayor que la fecha de inicio."
            titulo_alerta = "Error: Fecha fin"
            nombre_ico = "Error.ico"
            x_place_button, y_place_button =180, 65
            x_place_text, y_place_text =55, 20
            command = [f"Entry2_Transferencia_Horas.delete(0,\"end\")"]
            generar_ventana_alerta(mensaje_alerta,titulo_alerta,nombre_ico,x_place_text, y_place_text,x_place_button, y_place_button,command)

#%% -------------- FRAME TRANSFERENCIA HORAS: GENERAR VENTANA DE LOGS --------------
def crear_ventana_logs_transferencia_horas():

    #Extrae los exitos y fracasos de transferencia de horas
    with open(os.path.join(library_path, "contadores.pkl"), 'rb') as file:
        contadores = pickle.load(file)
    file.close()
    exitos, fracasos = contadores['exitos'],contadores['fracasos']
    #Creación de progreso
    window_logs = CTkToplevel()
    #Nombre de la ventana
    window_logs.title("Transferencia completada")
    #Resizable
    window_logs.resizable(False,False)
    window_logs.transient(home_window)
    window_logs.grab_set()
    #Geometría
    width = 400
    height = 100
    screen_width = window_logs.winfo_screenwidth()
    screen_height = window_logs.winfo_screenheight()
    x = (screen_width - width) // 2
    y = (screen_height - height) // 2
    window_logs.geometry(f"{width}x{height}+{x}+{y}")
    #Ícono ventana
    window_logs.after(201, lambda :window_logs.iconbitmap(os.path.join(images_path, "exito.ico")))
    #Label
    label_log = CTkLabel(master=window_logs,text=f"Se migraron {exitos} registros con éxito y {fracasos} registros fallaron.\n Revisar archivo de errores en Documentos.",font=('Gothic A1',13))
    label_log.place(x=40,y=18)
    #Botón de ok
    OKBoton_window_log = CTkButton(master= window_logs, text="OK", width=40, height=20, compound="left",font=('Gothic A1',15), command=window_logs.destroy)
    OKBoton_window_log.place(x=180,y=65)
    TransferirBoton_Transferencia_Horas.configure(state=tkinter.NORMAL)

#%% -------------- FRAME TRANSFERENCIA HORAS: GENERAR VENTANA DE PROGRESO  --------------
def generar_ventana_progreso_transferencia_horas():
    #Creación de progreso
    window_alert8 = CTkToplevel()
    #Nombre de la ventana
    window_alert8.title("Transfiriendo horas")
    #Resizable
    window_alert8.resizable(False,False)
    window_alert8.transient(home_window)
    window_alert8.grab_set()
    #Geometría
    width = 300
    height = 50
    screen_width = window_alert8.winfo_screenwidth()
    screen_height = window_alert8.winfo_screenheight()
    x = (screen_width - width) // 2
    y = (screen_height - height) // 2
    window_alert8.geometry(f"{width}x{height}+{x}+{y}")
    #Ícono ventana
    window_alert8.after(2, lambda :window_alert8.iconbitmap(os.path.join(images_path, "upload.ico")))
    #Barra de progreso
    progressbar1 = CTkProgressBar(master=window_alert8, orientation="horizontal",mode="indeterminate",width=250,height=10, progress_color="green",indeterminate_speed=1.5)
    progressbar1.place(x=22,y=20)
    progressbar1.start()

    def destruir_ventana_progreso():
        ruta_archivo = os.path.join(os.path.expanduser("~\\Documents"), f"TransferenciaHoras_log")
        
        if os.path.exists(ruta_archivo):
            window_alert8.after(1000, window_alert8.destroy)  # Cierra la ventana después de 1 segundo
            crear_ventana_logs_transferencia_horas()
        else:
            window_alert8.after(1000, destruir_ventana_progreso)  # Verifica nuevamente después de 1 segundo

    destruir_ventana_progreso()

#%% -------------- FRAME TRANSFERENCIA HORAS: EJECUTAR TRANSFERENCIA HORAS  --------------
def transferir_horas():

    #Elimina los logs existentes con respecto a la función
    ruta_documentos = os.path.expanduser("~\\Documents")
    lista_archivos = os.listdir(os.path.expanduser("~\\Documents"))
    for archivo in lista_archivos:
        # if "TransferenciaHoras_" in archivo:
        #     os.remove(f"{ruta_documentos}\{archivo}")
        if "TransferenciaHoras_log" in archivo:
            shutil.rmtree(f"{ruta_documentos}\{archivo}")

    TransferirBoton_Transferencia_Horas.configure(state=tkinter.DISABLED)

    def ejecutar_tarea():

        f_transferencia_horas(home_window, workspace_origen, workspace_destino, proyecto, fecha_inicio, fecha_fin)


    #Ejecuta la transferencia de horas
    home_window.after(100,ejecutar_tarea)
    generar_ventana_progreso_transferencia_horas()

#%% -------------- FRAME CARGAR HORAS: OBTENER WORKSPACE DE ORIGEN --------------
def obtener_workspace_origen_menu2(*args):
    global workspace_origen_menu2
    workspace_origen_menu2 = Workspace1_variable_menu2.get()

#%% -------------- FRAME CARGAR HORAS: OBTENER WORKSPACE DE DESTINO --------------
def obtener_workspace_destino_menu2(*args):
    global workspace_destino_menu2
    workspace_destino_menu2 = Workspace2_variable_menu2.get()

#%% -------------- FRAME CARGAR HORAS: OBTENER PROYECTO --------------
def obtener_proyecto_menu2(*args):
    global proyecto_menu2
    proyecto_menu2 = Project3_variable_menu2.get()

#%% -------------- FRAME CARGAR HORAS: MOSTRAR WORKSPACE DE DESTINO --------------
def mostrar_workspace_destino_menu2(*args):

    global Workspace2_variable_menu2, OptionMenu2_Cargar_Horas
    lista_workspace_destino_menu2 = [nombre for nombre in workspaces_name if nombre != workspace_origen_menu2]
    Workspace2_variable_menu2.set("")
    OptionMenu2_Cargar_Horas.configure(values=lista_workspace_destino_menu2)

    Project3_variable_menu2.set("")
    OptionMenu3_Cargar_Horas.configure(values="")

#%% -------------- FRAME CARGAR HORAS: MOSTRAR PROYECTO --------------
def mostrar_proyecto_menu2(*args):
    global Project3_variable_menu2, OptionMenu3_Cargar_Horas

    elementos_comunes = [elemento for elemento in projects_name[workspace_origen_menu2] if elemento in projects_name[workspace_destino_menu2]]

    #Crea la ventana de alerta
    if len(elementos_comunes)==0:

        mensaje_alerta = "No hay proyectos en común entre estos dos workspaces.\nPor favor selecciona otro(s) workspace(s)."
        titulo_alerta = "Error: Selección proyecto"
        nombre_ico = "Error.ico"
        x_place_button, y_place_button =180, 65
        x_place_text, y_place_text =38, 20
        command = [f"Project3_variable_menu2.set(\"\")", f"OptionMenu3_Cargar_Horas.configure(values=\"\")"]
        generar_ventana_alerta(mensaje_alerta,titulo_alerta,nombre_ico,x_place_text, y_place_text,x_place_button, y_place_button,command)
        
    else:

        Project3_variable_menu2.set("")
        OptionMenu3_Cargar_Horas.configure(values=elementos_comunes)

#%% -------------- FRAME CARGAR HORAS: FUNCIÓN DE CARGAR HORAS --------------
def cargar_archivo():

    global TextBox1_Cargar_Horas, archivo_horas, archivo

    #Carga el archivo
    archivo = filedialog.askopenfilename(filetypes=[("Archivos de Excel", "*.xlsx")])

    if archivo:
        # Muestra el nombre del archivo en el Textbox
        nombre_archivo = os.path.basename(archivo)
        TextBox1_Cargar_Horas.configure(state=NORMAL)
        TextBox1_Cargar_Horas.delete(0.0,"end")
        TextBox1_Cargar_Horas.insert(0.0,nombre_archivo)
        TextBox1_Cargar_Horas.configure(state=DISABLED)

        #Carga el archivo en un pandas
        archivo_horas = pd.read_excel(archivo)

        #Verifica si la descripcion es NaN, de serlo, le asigna ""
        archivo_horas["Descripción"] = archivo_horas["Descripción"].fillna("")

        #Verifica el formato de los archivos
        if archivo_horas["Tarea"].isna().any() or archivo_horas["Correo electrónico"].isna().any() or archivo_horas["Fecha de inicio"].isna().any() or archivo_horas["Hora de inicio"].isna().any() or archivo_horas["Fecha de finalización"].isna().any() or archivo_horas["Hora de finalización"].isna().any() :

            mensaje_alerta = "El archivo tiene algunos campos en blancos o mal formateados.\nVuelve a intentarlo. "
            titulo_alerta = "Error: Archivo inválido"
            nombre_ico = "Error.ico"
            x_place_button, y_place_button =180, 65
            x_place_text, y_place_text =20, 20
            command = [f"TextBox1_Cargar_Horas.configure(state=NORMAL)",
        "TextBox1_Cargar_Horas.delete(0.0,\"end\")"]
            generar_ventana_alerta(mensaje_alerta,titulo_alerta,nombre_ico,x_place_text, y_place_text,x_place_button, y_place_button,command)

        else:

            #Verifica el patron de horas 
            patron = r"\d{1,2}:\d{2} (AM|PM)"
            archivo_horas["coincide_patron_inicio"] = archivo_horas["Hora de inicio"].str.contains(patron)
            archivo_horas["coincide_patron_fin"] = archivo_horas["Hora de finalización"].str.contains(patron)
            correcion_hora_inicio = archivo_horas[~archivo_horas["coincide_patron_inicio"]]
            correcion_hora_fin = archivo_horas[~archivo_horas["coincide_patron_fin"]]
            if len(correcion_hora_inicio) > 0 or len(correcion_hora_fin)>0:
                mensaje_alerta = "El formato de hora no coincide.\nSe espera HH:MM (AM/PM)."
                titulo_alerta = "Error: Hora inválida"
                nombre_ico = "Error.ico"
                x_place_button, y_place_button =180, 65
                x_place_text, y_place_text =110, 20
                command = [f"TextBox1_Cargar_Horas.configure(state=NORMAL)",
                "TextBox1_Cargar_Horas.delete(0.0,\"end\")"]
                generar_ventana_alerta(mensaje_alerta,titulo_alerta,nombre_ico,x_place_text, y_place_text,x_place_button, y_place_button,command)
            
            archivo_horas = archivo_horas.drop("coincide_patron_inicio", axis=1)
            archivo_horas = archivo_horas.drop("coincide_patron_fin", axis=1)

            #Verifica el patron de fechas 
            patron = r"\d{2}/\d{2}/\d{4}"
            archivo_horas["coincide_patron_inicio"] = archivo_horas["Fecha de inicio"].str.contains(patron)
            archivo_horas["coincide_patron_fin"] = archivo_horas["Fecha de finalización"].str.contains(patron)
            correcion_fecha_inicio = archivo_horas[~archivo_horas["coincide_patron_inicio"]]
            correcion_fecha_fin = archivo_horas[~archivo_horas["coincide_patron_fin"]]
            if len(correcion_fecha_inicio) > 0 or len(correcion_fecha_fin)>0:
                mensaje_alerta = "El formato de fecha no coincide.\nSe espera dd/mm/aaaa."
                titulo_alerta = "Error: Hora inválida"
                nombre_ico = "Error.ico"
                x_place_button, y_place_button =180, 65
                x_place_text, y_place_text =100, 20
                command = [f"TextBox1_Cargar_Horas.configure(state=NORMAL)",
                "TextBox1_Cargar_Horas.delete(0.0,\"end\")"]
                generar_ventana_alerta(mensaje_alerta,titulo_alerta,nombre_ico,x_place_text, y_place_text,x_place_button, y_place_button,command)

            archivo_horas = archivo_horas.drop("coincide_patron_inicio", axis=1)
            archivo_horas = archivo_horas.drop("coincide_patron_fin", axis=1)
            
#%% -------------- FRAME CARGAR HORAS: HABILITAR BOTÓN CARGAR HORAS --------------    
def habilitar_boton_cargar_horas():

    global CargarHoras_Cargar_Horas

    if workspace_origen_menu2 and workspace_destino_menu2 and proyecto_menu2:
        
        CargarHoras_Cargar_Horas.configure(state=tkinter.NORMAL)
    else:
        CargarHoras_Cargar_Horas.configure(state=tkinter.DISABLED)

#%% -------------- FRAME CARGAR HORAS: HABILITAR BOTÓN CARGAR HORAS --------------    
def crear_ventana_logs_cargar_horas():

    #Extrae los exitos y fracasos de transferencia de horas
    with open(os.path.join(library_path, "contadores_cargarHoras.pkl"), 'rb') as file:
        contadores = pickle.load(file)
    file.close()
    exitos, fracasos = contadores['exitos'],contadores['fracasos']
    #Creación de progreso
    window_logs = CTkToplevel()
    #Nombre de la ventana
    window_logs.title("Transferencia completada")
    #Resizable
    window_logs.resizable(False,False)
    window_logs.transient(home_window)
    window_logs.grab_set()
    #Geometría
    width = 400
    height = 100
    screen_width = window_logs.winfo_screenwidth()
    screen_height = window_logs.winfo_screenheight()
    x = (screen_width - width) // 2
    y = (screen_height - height) // 2
    window_logs.geometry(f"{width}x{height}+{x}+{y}")
    #Ícono ventana
    window_logs.after(201, lambda :window_logs.iconbitmap(os.path.join(images_path, "exito.ico")))
    #Label
    label_log = CTkLabel(master=window_logs,text=f"Se migraron {exitos} registros con éxito y {fracasos} registros fallaron.\n Revisar archivo de errores en Documentos.",font=('Gothic A1',13))
    label_log.place(x=40,y=18)
    #Botón de ok
    OKBoton_window_log = CTkButton(master= window_logs, text="OK", width=40, height=20, compound="left",font=('Gothic A1',15), command=window_logs.destroy)
    OKBoton_window_log.place(x=180,y=65)
    TransferirBoton_Transferencia_Horas.configure(state=tkinter.NORMAL)

#%% -------------- FRAME CARGAR HORAS: GENERAR VENTANA PROGRESO --------------    
def generar_ventana_progreso_cargar_horas():

    #Creación de progreso
    window_alert8 = CTkToplevel()
    #Nombre de la ventana
    window_alert8.title("Transfiriendo horas")
    #Resizable
    window_alert8.resizable(False,False)
    window_alert8.transient(home_window)
    window_alert8.grab_set()
    #Geometría
    width = 300
    height = 50
    screen_width = window_alert8.winfo_screenwidth()
    screen_height = window_alert8.winfo_screenheight()
    x = (screen_width - width) // 2
    y = (screen_height - height) // 2
    window_alert8.geometry(f"{width}x{height}+{x}+{y}")
    #Ícono ventana
    window_alert8.after(2, lambda :window_alert8.iconbitmap(os.path.join(images_path, "upload.ico")))
    #Barra de progreso
    progressbar1 = CTkProgressBar(master=window_alert8, orientation="horizontal",mode="indeterminate",width=250,height=10, progress_color="green",indeterminate_speed=1.5)
    progressbar1.place(x=22,y=20)
    progressbar1.start()

    def destruir_ventana_progreso():
        
        ruta_archivo = os.path.join(os.path.expanduser("~\\Documents"), "CargarHoras.log")
        
        if os.path.exists(ruta_archivo):
            window_alert8.after(1000, window_alert8.destroy)  # Cierra la ventana después de 1 segundo
            crear_ventana_logs_cargar_horas()
        else:
            window_alert8.after(1000, destruir_ventana_progreso)  # Verifica nuevamente después de 1 segundo

    destruir_ventana_progreso()

#%% -------------- FRAME CARGAR HORAS: CARGAR HORAS -------------- 
def cargar_horas():

    #Elimina los logs existentes con respecto a la función
    ruta_documentos = os.path.expanduser("~\\Documents")
    lista_archivos = os.listdir(os.path.expanduser("~\\Documents"))
    for archivo in lista_archivos:
        if "CargarHoras" in archivo:
            os.remove(f"{ruta_documentos}\{archivo}")

    CargarHoras_Cargar_Horas.configure(state=tkinter.DISABLED)

    def ejecutar_tarea():

        f_cargar_horas(archivo_horas,workspace_origen_menu2, workspace_destino_menu2,proyecto_menu2)

    #Ejecuta la transferencia de horas
    home_window.after(100,ejecutar_tarea)
    generar_ventana_progreso_cargar_horas()
    
#%% -------------- FRAME SUBIR REGISTRO: OBTENER WORKSPACE --------------
def obtener_workspace_menu3(*args):
    global workspace_menu3
    workspace_menu3 = Workspace_menu3_variable.get()
    print(f"Workspace: {workspace_menu3}")

#%% -------------- FRAME SUBIR REGISTRO: MOSTRAR PROYECTOS --------------
def proyectos_menu3(*args):

    global OptionMenu2_Añadir_Registro_Individual, Proyectos_menu3_variable, Tareas_menu3_variable, OptionMenu4_Añadir_Registro_Individual, OptionMenu3_Añadir_Registro_Individual, Usuarios_menu3_variable

    proyectos_menu3 = projects_name[workspace_menu3]

    if len(proyectos_menu3)> 0:
        
        Proyectos_menu3_variable.set("")
        OptionMenu2_Añadir_Registro_Individual.configure(values=proyectos_menu3)

        Usuarios_menu3_variable.set("")
        OptionMenu3_Añadir_Registro_Individual.configure(values="")

        Tareas_menu3_variable.set("")
        OptionMenu4_Añadir_Registro_Individual.configure(values="")

    else:

        mensaje_alerta = "No hay proyectos en este workspace.\nPor favor selecciona otro workspace."
        titulo_alerta = "Error: Selección proyecto"
        nombre_ico = "Error.ico"
        x_place_button, y_place_button =180, 65
        x_place_text, y_place_text =90, 20
        command = [f"Proyectos_menu3_variable.set(\"\")",
                   f"OptionMenu2_Añadir_Registro_Individual.configure(values=\"\")",f"Usuarios_menu3_variable.set(\"\")",
                   f"OptionMenu3_Añadir_Registro_Individual.configure(values=\"\")",f"Tareas_menu3_variable.set(\"\")",
                   f"OptionMenu4_Añadir_Registro_Individual.configure(values=\"\")"]
        generar_ventana_alerta(mensaje_alerta,titulo_alerta,nombre_ico,x_place_text, y_place_text,x_place_button, y_place_button,command)
        
#%% -------------- FRAME SUBIR REGISTRO: OBTENER PROYECTOS --------------
def obtener_proyecto_menu3(*args):
    global proyecto_menu3
    proyecto_menu3 = Proyectos_menu3_variable.get()
    print(f"Proyecto:{proyecto_menu3}")    

#%% -------------- FRAME SUBIR REGISTRO: MOSTRAR USUARIOS --------------
def usuarios_menu3(*args):

    global OptionMenu3_Añadir_Registro_Individual, Usuarios_menu3_variable, Tareas_menu3_variable, OptionMenu4_Añadir_Registro_Individual

    nicknames = []
    nicknames = [user["name"] for user in users_data[workspace_menu3].values()]
    
    Usuarios_menu3_variable.set("")
    OptionMenu3_Añadir_Registro_Individual.configure(values=nicknames)

    Tareas_menu3_variable.set("")
    OptionMenu4_Añadir_Registro_Individual.configure(values="")

#%% -------------- FRAME SUBIR REGISTRO: OBTENER USUARIO --------------
def obtener_usuario_menu3(*args):
    global usuario_menu3, email_menu3
    usuario_menu3 = Usuarios_menu3_variable.get()
    email_menu3  = next((usuario["email"] for usuario in users_data[workspace_menu3].values() if usuario['name'] == usuario_menu3), None)
    print(f"Usuario: {usuario_menu3}\n Email: {email_menu3}")

#%% -------------- FRAME SUBIR REGISTRO: MOSTRAR TAREAS --------------
def mostrar_tareas_proyecto(*args):

    global Tareas_menu3_variable, OptionMenu4_Añadir_Registro_Individual

    tareas = getProjectTask(workspace_menu3,proyecto_menu3)

    if len(tareas["Tareas"])>0:
        Tareas_menu3_variable.set("")
        OptionMenu4_Añadir_Registro_Individual.configure(values=tareas["Tareas"])
    else:
        Tareas_menu3_variable.set("")
        OptionMenu4_Añadir_Registro_Individual.configure(values=[""])

#%% -------------- FRAME SUBIR REGISTRO: OBTENER TAREA --------------
def obtener_tarea(*args):
    global tarea_menu3
    tarea_menu3 = Tareas_menu3_variable.get()
    print(f"Tarea:{tarea_menu3}")

#%% -------------- FRAME SUBIR REGISTRO: VERIFICAR FECHA DE TAREA --------------
def verificar_fecha_tarea():
    
    global fecha_menu3

    fecha_menu3 = Entry1_Añadir_Registro_Individual.get()
    print(f"Fecha:{fecha_menu3}")

    if re.match(r"^\d{4}-\d{2}-\d{2}$", fecha_menu3):
        try:
            datetime.strptime(fecha_menu3, '%Y-%m-%d')
        except ValueError:
            mensaje_alerta = "El mes debe estar entre 1 y 12.\nEl día debe estar entre 1 y 31."
            titulo_alerta = "Error: Fecha de tarea"
            nombre_ico = "Error.ico"
            x_place_button, y_place_button =180, 65
            x_place_text, y_place_text =110, 20
            command = [f"Entry1_Añadir_Registro_Individual.delete(0,\"end\")"]
            generar_ventana_alerta(mensaje_alerta,titulo_alerta,nombre_ico,x_place_text, y_place_text,x_place_button, y_place_button,command)
            fecha_menu3 = ""
    elif fecha_menu3 == "":
        pass
    else:
        mensaje_alerta = "Se espera el formato de fecha aaaa-mm-dd.\nPor ejemplo: 2022-12-19."
        titulo_alerta = "Error: Fecha de tarea"
        nombre_ico = "Error.ico"
        x_place_button, y_place_button =180, 65
        x_place_text, y_place_text =70, 20
        command = [f"Entry1_Añadir_Registro_Individual.delete(0,\"end\")"]
        generar_ventana_alerta(mensaje_alerta,titulo_alerta,nombre_ico,x_place_text, y_place_text,x_place_button, y_place_button,command)
        fecha_menu3 = ""

#%% -------------- FRAME SUBIR REGISTRO: OBTENER HORA DE TAREA --------------
def obtener_hora(*args):
    global hora_menu3
    hora_menu3 = Hora_menu3_variable.get()
    print(f"Hora:{hora_menu3}")

#%% -------------- FRAME SUBIR REGISTRO: OBTENER DESCRIPCIÓN --------------
def obtener_descripcion(*args):
    global descripcion_menu3
    descripcion_menu3 = Entry2_Añadir_Registro_Individual.get()
    print(f"Descripcion:{descripcion_menu3}")  

#%% -------------- FRAME SUBIR REGISTRO: VERIFICAR DURACIÓN TAREA --------------
def verificar_duracion_tarea():
    global duracion_menu3

    duracion_menu3 = Entry3_Añadir_Registro_Individual.get()

    try:
        if duracion_menu3 != "":
            duracion_menu3 = float(duracion_menu3)
    except ValueError:
        mensaje_alerta = "La duración de la tarea debe ser un número."
        titulo_alerta = "Error: Duración tarea"
        nombre_ico = "Error.ico"
        x_place_button, y_place_button =180, 60
        x_place_text, y_place_text =80, 20
        command = [f"Entry3_Añadir_Registro_Individual.delete(0,\"end\")"]
        generar_ventana_alerta(mensaje_alerta,titulo_alerta,nombre_ico,x_place_text, y_place_text,x_place_button, y_place_button,command)
        duracion_menu3 = ""

#%% -------------- FRAME SUBIR REGISTRO: HABILITAR BOTÓN REGISTRO --------------
def habilitar_boton_subir_registro():

    if workspace_menu3 and proyecto_menu3 and usuario_menu3 and email_menu3 and fecha_menu3 and hora_menu3 and duracion_menu3:
        SubirRegistro_Añadir_Registro_Individual.configure(state=tkinter.NORMAL)
    else:
        SubirRegistro_Añadir_Registro_Individual.configure(state=tkinter.DISABLED)

#%% -------------- FRAME SUBIR REGISTRO: SUBIR REGISTRO --------------
def subir_registro():

    #Elimina los logs existentes con respecto a la función
    for archivo in os.listdir(library_path):
        if "exitoSubirRegistro.log" in archivo or "fallaSubirRegistro.log" in archivo:
            os.remove(f"{library_path}\{archivo}")

    SubirRegistro_Añadir_Registro_Individual.configure(state=tkinter.DISABLED)

    def ejecutar_tarea():

        f_subir_registro(workspace_menu3,proyecto_menu3,email_menu3,tarea_menu3, fecha_menu3, hora_menu3, duracion_menu3, descripcion_menu3)

    def generar_ventana_log():

        if "exitoSubirRegistro.log" in os.listdir(library_path):
            
            mensaje_alerta = "Se subió un registro con éxito."
            titulo_alerta = "Transferencia completada"
            nombre_ico = "exito.ico"
            x_place_button, y_place_button =180, 55
            x_place_text, y_place_text =110, 20
            command = [""]
            generar_ventana_alerta(mensaje_alerta,titulo_alerta,nombre_ico,x_place_text, y_place_text,x_place_button, y_place_button,command)

            SubirRegistro_Añadir_Registro_Individual.configure(state=tkinter.NORMAL)

        elif "fallaSubirRegistro.log" in os.listdir(library_path):
            
            mensaje_alerta = "Error al subir el registro."
            titulo_alerta = "Error"
            nombre_ico = "Error.ico"
            x_place_button, y_place_button =180, 55
            x_place_text, y_place_text =90, 20
            command = [""]

            generar_ventana_alerta(mensaje_alerta,titulo_alerta,nombre_ico,x_place_text, y_place_text,x_place_button, y_place_button,command)

            SubirRegistro_Añadir_Registro_Individual.configure(state=tkinter.NORMAL)

        else:
            home_window.after(1000, generar_ventana_log)

    #Ejecuta la transferencia de horas
    home_window.after(100,ejecutar_tarea)
    generar_ventana_log()

#%% ---------------------------------------------------
#%%                    PROGRESS WINDOW
#%% ---------------------------------------------------

#%% -------------- PROGRESS WINDOW: TAREAS A EJECUTAR -------------------
def actions_for_progress_window():

    #Realiza todas las acciones

    #Actualiza las claves API de los usuarios
    file_key = '1asbaD2XMx7GIKrcE9I9a9VyLi-1zloTh0M-dhjHwLEc'
    sheet_name = 'Respuestas de formulario 1'
    token_path = os.path.join(library_path, "service_account.json")
    updateUserAPIKeys(file_key,sheet_name,token_path)

    #Escribe la clave API del usuario que se loggeó en el archivo config.ini
    updateConfigIni(username)

    #Extrae los workspaces de clockify
    getWorkspaces()

    #Extrae los proyectos de cada workspace
    getProjects()

    #Extrae los usuarios de cada workspaces
    getWorkspaceUsers()

    #Extraer los grupos de los workspaces
    getGroups()
    
    #Destruye la ventana
    progress_window.destroy()

    # Muestra otra ventana Toplevel
    show_home_window()

#%% -------------- PROGRESS WINDOW: MOSTRAR VENTANA -------------------
def show_progressbar_window():

    global progress_window

    #Inicializa la ventana
    progress_window = CTkToplevel()
    width = 500
    height = 100
    screen_width = progress_window.winfo_screenwidth()
    screen_height = progress_window.winfo_screenheight()
    x = (screen_width - width) // 5
    y = (screen_height - height) // 4
    progress_window.geometry(f"{width}x{height}+{x}+{y}")
    progress_window.deiconify()
    progress_window.lift()
    #Nombre de la ventana
    progress_window.title("Cargando...")
    #Resizable
    progress_window.resizable(False,False)
    #Tema de la ventana
    set_appearance_mode("Dark")
    set_default_color_theme("dark-blue")  # Themes: blue (default), dark-blue, green
    #Ícono ventana
    progress_window.after(201, lambda :progress_window.iconbitmap(os.path.join(images_path, "logo.ico")))
    #Barra de progreso
    progressbar = CTkProgressBar(master=progress_window, orientation="horizontal",mode="indeterminate",width=400,height=20, progress_color="green",indeterminate_speed=1.5)
    progressbar.pack(padx=20, pady=45)
    progressbar.start()
    #Label de la barra de progreso
    label_progress = CTkLabel(master=progress_window, text="Preparando todo...",fg_color="transparent",font=('Gothic A1',13))
    label_progress.place(x=195,y=10)
    # Inicia el proceso de realización de acciones y cierre automático
    login_window.after(1000, actions_for_progress_window)

#%% ---------------------------------------------------
#%%                    LOGIN WINDOW 
#%% ---------------------------------------------------

#%% ----------------- LOGIN WINDOW: VALIDAR ACCESO LOGIN --------------------
def validar_acceso_login():

    global username
    global password
    global name_user

    #usuario
    username = user_entry.get()
    #contraseña
    password = password_entry.get()

    #Deserializa el archivo binario con la información de administradores
    with open(os.path.join(library_path, "login_credentials.pkl"), 'rb') as file:
        credentials = pickle.load(file)
    file.close()

    #Valida acceso
    if username in credentials['usernames'] and password in credentials['passwords']:

        #Nombre del usuario
        name_user = credentials['nombre'][credentials['usernames'].index(username)]
        
        #Segundo plano la ventana de login
        login_window.withdraw()

        #Muestra la barra de progreso
        show_progressbar_window()
        
    else:
        alert_label = CTkLabel(master=frame, text="El usuario es incorrecto o \n la contraseña es incorrecta.",fg_color="transparent",font=('Gothic A1',13), text_color='red')
        alert_label.place(x=60,y=238)

#%% ----------------- LOGIN WINDOW: HABILITAR BOTÓN CONECTAR --------------------
def habilitar_boton_conectar():

    usuario = user_entry.get()
    contraseña = password_entry.get()

    if usuario and contraseña:
        conectar.configure(state=tkinter.NORMAL)
    else:
        conectar.configure(state=tkinter.DISABLED)

#%% ----------------- VENTANA LOGIN PRINCIPAL --------------------
#Inicializa la ventana
login_window = CTk()
#Geometría
login_window.geometry("400x400")
#Nombre de la ventana
login_window.title("Login")
#Resizable
login_window.resizable(False,False)
#Tema de la ventana
set_appearance_mode("Dark")
set_default_color_theme("dark-blue")  # Themes: blue (default), dark-blue, green
#Background
images_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "WindowsImages")
background_image = ImageTk.PhotoImage(Image.open(os.path.join(images_path, "pattern.png")))
# background_image = CTkImage(dark_image=Image.open(os.path.join(images_path, "pattern.png")))
background_label = CTkLabel(master=login_window,image=background_image)
background_label.pack()
#Ícono ventana
login_window.after(201, lambda :login_window.iconbitmap(os.path.join(images_path, "logo.ico")))
# Frame central
frame = CTkFrame(master=background_label, width=300, height=340, corner_radius=20)
frame.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)
#Logo de pedelta
logo_image = CTkImage(Image.open(os.path.join(images_path, "Pedelta.png")), size=(220, 80))
logo_label = CTkLabel(master=frame,image=logo_image,text="",compound="center",fg_color="transparent")
logo_label.place(x=55, y=5)

#Label de iniciar sesión
login_label = CTkLabel(master=frame, text="Iniciar sesión",fg_color="transparent",font=('Gothic A1',22))
login_label.place(x=82,y=85)

#Input usuario
user_entry=CTkEntry(master=frame, width=180, placeholder_text='Username')
user_entry.place(x=62, y=145)

#Input password
password_entry=CTkEntry(master=frame, width=180, placeholder_text='Password', show="*")
password_entry.place(x=62, y=195)

#Botón de iniciar sesión
conectar= CTkButton(master=frame, text="Conectar", width=180, height=20, compound="left",font=('Gothic A1',15), command=validar_acceso_login,state=tkinter.DISABLED) 
conectar.place(x=62, y=270)

#Habilitar boton
user_entry.bind("<KeyRelease>", lambda event: habilitar_boton_conectar())
password_entry.bind("<KeyRelease>", lambda event: habilitar_boton_conectar())

#Ejecuta la ventana
login_window.mainloop()