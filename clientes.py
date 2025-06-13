import tkinter as tk
from tkinter import ttk, messagebox
import datetime
from reportlab.pdfgen import canvas

productos = [
    {"nombre": "Detergente Líquido", "descripcion": "Detergente para ropa, 1L", "precio": 3000.00, "stock": 50},
    {"nombre": "Lavandina", "descripcion": "Lavandina concentrada, 1L", "precio": 4000.00, "stock": 75},
    {"nombre": "Limpiador Multiuso", "descripcion": "Limpiador para superficies, 500ml", "precio": 1500.00, "stock": 100},
    {"nombre": "Esponjas", "descripcion": "Paquete x 5 unidades", "precio": 2000.00, "stock": 200},
    {"nombre": "Guantes de Látex", "descripcion": "Talla M, paquete x 10", "precio": 1500.00, "stock": 40},
    {"nombre": "Desinfectante", "descripcion": "Desinfectante en spray, 600ml", "precio": 3000.00, "stock": 60},
    {"nombre": "Jabón Líquido", "descripcion": "Jabón para manos, 250ml", "precio": 5000.00, "stock": 80},
]

carrito = []

def actualizar_tablas():
    for i in tree_productos.get_children():
        tree_productos.delete(i)
    for prod in productos:
        tree_productos.insert("", tk.END, values=(
            prod["nombre"], prod["descripcion"], f"{prod['precio']:.2f}", prod["stock"]
        ))

    for i in tree_carrito.get_children():
        tree_carrito.delete(i)

    total = 0
    for item in carrito:
        tree_carrito.insert("", tk.END, values=(
            item["producto"], item["cantidad"], f"{item['precio']:.2f}", f"{item['subtotal']:.2f}"
        ))
        total += item["subtotal"]

    label_total.config(text=f"${total:.2f}")

def agregar_al_carrito():
    seleccionado = tree_productos.focus()
    if not seleccionado:
        messagebox.showwarning("Atención", "Por favor, seleccioná un producto.")
        return

    valores = tree_productos.item(seleccionado, 'values')
    nombre_producto = valores[0]
    stock_disponible = int(valores[3])
    precio_unitario = float(valores[2])

    cantidad_texto = entry_cantidad.get()
    if not cantidad_texto.isdigit() or int(cantidad_texto) <= 0:
        messagebox.showwarning("Atención", "Ingresá una cantidad válida.")
        return
    cantidad = int(cantidad_texto)

    if cantidad > stock_disponible:
        messagebox.showerror("Error", f"No hay suficiente stock para {nombre_producto}.")
        return

    for item in carrito:
        if item["producto"] == nombre_producto:
            nueva_cantidad = item["cantidad"] + cantidad
            if nueva_cantidad > stock_disponible:
                messagebox.showerror("Error", f"No hay suficiente stock.")
                return
            item["cantidad"] = nueva_cantidad
            item["subtotal"] = item["cantidad"] * precio_unitario
            break
    else:
        carrito.append({
            "producto": nombre_producto,
            "cantidad": cantidad,
            "precio": precio_unitario,
            "subtotal": cantidad * precio_unitario
        })

    for prod in productos:
        if prod["nombre"] == nombre_producto:
            prod["stock"] -= cantidad

    actualizar_tablas()
    entry_cantidad.delete(0, tk.END)

def vaciar_carrito():
    for item in carrito:
        for prod in productos:
            if prod["nombre"] == item["producto"]:
                prod["stock"] += item["cantidad"]
    carrito.clear()
    actualizar_tablas()

def finalizar_compra():
    if not carrito:
        messagebox.showwarning("Carrito vacío", "Agregá productos antes de finalizar la compra.")
        return

    try:
        ahora = datetime.datetime.now()
        with open("compras.txt", "a", encoding="utf-8") as f:
            f.write(f"Compra realizada el {ahora.strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write("-" * 50 + "\n")
            total = 0
            for item in carrito:
                f.write(f"{item['producto']}: {item['cantidad']} x ${item['precio']:.2f} = ${item['subtotal']:.2f}\n")
                total += item["subtotal"]
            f.write(f"Total: ${total:.2f}\n")
            f.write("=" * 50 + "\n\n")
        messagebox.showinfo("Compra Finalizada", "La compra se guardó en 'compras.txt'.")
        carrito.clear()
        actualizar_tablas()
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo guardar la compra:\n{e}")

# Interfaz principal
root = tk.Tk()
root.title("Distribuidora de Productos de Limpieza")
root.geometry("950x550")

# Tabla de productos
columnas = ("Nombre", "Descripción", "Precio ($)", "Stock")
tree_productos = ttk.Treeview(root, columns=columnas, show='headings', height=10)
for col in columnas:
    tree_productos.heading(col, text=col)
    tree_productos.column(col, width=150 if col != "Descripción" else 300, anchor='center')
tree_productos.grid(row=0, column=0, columnspan=4, padx=10, pady=10)

# Entrada de cantidad
tk.Label(root, text="Cantidad:", font=("Arial", 12)).grid(row=1, column=0, sticky="e", padx=10)
entry_cantidad = tk.Entry(root, font=("Arial", 12), width=10)
entry_cantidad.grid(row=1, column=1, sticky="w")

# Botón agregar
tk.Button(root, text="Agregar al carrito", font=("Arial", 12), bg="#4caf50", fg="white",
          command=agregar_al_carrito).grid(row=1, column=2, sticky="w", padx=10)

# Tabla carrito
columnas_carrito = ("Producto", "Cantidad", "Precio Unitario ($)", "Subtotal ($)")
tree_carrito = ttk.Treeview(root, columns=columnas_carrito, show='headings', height=10)
for col in columnas_carrito:
    tree_carrito.heading(col, text=col)
    tree_carrito.column(col, width=150, anchor='center')
tree_carrito.grid(row=2, column=0, columnspan=4, padx=10, pady=10)

# Total
tk.Label(root, text="Total:", font=("Arial", 14, "bold")).grid(row=3, column=0, sticky="e", padx=10)
label_total = tk.Label(root, text="$0.00", font=("Arial", 14, "bold"))
label_total.grid(row=3, column=1, sticky="w")

# Botón vaciar
tk.Button(root, text="Vaciar carrito", font=("Arial", 12), bg="#b71c1c", fg="white",
          command=vaciar_carrito).grid(row=3, column=2, sticky="w", padx=10)

# Botón finalizar compra
tk.Button(root, text="Finalizar compra", font=("Arial", 12), bg="#2196f3", fg="white",
          command=finalizar_compra).grid(row=3, column=3, sticky="w", padx=10)

actualizar_tablas()
root.mainloop()

def guardar_como_pdf(nombre_archivo_txt, nombre_archivo_pdf):
    # Leer contenido del txt
    with open(nombre_archivo_txt, "r", encoding="utf-8") as archivo:
        lineas = archivo.readlines()

    # Crear el PDF
    c = canvas.Canvas(nombre_archivo_pdf)
    y = 800

    for linea in lineas:
        c.drawString(100, y, linea.strip())
        y -= 20 

    c.save()

guardar_como_pdf("compras.txt", "compras.pdf")