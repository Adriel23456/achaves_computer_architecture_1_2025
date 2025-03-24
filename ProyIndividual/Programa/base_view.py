import tkinter as tk
from tkinter import ttk

class BaseView:
    """Clase base para todas las vistas de la aplicación"""
    
    def __init__(self, parent, view_manager=None):
        self.parent = parent
        self.view_manager = view_manager
        self.frame = ttk.Frame(parent, style='Main.TFrame')
        self.frame.grid(row=0, column=0, sticky="nsew")
        parent.grid_rowconfigure(0, weight=1)
        parent.grid_columnconfigure(0, weight=1)
        
        # Crear estilos compartidos
        self.create_styles()
        
    def create_styles(self):
        """Crear estilos personalizados para widgets"""
        self.style = ttk.Style()
        
        # Configurar tema oscuro
        self.style.theme_use('alt')
        
        # Estilo para botones
        self.style.configure(
            'TButton',
            font=('Helvetica', 11),
            background="#2a2a2a",
            foreground="white",
            borderwidth=1,
            focusthickness=3,
            focuscolor='none',
            padding=(15, 8)
        )
        
        # Estilo para botones al pasar el mouse
        self.style.map(
            'TButton',
            background=[('active', '#3a3a3a')],
            relief=[('pressed', 'sunken')]
        )
        
        # Estilo para frame principal
        self.style.configure(
            'Main.TFrame',
            background="#121212"
        )
        
        # Estilo para frame de imagen
        self.style.configure(
            'Image.TFrame',
            background="#1e1e1e",
            borderwidth=2,
            relief="groove"
        )
        
        # Estilo para botones deshabilitados
        self.style.map(
            'TButton',
            background=[('disabled', '#1a1a1a')],
            foreground=[('disabled', '#555555')]
        )
        
    def show(self):
        """Mostrar esta vista"""
        self.frame.lift()
        
    def hide(self):
        """Ocultar esta vista"""
        self.frame.lower()
        
    def destroy(self):
        """Destruir esta vista"""
        self.frame.destroy()
        
    def center_window(self, window, width, height):
        """Centrar una ventana en la pantalla"""
        # Obtener dimensiones de la pantalla
        screen_width = window.winfo_screenwidth()
        screen_height = window.winfo_screenheight()
        
        # Calcular posición x, y
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2
        
        # Establecer geometría
        window.geometry(f"{width}x{height}+{x}+{y}")
        
    def show_message(self, title, message):
        """Mostrar un mensaje en una ventana centrada"""
        msg_window = tk.Toplevel(self.parent)
        msg_window.title(title)
        msg_window.configure(bg="#121212")
        msg_window.resizable(False, False)
        
        # Centrar la ventana
        width, height = 400, 200
        self.center_window(msg_window, width, height)
        
        # Frame para contenido
        frame = tk.Frame(msg_window, bg="#121212", padx=20, pady=20)
        frame.pack(fill="both", expand=True)
        
        # Mensaje
        msg_label = tk.Label(
            frame, 
            text=message, 
            font=("Helvetica", 11),
            bg="#121212",
            fg="white",
            justify="center",
            wraplength=360
        )
        msg_label.pack(pady=10)
        
        # Botón OK
        ok_button = ttk.Button(
            frame, 
            text="OK", 
            style='TButton',
            command=msg_window.destroy
        )
        ok_button.pack(pady=10)
        
        # Asegurar que la ventana sea modal
        msg_window.transient(self.parent)
        msg_window.grab_set()
        self.parent.wait_window(msg_window)