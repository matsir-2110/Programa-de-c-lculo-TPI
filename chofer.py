import tkinter as tk
from tkinter import messagebox
from openrouteservice import Client
import folium
import webbrowser
import os

# API Key de OpenRouteService
API_KEY = "5b3ce3597851110001cf624816dd98becc4e4cce880a6c473c5ba5d3"
client = Client(key=API_KEY)

# Coordenadas de Distribuidora Luicho
origen_coords = (-27.48857029818254, -58.761975598687)

# Destinos disponibles
DESTINOS = {
    "Puerto de Rosario": (-32.971816715054906, -60.6203869954716),
    "Empedrado": (-27.950793, -58.800928),
    "San Lorenzo": (-28.137027, -58.766337),
    "Saladas": (-28.257450, -58.623873),
    "Mburucuya": (-28.047187, -58.224567),
    "Caa Cati": (-27.751661, -57.621642),
    "San Miguel": (-27.998588, -57.591753),
    "Itaibate": (-27.426549, -57.337789),
    "Itati": (-27.269164, -58.243407),
    "Paso de la Patria": (-27.316371, -58.568572),
    "Paso de los Libres": (-29.714733, -57.102357),
}

def calcular():
    destino_nombre = destino_var.get()
    destino_coords = DESTINOS.get(destino_nombre)

    if not destino_coords:
        messagebox.showerror("Error", "Seleccione un destino válido.")
        return

    try:
        ruta = client.directions(
            coordinates=[origen_coords[::-1], destino_coords[::-1]],
            profile='driving-car',
            format='geojson'
        )
        distancia_km = ruta['features'][0]['properties']['segments'][0]['distance'] / 1000
        duracion_min = ruta['features'][0]['properties']['segments'][0]['duration'] / 60
    except Exception as e:
        print("Error al calcular ruta:", e)
        messagebox.showerror("Error", "No se pudo calcular la ruta.")
        return

    resumen = f"Destino: {destino_nombre}\nDistancia: {distancia_km:.2f} km\nDuración: {duracion_min:.2f} minutos"
    messagebox.showinfo("Resumen de Ruta", resumen)

    mapa = folium.Map(location=origen_coords, zoom_start=6)
    folium.Marker(location=origen_coords, tooltip="Distribuidora Luicho").add_to(mapa)
    folium.Marker(location=destino_coords, tooltip=f"Destino - {destino_nombre}").add_to(mapa)
    folium.GeoJson(ruta).add_to(mapa)
    nombre_mapa = "mapa_ruta.html"
    mapa.save(nombre_mapa)
    webbrowser.open(nombre_mapa)

# --- INTERFAZ ELEGANTE OSCURA ---
ventana = tk.Tk()
ventana.title("Simulador Logístico")
ventana.geometry("500x300")
ventana.configure(bg="#1e1e1e")

# Estilos
etiqueta_color = "#ffffff"
boton_bg = "#2d2d2d"
boton_fg = "#ffffff"
menu_bg = "#2d2d2d"
menu_fg = "#ffffff"
fuente = ("Segoe UI", 12)

#Botón para mostrar pedidos
def mostrar_pedidos():
    messagebox.showinfo("Pedidos", "Mostrando los pedidos diarios")
    abrir_pdf = "compras.pdf"
    try:
        os.startfile(abrir_pdf)
    except Exception as e:
        messagebox.showerror("Error", "No se pudo abrir el archivo PDF")

bot_pedidos = tk.Button(ventana,
                        text="Mostrar Pedidos",
                        font=("Segoe UI", 15, "bold"),
                        command=mostrar_pedidos)
bot_pedidos.pack(pady=10)

# Etiquetas
tk.Label(ventana, text="Seleccione destino:", font=fuente, bg="#1e1e1e", fg=etiqueta_color).pack(pady=10, padx=10)

# Menú de selección
destino_var = tk.StringVar()
destino_var.set("Puerto de Rosario")
opciones = list(DESTINOS.keys())
menu = tk.OptionMenu(ventana, destino_var, *opciones)
menu.config(bg=menu_bg, fg=menu_fg, font=fuente, highlightthickness=0, activebackground="#444")
menu["menu"].config(bg=menu_bg, fg=menu_fg)
menu.pack(padx=10)

# Botón
boton = tk.Button(ventana, text="Calcular Ruta", command=calcular, bg=boton_bg, fg=boton_fg, font=fuente)
boton.pack(pady=20)

ventana.mainloop()
