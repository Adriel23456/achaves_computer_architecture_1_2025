"""
styled_console.py - Componente de consola con números de línea
"""
import tkinter as tk
from tkinter import ttk
from GUI.Components.styled_scrollbar import StyledVerticalScrollbar

class StyledConsole(tk.Frame):
    """Consola estilizada con números de línea y scroll vertical"""
    def __init__(self, parent, design_manager, **kwargs):
        self.design_manager = design_manager
        colors = design_manager.get_colors()
        
        super().__init__(parent, bg=colors['bg'], relief=tk.SOLID, borderwidth=1, **kwargs)
        self.configure(highlightbackground=colors['button_bg'])
        self.configure(highlightcolor=colors['select_bg'])
        self.configure(highlightthickness=1)
        
        # Variables internas
        self.line_count = 0
        
        # Frame principal
        main_frame = tk.Frame(self, bg=colors['bg'])
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Frame para números de línea
        self.line_numbers_frame = tk.Frame(main_frame, bg=colors['sidebar_bg'], width=50)
        self.line_numbers_frame.pack(side=tk.LEFT, fill=tk.Y)
        self.line_numbers_frame.pack_propagate(False)
        
        # Canvas para números de línea (mejor control de posicionamiento)
        self.line_numbers = tk.Canvas(
            self.line_numbers_frame,
            bg=colors['sidebar_bg'],
            highlightthickness=0,
            width=50
        )
        self.line_numbers.pack(fill=tk.BOTH, expand=True)
        
        # Frame para el texto con scrollbar
        text_frame = tk.Frame(main_frame, bg=colors['bg'])
        text_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Scrollbar vertical estilizado
        self.scrollbar = StyledVerticalScrollbar(text_frame, self.design_manager)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Widget de texto principal
        self.text_widget = tk.Text(
            text_frame,
            wrap=tk.WORD,  # Word wrapping
            font=design_manager.get_font('normal'),
            bg=colors['entry_bg'],
            fg=colors['entry_fg'],
            insertbackground=colors['entry_fg'],
            selectbackground=colors['select_bg'],
            selectforeground=colors['select_fg'],
            yscrollcommand=self._on_text_scroll,
            state=tk.DISABLED,  # Solo lectura
            padx=10,
            pady=5,
            borderwidth=0,
            highlightthickness=0
        )
        self.text_widget.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Configurar scrollbar
        self.scrollbar.config(command=self._on_scrollbar_scroll)
        
        # Vincular eventos
        self.text_widget.bind('<<Change>>', self._on_text_change)
        self.text_widget.bind('<Configure>', self._on_text_configure)
        
        # Inicializar
        self._update_line_numbers()
        self._check_scrollbar_visibility()
    
    def printConsoleLn(self, value):
        """Agrega una línea de texto a la consola"""
        self.text_widget.config(state=tk.NORMAL)
        
        # Si no está vacío, agregar salto de línea antes
        if self.text_widget.get("1.0", "end-1c"):
            self.text_widget.insert(tk.END, "\n")
        
        # Insertar el texto
        self.text_widget.insert(tk.END, str(value))
        
        # Volver a solo lectura
        self.text_widget.config(state=tk.DISABLED)
        
        # Actualizar números de línea
        self._update_line_numbers()
        
        # Auto-scroll al final
        self.text_widget.see(tk.END)
        
        # Verificar visibilidad del scrollbar
        self._check_scrollbar_visibility()
    
    def clear(self):
        """Limpia todo el contenido de la consola"""
        self.text_widget.config(state=tk.NORMAL)
        self.text_widget.delete("1.0", tk.END)
        self.text_widget.config(state=tk.DISABLED)
        self._update_line_numbers()
        self._check_scrollbar_visibility()
    
    def _on_text_scroll(self, first, last):
        """Callback cuando el texto se desplaza"""
        self.scrollbar.set(first, last)
        # Actualizar números de línea cuando se hace scroll
        self._update_line_numbers()
    
    def _on_scrollbar_scroll(self, *args):
        """Callback cuando se mueve el scrollbar"""
        self.text_widget.yview(*args)
        # Actualizar números después del scroll
        self.text_widget.after_idle(self._update_line_numbers)
    
    def _on_text_change(self, event=None):
        """Callback cuando el texto cambia"""
        self._update_line_numbers()
    
    def _on_text_configure(self, event=None):
        """Callback cuando se reconfigura el widget de texto"""
        self._update_line_numbers()
    
    def _update_line_numbers(self):
        """Actualiza los números de línea para líneas lógicas (no visuales)"""
        colors = self.design_manager.get_colors()
        
        # Limpiar canvas
        self.line_numbers.delete("all")
        
        # Obtener el rango visible
        first_visible = self.text_widget.index("@0,0")
        last_visible = self.text_widget.index(f"@0,{self.text_widget.winfo_height()}")
        
        # Encontrar primera línea lógica visible
        first_line_num = int(first_visible.split('.')[0])
        last_line_num = int(last_visible.split('.')[0]) + 10  # Buffer adicional
        
        # Dibujar números solo para líneas visibles
        for line_num in range(max(1, first_line_num - 5), last_line_num):
            index = f"{line_num}.0"
            
            # Verificar si esta línea existe
            if self.text_widget.compare(index, ">=", "end"):
                break
                
            # Obtener información de display
            dline = self.text_widget.dlineinfo(index)
            if dline:
                y = dline[1] + (dline[3] // 2)  # Centro vertical
                self.line_numbers.create_text(
                    45, y+5,
                    anchor="e",
                    text=str(line_num),
                    font=self.design_manager.get_font('normal'),
                    fill=colors['sidebar_button_fg']
                )
        
        # NO actualizar scrollregion - mantener sincronizado con texto
        bbox = self.text_widget.bbox("1.0")
        if bbox:
            self.line_numbers.config(scrollregion=(0, bbox[1], 50, bbox[1] + self.text_widget.winfo_height()))
    
    def _check_scrollbar_visibility(self):
        """Oculta o muestra el scrollbar según sea necesario"""
        self.text_widget.update_idletasks()
        
        # Obtener las posiciones del scroll
        first, last = self.text_widget.yview()
        
        # Si todo el contenido es visible, ocultar scrollbar
        if first == 0.0 and last == 1.0:
            self.scrollbar.pack_forget()
        else:
            self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    
    def update_theme(self):
        """Actualiza los colores cuando cambia el tema"""
        colors = self.design_manager.get_colors()
        
        # Actualizar colores del frame principal
        self.configure(bg=colors['bg'])
        self.configure(highlightbackground=colors['button_bg'])
        self.configure(highlightcolor=colors['select_bg'])
        
        # Actualizar frame de números
        self.line_numbers_frame.configure(bg=colors['sidebar_bg'])
        self.line_numbers.configure(bg=colors['sidebar_bg'])
        
        # Redibujar números de línea con nuevos colores
        self._update_line_numbers()
        
        # Actualizar colores del texto
        self.text_widget.configure(
            bg=colors['entry_bg'],
            fg=colors['entry_fg'],
            insertbackground=colors['entry_fg'],
            selectbackground=colors['select_bg'],
            selectforeground=colors['select_fg']
        )
        
        # Actualizar scrollbar
        self.scrollbar.update_theme()