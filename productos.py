import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import database

ARCHIVO_PRODUCTOS = "productos.json"

def listar_productos():
    """Muestra la lista de productos con mejor diseño."""
    productos = database.cargar_datos(ARCHIVO_PRODUCTOS)

    ventana = tk.Toplevel()
    ventana.title("Listado de Productos")
    ventana.geometry("650x450")

    tk.Label(ventana, text="Lista de Productos", font=("Arial", 14)).pack(pady=10)

    frame = tk.Frame(ventana)
    frame.pack(pady=5, fill="both", expand=True)

    tabla = ttk.Treeview(frame, columns=("SKU", "Nombre", "Categoría", "Precio", "Stock", "Proveedor"), show="headings")
    tabla.heading("SKU", text="SKU")
    tabla.heading("Nombre", text="Nombre")
    tabla.heading("Categoría", text="Categoría")
    tabla.heading("Precio", text="Precio")
    tabla.heading("Stock", text="Stock")
    tabla.heading("Proveedor", text="Proveedor")

    tabla.column("SKU", width=50)
    tabla.column("Nombre", width=100)
    tabla.column("Categoría", width=80)
    tabla.column("Precio", width=60, anchor="center")
    tabla.column("Stock", width=60, anchor="center")
    tabla.column("Proveedor", width=80)

    scrollbar = ttk.Scrollbar(frame, orient="vertical", command=tabla.yview)
    tabla.configure(yscroll=scrollbar.set)

    scrollbar.pack(side="right", fill="y")
    tabla.pack(fill="both", expand=True)

    for producto in productos:
        tabla.insert("", "end", values=(producto["sku"], producto["nombre"], producto["categoria"], f"${producto['precio']}", producto["stock"], producto["proveedor"]))

    tk.Button(ventana, text="Agregar Producto", command=agregar_producto, width=20).pack(pady=5)
    tk.Button(ventana, text="Modificar Stock", command=modificar_stock, width=20).pack(pady=5)
    tk.Button(ventana, text="Eliminar Producto", command=eliminar_producto, width=20).pack(pady=5)