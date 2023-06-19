import tkinter as tk
from tkinter import messagebox, filedialog, ttk
import os
import shutil
import re
import webbrowser

# Estilo minimalista
# style = ttk.Style()

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
            print(linea_hosts)

            hosts_line.configure(state='normal')

            hosts_line.delete(0, tk.END)
            hosts_line.insert(0, linea_hosts)

            entry_ubicacion.configure(state='readonly')

            
            # Limpiar los campos de URL y colores
            entry_url.delete(0, tk.END)
            entry_color_principal.delete(0, tk.END)
            entry_color_secundario.delete(0, tk.END)
            entry_color_btn.delete(0, tk.END)
            entry_color_hover.delete(0, tk.END)

            texto_hosts = 'este sera el texto del hosts'

            hosts = 'este sera'
            # Obtener la ruta completa del archivo de logo en la carpeta clonada
            ruta_logo_clonado = os.path.join(ruta_destino, "img/logo.png")

            # Eliminar el archivo de logo existente, si existe
            if os.path.exists(ruta_logo_clonado):
                os.remove(ruta_logo_clonado)

            file_path = label_logo_path.get()
            # Copiar la imagen seleccionada como el nuevo logo
            shutil.copyfile(file_path, ruta_logo_clonado)

            #actualizar_campo(hosts)

            
            # try:
            #     pass
                # with open(ruta_host, "a") as f:
                #     f.write(f"\n{linea_hosts}")
                #     messagebox.showinfo("Archivo hosts modificado", f"Se ha modificado el archivo hosts para apuntar '{url}' a '{localhost}'")
            # except OSError:
            #     messagebox.showerror("Error", "No se pudo modificar el archivo hosts.")

    except OSError:
        messagebox.showerror("Error", "La carpeta ya existe o los datos estan incorrectos.")

    webbrowser.open_new_tab("http://"+url)
    webbrowser.open_new_tab("http://"+url + "/creadorperfiles")

def verificar_url():
    url = entry_url.get()
    if url.endswith(".trabajando.cl"):
        clonar_carpeta(url)
    else:
        messagebox.showerror("URL Inválido", "El URL no es válido.")

def actualizar_campo(campo_texto):
    mi_variable = tk.StringVar()
    mi_variable.set(campo_texto)
    hosts_line.delete(1.0, tk.END)  # Borrar el contenido actual del campo
    hosts_line.insert(tk.END, mi_variable.get())

def copy_to_clipboard():
    text = hosts_line.get()
    ventana.clipboard_clear()
    ventana.clipboard_append(text)
    messagebox.showinfo("Copiado", "Texto copiado al portapapeles.")

# Función para borrar el marcador de posición al hacer clic en el campo de entrada del URL
def borrar_placeholder_url(event):
    if entry_url.get() == "Escribir URL":
        entry_url.delete(0, tk.END)

# Función para abrir la ventana de diálogo para seleccionar la carpeta original
def seleccionar_carpeta():
    ubicacion = filedialog.askdirectory()
    if ubicacion:
        entry_ubicacion.configure(state='normal')
        entry_ubicacion.delete(0, tk.END)
        entry_ubicacion.insert(0, ubicacion)
        entry_ubicacion.configure(state='readonly')

def select_logo():
    # Abrir la ventana de diálogo para seleccionar el archivo de imagen
    file_path = filedialog.askopenfilename(title="Seleccionar Logo", filetypes=(("PNG files", "*.png"), ("All files", "*.*")))

    label_logo_path.configure(state='normal')
    label_logo_path.delete(0, tk.END)
    label_logo_path.insert(0, file_path)
    label_logo_path.configure(state='readonly')

    # if file_path:
    #     try:
    #         # Verificar que el archivo seleccionado sea una imagen PNG
    #         img = Image.open(file_path)
    #         if img.format == "PNG":
    #             messagebox.showinfo("Logo Seleccionado", f"Se ha seleccionado el archivo: {file_path}")
    #             # Puedes realizar acciones adicionales con la imagen seleccionada aquí
    #         else:
    #             messagebox.showerror("Formato Incorrecto", "El archivo seleccionado no es un PNG válido.")
    #     except Exception as e:
    #         messagebox.showerror("Error", f"No se pudo abrir el archivo: {str(e)}")

