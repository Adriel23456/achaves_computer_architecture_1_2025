from PIL import Image
import numpy as np
import os

def generate_input_file(image, output_path=None):
    """
    Genera un archivo input.img que contiene los valores de píxeles
    en escala de grises organizados en cuadrantes de 2x2.
    Los valores se guardan en formato binario (1 byte por píxel).
    
    Args:
        image: Objeto de imagen PIL
        output_path: Ruta del archivo de salida (por defecto se guarda en el directorio de ejecución)
    
    Returns:
        bool: True si la operación fue exitosa, False en caso contrario
    """
    try:
        # Si no se especifica ruta, usar el directorio actual
        if output_path is None:
            output_path = os.path.join(os.getcwd(), "input.img")
            
        # Convertir a escala de grises si no lo está ya
        if image.mode != 'L':
            image = image.convert('L')
            
        # Obtener matriz de píxeles
        pixels = np.array(image)
        height, width = pixels.shape
        
        # Asegurarse de que la imagen sea de 128x128
        if height != 128 or width != 128:
            raise ValueError(f"La imagen debe ser de 128x128 píxeles, no {width}x{height}")
        
        # Abrir archivo para escritura binaria
        with open(output_path, 'wb') as f:
            # Recorrer la imagen en bloques de 2x2
            for i in range(0, height, 2):
                for j in range(0, width, 2):
                    # Asegurarse de que estamos dentro de los límites
                    if i >= height or j >= width:
                        continue
                        
                    # Escribir los píxeles del bloque 2x2 como valores binarios (1 byte por píxel)
                    f.write(bytes([pixels[i, j]]))        # Superior izquierdo
                    
                    if j+1 < width:
                        f.write(bytes([pixels[i, j+1]]))  # Superior derecho
                    
                    if i+1 < height:
                        f.write(bytes([pixels[i+1, j]]))  # Inferior izquierdo
                    
                    if i+1 < height and j+1 < width:
                        f.write(bytes([pixels[i+1, j+1]]))  # Inferior derecho
        
        return True
    
    except Exception as e:
        print(f"Error al generar el archivo input.img: {str(e)}")
        return False