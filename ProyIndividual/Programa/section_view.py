import tkinter as tk
from tkinter import ttk
from PIL import ImageTk
from base_view import BaseView

class SectionView(BaseView):
    """Vista para mostrar y seleccionar secciones de la imagen"""
    
    def __init__(self, parent, view_manager=None):
        super().__init__(parent, view_manager)
        
        # Referencia al controlador
        self.controller = None
        
        # Imagen actual y secciones
        self.current_image = None
        self.section_buttons = []
        self.section_images = []  # Para mantener referencias
        
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
            text="Selección de Secciones",
            font=("Helvetica", 16, "bold"),
            bg="#121212",
            fg="white"
        )
        self.title_label.pack(pady=(20, 10))
        
        # Información
        self.info_label = tk.Label(
            self.frame,
            text="Seleccione una de las 16 secciones de la imagen",
            font=("Helvetica", 11),
            bg="#121212",
            fg="#aaaaaa"
        )
        self.info_label.pack(pady=(0, 20))
        
        # Frame para la cuadrícula de secciones
        self.grid_frame = ttk.Frame(self.frame, style='Image.TFrame')
        self.grid_frame.pack(pady=10, padx=20, fill="both", expand=True)
        
        # Crear cuadrícula 4x4 para las secciones
        self.section_grid = ttk.Frame(self.grid_frame, style='Main.TFrame')
        self.section_grid.pack(pady=20, padx=20)
        
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
        
        self.next_button = ttk.Button(
            self.button_frame,
            text="Siguiente Sección",
            style='TButton',
            command=self.next_section
        )
        self.next_button.pack(side=tk.RIGHT, padx=10)
    
    def on_view_shown(self, **kwargs):
        """Método llamado cuando la vista se muestra"""
        if 'image' in kwargs:
            self.current_image = kwargs['image']
            self.display_sections()
    
    def display_sections(self):
        """Mostrar la cuadrícula de secciones"""
        if not self.current_image or not self.controller:
            return
            
        # Limpiar secciones anteriores
        for button in self.section_buttons:
            button.destroy()
        self.section_buttons = []
        self.section_images = []
        
        # Obtener todas las secciones
        sections = self.controller.image_model.get_all_sections()
        
        # Crear la cuadrícula de secciones
        for i, section_data in enumerate(sections):
            row = i // 4
            col = i % 4
            
            # Crear imagen para Tkinter
            img = ImageTk.PhotoImage(section_data['image'])
            self.section_images.append(img)  # Mantener referencia
            
            # Crear botón con la imagen
            section_button = tk.Button(
                self.section_grid,
                image=img,
                bd=1,
                bg="#1e1e1e",
                activebackground="#3e3e3e",
                command=lambda pos=section_data['position']: self.select_section(pos)
            )
            section_button.grid(row=row, column=col, padx=2, pady=2)
            self.section_buttons.append(section_button)
    
    def select_section(self, position):
        """Manejar la selección de una sección"""
        row, col = position
        section_number = row * 4 + col + 1
        
        # Marcar la sección seleccionada con un borde
        for i, button in enumerate(self.section_buttons):
            if i == (row * 4 + col):
                button.config(bd=3, highlightbackground="white", highlightthickness=3)
            else:
                button.config(bd=1, highlightbackground="#1e1e1e", highlightthickness=0)
        
        # Imprimir en consola la sección seleccionada
        print(f"Sección seleccionada: {section_number} (Fila: {row+1}, Columna: {col+1})")
        
        # Actualizar etiqueta de información
        self.info_label.config(
            text=f"Sección {section_number} seleccionada (Fila: {row+1}, Columna: {col+1})"
        )
    
    def go_back(self):
        """Volver a la vista principal"""
        if self.controller:
            self.controller.switch_to_main_view()
    
    def next_section(self):
        """Pasar a la siguiente sección (por ahora muestra mensaje)"""
        self.show_message(
            "Información", 
            "Esta funcionalidad será implementada en futuras versiones."
        )