# Crear la ventana principal
ventana = tk.Tk()
ventana.title("Clonar Carpeta")
ventana.geometry("400x750")

style = ttk.Style()

ventana.configure(bg='#2e292e')
style.configure("TButton",
                background="#674d69",
                foreground="#000000",
                font=("Helvetica", 10),
                padding=3,)
style.configure("TLabel",
                background="#2e292e",
                foreground="white",
                font=("Helvetica", 10),
                width=43,anchor="nw")
style.configure("TEntry",
                background="#674d69",
                foreground="#000000",
                font=("Helvetica", 12))

# Crear el campo de entrada para el URL
entry_url_label = ttk.Label(ventana, text="Url nuevo:")
entry_url_label.pack(padx=0, pady=10)
entry_url = ttk.Entry(ventana, width=50)
entry_url.insert(0, "Escribir URL")  # Texto de marcador de posición
entry_url.pack(pady=5)
entry_url.bind("<Button-1>", borrar_placeholder_url)

# Crear el campo de entrada para la ubicación de la carpeta original
label_ubicacion = ttk.Label(ventana, text="Carpeta Original:")
label_ubicacion.pack(padx=0, pady=10)
entry_ubicacion = tk.Entry(ventana, width=50)
entry_ubicacion.configure(bg='#2e292e')
entry_ubicacion.pack(pady=5)

# Crear el botón para seleccionar la carpeta original
button_seleccionar_carpeta = ttk.Button(ventana, text="Seleccionar Carpeta", command=seleccionar_carpeta, style="TButton", width=42)
button_seleccionar_carpeta.pack(pady=3)

color_principal_var = tk.StringVar()
color_secundario_var = tk.StringVar()
color_btn_var = tk.StringVar()
color_hover_var = tk.StringVar()


label_color_principal = ttk.Label(ventana, text="Color Principal:")
label_color_principal.pack(padx=0, pady=10)
entry_color_principal = ttk.Entry(ventana, textvariable=color_principal_var,width=50)
entry_color_principal.pack(pady=5)

label_color_secundario = ttk.Label(ventana, text="Color Secundario:")
label_color_secundario.pack(padx=0, pady=10)
entry_color_secundario = ttk.Entry(ventana, textvariable=color_secundario_var,width=50)
entry_color_secundario.pack(pady=5)

label_color_btn = ttk.Label(ventana, text="Color del Botón:")
label_color_btn.pack(padx=0, pady=10)
entry_color_btn = ttk.Entry(ventana, textvariable=color_btn_var,width=50)
entry_color_btn.pack(pady=5)

label_color_hover = ttk.Label(ventana, text="Color Hover:")
label_color_hover.pack(padx=0, pady=10)
entry_color_hover = ttk.Entry(ventana, textvariable=color_hover_var,width=50)
entry_color_hover.pack(pady=5)

label_logo_path = tk.Entry(ventana, width=50)
label_logo_path.configure(bg='#2e292e')
label_logo_path.pack(padx=0, pady=10)
button_logo = ttk.Button(ventana, text="Logo", command=select_logo, style="TButton", width=42)
button_logo.pack(pady=10)

#texto linea host
hosts_line_label = ttk.Label(ventana, text="texto hosts:")
hosts_line_label.pack(padx=0, pady=10)
hosts_line = ttk.Entry(ventana, state='readonly', width=50)
hosts_line.pack(pady=5)
button = ttk.Button(ventana, text="Copiar", command=copy_to_clipboard, style="TButton", width=42)
button.pack(pady=10)

# Crear el botón de clonar
button_clonar = ttk.Button(ventana, text="Clonar", command=verificar_url, style="TButton", width=42)
button_clonar.pack(pady=10)


# Ejecutar la ventana principal
ventana.mainloop()