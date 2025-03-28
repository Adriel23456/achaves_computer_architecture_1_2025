import tkinter as tk
from tkinter import ttk
from PIL import ImageTk
from base_view import BaseView

class DetailView(BaseView):
    """Vista para mostrar el detalle de una sección y aplicar interpolación bilineal"""
    
    def __init__(self, parent, view_manager=None):
        super().__init__(parent, view_manager)
        
        # Referencia al controlador
        self.controller = None
        
        # Sección actual
        self.current_section = None
        self.section_position = None
        self.section_image_tk = None
        
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
            text="Detalle de Sección",
            font=("Helvetica", 16, "bold"),
            bg="#121212",
            fg="white"
        )
        self.title_label.pack(pady=(20, 10))
        
        # Información
        self.info_label = tk.Label(
            self.frame,
            text="",
            font=("Helvetica", 11),
            bg="#121212",
            fg="#aaaaaa"
        )
        self.info_label.pack(pady=(0, 20))
        
        # Frame para la imagen
        self.image_container = ttk.Frame(self.frame, style='Image.TFrame')
        self.image_container.pack(pady=10, padx=20, fill="both", expand=True)
        
        # Etiqueta para mostrar la imagen
        self.image_label = tk.Label(
            self.image_container, 
            bg="#1e1e1e",
            bd=0
        )
        self.image_label.pack(fill="both", expand=True, padx=5, pady=5)
        
        # Frame para botones inferiores
        self.button_frame = ttk.Frame(self.frame, style='Main.TFrame')
        self.button_frame.pack(pady=20, padx=20, fill="x", side=tk.BOTTOM)
        
        # Botones
        self.back_button = ttk.Button(
            self.button_frame,
            text="Volver",
            style='TButton',
            command=self.go_back
        )
        self.back_button.pack(side=tk.LEFT, padx=10)
        
        self.interpolate_button = ttk.Button(
            self.button_frame,
            text="Generar Aumento por Interpolación Bilineal",
            style='TButton',
            command=self.apply_bilinear_interpolation
        )
        self.interpolate_button.pack(side=tk.RIGHT, padx=10)
    
    def on_view_shown(self, **kwargs):
        """Método llamado cuando la vista se muestra"""
        if 'section_image' in kwargs and 'position' in kwargs:
            self.current_section = kwargs['section_image']
            self.section_position = kwargs['position']
            self.display_section()
    
    def display_section(self):
        """Mostrar la sección seleccionada"""
        if not self.current_section:
            return
            
        # Crear imagen para Tkinter
        self.section_image_tk = ImageTk.PhotoImage(self.current_section)
        
        # Mostrar la imagen
        self.image_label.config(image=self.section_image_tk)
        
        # Actualizar información
        row, col = self.section_position
        section_number = row * 4 + col + 1
        self.info_label.config(
            text=f"Sección {section_number} - Tamaño: 125x125 píxeles"
        )
        
        # Restablecer estado
        self.showing_upscaled = False
        self.interpolate_button.config(
            text="Generar Aumento por Interpolación Bilineal"
        )
    
    def apply_bilinear_interpolation(self):
        """Preparar para aplicar interpolación bilineal (genera archivos input.img y output.img)"""
        if not self.current_section:
            return
            
        # Importar las funciones
        from input_gen import generate_input_file
        from output_gen import generate_output_file
        import os
        
        # Generar el archivo input.img en el directorio actual
        success_input = generate_input_file(self.current_section)
        
        if success_input:
            input_path = os.path.join(os.getcwd(), "input.img")
            
            # Generar el archivo output.img
            success_output = generate_output_file()
            
            if success_output:
                output_path = os.path.join(os.getcwd(), "output.img")
                
                # Mostrar mensaje al usuario
                self.info_label.config(
                    text=f"Archivos input.img y output.img generados correctamente para la sección {self.section_position[0]*4+self.section_position[1]+1}"
                )
                
                # Cambiar a la vista de resultados
                if self.controller:
                    self.controller.switch_to_result_view()
                    
            else:
                print("Error al generar el archivo output.img")
                # Mostrar mensaje de error al usuario
                self.info_label.config(
                    text="Error al generar el archivo output.img"
                )
        else:
            print("Error al generar el archivo input.img")
            # Mostrar mensaje de error al usuario
            self.info_label.config(
                text="Error al generar el archivo input.img"
            )
    
    def go_back(self):
        """Volver a la vista de secciones"""
        if self.controller:
            self.controller.switch_to_section_view()