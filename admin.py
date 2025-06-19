import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
from openrouteservice import Client
import folium
import os
import json
import webbrowser

#Ventana
ventana = tk.Tk()
ventana.title("Administración")
ventana.geometry("600x750")
ventana.configure(bg="#1e1e1e")

#Logo
imagen = Image.open("Logo_DL.png")
imagen = imagen.resize((70, 70))
imagen_tk = ImageTk.PhotoImage(imagen)
label = tk.Label(image=imagen_tk, bg="#1e1e1e")
label.image = imagen_tk
label.place(relx=1, y=10, anchor="ne")

#Personita usuario
img_usu = Image.open("Perfil-de-Usuario.png")
img_usu = img_usu.resize((70, 70))
img_usu_tk = ImageTk.PhotoImage(img_usu)
label = tk.Label(image=img_usu_tk, bg="#1e1e1e")
label.image = img_usu_tk
label.place(relx=0, y=10, anchor="nw")

bienvenida = tk.Label(ventana, 
                      text="Panel de Administración", 
                      font=("Arial", 20, "bold"), 
                      bg="#2e2e2e",
                      fg="#d4af37")
bienvenida.pack(pady=10)

bot_espacio = tk.Label(ventana, bg="#1e1e1e")
bot_espacio.pack(pady=30)


#...FUNCIONES...
#Función para ver pedidos
def pedidos():
    messagebox.showinfo("Pedidos", "Mostrando los pedidos diarios")
    abrir_pdf = "compras.pdf"
    try:
        os.startfile(abrir_pdf)
    except Exception as e:
        messagebox.showerror("Error", "No se pudo abrir el archivo PDF")

