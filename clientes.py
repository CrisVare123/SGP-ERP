import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import database

ARCHIVO_CLIENTES = "clientes.json"

def listar_clientes():
    """Muestra la lista de clientes con mejor diseño."""
    clientes = database.cargar_datos(ARCHIVO_CLIENTES)

    ventana = tk.Toplevel()
    ventana.title("Listado de Clientes")
    ventana.geometry("650x450")

    tk.Label(ventana, text="Lista de Clientes", font=("Arial", 14)).pack(pady=10)

    # Crear tabla con scrollbar
    frame = tk.Frame(ventana)
    frame.pack(pady=5, fill="both", expand=True)

    tabla = ttk.Treeview(frame, columns=("ID", "Nombre", "Dirección", "Teléfono", "Email"), show="headings")
    tabla.heading("ID", text="ID")
    tabla.heading("Nombre", text="Nombre")
    tabla.heading("Dirección", text="Dirección")
    tabla.heading("Teléfono", text="Teléfono")
    tabla.heading("Email", text="Email")

    tabla.column("ID", width=30, anchor="center")
    tabla.column("Nombre", width=120)
    tabla.column("Dirección", width=120)
    tabla.column("Teléfono", width=80, anchor="center")
    tabla.column("Email", width=120)

    scrollbar = ttk.Scrollbar(frame, orient="vertical", command=tabla.yview)
    tabla.configure(yscroll=scrollbar.set)

    scrollbar.pack(side="right", fill="y")
    tabla.pack(fill="both", expand=True)

    for cliente in clientes:
        tabla.insert("", "end", values=(cliente["id"], cliente["nombre"], cliente["direccion"], cliente["telefono"], cliente["email"]))

    # Botones
    tk.Button(ventana, text="Agregar Cliente", command=agregar_cliente, width=20).pack(pady=5)
    tk.Button(ventana, text="Eliminar Cliente", command=eliminar_cliente, width=20).pack(pady=5)

def agregar_cliente():
    """Permite agregar un nuevo cliente."""
    clientes = database.cargar_datos(ARCHIVO_CLIENTES)

    nombre = simpledialog.askstring("Nuevo Cliente", "Nombre:")
    direccion = simpledialog.askstring("Nuevo Cliente", "Dirección:")
    telefono = simpledialog.askstring("Nuevo Cliente", "Teléfono:")
    email = simpledialog.askstring("Nuevo Cliente", "Email:")

    if nombre and direccion and telefono and email:
        nuevo_id = max([c["id"] for c in clientes], default=0) + 1
        clientes.append({"id": nuevo_id, "nombre": nombre, "direccion": direccion, "telefono": telefono, "email": email})
        database.guardar_datos(ARCHIVO_CLIENTES, clientes)
        messagebox.showinfo("Éxito", "Cliente agregado.")
    else:
        messagebox.showerror("Error", "Todos los campos son obligatorios.")

def eliminar_cliente():
    """Permite eliminar un cliente."""
    clientes = database.cargar_datos(ARCHIVO_CLIENTES)
    id_cliente = simpledialog.askinteger("Eliminar Cliente", "Ingrese ID del cliente:")

    clientes = [c for c in clientes if c["id"] != id_cliente]
    database.guardar_datos(ARCHIVO_CLIENTES, clientes)
    messagebox.showinfo("Éxito", "Cliente eliminado.")