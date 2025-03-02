import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import database

ARCHIVO_CLIENTES = "clientes.json"
ARCHIVO_PRODUCTOS = "productos.json"
ARCHIVO_PEDIDOS = "pedidos.json"

def crear_pedido():
    """Interfaz mejorada para generar un pedido con filtros de productos."""
    datos_clientes = database.cargar_datos(ARCHIVO_CLIENTES)
    datos_productos = database.cargar_datos(ARCHIVO_PRODUCTOS)
    pedidos = database.cargar_datos(ARCHIVO_PEDIDOS)

    if not datos_clientes:
        messagebox.showerror("Error", "No hay clientes registrados.")
        return

    if not datos_productos:
        messagebox.showerror("Error", "No hay productos disponibles.")
        return

    ventana = tk.Toplevel()
    ventana.title("Nuevo Pedido")
    ventana.geometry("400x750")

    tk.Label(ventana, text="Generar Nuevo Pedido", font=("Arial", 14)).pack(pady=10)

    frame = tk.Frame(ventana)
    frame.pack(pady=5, fill="both", expand=True)

    # Selección de Cliente
    tk.Label(frame, text="Seleccionar Cliente:", font=("Arial", 10, "bold")).grid(row=0, column=0, padx=5, pady=5, sticky="w")
    clientes_nombres = [f"{c['id']} - {c['nombre']}" for c in datos_clientes]
    combo_clientes = ttk.Combobox(frame, values=clientes_nombres, state="readonly", width=35)
    combo_clientes.grid(row=0, column=1, padx=5, pady=5)

    # Filtrar por Categoría
    tk.Label(frame, text="Filtrar por Categoría:", font=("Arial", 10, "bold")).grid(row=1, column=0, padx=5, pady=5, sticky="w")
    categorias = sorted(set(p["categoria"] for p in datos_productos))
    combo_categorias = ttk.Combobox(frame, values=categorias, state="readonly", width=20)
    combo_categorias.grid(row=1, column=1, padx=5, pady=5, sticky="w")

    # Filtrar por Proveedor
    tk.Label(frame, text="Filtrar por Proveedor:", font=("Arial", 10, "bold")).grid(row=2, column=0, padx=5, pady=5, sticky="w")
    proveedores = sorted(set(p["proveedor"] for p in datos_productos))
    combo_proveedores = ttk.Combobox(frame, values=proveedores, state="readonly", width=20)
    combo_proveedores.grid(row=2, column=1, padx=5, pady=5, sticky="w")

    # Selección de Producto
    tk.Label(frame, text="Seleccionar Producto:", font=("Arial", 10, "bold")).grid(row=3, column=0, padx=5, pady=5, sticky="w")
    combo_productos = ttk.Combobox(frame, state="readonly", width=35)
    combo_productos.grid(row=3, column=1, padx=5, pady=5)

    # Función para actualizar productos según filtro
    def actualizar_productos():
        categoria = combo_categorias.get()
        proveedor = combo_proveedores.get()

        productos_filtrados = [
            f"{p['sku']} - {p['nombre']} (Stock: {p['stock']})"
            for p in datos_productos
            if (categoria == "" or p["categoria"] == categoria) and (proveedor == "" or p["proveedor"] == proveedor)
        ]
        
        combo_productos["values"] = productos_filtrados
        combo_productos.set("")  # Limpiar selección

    combo_categorias.bind("<<ComboboxSelected>>", lambda _: actualizar_productos())
    combo_proveedores.bind("<<ComboboxSelected>>", lambda _: actualizar_productos())

    # Cantidad
    tk.Label(frame, text="Cantidad:", font=("Arial", 10, "bold")).grid(row=4, column=0, padx=5, pady=5, sticky="w")
    entry_cantidad = tk.Entry(frame, width=10)
    entry_cantidad.grid(row=4, column=1, padx=5, pady=5, sticky="w")

    # Tabla de Productos Agregados
    tk.Label(ventana, text="Productos en el Pedido:", font=("Arial", 10, "bold")).pack(pady=5)
    frame_tabla = tk.Frame(ventana)
    frame_tabla.pack(fill="both", expand=True)

    tabla = ttk.Treeview(frame_tabla, columns=("Producto", "Cantidad", "Precio", "Subtotal"), show="headings")
    tabla.heading("Producto", text="Producto")
    tabla.heading("Cantidad", text="Cantidad")
    tabla.heading("Precio", text="Precio")
    tabla.heading("Subtotal", text="Subtotal")

    scrollbar = ttk.Scrollbar(frame_tabla, orient="vertical", command=tabla.yview)
    tabla.configure(yscroll=scrollbar.set)

    scrollbar.pack(side="right", fill="y")
    tabla.pack(fill="both", expand=True)

    items_pedido = []

    # Función para agregar producto al pedido
    def agregar_producto():
        producto_seleccionado = combo_productos.get()
        cantidad = entry_cantidad.get()

        if not producto_seleccionado or not cantidad:
            messagebox.showerror("Error", "Todos los campos son obligatorios.")
            return

        cantidad = int(cantidad)
        sku_producto = producto_seleccionado.split(" - ")[0]
        producto = next(p for p in datos_productos if p["sku"] == sku_producto)

        if cantidad > producto["stock"]:
            messagebox.showerror("Error", f"Stock insuficiente. Disponible: {producto['stock']}")
            return

        subtotal = cantidad * producto["precio"]
        items_pedido.append({"producto": producto["nombre"], "cantidad": cantidad, "precio_unitario": producto["precio"], "subtotal": subtotal})
        
        tabla.insert("", "end", values=(producto["nombre"], cantidad, f"${producto['precio']}", f"${subtotal}"))
        
        producto["stock"] -= cantidad
        calcular_total()

    # Función para calcular total
    def calcular_total():
        total_pedido = sum(item["subtotal"] for item in items_pedido)
        label_total.config(text=f"Total: ${total_pedido:.2f}")

    # IVA
    tk.Label(ventana, text="IVA (%):", font=("Arial", 10, "bold")).pack(pady=5)
    combo_iva = ttk.Combobox(ventana, values=["0", "10.5", "21", "Otro"], state="readonly", width=10)
    combo_iva.pack()

    # Mostrar Total
    label_total = tk.Label(ventana, text="Total: $0.00", font=("Arial", 12, "bold"), fg="blue")
    label_total.pack(pady=10)

    # Función para guardar pedido
    def guardar_pedido():
        cliente_seleccionado = combo_clientes.get()
        iva = combo_iva.get()

        if not cliente_seleccionado or not items_pedido or not iva:
            messagebox.showerror("Error", "Todos los campos son obligatorios.")
            return

        iva = float(iva) if iva != "Otro" else float(simpledialog.askstring("IVA", "Ingrese porcentaje de IVA:"))
        subtotal_pedido = sum(item["subtotal"] for item in items_pedido)
        total_pedido = subtotal_pedido + (subtotal_pedido * (iva / 100))

        nuevo_pedido = {
            "id": len(pedidos) + 1,
            "cliente": cliente_seleccionado.split(" - ")[1],
            "items": items_pedido,
            "iva": iva,
            "total": round(total_pedido, 2)
        }

        pedidos.append(nuevo_pedido)
        database.guardar_datos(ARCHIVO_PEDIDOS, pedidos)
        database.guardar_datos(ARCHIVO_PRODUCTOS, datos_productos)

        messagebox.showinfo("Éxito", "Pedido registrado correctamente.")
        ventana.destroy()

    tk.Button(ventana, text="Agregar Producto", command=agregar_producto, width=25).pack(pady=5)
    tk.Button(ventana, text="Confirmar Pedido", command=guardar_pedido, width=25, bg="green", fg="white").pack(pady=5)

    ventana.mainloop()