#Función para agregar productos
def productos():
    messagebox.showinfo("Productos", "Apartado para Agregar/Editar productos")
    top_agregar = tk.Toplevel(ventana)
    top_agregar.title("Productos")
    top_agregar.geometry("600x600")
    top_agregar.configure(bg="#1e1e1e")
    label_productos = tk.Label(top_agregar,
                               text="Productos",
                               font=("Segoe UI", 25, "bold"),
                               bg="#4B4BA9",
                               fg="#FFFFFF")
    label_productos.pack(fill="x", pady=15)


    #Función para meter agregar productos a la lista
    def agregar_prod ():
        top2_agregar = tk.Toplevel(top_agregar)
        top2_agregar.title("Agregar Producto/s")
        top2_agregar.geometry("600x600")
        top2_agregar.configure(bg="#121426")
        
        est_label = {"bg": "#466561", "fg": "#000000", "font": ("Segoe UI", 12)}
        est_input = {"bg": "#ffffff", "fg": "#000000", "font": ("Segoe UI", 12), }

        #Nombre
        lab_nom = tk.Label(top2_agregar, text="Nombre del Producto", **est_label)
        lab_nom.pack(pady=10)
        inp_nombre = tk.Entry(top2_agregar, **est_input)
        inp_nombre.pack()
        nom = inp_nombre.get()

        #Descripcion
        lab_des = tk.Label(top2_agregar, text="Descripción", **est_label)
        lab_des.pack(pady=10)
        inp_descripcion = tk.Entry(top2_agregar, **est_input)
        inp_descripcion.pack()
        des = inp_descripcion.get()

        #Precio
        lab_pre = tk.Label(top2_agregar, text="Precio", **est_label)
        lab_pre.pack(pady=10)
        inp_precio = tk.Entry(top2_agregar, **est_input)
        inp_precio.pack()
        pre = inp_precio.get()
        
        #Stock
        lab_sto = tk.Label(top2_agregar, text="Cantidad de Stock", **est_label)
        lab_sto.pack(pady=10)
        inp_stock = tk.Entry(top2_agregar, **est_input)
        inp_stock.pack()
        sto = inp_stock.get()
        
        def guardar_datos():
            try:
                nom = inp_nombre.get()
                des = inp_descripcion.get()
                pre = float(inp_precio.get())
                sto = int(inp_stock.get())

                if not nom or not des:
                    raise ValueError("Faltan campos.")

                nuevo_producto = {
                    "nombre": nom,
                    "descripcion": des,
                    "precio": pre,
                    "stock": sto
                }

                productos.append(nuevo_producto)
                guardar_productos(productos)
                messagebox.showinfo("Producto agregado", "El producto fue agregado y guardado con éxito.")
                top2_agregar.destroy()

            except ValueError:
                messagebox.showerror("Error", "Por favor, completa todos los campos correctamente.")
        
        boton_guardar = tk.Button(top2_agregar, text="Guardar", font=("Segoe UI", 12, "bold"), bg="#4CAF50", fg="#FFFFFF", command=guardar_datos)
        boton_guardar.pack(pady=20)
        
    def modificar_prod():
        top2_modificar = tk.Toplevel(top_agregar)
        top2_modificar.title("Modificar Producto/s")
        top2_modificar.geometry("600x600")
        top2_modificar.configure(bg="#121426")

        est_label = {"bg": "#466561", "fg": "#000000", "font": ("Segoe UI", 12)}
        est_input = {"bg": "#ffffff", "fg": "#000000", "font": ("Segoe UI", 12), }

        #Se tiene que crear una listbox para mostrar los productos
        listbox_productos = tk.Listbox(top2_modificar, **est_input, width=50, height=10)
        listbox_productos.pack(pady=10)
        for p in productos:
            texto = f"{p['nombre']} - ${p['precio']:.2f} - Stock: {p['stock']}"
            listbox_productos.insert(tk.END, texto)
        
         # Campos para modificar
        lab_nom = tk.Label(top2_modificar, text="Nuevo Nombre", **est_label)
        lab_nom.pack()
        inp_nombre = tk.Entry(top2_modificar, **est_input)
        inp_nombre.pack()

        lab_des = tk.Label(top2_modificar, text="Nueva Descripción", **est_label)
        lab_des.pack()
        inp_descripcion = tk.Entry(top2_modificar, **est_input)
        inp_descripcion.pack()

        lab_pre = tk.Label(top2_modificar, text="Nuevo Precio", **est_label)
        lab_pre.pack()
        inp_precio = tk.Entry(top2_modificar, **est_input)
        inp_precio.pack()

        lab_sto = tk.Label(top2_modificar, text="Nuevo Stock", **est_label)
        lab_sto.pack()
        inp_stock = tk.Entry(top2_modificar, **est_input)
        inp_stock.pack()

        # Función para guardar los cambios
        def guardar_cambios():
            seleccion = listbox_productos.curselection()
            if not seleccion:
                messagebox.showwarning("Error", "Seleccioná un producto.")
            i = seleccion[0] 
            try:
                productos[i]["nombre"] = inp_nombre.get()
                productos[i]["descripcion"] = inp_descripcion.get()
                productos[i]["precio"] = float(inp_precio.get())
                productos[i]["stock"] = int(inp_stock.get())
                guardar_productos(productos)
                messagebox.showinfo("Éxito", "Producto modificado correctamente.")
                top2_modificar.destroy()
            except ValueError:
                messagebox.showerror("Error", "Revisá que el precio y stock sean números válidos.")

        # Botón de guardar
        boton_guardar = tk.Button(top2_modificar, text="Guardar Cambios", command=guardar_cambios,
                                font=("Segoe UI", 12, "bold"), bg="#4CAF50", fg="white")
        boton_guardar.pack(pady=20)
        

    bot_agregar_productos = tk.Button(top_agregar,
                                      text="Agregar Producto", 
                                      font=("Segoe UI", 16, "bold"),
                                      width= 20,
                                      height= 2,
                                      bg="#3a3f51", 
                                      fg="#d4af37",
                                      command=agregar_prod)
    bot_agregar_productos.pack(pady=60)


    #Función para cambiar cosas de la lista
    bot_cambiar_productos = tk.Button(top_agregar,
                                      text="Modificar Valores",
                                      font=("Segoe UI", 16, "bold"),
                                      width= 20,
                                      height= 2,
                                      bg="#3a3f51", 
                                      fg="#d4af37",
                                      command=modificar_prod)
    bot_cambiar_productos.pack(pady=20)
    
