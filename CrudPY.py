import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector
from mysql.connector import Error
from mostrarDatos import mostrarDatos

# Variables globales para los widgets de entrada y label
entryId = None
id_label = None

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

def obtener_siguiente_id():
    conexion = conectar()
    cursor = conexion.cursor()
    try:
        cursor.execute("SELECT MAX(id) FROM misdatos")
        resultado = cursor.fetchone()
        if resultado[0] is not None:
            siguiente_id = resultado[0] + 1
        else:
            siguiente_id = 1  # Si no hay registros, comenzamos desde el ID 1
        return siguiente_id
    except Error as e:
        messagebox.showerror('Error al obtener siguiente ID', str(e))
    finally:
        conexion.close()

def mostrar_siguiente_id():
    conexion = conectar()
    cursor = conexion.cursor()
    try:
        # Obtener el último ID
        cursor.execute("SELECT MAX(id) FROM misdatos")
        resultado = cursor.fetchone()
        ultimo_id = resultado[0] if resultado[0] is not None else 0
        
        # Mostrar el siguiente ID en entryId
        siguiente_id = ultimo_id + 1
        entryId.config(state="normal")  # Habilitar para modificar temporalmente
        entryId.delete(0, tk.END)
        entryId.insert(0, siguiente_id)
        entryId.config(state="readonly")  # Volver a readonly después de actualizar
    except Error as e:
        messagebox.showerror('Error al obtener siguiente ID', str(e))
    finally:
        conexion.close()

def insertar():
    conexion = conectar()
    cursor = conexion.cursor()
    sql = "INSERT INTO misdatos (id, nombres, apellidos, telefono, email) VALUES (%s,%s,%s,%s,%s);"
    valores = (entryId.get(), entryNombres.get(), entryApellidos.get(), entrytelefono.get(), entryMail.get())
    try:
        cursor.execute(sql, valores)
        conexion.commit()
        messagebox.showinfo('Informacion', 'Registro insertado con éxito!')
        mostrar_siguiente_id()  # Mostrar el siguiente ID después de insertar
        limpiarCampos()
        
    except Error as e:
        messagebox.showerror('Error al insertar datos', str(e))
    finally:
        conexion.close()

def editar():
    conexion = conectar()
    cursor = conexion.cursor()
    sql = "UPDATE misdatos SET id=%s,nombres=%s, apellidos=%s, telefono=%s WHERE email=%s"
    valores = (entryId.get(),entryNombres.get(), entryApellidos.get(), entrytelefono.get(),entryMail.get())
    try:
        cursor.execute(sql, valores)
        conexion.commit()
        messagebox.showinfo('Informacion', 'Registro actualizado con éxito!')
        limpiarCampos()
    except Error as e:
        messagebox.showerror('Error al Editar datos', str(e))
    finally:
        conexion.close()


def eliminar():
    conexion = conectar()
    cursor = conexion.cursor()
    sql = "DELETE FROM misdatos WHERE id=%s"
    try:
        cursor.execute(sql, (entryBuscarId.get(),))
        conexion.commit()
        messagebox.showinfo('Informacion', 'Registro eliminado con éxito!')
        limpiarCampos()
    except Error as e:
        messagebox.showerror('Error al Eliminar datos', str(e))
    finally:
        conexion.close()

def buscar():
    conexion = conectar()
    cursor = conexion.cursor()
    sql = "SELECT * FROM misdatos WHERE id=%s"
    try:
        cursor.execute(sql, (entryBuscarId.get(),))
        registro = cursor.fetchone()
 
        if registro:
            id_label.config(text=f"ID ENCONTRADO: {registro[0]}")
            entryId.insert(0, registro[0])
            entryNombres.insert(0, registro[1])
            entryApellidos.insert(0, registro[2])
            entrytelefono.insert(0, registro[3])
            entryMail.insert(0, registro[4])
        else:
            messagebox.showinfo('Informacion', 'No se encontró el registro solicitado')
    except Error as e:
        messagebox.showerror('Error al buscar datos', str(e))
    finally:
        conexion.close()

def limpiarCampos():
    entryBuscarId.delete(0, tk.END)  # Limpiar el campo de búsqueda
    entryNombres.delete(0, tk.END)
    entryApellidos.delete(0, tk.END)
    entrytelefono.delete(0, tk.END)
    entryMail.delete(0, tk.END)

# CONFIGURACION DE LA VENTANA PRINCIPAL
app = tk.Tk()
app.title("Formulario de datos personales")
app.geometry("500x400")

# LOS LABELS Y ENTRADAS DE DATOS
id_label = ttk.Label(app, text="Siguiente ID a insertar: ")
id_label.grid(column=0, row=0)

ttk.Label(app, text='ID a buscar:').grid(column=0, row=1)
entryBuscarId = ttk.Entry(app)
entryBuscarId.grid(column=1, row=1)

ttk.Label(app, text='Nombres:').grid(column=0, row=2)
entryNombres = ttk.Entry(app)
entryNombres.grid(column=1, row=2)

ttk.Label(app, text='Apellidos:').grid(column=0, row=3)
entryApellidos = ttk.Entry(app)
entryApellidos.grid(column=1, row=3)

ttk.Label(app, text='Teléfono:').grid(column=0, row=4)
entrytelefono = ttk.Entry(app)
entrytelefono.grid(column=1, row=4)

ttk.Label(app, text='Email:').grid(column=0, row=5)
entryMail = ttk.Entry(app)
entryMail.grid(column=1, row=5)

# Configuración para hacer el campo entryId readonly
entryId = ttk.Entry(app, state="readonly")
entryId.grid(column=1, row=0)
mostrar_siguiente_id()  # Mostrar el siguiente ID al iniciar la aplicación

# ACA HACEMOS LOS BOTONES PARA LAS OPERACIONES
ttk.Button(app, text='Insertar', command=insertar).grid(column=0, row=6)
ttk.Button(app, text='Editar', command=editar).grid(column=1, row=6)
ttk.Button(app, text='Eliminar', command=eliminar).grid(column=2, row=6)
ttk.Button(app, text='Buscar', command=buscar).grid(column=3, row=6)
ttk.Button(app, text='Limpiar', command=limpiarCampos).grid(column=4, row=6)
ttk.Button(app, text='Mostrar Datos', command=mostrarDatos).grid(column=0, row=7, columnspan=5)



app.mainloop()
