import tkinter as tk
from tkinter import messagebox
import menu

def validar_login(ventana_login, entry_usuario, entry_contrasena):
    """Valida usuario y contraseña."""
    usuario = entry_usuario.get()
    contrasena = entry_contrasena.get()

    if usuario == "admin" and contrasena == "1234":
        ventana_login.destroy()
        menu.mostrar_menu_principal()  # Llamar al menú principal
    else:
        messagebox.showerror("Error", "Usuario o contraseña incorrectos")

def mostrar_login():
    """Muestra la ventana de login."""
    ventana_login = tk.Tk()
    ventana_login.title("SGP // ERP - Login")
    ventana_login.geometry("300x300")

    tk.Label(ventana_login, text="Usuario:").pack(pady=5)
    entry_usuario = tk.Entry(ventana_login)
    entry_usuario.pack(pady=5)

    tk.Label(ventana_login, text="Contraseña:").pack(pady=5)
    entry_contrasena = tk.Entry(ventana_login, show="*")
    entry_contrasena.pack(pady=5)

    tk.Button(ventana_login, text="Ingresar", command=lambda: validar_login(ventana_login, entry_usuario, entry_contrasena)).pack(pady=10)

    ventana_login.mainloop()