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
        label = tk.Label(parent, image=imagen_tk, bg="#e3f2fd")
        label.image = imagen_tk
        label.place(relx=1.0, y=10, anchor="ne")  # Esquina superior derecha
    except:
        tk.Label(parent, text="Sin logo", bg="#e3f2fd", fg="red").place(relx=1.0, y=10, anchor="ne")

ventana = tk.Tk()
ventana.title("Sistema de Login")
ventana.geometry("600x600")
ventana.configure(bg="#e3f2fd")
cargar_logo(ventana)

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
    top_crear.configure(bg="#e3f2fd")
    cargar_logo(top_crear)

    tk.Label(top_crear, text="Usuario:", bg="#e3f2fd", fg="#0d47a1", font=("Arial", 12)).pack(pady=5)
    entry_usuario = tk.Entry(top_crear, font=("Arial", 11), bg="white", fg="black")
    entry_usuario.pack()

    tk.Label(top_crear, text="Contraseña:", bg="#e3f2fd", fg="#0d47a1", font=("Arial", 12)).pack(pady=5)
    entry_contraseña = tk.Entry(top_crear, show="*", font=("Arial", 11), bg="white", fg="black")
    entry_contraseña.pack()

    tk.Label(top_crear, text="Confirmar contraseña:", bg="#e3f2fd", fg="#0d47a1", font=("Arial", 12)).pack(pady=5)
    entry_confirmar = tk.Entry(top_crear, show="*", font=("Arial", 11), bg="white", fg="black")
    entry_confirmar.pack()

    tk.Button(top_crear, text="Guardar", command=guardar_usuario,
              bg="#2196f3", fg="white", font=("Arial", 11), width=15).pack(pady=20)

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
    top_login.configure(bg="#e3f2fd")
    cargar_logo(top_login)

    tk.Label(top_login, text="Usuario:", bg="#e3f2fd", fg="#0d47a1", font=("Arial", 12)).pack(pady=5)
    entry_usuario = tk.Entry(top_login, font=("Arial", 11), bg="white", fg="black")
    entry_usuario.pack()

    tk.Label(top_login, text="Contraseña:", bg="#e3f2fd", fg="#0d47a1", font=("Arial", 12)).pack(pady=5)
    entry_contraseña = tk.Entry(top_login, show="*", font=("Arial", 11), bg="white", fg="black")
    entry_contraseña.pack()

    tk.Button(top_login, text="Ingresar", command=validar,
              bg="#2196f3", fg="white", font=("Arial", 11), width=15).pack(pady=20)

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
    top_login.configure(bg="#e3f2fd")
    cargar_logo(top_login)

    tk.Label(top_login, text="Usuario:", bg="#e3f2fd", fg="#0d47a1", font=("Arial", 12)).pack(pady=5)
    entry_usuario = tk.Entry(top_login, font=("Arial", 11), bg="white", fg="black")
    entry_usuario.pack()

    tk.Label(top_login, text="Contraseña:", bg="#e3f2fd", fg="#0d47a1", font=("Arial", 12)).pack(pady=5)
    entry_contraseña = tk.Entry(top_login, show="*", font=("Arial", 11), bg="white", fg="black")
    entry_contraseña.pack()

    tk.Button(top_login, text="Ingresar", command=validar,
              bg="#2196f3", fg="white", font=("Arial", 11), width=15).pack(pady=20)

# Interfaz principal
tk.Label(ventana, text="Menú Principal", font=("Arial", 16, "bold"),
         bg="#e3f2fd", fg="#0d47a1").pack(pady=20)

tk.Button(ventana, text="Crear usuario", width=30, command=crear_usuario,
          bg="#2196f3", fg="white", font=("Arial", 11)).pack(pady=10)

tk.Button(ventana, text="Iniciar sesión como Trabajador", width=30, command=login_trabajador,
          bg="#1976d2", fg="white", font=("Arial", 11)).pack(pady=10)

tk.Button(ventana, text="Iniciar sesión como Dueño", width=30, command=login_dueño,
          bg="#1565c0", fg="white", font=("Arial", 11)).pack(pady=10)

tk.Button(ventana, text="Salir", width=20, command=ventana.quit,
          bg="#b71c1c", fg="white", font=("Arial", 11)).pack(pady=30)

ventana.mainloop()
