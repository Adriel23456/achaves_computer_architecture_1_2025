import tkinter as tk
from tkinter import ttk
from PIL import ImageTk
import os
from base_view import BaseView
from image_generator import load_input_image, load_output_image, save_as_jpg

class ResultView(BaseView):
    """Vista para mostrar las imágenes generadas a partir de input.img y output.img"""
    
    def __init__(self, parent, view_manager=None):
        super().__init__(parent, view_manager)
        
        # Referencia al controlador
        self.controller = None
        
        # Imágenes
        self.input_image = None
        self.output_image = None
        self.input_image_tk = None
        self.output_image_tk = None
        
        # Crear widgets
        self.create_widgets()
    
    def set_controller(self, controller):
        """Establecer el controlador"""
        self.controller = controller
    
    def create_widgets(self):
        """Crear widgets de la interfaz"""
        # Título
        self.title_label = tk.Label(
            self.frame,
            text="Resultados de Interpolación Bilineal",
            font=("Helvetica", 16, "bold"),
            bg="#121212",
            fg="white"
        )
        self.title_label.pack(pady=(20, 10))
        
        # Frame para ambas imágenes
        self.images_frame = ttk.Frame(self.frame, style='Main.TFrame')
        self.images_frame.pack(pady=10, padx=20, fill="both", expand=True)
        
        # Frame para imagen input
        self.input_frame = ttk.Frame(self.images_frame, style='Image.TFrame')
        self.input_frame.pack(side=tk.LEFT, padx=10, fill="both", expand=True)
        
        # Título de imagen input
        self.input_title = tk.Label(
            self.input_frame,
            text="Imagen Original (128x128)",
            font=("Helvetica", 11),
            bg="#1e1e1e",
            fg="white"
        )
        self.input_title.pack(pady=5)
        
        # Etiqueta para mostrar imagen input
        self.input_label = tk.Label(
            self.input_frame, 
            bg="#1e1e1e",
            bd=0
        )
        self.input_label.pack(fill="both", expand=True, padx=5, pady=5)
        
        # Botón para guardar imagen input
        self.save_input_button = ttk.Button(
            self.input_frame,
            text="Guardar como JPG",
            style='TButton',
            command=self.save_input_image
        )
        self.save_input_button.pack(pady=10)
        
        # Frame para imagen output
        self.output_frame = ttk.Frame(self.images_frame, style='Image.TFrame')
        self.output_frame.pack(side=tk.RIGHT, padx=10, fill="both", expand=True)
        
        # Título de imagen output
        self.output_title = tk.Label(
            self.output_frame,
            text="Imagen Interpolada (256x256)",
            font=("Helvetica", 11),
            bg="#1e1e1e",
            fg="white"
        )
        self.output_title.pack(pady=5)
        
        # Etiqueta para mostrar imagen output
        self.output_label = tk.Label(
            self.output_frame, 
            bg="#1e1e1e",
            bd=0
        )
        self.output_label.pack(fill="both", expand=True, padx=5, pady=5)
        
        # Botón para guardar imagen output
        self.save_output_button = ttk.Button(
            self.output_frame,
            text="Guardar como JPG",
            style='TButton',
            command=self.save_output_image
        )
        self.save_output_button.pack(pady=10)
        
        # Frame para botones inferiores
        self.button_frame = ttk.Frame(self.frame, style='Main.TFrame')
        self.button_frame.pack(pady=20, padx=20, fill="x", side=tk.BOTTOM)
        
        # Botón para volver al inicio
        self.home_button = ttk.Button(
            self.button_frame,
            text="Volver al Inicio",
            style='TButton',
            command=self.go_to_home
        )
        self.home_button.pack()
    
    def on_view_shown(self, **kwargs):
        """Método llamado cuando la vista se muestra"""
        try:
            # Cargar imágenes desde los archivos
            self.input_image = load_input_image()
            self.output_image = load_output_image()
            
            # Crear imágenes para Tkinter
            self.input_image_tk = ImageTk.PhotoImage(self.input_image)
            self.output_image_tk = ImageTk.PhotoImage(self.output_image)
            
            # Mostrar imágenes
            self.input_label.config(image=self.input_image_tk)
            self.output_label.config(image=self.output_image_tk)
            
        except Exception as e:
            print(f"Error al cargar las imágenes: {str(e)}")
            self.show_message("Error", f"Error al cargar las imágenes: {str(e)}")
    
    def save_input_image(self):
        """Guardar la imagen input como JPG"""
        if self.input_image:
            try:
                success = save_as_jpg(self.input_image, "input.jpg")
                if success:
                    self.show_message("Éxito", "Imagen guardada como input.jpg")
                else:
                    self.show_message("Error", "No se pudo guardar la imagen")
            except Exception as e:
                self.show_message("Error", f"Error al guardar la imagen: {str(e)}")
    
    def save_output_image(self):
        """Guardar la imagen output como JPG"""
        if self.output_image:
            try:
                success = save_as_jpg(self.output_image, "output.jpg")
                if success:
                    self.show_message("Éxito", "Imagen guardada como output.jpg")
                else:
                    self.show_message("Error", "No se pudo guardar la imagen")
            except Exception as e:
                self.show_message("Error", f"Error al guardar la imagen: {str(e)}")
    
    def go_to_home(self):
        """Volver a la vista principal"""
        if self.controller:
            self.controller.switch_to_main_view()