#Función apartado chofer
def apartado_chofer():
    top_chofer = tk.Toplevel(ventana)
    top_chofer.title("Chofer")
    top_chofer.geometry("600x600")
    top_chofer.configure(bg="#1e1e1e")
    label_chofer = tk.Label(top_chofer,
                               text="Chofer",
                               font=("Segoe UI", 25, "bold"),
                               bg="#4B4BA9",
                               fg="#FFFFFF")
    label_chofer.pack(fill="x", pady=15)

    def caso_averia():
        messagebox.showinfo("Datos Obtenidos del problema", f"...La avería se produce al 70{'%'} del camino (525,7 km aprox)...\n\nEn la localidad mas cercana (Nelson)")
        abrir_pdf = "averia_caso_fisica.pdf"
        os.startfile(abrir_pdf)

        # API Key de OpenRouteService
        API_KEY = "5b3ce3597851110001cf624816dd98becc4e4cce880a6c473c5ba5d3"
        client = Client(key=API_KEY)
        # Coordenadas de Distribuidora Luicho
        origen_coords = (-58.761975598687, -27.48857029818254)
        #Coordenadas del lugar donde ocurre la avería
        destino_coords = (-60.755434, -31.307345) 

        ruta = client.directions(
            coordinates=[origen_coords, destino_coords],
            profile='driving-car',
            format='geojson'
        )
        
        mapa = folium.Map(location=(origen_coords[1],origen_coords[0]), zoom_start=6)
        folium.Marker(location=(origen_coords[1],origen_coords[0]), tooltip="Distribuidora Luicho").add_to(mapa)
        folium.Marker(location=(destino_coords[1],destino_coords[0]), tooltip=f"Nelson").add_to(mapa)
        folium.GeoJson(ruta).add_to(mapa)
        nombre_mapa = "ruta_averia.html"
        mapa.save(nombre_mapa)
        webbrowser.open(nombre_mapa)


    boton_averia = tk.Button(top_chofer,
                            text="Caso Avería Física",
                            font=("Segoe UI", 25, "bold"),
                            bg="#454555",
                            fg="#FFFFFF",
                            command=caso_averia)
    boton_averia.pack(pady=40)


#...BOTONES...
#Botón para ver pedidos
bot_pedidos = tk.Button(ventana, 
                        text="Pedidos diarios", 
                        font=("Segoe UI", 16, "bold"),
                        width= 20,
                        height= 2,
                        bg="#3a3f51", 
                        fg="#d4af37",
                        command=pedidos)
bot_pedidos.pack(pady=30)

#Botón para agregar productos
bot_productos = tk.Button(ventana, 
                                text="Productos", 
                                font=("Segoe UI", 16, "bold"),
                                width= 20,
                                height= 2,
                                bg="#3a3f51", 
                                fg="#d4af37",
                                command=productos)
bot_productos.pack(pady=30)

#Botón para apartado chofer
bot_chofer = tk.Button(ventana,
                        text="Apartado Chofer", 
                        font=("Segoe UI", 16, "bold"),
                        width= 20,
                        height= 2,
                        bg="#3a3f51", 
                        fg="#d4af37",
                        command=apartado_chofer)
bot_chofer.pack(pady=30)

#Abrir json
def cargar_productos():
    with open("productos.json", "r", encoding="utf-8") as f:
        return json.load(f)
productos = cargar_productos()

#Guardar en el json
def guardar_productos(lista):
    with open("productos.json", "w", encoding="utf-8") as f:
        json.dump(lista, f, indent=4, ensure_ascii=False)

ventana.mainloop()