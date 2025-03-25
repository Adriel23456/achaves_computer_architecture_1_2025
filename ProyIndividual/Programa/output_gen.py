import os
import subprocess

def generate_output_file(input_path=None, output_path=None):
    """
    Ejecuta el script run_output.sh para generar un archivo output.img aplicando
    interpolación bilineal a los datos contenidos en input.img.
    
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
        
        # Obtener el directorio del script actual
        current_dir = os.path.dirname(os.path.abspath(__file__))
        
        # Ruta del script run_output.sh
        script_path = os.path.join(current_dir, "run_output.sh")
        
        # Verificar que existe el script
        if not os.path.exists(script_path):
            print(f"Error: No se encontró el script {script_path}")
            return False
        
        # Dar permisos de ejecución al script
        os.chmod(script_path, 0o755)
        
        # Ejecutar el script
        result = subprocess.run([script_path, input_path, output_path], cwd=current_dir)
        
        # Verificar que la ejecución fue exitosa
        if result.returncode != 0:
            print(f"Error: El script run_output.sh falló con código de salida {result.returncode}")
            return False
        
        # Verificar que se creó el archivo output.img
        if not os.path.exists(output_path):
            print(f"Error: No se creó el archivo {output_path}")
            return False
        
        return True
    
    except Exception as e:
        print(f"Error al generar el archivo output.img: {str(e)}")
        return False