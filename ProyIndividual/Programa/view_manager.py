class ViewManager:
    """Administrador de vistas para la aplicación"""
    
    def __init__(self, root):
        self.root = root
        self.views = {}
        self.current_view = None
        self.app_data = {}  # Datos compartidos entre vistas
    
    def register_view(self, view_id, view):
        """Registrar una vista en el administrador"""
        self.views[view_id] = view
        
    def show_view(self, view_id, **kwargs):
        """Mostrar una vista específica y ocultar las demás"""
        if view_id in self.views:
            # Ocultar vista actual si existe
            if self.current_view:
                self.views[self.current_view].hide()
                
            # Mostrar nueva vista
            self.views[view_id].show()
            
            # Pasar datos adicionales si son necesarios
            if hasattr(self.views[view_id], 'on_view_shown'):
                self.views[view_id].on_view_shown(**kwargs)
                
            # Actualizar vista actual
            self.current_view = view_id
            return True
        return False
    
    def set_data(self, key, value):
        """Almacenar datos para ser compartidos entre vistas"""
        self.app_data[key] = value
        
    def get_data(self, key, default=None):
        """Obtener datos compartidos"""
        return self.app_data.get(key, default)
        
    def close_all(self):
        """Cerrar todas las vistas"""
        for view in self.views.values():
            view.destroy()
        self.views = {}
        self.current_view = None