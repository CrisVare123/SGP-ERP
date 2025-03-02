import tkinter as tk
from tkinter import ttk, messagebox
import database

ARCHIVO_PEDIDOS = "pedidos.json"

def listar_pedidos():
    """Muestra los pedidos generados con opción de ver detalles."""
    pedidos = database.cargar_datos(ARCHIVO_PEDIDOS)

    ventana = tk.Toplevel()
    ventana.title("Pedidos Generados")
    ventana.geometry("400x550")

    tk.Label(ventana, text="Lista de Pedidos", font=("Arial", 14)).pack(pady=10)

    frame_tabla = tk.Frame(ventana)
    frame_tabla.pack(fill="both", expand=True)

    tabla = ttk.Treeview(frame_tabla, columns=("ID", "Cliente", "Total"), show="headings")
    tabla.heading("ID", text="ID")
    tabla.heading("Cliente", text="Cliente")
    tabla.heading("Total", text="Total")

    tabla.column("ID", width=40, anchor="center")
    tabla.column("Cliente", width=200)
    tabla.column("Total", width=80, anchor="center")

    scrollbar = ttk.Scrollbar(frame_tabla, orient="vertical", command=tabla.yview)
    tabla.configure(yscroll=scrollbar.set)
    scrollbar.pack(side="right", fill="y")
    tabla.pack(fill="both", expand=True)

    if not pedidos:
        tk.Label(ventana, text="No hay pedidos registrados.", fg="red").pack()
        return

    for pedido in pedidos:
        tabla.insert("", "end", values=(pedido["id"], pedido["cliente"], f"${pedido['total']}"))

    def mostrar_detalle():
        """Muestra el detalle de un pedido seleccionado."""
        seleccion = tabla.selection()
        if not seleccion:
            messagebox.showerror("Error", "Seleccione un pedido para ver detalles.")
            return

        pedido_id = int(tabla.item(seleccion[0], "values")[0])
        pedido = next(p for p in pedidos if p["id"] == pedido_id)

        detalle_ventana = tk.Toplevel()
        detalle_ventana.title(f"Detalle del Pedido #{pedido['id']}")
        detalle_ventana.geometry("400x400")

        tk.Label(detalle_ventana, text=f"Cliente: {pedido['cliente']}", font=("Arial", 12, "bold")).pack(pady=5)
        tk.Label(detalle_ventana, text=f"IVA aplicado: {pedido['iva']}%", font=("Arial", 10)).pack(pady=2)

        frame_detalle = tk.Frame(detalle_ventana)
        frame_detalle.pack(pady=5, fill="both", expand=True)

        tabla_detalle = ttk.Treeview(frame_detalle, columns=("Producto", "Cantidad", "Precio", "Subtotal"), show="headings")
        tabla_detalle.heading("Producto", text="Producto")
        tabla_detalle.heading("Cantidad", text="Cantidad")
        tabla_detalle.heading("Precio", text="Precio")
        tabla_detalle.heading("Subtotal", text="Subtotal")

        tabla_detalle.column("Producto", width=120)
        tabla_detalle.column("Cantidad", width=60, anchor="center")
        tabla_detalle.column("Precio", width=80, anchor="center")
        tabla_detalle.column("Subtotal", width=80, anchor="center")

        scrollbar_detalle = ttk.Scrollbar(frame_detalle, orient="vertical", command=tabla_detalle.yview)
        tabla_detalle.configure(yscroll=scrollbar_detalle.set)

        scrollbar_detalle.pack(side="right", fill="y")
        tabla_detalle.pack(fill="both", expand=True)

        for item in pedido["items"]:
            tabla_detalle.insert("", "end", values=(item["producto"], item["cantidad"], f"${item['precio_unitario']}", f"${item['subtotal']}"))

        tk.Label(detalle_ventana, text=f"Total con IVA: ${pedido['total']}", font=("Arial", 12, "bold"), fg="blue").pack(pady=10)

    tk.Button(ventana, text="Ver Detalle", command=mostrar_detalle, width=25).pack(pady=10)