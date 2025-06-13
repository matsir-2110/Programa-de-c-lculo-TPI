import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk

# Usuarios por defecto
usuario_trabajador = "usuario1"
contraseña_trabajador = "contraseña1"

usuario_dueño = "Luicho"
contraseña_dueño = "luichos"

nuevo_usuario = None
nueva_contraseña = None

def cargar_logo(parent):
    try:
        imagen = Image.open("logoluicho.png")
        imagen = imagen.resize((100, 100))
        imagen_tk = ImageTk.PhotoImage(imagen)
        label = tk.Label(parent, image=imagen_tk, bg="#d0f0fd")  # celeste claro
        label.image = imagen_tk
        label.place(relx=1.0, y=10, anchor="ne")  # Esquina superior derecha
    except:
        tk.Label(parent, text="Sin logo", bg="#d0f0fd", fg="#f9a825").place(relx=1.0, y=10, anchor="ne")

ventana = tk.Tk()
ventana.title("Sistema de Login")
ventana.geometry("600x600")
ventana.configure(bg="#d0f0fd")  # celeste claro

# Login Usuarios _____________________________________________________________________________________________________________

def crear_usuario():
    def guardar_usuario():
        global nuevo_usuario, nueva_contraseña
        u = entry_usuario.get()
        c = entry_contraseña.get()
        c2 = entry_confirmar.get()
        if c != c2:
            messagebox.showerror("Error", "Las contraseñas no coinciden.")
        elif not u or not c:
            messagebox.showerror("Error", "Los campos no pueden estar vacíos.")
        else:
            nuevo_usuario = u
            nueva_contraseña = c
            messagebox.showinfo("Éxito", "Usuario creado exitosamente.")
            top_crear.destroy()

    top_crear = tk.Toplevel(ventana)
    top_crear.title("Crear Usuario")
    top_crear.geometry("600x600")
    top_crear.configure(bg="#d0f0fd")  # celeste claro
    cargar_logo(top_crear)

    tk.Label(top_crear, text="Usuario:", bg="#d0f0fd", fg="#f9a825", font=("Arial", 12)).pack(pady=5)  # amarillo
    entry_usuario = tk.Entry(top_crear, font=("Arial", 12), bg="#ffffcc", fg="#004d40")  # fondo amarillo claro, texto verde oscuro
    entry_usuario.pack()

    tk.Label(top_crear, text="Contraseña:", bg="#d0f0fd", fg="#f9a825", font=("Arial", 12)).pack(pady=5)
    entry_contraseña = tk.Entry(top_crear, show="*", font=("Arial", 12), bg="#ffffcc", fg="#004d40")
    entry_contraseña.pack()

    tk.Label(top_crear, text="Confirmar contraseña:", bg="#d0f0fd", fg="#f9a825", font=("Arial", 12)).pack(pady=5)
    entry_confirmar = tk.Entry(top_crear, show="*", font=("Arial", 12), bg="#ffffcc", fg="#004d40")
    entry_confirmar.pack()

    tk.Button(top_crear, text="Guardar", command=guardar_usuario,
              bg="#81d4fa", fg="#01579b", font=("Arial", 12), width=15).pack(pady=20)  # celeste brillante, azul oscuro

import clientes
# Login Trabajador ____________________________________________________________________________________________________________

def login_trabajador():
    def validar():
        u = entry_usuario.get()
        c = entry_contraseña.get()
        if (u == usuario_trabajador and c == contraseña_trabajador) or (u == nuevo_usuario and c == nueva_contraseña):
            messagebox.showinfo("Acceso concedido", "¡Acceso concedido al trabajador!")
            top_login.destroy()
        else:
            messagebox.showerror("Error", "Usuario o contraseña incorrectos.")

    top_login = tk.Toplevel(ventana)
    top_login.title("Login Trabajador")
    top_login.geometry("600x600")
    top_login.configure(bg="#d0f0fd")
    cargar_logo(top_login)

    tk.Label(top_login, text="Usuario:", bg="#d0f0fd", fg="#f9a825", font=("Arial", 12)).pack(pady=5)
    entry_usuario = tk.Entry(top_login, font=("Arial", 12), bg="#ffffcc", fg="#004d40")
    entry_usuario.pack()

    tk.Label(top_login, text="Contraseña:", bg="#d0f0fd", fg="#f9a825", font=("Arial", 12)).pack(pady=5)
    entry_contraseña = tk.Entry(top_login, show="*", font=("Arial", 12), bg="#ffffcc", fg="#004d40")
    entry_contraseña.pack()

    tk.Button(top_login, text="Ingresar", command=validar,
              bg="#81d4fa", fg="#01579b", font=("Arial", 12), width=15).pack(pady=20)


# Login Dueño ________________________________________________________________________________________________________________

def login_dueño():
    def validar():
        u = entry_usuario.get()
        c = entry_contraseña.get()
        if u == usuario_dueño and c == contraseña_dueño:
            messagebox.showinfo("Acceso concedido", "¡Acceso concedido al dueño!")
            top_login.destroy()
        else:
            messagebox.showerror("Error", "Usuario o contraseña incorrectos.")

    top_login = tk.Toplevel(ventana)
    top_login.title("Login Dueño")
    top_login.geometry("600x600")
    top_login.configure(bg="#d0f0fd")
    cargar_logo(top_login)

    tk.Label(top_login, text="Usuario:", bg="#d0f0fd", fg="#f9a825", font=("Arial", 12)).pack(pady=5)
    entry_usuario = tk.Entry(top_login, font=("Arial", 12), bg="#ffffcc", fg="#004d40")
    entry_usuario.pack()

    tk.Label(top_login, text="Contraseña:", bg="#d0f0fd", fg="#f9a825", font=("Arial", 12)).pack(pady=5)
    entry_contraseña = tk.Entry(top_login, show="*", font=("Arial", 12), bg="#ffffcc", fg="#004d40")
    entry_contraseña.pack()

    tk.Button(top_login, text="Ingresar", command=validar,
              bg="#81d4fa", fg="#01579b", font=("Arial", 12), width=15).pack(pady=20)


# Interfaz principal _________________________________________________________________________________________
tk.Label(ventana, text=" Menú Principal ", font=("Arial", 18, "bold"),
         bg="#d0f0fd", fg="#0288d1").pack(pady=20)  # azul celeste medio

tk.Button(ventana, text="Inicia sesion como Cliente", width=30, command=crear_usuario,
          bg="#81d4fa", fg="#01579b", font=("Arial", 12)).pack(pady=10)

tk.Button(ventana, text="Inicia sesion como Chofer", width=30, command=login_trabajador,
          bg="#4fc3f7", fg="#01579b", font=("Arial", 12)).pack(pady=10)

tk.Button(ventana, text="Iniciar sesión como Administrador", width=30, command=login_dueño,
          bg="#29b6f6", fg="#01579b", font=("Arial", 12)).pack(pady=10)

tk.Button(ventana, text="Salir", width=20, command=ventana.quit,
          bg="#f9a825", fg="#004d40", font=("Arial", 12)).pack(pady=30)  # amarillo

ventana.mainloop()
