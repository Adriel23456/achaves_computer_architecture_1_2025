import openpyxl
from openpyxl import Workbook
import threading
import queue
from enum import Enum
from typing import Union, Tuple, Optional, Any, List
import time
import os
from datetime import datetime


class ActionType(Enum):
    """Tipos de acciones que puede realizar TableControl"""
    READ = "READ"
    WRITE = "WRITE"


class DataType(Enum):
    """Tipos de datos soportados"""
    STRING = "string"
    INT = "int"
    BINARY = "binary"
    HEX = "hex"


class TableAction:
    """Representa una acción en la cola"""
    def __init__(self, action_type: ActionType, row: int, column: int, 
                 content: Any = None, callback: callable = None):
        self.action_type = action_type
        self.row = row
        self.column = column
        self.content = content
        self.callback = callback
        self.timestamp = datetime.now()


class TableControl:
    """
    Clase Singleton para controlar lectura/escritura de archivos Excel.
    Implementa una cola FIFO para procesar acciones de forma manual.
    """
    _instance = None
    _lock = threading.Lock()
    
    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super(TableControl, cls).__new__(cls)
                    cls._instance._initialized = False
        return cls._instance
    
    def __init__(self, filename: str = "Assets/table_data.xlsx"):
        """
        Inicializa TableControl con un archivo Excel.
        
        Args:
            filename: Nombre del archivo Excel a utilizar
        """
        if self._initialized:
            return
            
        self.filename = filename
        self.action_queue = queue.Queue()
        self.workbook = None
        self.worksheet = None
        
        # Crear directorio Assets si no existe
        os.makedirs("Assets", exist_ok=True)
        
        # Inicializar archivo Excel
        self._initialize_excel()
        
        self._initialized = True
        print("✓ TableControl inicializado en modo MANUAL")
        
    def _initialize_excel(self):
        """Inicializa o carga el archivo Excel"""
        try:
            if os.path.exists(self.filename):
                self.workbook = openpyxl.load_workbook(self.filename)
                self.worksheet = self.workbook.active
                print(f"✓ Archivo '{self.filename}' cargado exitosamente")
            else:
                self.workbook = Workbook()
                self.worksheet = self.workbook.active
                self.worksheet.title = "Datos"
                
                # Agregar encabezados de ejemplo
                headers = ["String", "Integer", "Binary", "Hexadecimal", "Mixed"]
                for idx, header in enumerate(headers, 1):
                    self.worksheet.cell(row=1, column=idx, value=header)
                
                # Ajustar ancho de columnas
                for column in self.worksheet.columns:
                    self.worksheet.column_dimensions[column[0].column_letter].width = 25
                
                self._save_workbook()
                print(f"✓ Archivo '{self.filename}' creado exitosamente")
                
        except Exception as e:
            print(f"✗ Error al inicializar Excel: {e}")
            raise
    
    def _save_workbook(self):
        """Guarda el archivo Excel de forma segura"""
        try:
            # Intentar guardar directamente
            self.workbook.save(self.filename)
        except PermissionError:
            # Si el archivo está abierto, intentar guardar con otro nombre
            backup_name = f"Assets/table_data_temp.xlsx"
            self.workbook.save(backup_name)
            print(f"⚠ Archivo principal bloqueado, guardado en: {backup_name}")
        except Exception as e:
            print(f"✗ Error al guardar: {e}")
    
    def execute_all(self):
        """Ejecuta todas las acciones pendientes en la cola en orden FIFO"""
        executed = 0
        total_actions = self.action_queue.qsize()
        
        if total_actions == 0:
            print("⚠ No hay acciones pendientes en la cola")
            return 0
        
        print(f"\n🚀 Ejecutando {total_actions} acciones pendientes...")
        
        while not self.action_queue.empty():
            try:
                action = self.action_queue.get_nowait()
                self._execute_action(action)
                self.action_queue.task_done()
                executed += 1
            except queue.Empty:
                break
            except Exception as e:
                print(f"✗ Error ejecutando acción: {e}")
        
        print(f"✓ {executed} acciones ejecutadas")
        return executed
    
    def execute_reads_only(self):
        """Ejecuta solo las acciones de lectura en orden FIFO"""
        # Obtener todas las acciones de la cola
        actions = []
        while not self.action_queue.empty():
            try:
                actions.append(self.action_queue.get_nowait())
            except queue.Empty:
                break
        
        # Separar lecturas y escrituras
        reads = [a for a in actions if a.action_type == ActionType.READ]
        writes = [a for a in actions if a.action_type == ActionType.WRITE]
        
        if len(reads) == 0:
            print("⚠ No hay acciones de lectura en la cola")
            # Devolver las escrituras a la cola
            for action in writes:
                self.action_queue.put(action)
            return 0
        
        print(f"\n📖 Ejecutando {len(reads)} acciones de LECTURA...")
        
        # Ejecutar solo las lecturas
        executed = 0
        for action in reads:
            try:
                self._execute_action(action)
                executed += 1
            except Exception as e:
                print(f"✗ Error ejecutando lectura: {e}")
        
        # Devolver las escrituras a la cola
        for action in writes:
            self.action_queue.put(action)
        
        print(f"✓ {executed} lecturas ejecutadas")
        print(f"💾 {len(writes)} escrituras permanecen en la cola")
        return executed
    
    def execute_writes_only(self):
        """Ejecuta solo las acciones de escritura en orden FIFO"""
        # Obtener todas las acciones de la cola
        actions = []
        while not self.action_queue.empty():
            try:
                actions.append(self.action_queue.get_nowait())
            except queue.Empty:
                break
        
        # Separar lecturas y escrituras
        reads = [a for a in actions if a.action_type == ActionType.READ]
        writes = [a for a in actions if a.action_type == ActionType.WRITE]
        
        if len(writes) == 0:
            print("⚠ No hay acciones de escritura en la cola")
            # Devolver las lecturas a la cola
            for action in reads:
                self.action_queue.put(action)
            return 0
        
        print(f"\n✏️ Ejecutando {len(writes)} acciones de ESCRITURA...")
        
        # Ejecutar solo las escrituras
        executed = 0
        for action in writes:
            try:
                self._execute_action(action)
                executed += 1
            except Exception as e:
                print(f"✗ Error ejecutando escritura: {e}")
        
        # Devolver las lecturas a la cola
        for action in reads:
            self.action_queue.put(action)
        
        print(f"✓ {executed} escrituras ejecutadas")
        print(f"📖 {len(reads)} lecturas permanecen en la cola")
        return executed
    
    def reorder_reads_first(self):
        """Reordena la cola para que todas las lecturas estén primero, luego las escrituras"""
        # Obtener todas las acciones de la cola
        actions = []
        while not self.action_queue.empty():
            try:
                actions.append(self.action_queue.get_nowait())
            except queue.Empty:
                break
        
        # Separar lecturas y escrituras manteniendo su orden original
        reads = [a for a in actions if a.action_type == ActionType.READ]
        writes = [a for a in actions if a.action_type == ActionType.WRITE]
        
        # Volver a llenar la cola con lecturas primero, luego escrituras
        for action in reads:
            self.action_queue.put(action)
        for action in writes:
            self.action_queue.put(action)
        
        print(f"\n🔄 Cola reordenada: {len(reads)} lecturas primero, {len(writes)} escrituras después")
        print(f"📊 Total de acciones en cola: {self.get_queue_size()}")
    
    def _execute_action(self, action: TableAction):
        """Ejecuta una acción individual"""
        print(f"\n📋 Procesando acción: {action.action_type.value} "
              f"en [{action.row}, {action.column}]")
        
        if action.action_type == ActionType.WRITE:
            self._execute_write(action)
        elif action.action_type == ActionType.READ:
            self._execute_read(action)
    
    def _execute_write(self, action: TableAction):
        """Ejecuta una acción de escritura"""
        try:
            # Procesar y validar el contenido
            content, display_value = self._process_content(action.content)
            
            # Escribir en la celda
            self.worksheet.cell(row=action.row, column=action.column, value=display_value)
            
            # Guardar archivo
            self._save_workbook()
            
            print(f"✓ Escrito '{display_value}' en celda [{action.row}, {action.column}]")
            
            # Ejecutar callback si existe
            if action.callback:
                action.callback(True, content)
                
        except Exception as e:
            print(f"✗ Error en escritura: {e}")
            if action.callback:
                action.callback(False, str(e))
    
    def _execute_read(self, action: TableAction):
        """Ejecuta una acción de lectura"""
        try:
            # Leer valor de la celda
            cell_value = self.worksheet.cell(row=action.row, column=action.column).value
            
            print(f"✓ Leído '{cell_value}' de celda [{action.row}, {action.column}]")
            
            # Ejecutar callback con el valor
            if action.callback:
                action.callback(True, cell_value)
            
            return cell_value
            
        except Exception as e:
            print(f"✗ Error en lectura: {e}")
            if action.callback:
                action.callback(False, str(e))
            return None
    
    def _process_content(self, content: Any) -> Tuple[Any, str]:
        """
        Procesa el contenido según su tipo y retorna (valor_procesado, valor_display)
        
        Soporta:
        - String: 'texto' o "texto"
        - Int: 0d12345 (decimal)
        - Binary: 0b1010101
        - Hex: 0xDEADBEEF
        """
        if content is None:
            return None, "None"
        
        content_str = str(content)
        
        # String con comillas
        if ((content_str.startswith("'") and content_str.endswith("'")) or 
            (content_str.startswith('"') and content_str.endswith('"'))):
            # Remover comillas
            actual_content = content_str[1:-1]
            return actual_content, f"String: '{actual_content}'"
        
        # Entero decimal con prefijo 0d
        elif content_str.startswith("0d"):
            try:
                decimal_value = int(content_str[2:])
                return decimal_value, f"Int: 0d{decimal_value}"
            except ValueError:
                raise ValueError(f"Valor decimal inválido: {content_str}")
        
        # Binario con prefijo 0b
        elif content_str.startswith("0b"):
            try:
                binary_str = content_str[2:]
                # Validar que solo contenga 0 y 1
                if all(c in '01' for c in binary_str):
                    # Para números grandes, guardar como string
                    if len(binary_str) > 64:
                        return binary_str, f"Binary(large): 0b{binary_str}"
                    else:
                        decimal_value = int(content_str, 2)
                        return decimal_value, f"Binary: 0b{binary_str}"
                else:
                    raise ValueError(f"Valor binario inválido: {content_str}")
            except ValueError as e:
                raise ValueError(f"Error procesando binario: {e}")
        
        # Hexadecimal con prefijo 0x o 0X
        elif content_str.lower().startswith("0x"):
            try:
                hex_str = content_str[2:]
                # Validar caracteres hexadecimales
                if all(c in '0123456789abcdefABCDEF' for c in hex_str):
                    # Para números grandes, guardar como string
                    if len(hex_str) > 16:
                        return hex_str.upper(), f"Hex(large): 0x{hex_str.upper()}"
                    else:
                        decimal_value = int(content_str, 16)
                        return decimal_value, f"Hex: 0x{hex_str.upper()}"
                else:
                    raise ValueError(f"Valor hexadecimal inválido: {content_str}")
            except ValueError as e:
                raise ValueError(f"Error procesando hexadecimal: {e}")
        
        # Si es un entero simple sin prefijo
        elif isinstance(content, int) and not isinstance(content, bool):
            return content, f"Int: 0d{content}"
        
        # Cualquier otro caso, tratar como string sin comillas
        else:
            return content_str, f"String: '{content_str}'"
    
    def write(self, row: int, column: int, content: Any, callback: callable = None):
        """
        Agrega una acción de escritura a la cola.
        
        Args:
            row: Fila donde escribir (1-indexed)
            column: Columna donde escribir (1-indexed)
            content: Contenido a escribir (formatos: 'string', 0d123, 0b101, 0xABC)
            callback: Función a llamar cuando se complete (opcional)
        """
        action = TableAction(ActionType.WRITE, row, column, content, callback)
        self.action_queue.put(action)
        print(f"➕ Acción de escritura agregada a la cola (Total: {self.get_queue_size()})")
    
    def read(self, row: int, column: int, callback: callable = None):
        """
        Agrega una acción de lectura a la cola.
        
        Args:
            row: Fila de donde leer (1-indexed)
            column: Columna de donde leer (1-indexed)
            callback: Función a llamar con el resultado
        """
        action = TableAction(ActionType.READ, row, column, callback=callback)
        self.action_queue.put(action)
        print(f"➕ Acción de lectura agregada a la cola (Total: {self.get_queue_size()})")
    
    def get_queue_size(self) -> int:
        """Retorna el número de acciones pendientes en la cola"""
        return self.action_queue.qsize()
    
    def clear_queue(self):
        """Limpia todas las acciones pendientes en la cola"""
        cleared = 0
        while not self.action_queue.empty():
            try:
                self.action_queue.get_nowait()
                cleared += 1
            except queue.Empty:
                break
        print(f"🗑️ {cleared} acciones eliminadas de la cola")
        return cleared
    
    def __del__(self):
        """Limpieza al destruir la instancia"""
        if hasattr(self, 'workbook') and self.workbook:
            self.workbook.close()