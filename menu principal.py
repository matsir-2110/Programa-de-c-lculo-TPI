import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import subprocess
import os

USUARIOS_FILE = "usuarios.txt"

usuario_chofer = "chofer"
contraseña_chofer = "chof"

usuario_dueño = "Luicho"
contraseña_dueño = "luichos"

def cargar_logo(parent):
    try:
        imagen = Image.open("Logo_DL.png")
        imagen = imagen.resize((60, 60))
        imagen_tk = ImageTk.PhotoImage(imagen)
        label = tk.Label(parent, image=imagen_tk, bg="#1e1e1e")
        label.image = imagen_tk
        label.place(relx=1.0, y=10, anchor="ne")
    except:
        tk.Label(parent, text="Sin logo", bg="#1e1e1e", fg="#d4af37", font=("Segoe UI", 12)).place(relx=1.0, y=10, anchor="ne")

def guardar_usuario_archivo(usuario, contraseña):
    with open(USUARIOS_FILE, "a", encoding="utf-8") as f:
        f.write(f"{usuario},{contraseña}\n")

def validar_usuario(usuario, contraseña):
    if not os.path.exists(USUARIOS_FILE):
        return False
    with open(USUARIOS_FILE, "r") as f:
        for linea in f:
            if "," in linea:
                u, c = linea.strip().split(",", 1)
                if u == usuario and c == contraseña:
                    return True
    return False

#Crear usuario de cliente
def crear_usuario():
    def guardar_usuario():
        u = entry_usuario.get().strip()
        c = entry_contraseña.get()
        c2 = entry_confirmar.get()
        if c != c2:
            messagebox.showerror("Error", "Las contraseñas no coinciden.")
            return
        if not u or not c:
            messagebox.showerror("Error", "Los campos no pueden estar vacíos.")
            return
        # Verificar que usuario no exista
        if os.path.exists(USUARIOS_FILE):
            with open(USUARIOS_FILE, "r") as f:
                for linea in f:
                    if "," in linea:
                        if linea.split(",")[0] == u:
                            messagebox.showerror("Error", "El usuario ya existe.")
                            return
        guardar_usuario_archivo(u, c)
        messagebox.showinfo("Éxito", "Usuario creado exitosamente.")
        top_crear.destroy()

    top_crear = tk.Toplevel(ventana)
    top_crear.title("Crear Usuario")
    top_crear.geometry("400x300")
    top_crear.configure(bg="#1e1e1e")
    cargar_logo(top_crear)

    estilo_label = {"bg": "#1e1e1e", "fg": "#d4af37", "font": ("Segoe UI", 12)}
    estilo_entry = {"font": ("Segoe UI", 12), "bg": "#2e2e2e", "fg": "#ffffff", "insertbackground": "white"}

    tk.Label(top_crear, text="Usuario:", **estilo_label).pack(pady=5)
    entry_usuario = tk.Entry(top_crear, **estilo_entry)
    entry_usuario.pack()

    tk.Label(top_crear, text="Contraseña:", **estilo_label).pack(pady=5)
    entry_contraseña = tk.Entry(top_crear, show="*", **estilo_entry)
    entry_contraseña.pack()

    tk.Label(top_crear, text="Confirmar contraseña:", **estilo_label).pack(pady=5)
    entry_confirmar = tk.Entry(top_crear, show="*", **estilo_entry)
    entry_confirmar.pack()

    tk.Button(top_crear, text="Guardar", command=guardar_usuario,
              bg="#3a3f51", fg="#d4af37", font=("Segoe UI", 12), width=15).pack(pady=20)

#Iniciar sesión como cliente
def login_cliente():
    def validar():
        u = entry_usuario.get().strip()
        c = entry_contraseña.get()
        if validar_usuario(u, c):
            messagebox.showinfo("Acceso concedido", f"¡Bienvenido {u}!")
            subprocess.run(["python", "cliente.py"])
            top_login.destroy()
        else:
            messagebox.showerror("Error", "Usuario o contraseña incorrectos.")

    def abrir_registro():
        crear_usuario()

    top_login = tk.Toplevel(ventana)
    top_login.title("Login Cliente")
    top_login.geometry("400x300")
    top_login.configure(bg="#1e1e1e")
    cargar_logo(top_login)

    estilo_label = {"bg": "#1e1e1e", "fg": "#d4af37", "font": ("Segoe UI", 12)}
    estilo_entry = {"font": ("Segoe UI", 12), "bg": "#2e2e2e", "fg": "#ffffff", "insertbackground": "white"}

    tk.Label(top_login, text="Usuario:", **estilo_label).pack(pady=5)
    entry_usuario = tk.Entry(top_login, **estilo_entry)
    entry_usuario.pack()

    tk.Label(top_login, text="Contraseña:", **estilo_label).pack(pady=5)
    entry_contraseña = tk.Entry(top_login, show="*", **estilo_entry)
    entry_contraseña.pack()

    tk.Button(top_login, text="Iniciar sesión", command=validar,
              bg="#3a3f51", fg="#d4af37", font=("Segoe UI", 12), width=15).pack(pady=10)

    tk.Button(top_login, text="Crear cuenta", command=abrir_registro,
              bg="#444b68", fg="#d4af37", font=("Segoe UI", 10), width=15).pack()

