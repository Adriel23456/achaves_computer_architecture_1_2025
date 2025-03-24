from PIL import Image, ImageTk

class ImageModel:
    """Modelo para manejar la lógica de imágenes"""
    
    def __init__(self):
        self.image_path = None
        self.original_image = None
        self.processed_image = None
        self.display_image = None
        self.target_size = (500, 500)
        self.section_size = (125, 125)  # Tamaño de cada sección (16 secciones en total)
    
    def load_image(self, file_path):
        """Cargar una imagen desde el sistema de archivos"""
        try:
            self.image_path = file_path
            self.original_image = Image.open(file_path)
            self.process_image()
            return True
        except Exception as e:
            print(f"Error al cargar la imagen: {str(e)}")
            return False
    
    def process_image(self):
        """Procesar la imagen original (reescalar a 500x500)"""
        if self.original_image:
            # Reescalar la imagen sin mantener proporción
            self.processed_image = self.original_image.resize(
                self.target_size, 
                Image.LANCZOS
            )
    
    def get_display_image(self):
        """Obtener la imagen procesada en formato compatible con Tkinter"""
        if self.processed_image:
            self.display_image = ImageTk.PhotoImage(self.processed_image)
            return self.display_image
        return None
    
    def get_image_info(self):
        """Obtener información sobre la imagen cargada"""
        if self.original_image and self.image_path:
            original_size = self.original_image.size
            return {
                "path": self.image_path,
                "original_size": original_size,
                "new_size": self.target_size,
                "format": self.original_image.format
            }
        return None
    
    def has_image(self):
        """Verificar si hay una imagen cargada"""
        return self.processed_image is not None
    
    def get_section(self, row, col):
        """Obtener una sección específica de la imagen"""
        if not self.processed_image:
            return None
            
        # Calcular coordenadas de la sección
        left = col * self.section_size[0]
        upper = row * self.section_size[1]
        right = left + self.section_size[0]
        lower = upper + self.section_size[1]
        
        # Extraer la sección
        section = self.processed_image.crop((left, upper, right, lower))
        return section
    
    def get_all_sections(self):
        """Obtener todas las secciones de la imagen (16 en total)"""
        sections = []
        
        if not self.processed_image:
            return sections
            
        # Dividir en 4x4 secciones
        for row in range(4):
            for col in range(4):
                section = self.get_section(row, col)
                sections.append({
                    'image': section,
                    'position': (row, col),
                    'coordinates': (
                        col * self.section_size[0],
                        row * self.section_size[1],
                        (col + 1) * self.section_size[0],
                        (row + 1) * self.section_size[1]
                    )
                })
                
        return sections