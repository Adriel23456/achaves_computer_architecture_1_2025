import os

def generate_output_file(input_path=None, output_path=None):
    """
    Genera un archivo output.img aplicando interpolación bilineal a los datos
    contenidos en input.img.
    
    Args:
        input_path: Ruta del archivo de entrada (por defecto se busca en el directorio de ejecución)
        output_path: Ruta del archivo de salida (por defecto se guarda en el directorio de ejecución)
    
    Returns:
        bool: True si la operación fue exitosa, False en caso contrario
    """
    try:
        # Si no se especifica ruta, usar el directorio actual
        if input_path is None:
            input_path = os.path.join(os.getcwd(), "input.img")
        if output_path is None:
            output_path = os.path.join(os.getcwd(), "output.img")
        
        # Verificar que existe el archivo input.img
        if not os.path.exists(input_path):
            print(f"Error: No se encontró el archivo {input_path}")
            return False
        
        # Abrir el archivo input.img para lectura binaria
        with open(input_path, 'rb') as f_in:
            input_data = f_in.read()
        
        # Verificar que hay datos
        if len(input_data) == 0:
            print("Error: El archivo input.img está vacío")
            return False
        
        # Abrir el archivo output.img para escritura binaria
        with open(output_path, 'wb') as f_out:
            # Procesar datos en bloques de 4 bytes (cuadrantes 2x2)
            for i in range(0, len(input_data), 4):
                # Si no hay suficientes bytes para un cuadrante completo, salir
                if i + 3 >= len(input_data):
                    break
                
                # Obtener los 4 valores del cuadrante 2x2
                a = input_data[i]
                b = input_data[i+1]
                c = input_data[i+2]
                d = input_data[i+3]
                
                # Calcular valores interpolados horizontales y verticales
                a1 = int((2/3)*a + (1/3)*b)
                b1 = int((1/3)*a + (2/3)*b)
                c1 = int((2/3)*a + (1/3)*c)
                g1 = int((1/3)*a + (2/3)*c)
                k1 = int((2/3)*c + (1/3)*d)
                l1 = int((1/3)*c + (2/3)*d)
                f1 = int((2/3)*b + (1/3)*d)
                j1 = int((1/3)*b + (2/3)*d)
                
                # Calcular valores interpolados internos
                d1 = int((2/3)*c1 + (1/3)*f1)
                e1 = int((1/3)*c1 + (2/3)*f1)
                h1 = int((2/3)*g1 + (1/3)*j1)
                i1 = int((1/3)*g1 + (2/3)*j1)
                
                # Guardar los 16 valores del cuadrante 4x4 en el archivo de salida
                f_out.write(bytes([a, a1, b1, b,
                                  c1, d1, e1, f1,
                                  g1, h1, i1, j1,
                                  c, k1, l1, d]))
        
        return True
    
    except Exception as e:
        print(f"Error al generar el archivo output.img: {str(e)}")
        return False