#Iniciar sesión como chofer
def login_chofer():
    def validar():
        u = entry_usuario.get()
        c = entry_contraseña.get()
        if (u == usuario_chofer and c == contraseña_chofer):
            messagebox.showinfo("Acceso concedido", "¡Acceso concedido al chofer!")
            top_login.destroy()
            subprocess.run(["python", "chofer.py"])
        else:
            messagebox.showerror("Error", "Usuario o contraseña incorrectos.")

    top_login = tk.Toplevel(ventana)
    top_login.title("Login Trabajador")
    top_login.geometry("400x300")
    top_login.configure(bg="#1e1e1e")
    cargar_logo(top_login)

    estilo_label = {"bg": "#1e1e1e", "fg": "#d4af37", "font": ("Segoe UI", 12)}
    estilo_entry = {"font": ("Segoe UI", 12), "bg": "#2e2e2e", "fg": "#ffffff", "insertbackground": "white"}

    tk.Label(top_login, text="Usuario:", **estilo_label).pack(pady=5)
    entry_usuario = tk.Entry(top_login, **estilo_entry)
    entry_usuario.pack()

    tk.Label(top_login, text="Contraseña:", **estilo_label).pack(pady=5)
    entry_contraseña = tk.Entry(top_login, show="*", **estilo_entry)
    entry_contraseña.pack()

    tk.Button(top_login, text="Ingresar", command=validar,
              bg="#3a3f51", fg="#d4af37", font=("Segoe UI", 12), width=15).pack(pady=20)

#Iniciar sesión como dueño
def login_dueño():
    def validar():
        u = entry_usuario.get()
        c = entry_contraseña.get()
        if u == usuario_dueño and c == contraseña_dueño:
            messagebox.showinfo("Acceso concedido", "¡Acceso concedido al dueño!")
            top_login.destroy()
            subprocess.run(["python", "admin.py"])
        else:
            messagebox.showerror("Error", "Usuario o contraseña incorrectos.")

    top_login = tk.Toplevel(ventana)
    top_login.title("Login Dueño")
    top_login.geometry("400x300")
    top_login.configure(bg="#1e1e1e")
    cargar_logo(top_login)

    estilo_label = {"bg": "#1e1e1e", "fg": "#d4af37", "font": ("Segoe UI", 12)}
    estilo_entry = {"font": ("Segoe UI", 12), "bg": "#2e2e2e", "fg": "#ffffff", "insertbackground": "white"}

    tk.Label(top_login, text="Usuario:", **estilo_label).pack(pady=5)
    entry_usuario = tk.Entry(top_login, **estilo_entry)
    entry_usuario.pack()

    tk.Label(top_login, text="Contraseña:", **estilo_label).pack(pady=5)
    entry_contraseña = tk.Entry(top_login, show="*", **estilo_entry)
    entry_contraseña.pack()

    tk.Button(top_login, text="Ingresar", command=validar,
              bg="#3a3f51", fg="#d4af37", font=("Segoe UI", 12), width=15).pack(pady=20)

# Interfaz principal
ventana = tk.Tk()
ventana.title("Sistema de Login")
ventana.geometry("500x450")
ventana.configure(bg="#1e1e1e")
cargar_logo(ventana)

tk.Label(ventana, text=" Menú Principal ", font=("Segoe UI", 18, "bold"),
         bg="#1e1e1e", fg="#d4af37").pack(pady=20)

tk.Button(ventana, text="Iniciar sesión como Cliente", width=30, command=login_cliente,
          bg="#3a3f51", fg="#d4af37", font=("Segoe UI", 12)).pack(pady=10)

tk.Button(ventana, text="Iniciar sesión como Chofer", width=30, command=login_chofer,
          bg="#2e2e2e", fg="#d4af37", font=("Segoe UI", 12)).pack(pady=10)

tk.Button(ventana, text="Iniciar sesión como Administrador", width=30, command=login_dueño,
          bg="#2e2e2e", fg="#d4af37", font=("Segoe UI", 12)).pack(pady=10)

tk.Button(ventana, text="Salir", width=20, command=ventana.quit,
          bg="#ec0c0c", fg="#ffffff", font=("Segoe UI", 12)).pack(pady=30)

ventana.mainloop()