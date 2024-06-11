'''
Gestor de Tareas Interactivo en Python
Descripción:
Aplicación con un interfaz para gestionar tareas diarias.
A través de un menú, los usuarios podrán realizar las siguientes acciones:
1. Agregar nuevas tareas: Los usuarios podrán crear una tarea en un archivo 
   txt con un nombre a su elección y se guardará en la carpeta "tareas" que está 
   en el mismo directorio del ejecutable, si la carpeta "tareas" no existe, se creará automáticamente.
   Se podrá ingresar una descripción breve de la tarea y asignarle una fecha de vencimiento.
2. Marcar tareas como completadas: Una vez que hayan completado una
   tarea, podrán marcarla como finalizada.
3. Listar todas las tareas existentes: Mostrar todas las tareas registradas,
   incluyendo su descripción, fecha de vencimiento y estado.
4. Visualizar tareas completadas y pendientes por separado.
5. Opción para borrar individualmente a elección del usuario.
6. Salir del programa dejando las tareas guardadas.
'''

import os # libreria para ineractuar con el sistema operativo y operar con rutas y archivos
from datetime import datetime # libreria para poder manipular fechas


class Tareas_clase: # creación de la clase
    
    def __init__(self, titulo, descripcion, fecha_vencimiento, estado): # método constructor de la clase
        
        self.titulo = titulo
        self.descripcion = descripcion
        self.fecha_vencimiento = fecha_vencimiento
        self.estado = estado


def cargar_tareas(): # función para cargar las tareas guardadas
    
    tareas = [] # crea una lista vacia
    directorio_tareas = os.path.join(os.getcwd(), "tareas") # ruta de la carpeta tareas
    
    if not os.path.exists(directorio_tareas): # si no existe la carpeta tareas, la crea
        os.makedirs(directorio_tareas)
        
    for nombre_archivo in os.listdir(directorio_tareas): # itera por los archivos de la carpeta tareas
        ruta_archivo = os.path.join(directorio_tareas, nombre_archivo)
        with open(ruta_archivo, "r") as archivo: # abre los archivos guardados
            tarea = archivo.read().split(", ") # lee los campos del .txt separados por ,
            titulo = tarea[0]
            descripcion = tarea[1]
            fecha_vencimiento = datetime.strptime(tarea[2], "%d/%m/%y")
            estado = eval(tarea[3]) # convierte el estado de texto a booleano
            tareas.append(Tareas_clase(titulo, descripcion, fecha_vencimiento, estado)) # añade los elementos de la clase a la lista tareas
    
    return tareas


def guardar_tareas(tareas): # función para guardar las tareas
    
    carpeta_tareas = os.path.join(os.getcwd(), "tareas") # ruta de la carpeta tareas
    
    for tarea in tareas: # itera a través de las tareas
        name = f"{tarea.titulo}.txt" # nombre del archivo .txt donde se guarda la tarea
        ruta_tareas = os.path.join(carpeta_tareas, name) # ruta del archivo .txt dentro de la carpeta tareas
        with open(ruta_tareas, "w") as archivo: # excribe en el archivo .txt
            archivo.write(f"{tarea.titulo}, {tarea.descripcion}, {tarea.fecha_vencimiento.strftime('%d/%m/%y')}, {tarea.estado}\n") #formato en el que escribe


def agregar_tarea(tareas): # función para agregar nuevas tareas
    
    while True:
        titulo = input("\nIntroduce el nombre con el que vas a guardar la tarea: ")
        
        if any(titulo == tarea.titulo for tarea in tareas): # comprueba si el nombre de la tarea ya existe
            print(f"\nEl nombre {titulo} ya existe.")
        
        else:
            break

    descripcion = input("\nIntroduce la tarea: ")
    
    while True:
        fecha = input("\nIntroduce fecha de vencimiento (dd/mm/aa): ")
        
        try:
            fecha_vencimiento= datetime.strptime(fecha, "%d/%m/%y") # comprueba que el formato de la fecha introducida sea el correcto
            break
        
        except ValueError:
            print("El valor introducido no es correcto.")

    estado = False

    tarea = Tareas_clase(titulo, descripcion, fecha_vencimiento, estado) # añade a la clase los valores para los atributos
    tareas.append(tarea)
    guardar_tareas(tareas)
    print(f"\nLa tarea \"{titulo}\" ha sido guardada correctamente.\n")
    listar_tareas(tareas)


