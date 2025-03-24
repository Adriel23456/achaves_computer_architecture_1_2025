import numpy as np
from PIL import Image

def load_input_image(filename="input.img"):
    """
    Carga la imagen de 128x128 píxeles desde un archivo binario 'filename'.
    
    En este archivo se guardan 16,384 bytes (cada byte representa un píxel en escala de grises 0-255),
    organizados en bloques de 2x2 píxeles. Cada bloque se almacena en el siguiente orden:
    
        byte 1, byte 2,
        byte 3, byte 4.
    
    Los bloques se almacenan secuencialmente en orden de filas y columnas dentro de la imagen.
    
    Devuelve la imagen reconstruida como un objeto PIL Image.
    """
    # Abrir el archivo en modo binario y leer todos los bytes
    with open(filename, 'rb') as f:
        data = np.frombuffer(f.read(), dtype=np.uint8)
    
    if data.size != 16384:
        raise ValueError(f"El archivo no contiene 16384 píxeles. Contiene {data.size} bytes.")
    
    # Inicializa la imagen de 128x128
    img = np.zeros((128, 128), dtype=np.uint8)
    idx = 0  # Índice para recorrer 'data'
    
    # Número de bloques por fila/columna (128/2 = 64)
    for block_row in range(64):
        for block_col in range(64):
            # Coordenadas de inicio del bloque en la imagen final
            row_start = block_row * 2
            col_start = block_col * 2
            
            # Asigna el bloque 2x2:
            img[row_start, col_start]       = data[idx]
            img[row_start, col_start + 1]   = data[idx + 1]
            img[row_start + 1, col_start]   = data[idx + 2]
            img[row_start + 1, col_start + 1] = data[idx + 3]
            idx += 4

    # Convertir a imagen PIL
    return Image.fromarray(img)

def load_output_image(filename="output.img"):
    """
    Carga la imagen de 256x256 píxeles desde un archivo binario 'filename'.
    
    En este archivo se guardan 65,536 bytes (cada byte representa un píxel en escala de grises 0-255),
    organizados en bloques de 4x4 píxeles. Cada bloque se almacena en el siguiente orden:
    
        byte a,  byte a1, byte b1, byte b,
        byte c1, byte d1, byte e1, byte f1,
        byte g1, byte h1, byte i1, byte j1,
        byte c,  byte k1, byte l1, byte d.
        
    Los bloques se almacenan secuencialmente en orden de filas y columnas dentro de la imagen.
    
    Devuelve la imagen reconstruida como un objeto PIL Image.
    """
    # Abrir el archivo en modo binario y leer todos los bytes
    with open(filename, 'rb') as f:
        data = np.frombuffer(f.read(), dtype=np.uint8)
    
    if data.size != 65536:
        raise ValueError(f"El archivo no contiene 65,536 píxeles. Contiene {data.size} bytes.")
    
    # La imagen final es de 256x256
    img = np.zeros((256, 256), dtype=np.uint8)
    idx = 0  # Índice para recorrer 'data'
    
    # La imagen se divide en bloques de 4x4.
    # Número de bloques en cada dimensión: 256 / 4 = 64
    for block_row in range(64):
        for block_col in range(64):
            # Coordenadas de inicio del bloque en la imagen final
            row_start = block_row * 4
            col_start = block_col * 4
            
            # Patrón específico de almacenamiento:
            # a, a1, b1, b,    <- Fila 0
            # c1, d1, e1, f1,  <- Fila 1
            # g1, h1, i1, j1,  <- Fila 2
            # c, k1, l1, d     <- Fila 3
            
            # Creamos el mapa de posiciones tal como se almacenan
            # Formato: (fila, columna) para cada uno de los 16 bytes
            mapping = [
                (0, 0), (0, 1), (0, 2), (0, 3),  # Fila 0: a, a1, b1, b
                (1, 0), (1, 1), (1, 2), (1, 3),  # Fila 1: c1, d1, e1, f1
                (2, 0), (2, 1), (2, 2), (2, 3),  # Fila 2: g1, h1, i1, j1
                (3, 0), (3, 1), (3, 2), (3, 3)   # Fila 3: c, k1, l1, d
            ]
            
            # Asignar los píxeles según el mapa
            for i, (r, c) in enumerate(mapping):
                img[row_start + r, col_start + c] = data[idx + i]
            
            idx += 16

    # Convertir a imagen PIL
    return Image.fromarray(img)

def save_as_jpg(image, filename):
    """
    Guarda una imagen PIL como archivo JPG.
    
    Args:
        image: Objeto PIL Image
        filename: Nombre del archivo de salida
    
    Returns:
        bool: True si la operación fue exitosa, False en caso contrario
    """
    try:
        image.save(filename)
        print(f"Imagen guardada exitosamente como {filename}")
        return True
    except Exception as e:
        print(f"Error al guardar la imagen {filename}: {str(e)}")
        return False