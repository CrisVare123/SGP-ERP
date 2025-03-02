import tkinter as tk
from tkinter import messagebox
import database
import clientes 
import productos
import nuevo_pedido 
import pedidos


def mostrar_mensaje():
    """Muestra un mensaje de mantenimiento."""
    messagebox.showinfo("Módulo en Mantenimiento", "Esta función aún no está disponible.")

def mostrar_menu_principal():
    """Muestra el menú principal sin crear una ventana adicional."""
    menu_principal = tk.Tk()  # Usa Toplevel en lugar de Tk para evitar ventanas extra
    menu_principal.title("SGP // ERP - Menú Principal")
    menu_principal.geometry("400x550")

    # Título
    tk.Label(menu_principal, text="Menú Principal", font=("Arial", 14)).pack(pady=10)

    # Botones con funcionalidad de mensaje
    tk.Button(menu_principal, text="Nuevo Pedido", command=nuevo_pedido.crear_pedido, width=25).pack(pady=5)
    tk.Button(menu_principal, text="Pedidos Generados", command=pedidos.listar_pedidos, width=25).pack(pady=5)
    tk.Button(menu_principal, text="Clientes", command=clientes.listar_clientes, width=25).pack(pady=5)
    tk.Button(menu_principal, text="Listado de Productos", command=productos.listar_productos, width=25).pack(pady=5)

    # Botón para salir
    tk.Button(menu_principal, text="Salir", command=menu_principal.destroy, width=25, fg="red").pack(pady=10)

    menu_principal.mainloop()