def marcar_completada(tareas): # función para cambiar el estado de una tarea a completada
    
    numero = int(input("\nIntroduce el número de la tarea que deseas marcar como completada: "))
    
    if 1 <= numero <= len(tareas): # comprueba si el número de tarea introducido existe
        tareas[numero - 1].estado = True # cambia el estado a True, para después mostrar que está completada
        guardar_tareas(tareas)
        print(f"La tarea {numero} ha sido completada.\n")
    
    else:
        print("El número de tarea ingresado no es válido.")


def listar_tareas(tareas): # función para listar todas las tareas que tenemos en la carpeta
    
    if not tareas: # comprueba si hay alguna tarea en la lista
        print("No hay ninguna tarea.")
    
    else:
        print("LISTA DE TAREAS: \n")
    
    for i, tarea in enumerate(tareas, 1): # itera a través de las tareas
        status = "Completada" if tarea.estado else "Sin completar" # comprueba si el estado es True o False
        print(f"{i}. {tarea.descripcion} - Fecha de vencimiento: {tarea.fecha_vencimiento.strftime("%d/%m/%y")} - Estado: {status}")


def visualizar_completadas(tareas): # función para visualizar tareas completadas
    
    print("\nLista de tareas completadas: ")
            
    for tarea in tareas:
    
        if tarea.estado: # si tarea.estado es True muestra la tarea como completada
            print(f"{tarea.descripcion} - Estado: Completada")
        
        else:
            print("No hay ninguna tarea completada.")
            


def visualizar_pendientes(tareas): # función para visualizar tareas no completadas

    print("\nLista de tareas pendientes: ")
    
    for tarea in tareas:
    
        if not tarea.estado: # si tarea.estado es False la muestra como sin completar
            print(f"{tarea.descripcion} - Estado: Sin Completar")
            
        else:
            print("No hay ninguna tarea pendiente.")


def borrar_tarea(tareas): # función para borrar la tarea seleccionada
    
    listar_tareas(tareas)
    numero = int(input("\nIntroduce el número de la tarea que deseas borrar: "))
    
    if 1 <= numero <= len(tareas): # comprueba si el número introducido corresponde con una tarea existente
        tarea = tareas.pop(numero - 1)
        os.remove(os.path.join(os.getcwd(), "tareas", f"{tarea.titulo}.txt")) # elimina la tarea seleccionada
        guardar_tareas(tareas)
        print(f"La tarea {numero} ha sido borrada.\n")
        listar_tareas(tareas)
    
    else:
        print("El número de tarea ingresado no es válido.")


def gestor_tareas(): # función principal
    
    tareas = cargar_tareas()
    
    try:
        
        while True: # menú del gestor de tareas
            print("\nGESTOR DE TAREAS: \n")
            print("1. AGREGAR NUEVAS TAREAS")
            print("2. MARCAR TAREAS COMO COMPLETADAS")
            print("3. LISTAR TODAS LAS TAREAS EXISTENTES")
            print("4. VISUALIZAR TAREAS COMPLETADAS")
            print("5. VISUALIZAR TAREAS PENDIENTES")
            print("6. BORRAR TAREA")
            print("7. SALIR")

            opcion = input("\nINTRODUCE UNA OPCIÓN: ")

            if opcion == '1':
                agregar_tarea(tareas)
            
            elif opcion == '2':
                marcar_completada(tareas)
            
            elif opcion == '3':
                listar_tareas(tareas)
            
            elif opcion == '4':
                visualizar_completadas(tareas)
            
            elif opcion == '5':
                visualizar_pendientes(tareas)
            
            elif opcion == '6':
                borrar_tarea(tareas)
            
            elif opcion == '7':
                print("\nGRACIAS POR UTILIZAR EL GESTOR DE TAREAS.")
                break # sale del bucle
            
            else:
                print("\n¡¡¡LA OPCIÓN INTRODUCIDA NO ES VÁLIDA!!!")
                print("\nINTRODUZCA UNA DE LAS SIGUIENTES OPCIONES (1, 2, 3, 4, 5, 6, 7). ")
    
    finally: # termina el programa guardando las tareas
        guardar_tareas(tareas)
        print("\nTareas guardadas correctamente.\n")


if __name__ == "__main__": # método para llamar a la función principal
    gestor_tareas()
