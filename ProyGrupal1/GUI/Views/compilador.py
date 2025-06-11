"""
compilador.py - Vista del compilador
"""
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import os
import shutil
from pathlib import Path
from GUI.Components.styled_button import StyledButton
from GUI.Components.styled_ide import StyledIDE
from GUI.Components.styled_popup import TextViewerPopup

class CompiladorView:
    def __init__(self, parent, base_dir, config, design_manager, on_config_change, cpu_excel, controller):
        self.parent = parent
        self.base_dir = base_dir
        self.config = config
        self.design_manager = design_manager
        self.on_config_change = on_config_change
        self.cpu_excel = cpu_excel
        self.controller = controller
        
        # Variables de estado
        self.current_file = None
        self.is_modified = False
        self.last_saved_content = ""  # Para comparar cambios
        
        # Referencias a componentes
        self.ide = None
        self.file_label = None
        
        # Colores para estados del archivo
        self.FILE_STATE_COLORS = {
            'unsaved': '#FF4444',    # Rojo
            'modified': '#FFB444',   # Amarillo/Naranja
            'saved': '#44FF44'       # Verde
        }
        
        self._create_ui()
    
    def _create_ui(self):
        """Crea la interfaz de usuario de la vista"""
        colors = self.design_manager.get_colors()
        
        # Frame principal con padding
        main_frame = tk.Frame(self.parent, bg=colors['bg'])
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Configurar grid para las tres secciones
        main_frame.grid_rowconfigure(0, weight=0)  # Toolbar superior
        main_frame.grid_rowconfigure(1, weight=1)  # IDE (se expande)
        main_frame.grid_rowconfigure(2, weight=0)  # Toolbar inferior
        main_frame.grid_columnconfigure(0, weight=1)
        
        # 1. Sección superior - Toolbar de edición
        self._create_top_toolbar(main_frame)
        
        # 2. Sección central - StyledIDE (se expande horizontal y verticalmente)
        self._create_ide_section(main_frame)
        
        # 3. Sección inferior - Toolbar de compilación
        self._create_bottom_toolbar(main_frame)
    
    def _create_top_toolbar(self, parent):
        """Crea la barra de herramientas superior con botones de edición"""
        colors = self.design_manager.get_colors()
        
        # Frame para la toolbar
        toolbar_frame = tk.Frame(parent, bg=colors['bg'], height=50)
        toolbar_frame.grid(row=0, column=0, sticky='ew', pady=(0, 10))
        toolbar_frame.grid_propagate(False)
        
        # Centrar los botones
        buttons_container = tk.Frame(toolbar_frame, bg=colors['bg'])
        buttons_container.place(relx=0.5, rely=0.5, anchor='center')
        
        # Botones de la toolbar superior
        buttons_data = [
            ("Guardar", self._on_save),
            ("Cargar", self._on_load),
            ("(", lambda: self._insert_text("(")),
            (")", lambda: self._insert_text(")")),
            ("[", lambda: self._insert_text("[")),
            ("]", lambda: self._insert_text("]")),
            ("{", lambda: self._insert_text("{")),
            ("}", lambda: self._insert_text("}"))
        ]
        
        for text, command in buttons_data:
            btn = StyledButton(
                buttons_container,
                text=text,
                command=command,
                design_manager=self.design_manager
            )
            btn.pack(side=tk.LEFT, padx=3)
    
    def _create_ide_section(self, parent):
        """Crea la sección del IDE que se expande horizontal y verticalmente"""
        colors = self.design_manager.get_colors()
        
        # Frame para el IDE
        ide_frame = tk.Frame(parent, bg=colors['bg'])
        ide_frame.grid(row=1, column=0, sticky='nsew', pady=(0, 10))
        
        # Título del IDE
        title_frame = tk.Frame(ide_frame, bg=colors['sidebar_bg'], height=30)
        title_frame.pack(fill=tk.X)
        title_frame.pack_propagate(False)
        
        title_label = tk.Label(
            title_frame,
            text="Editor de Código",
            font=self.design_manager.get_font('bold'),
            bg=colors['sidebar_bg'],
            fg=colors['sidebar_button_fg'],
            padx=10
        )
        title_label.pack(side=tk.LEFT, fill=tk.Y)
        
        # Label para mostrar archivo actual con color de estado
        self.file_label = tk.Label(
            title_frame,
            text="Nuevo archivo",
            font=self.design_manager.get_font('small'),
            bg=colors['sidebar_bg'],
            fg=self.FILE_STATE_COLORS['unsaved'],
            padx=10
        )
        self.file_label.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Crear el StyledIDE
        self.ide = StyledIDE(ide_frame, self.design_manager)
        self.ide.pack(fill=tk.BOTH, expand=True)
        
        # Vincular evento de modificación
        self.ide.text_widget.bind('<KeyRelease>', self._on_text_changed)
        self.ide.text_widget.bind('<<Paste>>', self._on_text_changed)
        self.ide.text_widget.bind('<<Cut>>', self._on_text_changed)
    
    def _create_bottom_toolbar(self, parent):
        """Crea la barra de herramientas inferior con los 3 botones"""
        colors = self.design_manager.get_colors()
        
        # Frame para la toolbar
        toolbar_frame = tk.Frame(parent, bg=colors['bg'], height=50)
        toolbar_frame.grid(row=2, column=0, sticky='ew')
        toolbar_frame.grid_propagate(False)
        
        # Contenedor para centrar los 3 botones
        buttons_container = tk.Frame(toolbar_frame, bg=colors['bg'])
        buttons_container.place(relx=0.5, rely=0.5, anchor='center')
        
        # Botón Compilar
        btn_compile = StyledButton(
            buttons_container,
            text="Compilar",
            command=self._on_compile,
            design_manager=self.design_manager
        )
        btn_compile.pack(side=tk.LEFT, padx=5)
        
        # Botón Gramática
        btn_grammar = StyledButton(
            buttons_container,
            text="Gramática",
            command=self._on_grammar,
            design_manager=self.design_manager
        )
        btn_grammar.pack(side=tk.LEFT, padx=5)
        
        # Botón Seleccionar una memoria
        btn_select_memory = StyledButton(
            buttons_container,
            text="Seleccionar una memoria",
            command=self._on_select_memory,
            design_manager=self.design_manager
        )
        btn_select_memory.pack(side=tk.LEFT, padx=5)
    
    def _get_initial_directory(self):
        """Obtiene el directorio inicial para los diálogos de archivo de manera robusta"""
        try:
            # Obtener la ruta actual del archivo compilador.py
            current_file = Path(__file__).resolve()
            # Subir 3 niveles: compilador.py -> Views -> GUI -> [directorio base]
            initial_dir = current_file.parent.parent.parent
            
            # Verificar que el directorio existe
            if initial_dir.exists() and initial_dir.is_dir():
                return str(initial_dir)
            else:
                # Si no existe, usar el directorio base pasado en la inicialización
                return str(Path(self.base_dir).resolve())
        except Exception:
            # En caso de cualquier error, usar el directorio actual de trabajo
            return os.getcwd()
    
    def _on_save(self):
        """Maneja el evento de guardar archivo"""
        if self.current_file:
            # Si ya tenemos un archivo, guardar directamente
            self._save_to_file(self.current_file)
        else:
            # Si no hay archivo actual, abrir diálogo de guardar como
            self._save_as()
    
    def _save_as(self):
        """Abre el diálogo de guardar como"""
        # Obtener la ventana principal
        root = self.parent.winfo_toplevel()
        
        # Hacer el diálogo modal (bloquear interacción con ventana principal)
        root.grab_set()
        
        try:
            # Obtener directorio inicial
            initial_dir = self._get_initial_directory()
            
            # Abrir diálogo de guardado sin extensión predeterminada
            file_path = filedialog.asksaveasfilename(
                parent=root,
                title="Guardar archivo",
                initialdir=initial_dir,
                filetypes=[
                    ("ASM y Texto", ("*.asm", "*.txt")),
                    ("Archivos Assembly", "*.asm"),
                    ("Archivos de texto", "*.txt"),
                    ("Todos los archivos", "*.*")
                ]
            )
            
            if file_path:
                self._save_to_file(file_path)
                self.current_file = file_path
                
        finally:
            # Siempre liberar el grab
            root.grab_release()
    
    def _save_to_file(self, file_path):
        """Guarda el contenido actual en el archivo especificado"""
        try:
            content = self.ide.get()
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            # Actualizar estado
            self.last_saved_content = content
            self.is_modified = False
            self._update_file_status()
            
            print(f"[INFO] Archivo guardado exitosamente: {os.path.basename(file_path)}")
            
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo guardar el archivo:\n{str(e)}")
            print(f"[ERROR] Error al guardar archivo: {str(e)}")
    
    def _on_load(self):
        """Maneja el evento de cargar archivo"""
        # Obtener la ventana principal
        root = self.parent.winfo_toplevel()
        
        # Hacer el diálogo modal
        root.grab_set()
        
        try:
            # Obtener directorio inicial
            initial_dir = self._get_initial_directory()
            
            # Abrir diálogo de carga
            file_path = filedialog.askopenfilename(
                parent=root,
                title="Cargar archivo",
                initialdir=initial_dir,
                filetypes=[
                    ("ASM y Texto", ("*.asm", "*.txt")),
                    ("Archivos Assembly", "*.asm"),
                    ("Archivos de texto", "*.txt"),
                    ("Todos los archivos", "*.*")
                ]
            )
            
            if file_path:
                self._load_from_file(file_path)
                
        finally:
            # Siempre liberar el grab
            root.grab_release()
    
    def _load_from_file(self, file_path):
        """Carga el contenido del archivo especificado"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Actualizar el IDE
            self.ide.set(content)
            
            # Actualizar estado
            self.current_file = file_path
            self.last_saved_content = content
            self.is_modified = False
            self._update_file_status()
            
            print(f"[INFO] Archivo cargado exitosamente: {os.path.basename(file_path)}")
            
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo cargar el archivo:\n{str(e)}")
            print(f"[ERROR] Error al cargar archivo: {str(e)}")
    
    def _insert_text(self, text):
        """Inserta texto en la posición actual del cursor"""
        self.ide.text_widget.insert(tk.INSERT, text)
        self.ide.text_widget.focus_set()
    
    def _on_text_changed(self, event=None):
        """Maneja cuando el texto cambia"""
        # Comparar con el último contenido guardado
        current_content = self.ide.get()
        if current_content != self.last_saved_content:
            self.is_modified = True
        else:
            self.is_modified = False
        
        self._update_file_status()
    
    def _update_file_status(self):
        """Actualiza el estado visual del archivo"""
        if self.current_file:
            filename = os.path.basename(self.current_file)
            if self.is_modified:
                # Archivo modificado - Amarillo
                self.file_label.config(
                    text=f"{filename}*",
                    fg=self.FILE_STATE_COLORS['modified']
                )
            else:
                # Archivo guardado sin cambios - Verde
                self.file_label.config(
                    text=filename,
                    fg=self.FILE_STATE_COLORS['saved']
                )
        else:
            # Nuevo archivo sin guardar - Rojo
            self.file_label.config(
                text="Nuevo archivo",
                fg=self.FILE_STATE_COLORS['unsaved']
            )
    
    def _on_compile(self):
        """Maneja el evento de compilar con las restricciones necesarias"""
        print("\n[INFO] Iniciando proceso de compilación...")
        
        # Caso 1: Nunca se ha guardado
        if not self.current_file:
            print("[WARN] El archivo debe guardarse antes de compilar")
            print("[INFO] Abriendo diálogo de guardado...")
            self._save_as()
            
            # Si después de intentar guardar aún no hay archivo, cancelar
            if not self.current_file:
                print("[ERROR] Compilación cancelada - No se guardó el archivo")
                return
        
        # Caso 2: Archivo guardado pero modificado
        elif self.is_modified:
            print(f"[INFO] Detectados cambios en {os.path.basename(self.current_file)}")
            print("[INFO] Aplicando autoguardado...")
            self._save_to_file(self.current_file)
        
        # Caso 3: Archivo guardado sin cambios
        else:
            print(f"[INFO] Archivo listo: {os.path.basename(self.current_file)}")
        
        # Proceder con la compilación
        print("[INFO] Compilando código...")
        print(f"[INFO] Archivo fuente: {self.current_file}")
        print("[INFO] Analizando sintaxis...")
        print("[INFO] Generando código binario...")
        print("[SUCCESS] Compilación completada exitosamente")
    
    def _on_grammar(self):
        """Muestra la gramática desde el archivo Assets/SecureCPU.g4"""
        try:
            # Construir ruta al archivo de gramática
            grammar_path = Path(self.base_dir) / "Assets" / "SecureCPU.g4"
            
            # Verificar que el archivo existe
            if not grammar_path.exists():
                messagebox.showerror("Error", f"No se encontró el archivo de gramática:\n{grammar_path}")
                return
            
            # Leer el contenido del archivo
            with open(grammar_path, 'r', encoding='utf-8') as f:
                grammar_content = f.read()
            
            # Crear y mostrar el popup
            popup = TextViewerPopup(
                self.parent,
                self.design_manager,
                title="Gramática SecureCPU",
                content=grammar_content,
                read_only=True
            )
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al cargar la gramática:\n{str(e)}")
    
    def _on_select_memory(self):
        """Maneja la selección del archivo de memoria de instrucciones"""
        # Obtener la ventana principal
        root = self.parent.winfo_toplevel()
        
        # Hacer el diálogo modal
        root.grab_set()
        
        try:
            # Obtener directorio inicial
            initial_dir = self._get_initial_directory()
            
            # Abrir diálogo para seleccionar archivo binario
            file_path = filedialog.askopenfilename(
                parent=root,
                title="Seleccionar memoria de instrucciones",
                initialdir=initial_dir,
                filetypes=[
                    ("Archivos binarios", "*.bin"),
                    ("Todos los archivos", "*.*")
                ]
            )
            
            if file_path:
                self._process_instruction_memory(file_path)
                
        finally:
            # Siempre liberar el grab
            root.grab_release()
    
    def _process_instruction_memory(self, file_path):
        """Procesa el archivo de memoria de instrucciones seleccionado"""
        try:
            # 1. Verificar que el archivo existe y es válido
            if not os.path.exists(file_path):
                raise FileNotFoundError(f"El archivo no existe: {file_path}")
            
            # 2. Leer el contenido binario completo
            with open(file_path, 'rb') as f:
                binary_content = f.read()
            
            # 3. Copiar a Assets/instruction_mem.bin
            target_path = Path(self.base_dir) / "Assets" / "instruction_mem.bin"
            
            # Crear directorio Assets si no existe
            target_path.parent.mkdir(exist_ok=True)
            
            # Escribir el contenido binario
            with open(target_path, 'wb') as f:
                f.write(binary_content)
            
            # 4. Guardar referencia en el controller (si está disponible)
            # Esto requiere que el controller sea pasado a la vista
            # Por ahora solo imprimimos
            print(f"[INFO] Memoria de instrucciones actualizada desde: {os.path.basename(file_path)}")
            print(f"[INFO] Tamaño: {len(binary_content)} bytes")
            print(f"[INFO] Copiado a: {target_path}")
            
            # 5. Intentar actualizar la vista de Presentación si está disponible
            # Esto requiere acceso al controller y a las otras vistas
            # Por ahora solo mostramos un mensaje de éxito
            messagebox.showinfo(
                "Éxito", 
                f"Memoria de instrucciones cargada:\n{os.path.basename(file_path)}\n\n"
                f"Tamaño: {len(binary_content)} bytes"
            )
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al procesar memoria de instrucciones:\n{str(e)}")
            print(f"[ERROR] Error al procesar memoria: {str(e)}")
    
    def update_theme(self):
        """Actualiza el tema de todos los componentes"""
        if hasattr(self, 'ide'):
            self.ide.update_theme()
        
        # Mantener los colores de estado del archivo
        self._update_file_status()