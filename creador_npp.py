import tkinter as tk
from tkinter import messagebox
import os
import shutil
from tkinter import filedialog
from tkinter import colorchooser
import re

def verificar_url():
    url = entry_url.get()
    if url.endswith(".trabajando.cl"):
        clonar_carpeta(url)
    else:
        messagebox.showerror("URL Inválido", "El URL no es válido.")

def clonar_carpeta(url):
    nombre_carpeta = url.lower().replace(".", "_")

    # Obtener la ubicación seleccionada
    ubicacion = entry_ubicacion.get()
    if not ubicacion:
        messagebox.showerror("Error", "No se ha seleccionado una carpeta.")
        return

    # Abrir la ventana de diálogo para seleccionar la ubicación de la carpeta clonada
    directorio_clonado = filedialog.askdirectory()
    if not directorio_clonado:
        return

    # Crear la ruta original y la ruta destino
    ruta_original = ubicacion
    ruta_destino = os.path.join(directorio_clonado, nombre_carpeta)

    try:
        print("entro al try")
        shutil.copytree(ruta_original, ruta_destino)
        messagebox.showinfo("Carpeta Clonada", f"Se ha clonado la carpeta en: {ruta_destino}")

        # Obtener los colores seleccionados
        color_principal = color_principal_var.get()
        color_secundario = color_secundario_var.get()
        color_btn = color_btn_var.get()
        color_hover = color_hover_var.get()

        # Modificar el archivo custom.css
        ruta_css = os.path.join(ruta_destino, "css/custom.css")
        ruta_host = "C:/Windows/System32/drivers/etc/hosts"

        if os.path.exists(ruta_css):
            with open(ruta_css, 'r+') as css_file:
                contenido = css_file.read()

                # Reemplazar los colores en el archivo custom.css
                contenido = re.sub(r"--color-principal:\s*[^;]+;", f"--color-principal: {color_principal};", contenido)
                contenido = re.sub(r"--color-secundario:\s*[^;]+;", f"--color-secundario: {color_secundario};", contenido)
                contenido = re.sub(r"--color-btn:\s*[^;]+;", f"--color-btn: {color_btn};", contenido)
                contenido = re.sub(r"--color-hover:\s*[^;]+;", f"--color-hover: {color_hover};", contenido)

                css_file.seek(0)
                css_file.write(contenido)
                css_file.truncate()

        if os.path.exists(ruta_host):
            # Obtener el localhosts
            localhost = "127.0.0.1"
            linea_hosts = f"{localhost} {url}"

            texto_hosts = 'este sera el texto del hosts'

            hosts = 'este sera'

            actualizar_campo(hosts)

            
            # try:
            #     pass
                # with open(ruta_host, "a") as f:
                #     f.write(f"\n{linea_hosts}")
                #     messagebox.showinfo("Archivo hosts modificado", f"Se ha modificado el archivo hosts para apuntar '{url}' a '{localhost}'")
            # except OSError:
            #     messagebox.showerror("Error", "No se pudo modificar el archivo hosts.")

    except OSError:
        messagebox.showerror("Error", "No se pudo clonar la carpeta.")

def actualizar_campo(campo_texto):
    mi_variable = tk.StringVar()
    mi_variable.set(campo_texto)
    hosts_line.delete(1.0, tk.END)  # Borrar el contenido actual del campo
    hosts_line.insert(tk.END, mi_variable.get())

# Crear la ventana principal
ventana = tk.Tk()
ventana.title("Clonar Carpeta")

# Crear el campo de entrada para el URL
label_url = tk.Label(ventana, text="URL:")
label_url.pack()
entry_url = tk.Entry(ventana, width=50)
entry_url.insert(0, "Escribir URL")  # Texto de marcador de posición
entry_url.pack(pady=5)

# Crear el campo de entrada para la ubicación de la carpeta original
label_ubicacion = tk.Label(ventana, text="Carpeta Original:")
label_ubicacion.pack()
entry_ubicacion = tk.Entry(ventana, width=50, state='readonly')
entry_ubicacion.pack(pady=5)

# Función para borrar el marcador de posición al hacer clic en el campo de entrada del URL
def borrar_placeholder_url(event):
    if entry_url.get() == "Escribir URL":
        entry_url.delete(0, tk.END)

entry_url.bind("<Button-1>", borrar_placeholder_url)

# Función para abrir la ventana de diálogo para seleccionar la carpeta original
def seleccionar_carpeta():
    ubicacion = filedialog.askdirectory()
    if ubicacion:
        entry_ubicacion.configure(state='normal')
        entry_ubicacion.delete(0, tk.END)
        entry_ubicacion.insert(0, ubicacion)
        entry_ubicacion.configure(state='readonly')

# Crear el botón para seleccionar la carpeta original
button_seleccionar_carpeta = tk.Button(ventana, text="Seleccionar Carpeta", command=seleccionar_carpeta)
button_seleccionar_carpeta.pack(pady=5)

# Crear los campos para seleccionar los colores
label_colores = tk.Label(ventana, text="Colores:")
label_colores.pack()

color_principal_var = tk.StringVar()
color_secundario_var = tk.StringVar()
color_btn_var = tk.StringVar()
color_hover_var = tk.StringVar()

def seleccionar_color(var):
    color = colorchooser.askcolor()[1]
    var.set(color)

label_color_principal = tk.Label(ventana, text="Color Principal:")
label_color_principal.pack()
entry_color_principal = tk.Entry(ventana, textvariable=color_principal_var, state='readonly')
entry_color_principal.pack(pady=5)
button_seleccionar_color_principal = tk.Button(ventana, text="Seleccionar Color", command=lambda: seleccionar_color(color_principal_var))
button_seleccionar_color_principal.pack()

label_color_secundario = tk.Label(ventana, text="Color Secundario:")
label_color_secundario.pack()
entry_color_secundario = tk.Entry(ventana, textvariable=color_secundario_var, state='readonly')
entry_color_secundario.pack(pady=5)
button_seleccionar_color_secundario = tk.Button(ventana, text="Seleccionar Color", command=lambda: seleccionar_color(color_secundario_var))
button_seleccionar_color_secundario.pack()

label_color_btn = tk.Label(ventana, text="Color del Botón:")
label_color_btn.pack()
entry_color_btn = tk.Entry(ventana, textvariable=color_btn_var, state='readonly')
entry_color_btn.pack(pady=5)
button_seleccionar_color_btn = tk.Button(ventana, text="Seleccionar Color", command=lambda: seleccionar_color(color_btn_var))
button_seleccionar_color_btn.pack()

label_color_hover = tk.Label(ventana, text="Color Hover:")
label_color_hover.pack()
entry_color_hover = tk.Entry(ventana, textvariable=color_hover_var, state='readonly')
entry_color_hover.pack(pady=5)
button_seleccionar_color_hover = tk.Button(ventana, text="Seleccionar Color", command=lambda: seleccionar_color(color_hover_var))
button_seleccionar_color_hover.pack()

#texto linea host
hosts_line_label = tk.Label(ventana, text="texto hosts:")
hosts_line_label.pack()
hosts_line = tk.Entry(ventana, state='readonly')
hosts_line.pack(pady=5)

# Crear el botón de clonar
button_clonar = tk.Button(ventana, text="Clonar", command=verificar_url)
button_clonar.pack(pady=10)

# Ejecutar la ventana principal
ventana.mainloop()