import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector
from mysql.connector import Error

def conectar():
    try:
        conexion = mysql.connector.connect(
            host='localhost',
            user='root',
            password='admin',
            database='datospersonales',
        )
        return conexion
    except Error as e:
        messagebox.showerror('No se pudo conectar a la Base de datos', str(e))

def mostrarDatos():
    nueva_ventana = tk.Toplevel()
    nueva_ventana.title("Datos Personales")
    nueva_ventana.geometry("600x500")
    
    tree = ttk.Treeview(nueva_ventana, columns=('ID', 'Nombres', 'Apellidos', 'Teléfono', 'Email'), show='headings')
    tree.heading('ID', text='ID')
    tree.heading('Nombres', text='Nombres')
    tree.heading('Apellidos', text='Apellidos')
    tree.heading('Teléfono', text='Teléfono')
    tree.heading('Email', text='Email')
    
    tree.grid(row=0, column=0, sticky='nsew')
    
    scrollbar = ttk.Scrollbar(nueva_ventana, orient='vertical', command=tree.yview)
    tree.configure(yscroll=scrollbar.set)
    scrollbar.grid(row=0, column=1, sticky='ns')
    
    conexion = conectar()
    cursor = conexion.cursor()
    sql = "SELECT * FROM misdatos"
    try:
        cursor.execute(sql)
        registros = cursor.fetchall()
        for registro in registros:
            tree.insert('', tk.END, values=registro)
    except Error as e:
        messagebox.showerror('Error al obtener datos', str(e))
    finally:
        conexion.close()


    combobox_frame = ttk.Frame(nueva_ventana)
    combobox_frame.grid(row=1, column=0, sticky='ew')
    
    nombres = [registro[1] for registro in registros]  # Obtener solo los nombres de los registros
    
    # Añadir "Seleccione cliente" como primer elemento en la lista de nombres
    nombres.insert(0, "Seleccione cliente")
    
    combobox = ttk.Combobox(combobox_frame, values=nombres, state='readonly')
    combobox.grid(row=0, column=0, sticky='ew')
    combobox.current(0)  # Establecer "Seleccione cliente" como opción inicial


if __name__ == "__main__":
    mostrarDatos()
