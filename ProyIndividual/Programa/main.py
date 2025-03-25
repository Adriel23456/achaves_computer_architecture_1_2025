import tkinter as tk
from app_controller import AppController

def main():
    """Función principal para iniciar la aplicación"""
    # Crear ventana principal
    root = tk.Tk()
    
    # Inicializar el controlador de la aplicación
    app = AppController(root)
    
    # Iniciar bucle principal de eventos
    root.mainloop()

if __name__ == "__main__":
    main()