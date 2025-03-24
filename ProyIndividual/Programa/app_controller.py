import tkinter as tk
from view_manager import ViewManager
from main_view import MainView
from section_view import SectionView
from image_model import ImageModel

class AppController:
    """Controlador principal de la aplicación"""
    
    def __init__(self, root):
        # Configurar ventana principal
        self.root = root
        self.root.title("Visor de Imágenes")
        self.root.configure(bg="#121212")
        
        # Establecer tamaño y centrar
        width, height = 1500, 850
        self.center_window(self.root, width, height)
        
        # Crear modelo compartido
        self.image_model = ImageModel()
        
        # Inicializar el administrador de vistas
        self.view_manager = ViewManager(root)
        
        # Crear y registrar vistas
        self.init_views()
        
        # Mostrar la vista principal
        self.view_manager.show_view("main")
    
    def init_views(self):
        """Inicializar todas las vistas de la aplicación"""
        # Vista principal
        main_view = MainView(self.root, self.view_manager)
        self.view_manager.register_view("main", main_view)
        
        # Vista de secciones
        section_view = SectionView(self.root, self.view_manager)
        self.view_manager.register_view("section", section_view)
        
        # Configurar comunicación entre vistas y controlador
        main_view.set_controller(self)
        section_view.set_controller(self)
    
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
    
    def load_image(self, file_path):
        """Cargar una imagen en el modelo compartido"""
        success = self.image_model.load_image(file_path)
        return success
    
    def get_display_image(self):
        """Obtener la imagen procesada para mostrar"""
        return self.image_model.get_display_image()
    
    def get_image_info(self):
        """Obtener información de la imagen"""
        return self.image_model.get_image_info()
    
    def get_processed_image(self):
        """Obtener la imagen procesada (objeto PIL)"""
        return self.image_model.processed_image
    
    def has_image(self):
        """Verificar si hay una imagen cargada"""
        return self.image_model.has_image()
    
    def switch_to_section_view(self):
        """Cambiar a la vista de secciones"""
        if self.has_image():
            self.view_manager.show_view("section", image=self.get_processed_image())
    
    def switch_to_main_view(self):
        """Cambiar a la vista principal"""
        self.view_manager.show_view("main")