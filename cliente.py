import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import datetime
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
import os

import json
# Cargar productos desde un archivo JSON
with open("productos.json", "r", encoding="utf-8") as f:
    productos = json.load(f)

carrito = []

# Funciones
def actualizar_listboxes():
    listbox_productos.delete(0, tk.END)
    for p in productos:
        texto = f"{p['nombre']} - ${p['precio']:.2f} - Stock: {p['stock']}"
        listbox_productos.insert(tk.END, texto)

    listbox_carrito.delete(0, tk.END)
    total = 0
    for item in carrito:
        texto = f"{item['producto']} x{item['cantidad']} = ${item['subtotal']:.2f}"
        listbox_carrito.insert(tk.END, texto)
        total += item['subtotal']
    label_total.config(text=f"Total: ${total:.2f}")

def agregar_al_carrito():
    seleccion = listbox_productos.curselection()
    if not seleccion:
        messagebox.showwarning("Atención", "Seleccioná un producto.")
        return

    indice = seleccion[0]
    producto = productos[indice]
    try:
        cantidad = int(entry_cantidad.get())
        if cantidad <= 0:
            raise ValueError
    except ValueError:
        messagebox.showwarning("Atención", "Ingresá una cantidad válida.")
        return

    if cantidad > producto['stock']:
        messagebox.showerror("Error", "No hay suficiente stock.")
        return

    for item in carrito:
        if item['producto'] == producto['nombre']:
            if item['cantidad'] + cantidad > producto['stock']:
                messagebox.showerror("Error", "No hay suficiente stock.")
                return
            item['cantidad'] += cantidad
            item['subtotal'] = item['cantidad'] * producto['precio']
            break
    else:
        carrito.append({
            "producto": producto['nombre'],
            "cantidad": cantidad,
            "precio": producto['precio'],
            "subtotal": cantidad * producto['precio']
        })

    producto['stock'] -= cantidad
    entry_cantidad.delete(0, tk.END)
    actualizar_listboxes()

def vaciar_carrito():
    for item in carrito:
        for p in productos:
            if p['nombre'] == item['producto']:
                p['stock'] += item['cantidad']
    carrito.clear()
    actualizar_listboxes()

