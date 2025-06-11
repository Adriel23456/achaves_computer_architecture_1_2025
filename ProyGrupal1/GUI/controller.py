"""
controller.py - Controlador para manejar las vistas y su navegación
"""
import importlib
import tkinter as tk
from tkinter import ttk

class ViewController:
    def __init__(self, parent_frame, base_dir, config, design_manager, on_config_change, cpu_excel):
        self.parent_frame = parent_frame
        self.base_dir = base_dir
        self.config = config
        self.design_manager = design_manager
        self.on_config_change = on_config_change
        self.cpu_excel = cpu_excel
        
        # Cache de vistas cargadas
        self.loaded_views = {}
        
        # Vista actual
        self.current_view = None
        self.current_view_name = None
        
        # Mapeo de nombres a módulos y clases (sin tildes en las clases)
        self.view_mapping = {
            "Presentación": {
                "module": "GUI.Views.presentacion",
                "class": "PresentacionView"  # Sin tilde
            },
            "Compilador": {
                "module": "GUI.Views.compilador",
                "class": "CompiladorView"
            },
            "CPU": {
                "module": "GUI.Views.cpu",
                "class": "CPUView"
            },
            "Análisis": {
                "module": "GUI.Views.analisis",
                "class": "AnalisisView"  # Sin tilde
            },
            "Configuración": {
                "module": "GUI.Views.configuracion",
                "class": "ConfiguracionView"  # Sin tilde
            },
            "Créditos": {
                "module": "GUI.Views.creditos",
                "class": "CreditosView"  # Sin tilde
            }
        }
    
    def show_view(self, view_name):
        """Muestra la vista especificada"""
        # Si ya es la vista actual, no hacer nada
        if view_name == self.current_view_name:
            return
        
        # Ocultar vista actual si existe
        if self.current_view:
            self.current_view.hide()
        
        # Cargar o mostrar la nueva vista
        if view_name in self.loaded_views:
            # Vista ya cargada, solo mostrarla
            self.current_view = self.loaded_views[view_name]
            self.current_view.show()
        else:
            # Cargar nueva vista
            self._load_view(view_name)
        
        self.current_view_name = view_name
    
    def _load_view(self, view_name):
        """Carga una vista desde su módulo"""
        try:
            # Obtener información del mapeo
            view_info = self.view_mapping.get(view_name)
            if not view_info:
                raise ValueError(f"Vista '{view_name}' no encontrada en el mapeo")
            
            # Importar el módulo de la vista
            module_name = view_info["module"]
            module = importlib.import_module(module_name)
            
            # Obtener la clase de la vista (sin tildes)
            view_class_name = view_info["class"]
            view_class = getattr(module, view_class_name)
            
            # Crear frame para la vista
            view_frame = ttk.Frame(self.parent_frame)
            view_frame.pack(fill=tk.BOTH, expand=True)
            
            # Instanciar la vista
            view_instance = view_class(
                view_frame, 
                self.base_dir, 
                self.config,
                self.design_manager,
                self.on_config_change,
                self.cpu_excel,
                self
            )
            
            # Agregar métodos de control a la vista
            view_instance.frame = view_frame
            view_instance.show = lambda: view_frame.pack(fill=tk.BOTH, expand=True)
            view_instance.hide = lambda: view_frame.pack_forget()
            
            # Guardar en cache
            self.loaded_views[view_name] = view_instance
            self.current_view = view_instance
            
        except Exception as e:
            # En caso de error, mostrar mensaje
            error_frame = ttk.Frame(self.parent_frame)
            error_frame.pack(fill=tk.BOTH, expand=True)
            
            error_label = ttk.Label(
                error_frame,
                text=f"Error al cargar la vista '{view_name}':\n{str(e)}",
                font=self.design_manager.get_font('normal')
            )
            error_label.pack(expand=True)
            
            # Crear vista temporal de error
            class ErrorView:
                def __init__(self):
                    self.frame = error_frame
                def show(self):
                    self.frame.pack(fill=tk.BOTH, expand=True)
                def hide(self):
                    self.frame.pack_forget()
            
            self.current_view = ErrorView()
    
    def refresh_current_view(self):
        """Actualiza la vista actual (útil cuando cambian las fuentes)"""
        # Guardar el nombre de la vista actual
        current_name = self.current_view_name
        
        # Limpiar TODO el caché para forzar la recreación de todas las vistas
        self.clear_cache()
        
        # Recargar la vista actual
        if current_name:
            self.current_view_name = None  # Forzar recarga
            self.show_view(current_name)
    
    def get_current_view(self):
        """Retorna la vista actual"""
        return self.current_view
    
    def get_view(self, view_name):
        """Retorna una vista específica del cache"""
        return self.loaded_views.get(view_name)
    
    def clear_cache(self):
        """Limpia el cache de vistas (útil para desarrollo)"""
        for view in self.loaded_views.values():
            if hasattr(view, 'frame'):
                view.frame.destroy()
        self.loaded_views.clear()
        self.current_view = None
        # No limpiar current_view_name aquí para poder recargar