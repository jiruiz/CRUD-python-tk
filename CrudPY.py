import tkinter as tk 
from tkinter import ttk, messagebox
import mysql.connector
from mysql.connector import Error


def conectar():
    try:
        conexion = mysql.connector.connect(
            host= 'localhost',
            user= 'root',
            password='admin',
            database='datospersonales',
        )
        return conexion
    except Error as e:
        messagebox.showerror('No se pudo conectar a la Base de datos',str(e))



def insertar():
    conexion = conectar()
    cursor = conexion.cursor()
    sql = "INSERT INTO misdatos (id, nombres, apellidos, telefono, email) VALUES (%s,%s,%s,%s,%s);"
    valores = (entryId.get(), entryNombres.get(),entryApellidos.get(), entrytelefono.get(),entryMail.get())
    try:
        cursor.execute(sql,valores)
        conexion.commit()
        messagebox.showinfo('Informacion', 'Registro insertado con éxito!')
        limpiarCampos()
    except Error as e:
        messagebox.showerror('Error al insetar datos',str(e))
    finally:
        conexion.close()    

def editar():
    conexion = conectar()
    cursor = conexion.cursor()
    sql = "UPDATE misdatos SET id=%s, nombres=%s, apellidos=%s, telefono=%s WHERE email=%s"
    valores = (entryId.get(), entryNombres.get(),entryApellidos.get(), entrytelefono.get(),entryMail.get())
    try:
        cursor.execute(sql,valores)
        conexion.commit()
        messagebox.showinfo('Informacion', 'Registro actualizado con éxito!')
        limpiarCampos()
    except Error as e:
        messagebox.showerror('Error al Editar datos',str(e))
    finally:
        conexion.close()       
        
def eliminar():
    conexion = conectar()
    cursor = conexion.cursor()
    sql = "DELETE FROM misdatos WHERE id=%s"
    valores = (entryId.get(), entryNombres.get(),entryApellidos.get(), entrytelefono.get(),entryMail.get())
    
    try:
        cursor.execute(sql,(entryId.get(),))
        conexion.commit()
        messagebox.showinfo('Informacion', 'Registro eliminado con éxito!')
        limpiarCampos()
    except Error as e:
        messagebox.showerror('Error al Eliminar datos',str(e))
    finally:
        conexion.close()    
           
           
def buscar():
    conexion = conectar()
    cursor = conexion.cursor()      
    sql = "SELECT * FROM misdatos WHERE id=%s"    
    try:
        cursor.execute(sql,(entryId.get(),))
        registro = cursor.fetchone()
        if registro:
            entryNombres.insert(0, registro[1])
            entryApellidos.insert(0, registro[2])
            entrytelefono.insert(0, registro[3])
            entryMail.insert(0, registro[4])
        else:
            messagebox.showinfo('Informacion', 'No se encontro el registro solicitado')
    finally:
        conexion.close()    
    
def limpiarCampos():
    entryId.delete(0,tk.END)
    entryNombres.delete(0,tk.END)
    entryApellidos.delete(0,tk.END)
    entrytelefono.delete(0,tk.END)
    entryMail.delete(0,tk.END)



app = tk.Tk()
app.title("Formulario de datos personales")
app.geometry("500x400")

ttk.Label(app,text="ID: ").grid(column=0,row=0)

# el texto que vamos a ingresar es el entry
entryId = ttk.Entry(app)
entryId.grid(column=1,row=0)


ttk.Label(app, text='Nombres:').grid(column=0,row=1)
entryNombres = ttk.Entry(app)
entryNombres.grid(column=1,row=1)

ttk.Label(app, text='Apellidos:').grid(column=0,row=2)
entryApellidos = ttk.Entry(app)
entryApellidos.grid(column=1,row=2)

ttk.Label(app, text='Teléfono:').grid(column=0,row=3)
entrytelefono = ttk.Entry(app)
entrytelefono.grid(column=1,row=3)

ttk.Label(app, text='Email:').grid(column=0,row=4)
entryMail = ttk.Entry(app)
entryMail.grid(column=1,row=4)

ttk.Button(app,text='Insertar',command=insertar).grid(column=0,row=5)

ttk.Button(app,text='Editar',command=editar).grid(column=1,row=5)

ttk.Button(app,text='Eliminar',command=eliminar).grid(column=2,row=5)

ttk.Button(app,text='Buscar',command=buscar).grid(column=3,row=5)

ttk.Button(app,text='Limpiar',command=limpiarCampos).grid(column=4,row=5)

app.mainloop()