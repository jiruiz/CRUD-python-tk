# Importar módulos necesarios de tkinter y MySQL
import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector
from mysql.connector import Error

# definimos la funcion para la conexión con la base de datos
def conectar():
    try:
        # la configuramos la conexión con MySQL
        conexion = mysql.connector.connect(
            host='localhost',
            user='root',
            password='admin',
            database='datospersonales',
        )
        return conexion  # Devolver el objeto de conexión establecido
    except Error as e:
        # Mostrar mensaje de error si no se puede conectar
        messagebox.showerror('No se pudo conectar a la Base de datos', str(e))





# Función para mostrar los datos en una nueva ventana
def mostrarDatos():
    # Crear una nueva ventana superior para mostrar datos personales
    nueva_ventana = tk.Toplevel()
    nueva_ventana.title("Datos Personales")
    nueva_ventana.geometry("600x500")  # Establecer tamaño de la ventana


    # Crear un árbol (treeview) para mostrar los datos
    tree = ttk.Treeview(nueva_ventana, columns=('ID', 'Nombres', 'Apellidos', 'Teléfono', 'Email'), show='headings')
    tree.heading('ID', text='ID')  # Configurar encabezados de columna
    tree.heading('Nombres', text='Nombres')
    tree.heading('Apellidos', text='Apellidos')
    tree.heading('Teléfono', text='Teléfono')
    tree.heading('Email', text='Email')
    tree.grid(row=0, column=0, sticky='nsew')  # Posicionar el árbol en la ventana

    # Configurar barra de desplazamiento vertical para el árbol
    scrollbar = ttk.Scrollbar(nueva_ventana, orient='vertical', command=tree.yview)
    tree.configure(yscroll=scrollbar.set)
    scrollbar.grid(row=0, column=1, sticky='ns')  # Posicionar la barra de desplazamiento


    # Establecer conexión con la base de datos y ejecutar consulta SQL
    conexion = conectar()
    cursor = conexion.cursor()
    sql = "SELECT * FROM misdatos"
    try:
        cursor.execute(sql)
        registros = cursor.fetchall()  # Obtener todos los registros de la consulta

        # Insertar cada registro como una fila en el árbol
        for registro in registros:
            tree.insert('', tk.END, values=registro)
    except Error as e:
        # Mostrar mensaje de error si ocurre un problema al obtener datos
        messagebox.showerror('Error al obtener datos', str(e))
    finally:
        conexion.close()  # Cerrar la conexión después de usarla


    # Crear un marco para el cuadro combinado (combobox)
    combobox_frame = ttk.Frame(nueva_ventana)
    combobox_frame.grid(row=1, column=0, sticky='ew')  # Posicionar el marco en la ventana

    # Obtener una lista de nombres de los registros para el cuadro combinado
    nombres = [registro[1] for registro in registros]  # Obtener solo los nombres de los registros

    # Añadir "Seleccione cliente" como primer elemento en la lista de nombres
    nombres.insert(0, "Seleccione cliente")

    # Crear el cuadro combinado (combobox) con los nombres y configurarlo como solo lectura
    combobox = ttk.Combobox(combobox_frame, values=nombres, state='readonly')
    combobox.grid(row=0, column=0, sticky='ew')  # Posicionar el cuadro combinado en el marco
    combobox.current(0)  # Establecer "Seleccione cliente" como opción inicial seleccionada



# Punto de entrada principal para ejecutar la función mostrarDatos()
if __name__ == "__main__":
    mostrarDatos()
