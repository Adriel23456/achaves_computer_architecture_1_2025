import os
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from base_view import BaseView

class MainView(BaseView):
    """Vista principal del visor de imágenes"""
    
    def __init__(self, parent, view_manager=None):
        super().__init__(parent, view_manager)
        
        # Referencia al controlador
        self.controller = None
        
        # Crear widgets
        self.create_widgets()
    
    def set_controller(self, controller):
        """Establecer el controlador"""
        self.controller = controller
    
    def create_widgets(self):
        """Crear widgets de la interfaz"""
        # Frame para controles superiores
        self.control_frame = ttk.Frame(self.frame, style='Main.TFrame')
        self.control_frame.pack(pady=20, padx=20, fill="x")
        
        # Botones en el frame de control
        self.browse_button = ttk.Button(
            self.control_frame, 
            text="Buscar Imagen", 
            style='TButton',
            command=self.browse_image
        )
        self.browse_button.pack(side=tk.LEFT, padx=10)
        
        self.next_section_button = ttk.Button(
            self.control_frame, 
            text="Siguiente Sección", 
            style='TButton',
            command=self.next_section,
            state="disabled"  # Inicialmente deshabilitado
        )
        self.next_section_button.pack(side=tk.LEFT, padx=10)
        
        # Frame para mostrar la imagen con borde
        self.image_container = ttk.Frame(self.frame, style='Image.TFrame')
        self.image_container.pack(pady=10, padx=20, fill="both", expand=True)
        
        # Etiqueta para mostrar la imagen
        self.image_label = tk.Label(
            self.image_container, 
            bg="#1e1e1e",
            bd=0
        )
        self.image_label.pack(fill="both", expand=True, padx=5, pady=5)
        
        # Frame para información de la imagen
        self.info_frame = ttk.Frame(self.frame, style='Main.TFrame')
        self.info_frame.pack(pady=10, padx=20, fill="x")
        
        # Etiqueta para mostrar información de la imagen
        self.info_label = tk.Label(
            self.info_frame,
            text="Ninguna imagen cargada",
            bg="#121212",
            fg="#aaaaaa",
            font=('Helvetica', 10)
        )
        self.info_label.pack(pady=5)
        
        # Frame para botón de créditos
        self.credits_frame = ttk.Frame(self.frame, style='Main.TFrame')
        self.credits_frame.pack(pady=10, padx=20, fill="x", side=tk.BOTTOM)
        
        # Botón de créditos
        self.credits_button = ttk.Button(
            self.credits_frame, 
            text="Créditos", 
            style='TButton',
            command=self.show_credits
        )
        self.credits_button.pack(side=tk.RIGHT, padx=10, pady=10)
    
    def browse_image(self):
        """Buscar y cargar una imagen"""
        if not self.controller:
            return
            
        try:
            # Abrir diálogo centrado en directorio actual
            file_path = filedialog.askopenfilename(
                title="Seleccionar una Imagen",
                filetypes=[("Archivos JPEG", "*.jpg"), ("Archivos JPEG", "*.jpeg")],
                initialdir=os.getcwd()
            )
            
            # Si se seleccionó un archivo
            if file_path:
                # Resetear estado actual
                self.reset_view()
                
                # Cargar la imagen
                success = self.controller.load_image(file_path)
                
                if success:
                    # Obtener la imagen procesada para mostrar
                    display_image = self.controller.get_display_image()
                    
                    # Mostrar la imagen
                    self.set_image(display_image)
                    
                    # Actualizar información
                    self.update_info(self.controller.get_image_info())
                    
                    # Habilitar botón de siguiente sección
                    self.next_section_button.config(state="normal")
                    
                    # Actualizar título
                    self.parent.title(f"Visor de Imágenes - {os.path.basename(file_path)}")
        
        except Exception as e:
            messagebox.showerror("Error", f"Error al cargar la imagen: {str(e)}")
    
    def next_section(self):
        """Pasar a la vista de secciones"""
        if self.controller:
            self.controller.switch_to_section_view()
    
    def set_image(self, image_tk):
        """Establecer la imagen en la etiqueta"""
        if image_tk:
            self.image_label.configure(image=image_tk)
            self.image_label.image = image_tk  # Mantener referencia
            
    def reset_view(self):
        """Restaurar la vista a su estado inicial"""
        # Limpiar imagen
        self.image_label.configure(image="")
        self.image_label.image = None
        
        # Actualizar información
        self.info_label.configure(text="Ninguna imagen cargada")
        
        # Deshabilitar botón de siguiente sección
        self.next_section_button.config(state="disabled")
        
        # Restaurar título
        self.parent.title("Visor de Imágenes")
    
    def update_info(self, info):
        """Actualizar información de la imagen"""
        if info:
            text = f"Archivo: {info.get('path')}\n"
            text += f"Tamaño original: {info.get('original_size')}\n"
            text += f"Nuevo tamaño: {info.get('new_size')}"
            self.info_label.configure(text=text)
        else:
            self.info_label.configure(text="Ninguna imagen cargada")
    
    def show_credits(self):
        """Mostrar ventana de créditos"""
        credits_window = tk.Toplevel(self.parent)
        credits_window.title("Créditos")
        credits_window.configure(bg="#121212")
        credits_window.resizable(False, False)
        
        # Centrar la ventana
        width, height = 600, 400
        self.center_window(credits_window, width, height)
        
        # Frame para contenido
        frame = tk.Frame(credits_window, bg="#121212", padx=30, pady=30)
        frame.pack(fill="both", expand=True)
        
        # Título del proyecto
        title_label = tk.Label(
            frame, 
            text="Visor de Imágenes y Procesamiento por Secciones", 
            font=("Helvetica", 16, "bold"),
            bg="#121212",
            fg="white"
        )
        title_label.pack(pady=(0, 20))
        
        # Información de estudiante y curso
        credits_text = tk.Label(
            frame, 
            text="Elaborado por:\nAdriel Sebastian Chaves Salazar\n\n" +
                 "Profesor:\nLuis A. Chavarría Zamora\n\n" +
                 "Instituto Tecnológico de Costa Rica\n" +
                 "Escuela de Ingeniería en Computadores\n" +
                 "CE4301 — Arquitectura de Computadores I\n\n" +
                 "El proceso de interpolación bilineal es un proceso complejo pues\n" +
                 "trata de rellenar el espacio con información continua,\n" +
                 "no replicando un mismo valor.",
            font=("Helvetica", 12),
            bg="#121212",
            fg="white",
            justify="center"
        )
        credits_text.pack(pady=10)
        
        # Botón para cerrar
        close_button = ttk.Button(
            frame, 
            text="Cerrar", 
            style='TButton',
            command=credits_window.destroy
        )
        close_button.pack(pady=20)
        
        # Hacer la ventana modal
        credits_window.transient(self.parent)
        credits_window.grab_set()
        self.parent.wait_window(credits_window)