def guardar_txt(nombre, envio, direccion, pago):
    ahora = datetime.datetime.now()
    with open("compras.txt", "a", encoding="utf-8") as f:
        f.write(f"Compra realizada el {ahora.strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"Cliente: {nombre}\n")
        f.write(f"Modalidad: {envio}\n")
        f.write(f"Método de Pago: {pago}\n")
        if envio == "Envío":
            f.write(f"Dirección: {direccion}\n")
        f.write("-" * 40 + "\n")
        total = 0
        for item in carrito:
            f.write(f"{item['producto']}: {item['cantidad']} x ${item['precio']:.2f} = ${item['subtotal']:.2f}\n")
            total += item['subtotal']
        f.write(f"Total: ${total:.2f}\n")
        f.write("=" * 40 + "\n\n")
    return ahora

def generar_historial_pdf(nombre_pdf="compras.pdf"):
    try:
        with open("compras.txt", "r", encoding="utf-8") as f:
            lineas = f.readlines()

        c = canvas.Canvas(nombre_pdf, pagesize=letter)
        ancho, alto = letter
        c.setFont("Helvetica", 10)
        y = alto - 40

        for linea in lineas:
            if y < 40:
                c.showPage()
                c.setFont("Helvetica", 10)
                y = alto - 40
            c.drawString(50, y, linea.strip())
            y -= 12

        c.save()
        print(f"Historial PDF guardado como {nombre_pdf}")

    except Exception as e:
        messagebox.showerror("Error", "No se pudo generar el historial PDF")

def generar_pdf(fecha):
    filename = f"ticket_{fecha.strftime('%Y%m%d_%H%M%S')}.pdf"
    c = canvas.Canvas(filename, pagesize=letter)
    ancho, alto = letter
    c.setFont("Helvetica-Bold", 16)
    c.drawString(50, alto - 50, "Ticket de Compra")
    y = alto - 80
    c.setFont("Helvetica", 12)

    with open("compras.txt", "r", encoding="utf-8") as f:
        lineas = f.readlines()

    fecha_str = fecha.strftime('%Y-%m-%d %H:%M:%S')
    inicio = None
    fin = None
    for i, linea in enumerate(lineas):
        if f"Compra realizada el {fecha_str}" in linea:
            inicio = i
        if inicio is not None and linea.startswith("="*40):
            fin = i
            break

    if inicio is not None and fin is not None:
        y_pos = y
        for linea in lineas[inicio:fin+1]:
            c.drawString(50, y_pos, linea.strip())
            y_pos -= 15
            if y_pos < 50:
                c.showPage()
                y_pos = alto - 50
    else:
        c.drawString(50, y, "No se encontró la compra en el archivo.")
    c.save()
    abrir_pdf = filename
    os.startfile(abrir_pdf)
    return filename

def mostrar_datos_transferencia():
    messagebox.showinfo(
        "Datos para Transferencia",
        "CVU:  0000003100023438941073\nAlias: maxirep.mp"
    )

def finalizar_compra():
    nombre = entry_nombre.get().strip()
    if not nombre:
        messagebox.showwarning("Atención", "Ingresá nombre y apellido.")
        return
    envio = envio_var.get()
    if envio not in ("Envío", "Retiro en local"):
        messagebox.showwarning("Atención", "Seleccioná modalidad de entrega.")
        return
    pago = pago_var.get()
    if pago not in ("Efectivo", "Transferencia"):
        messagebox.showwarning("Atención", "Seleccioná un método de pago.")
        return
    direccion = entry_direccion.get().strip()
    if envio == "Envío" and not direccion:
        messagebox.showwarning("Atención", "Ingresá la dirección para el envío.")
        return
    if not carrito:
        messagebox.showwarning("Carrito vacío", "Agregá productos antes de finalizar la compra.")
        return
    try:
        fecha = guardar_txt(nombre, envio, direccion, pago)
        pdf_file = generar_pdf(fecha)
        generar_historial_pdf()
        messagebox.showinfo("Compra Finalizada", f"Compra guardada y PDF generado:\n{pdf_file}")
        carrito.clear()
        actualizar_listboxes()
        entry_nombre.delete(0, tk.END)
        envio_var.set(None)
        entry_direccion.delete(0, tk.END)
        pago_var.set(None)
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo guardar la compra o generar PDF:\n{e}")

# ------------------------ Interfaz Gráfica ------------------------
root = tk.Tk()
root.title("Distribuidora de Productos de Limpieza")
root.geometry("820x600")
root.configure(bg="#adadad") # Fondo gris claro

# Ícono de la ventana
if os.path.exists("Logo-DL.ico"):
    root.iconbitmap("Logo-DL.ico")

# Logo
if os.path.exists("Logo_DL.png"):
    logo_img = Image.open("Logo_DL.png")
    logo_img = logo_img.resize((80, 80))
    logo_tk = ImageTk.PhotoImage(logo_img)
    tk.Label(root, image=logo_tk, bg="#adadad").grid(row=0, column=3, rowspan=3, sticky="ne", padx=10, pady=10)

# Campos y etiquetas
estilo_lbl = {"bg": "#adadad", "fg": "black"}
tk.Label(root, text="Nombre y Apellido:", **estilo_lbl).grid(row=0, column=0, padx=10, pady=5, sticky="e")
entry_nombre = tk.Entry(root, width=30)
entry_nombre.grid(row=0, column=1, pady=5, sticky="w")

envio_var = tk.StringVar()
tk.Label(root, text="Modalidad de entrega:", **estilo_lbl).grid(row=1, column=0, padx=10, sticky="e")
tk.Radiobutton(root, text="Envío", variable=envio_var, value="Envío", bg="#adadad", fg="black").grid(row=1, column=1, sticky="w")
tk.Radiobutton(root, text="Retiro en local", variable=envio_var, value="Retiro en local", bg="#adadad", fg="black").grid(row=1, column=2, sticky="w")

tk.Label(root, text="Dirección (si es envío):", **estilo_lbl).grid(row=2, column=0, padx=10, pady=5, sticky="e")
entry_direccion = tk.Entry(root, width=40)
entry_direccion.grid(row=2, column=1, columnspan=2, pady=5, sticky="w")

# Método de pago
pago_var = tk.StringVar()
tk.Label(root, text="Método de pago:", **estilo_lbl).grid(row=3, column=0, padx=10, sticky="e")
tk.Radiobutton(root, text="Efectivo", variable=pago_var, value="Efectivo", bg="#adadad", fg="black").grid(row=3, column=1, sticky="w")
tk.Radiobutton(root, text="Transferencia", variable=pago_var, value="Transferencia", bg="#adadad", fg="black", command=mostrar_datos_transferencia).grid(row=3, column=2, sticky="w")

tk.Label(root, text="Productos", **estilo_lbl).grid(row=4, column=0, padx=10)
tk.Label(root, text="Carrito", **estilo_lbl).grid(row=4, column=2, padx=10)

listbox_productos = tk.Listbox(root, width=40, height=15)
listbox_productos.grid(row=5, column=0, padx=10, pady=5)

listbox_carrito = tk.Listbox(root, width=40, height=15)
listbox_carrito.grid(row=5, column=2, padx=10, pady=5)

tk.Label(root, text="Cantidad:", **estilo_lbl).grid(row=6, column=0, sticky="e", padx=10)
entry_cantidad = tk.Entry(root, width=10)
entry_cantidad.grid(row=6, column=1, sticky="w")

tk.Button(root, text="Agregar al carrito", bg="#c2e798", fg="black", command=agregar_al_carrito).grid(row=6, column=2, sticky="w", padx=10)
tk.Button(root, text="Vaciar carrito", bg="#ff5a5d", fg="black", command=vaciar_carrito).grid(row=7, column=0, pady=10, padx=10)
label_total = tk.Label(root, text="Total: $0.00", font=("Arial", 14, "bold"), fg="black")
label_total.grid(row=7, column=1, sticky="w")
tk.Button(root, text="Finalizar compra", bg="#9dd8ff", fg="black", command=finalizar_compra).grid(row=7, column=2, pady=10, padx=10)

# Iniciar
actualizar_listboxes()
root.mainloop()
