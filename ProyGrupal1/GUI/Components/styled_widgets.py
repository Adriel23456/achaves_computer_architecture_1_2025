"""
styled_widgets.py - Widgets estilizados adicionales
"""
import tkinter as tk
from tkinter import ttk

class StyledLabel(tk.Label):
    """Label estilizada que se actualiza con el tema"""
    def __init__(self, parent, text, design_manager, font_type='normal', **kwargs):
        self.design_manager = design_manager
        colors = design_manager.get_colors()
        
        super().__init__(
            parent,
            text=text,
            font=design_manager.get_font(font_type),
            bg=colors['bg'],
            fg=colors['fg'],
            **kwargs
        )
    
    def update_theme(self):
        """Actualiza los colores cuando cambia el tema"""
        colors = self.design_manager.get_colors()
        self.configure(bg=colors['bg'], fg=colors['fg'])


class StyledEntry(tk.Frame):
    """Entry estilizada con bordes correctos"""
    def __init__(self, parent, design_manager, **kwargs):
        self.design_manager = design_manager
        colors = design_manager.get_colors()
        
        # Frame contenedor con borde
        super().__init__(parent, bg=colors['button_bg'], highlightthickness=1)
        self.configure(highlightbackground=colors['button_bg'])
        self.configure(highlightcolor=colors['select_bg'])
        
        # Entry sin borde
        self.entry = tk.Entry(
            self,
            font=design_manager.get_font('normal'),
            bg=colors['entry_bg'],
            fg=colors['entry_fg'],
            insertbackground=colors['entry_fg'],
            bd=0,
            highlightthickness=0,
            **kwargs
        )
        self.entry.pack(padx=1, pady=1)
        
        # Configurar eventos de foco
        self.entry.bind('<FocusIn>', self._on_focus_in)
        self.entry.bind('<FocusOut>', self._on_focus_out)
    
    def _on_focus_in(self, event=None):
        """Maneja cuando el entry obtiene foco"""
        colors = self.design_manager.get_colors()
        self.configure(highlightbackground=colors['select_bg'])
    
    def _on_focus_out(self, event=None):
        """Maneja cuando el entry pierde foco"""
        colors = self.design_manager.get_colors()
        self.configure(highlightbackground=colors['button_bg'])
    
    def get(self):
        """Obtiene el valor del entry"""
        return self.entry.get()
    
    def set(self, value):
        """Establece el valor del entry"""
        self.entry.delete(0, tk.END)
        self.entry.insert(0, value)
    
    def configure_var(self, textvariable):
        """Configura la variable de texto"""
        self.entry.configure(textvariable=textvariable)
    
    def update_theme(self):
        """Actualiza los colores cuando cambia el tema"""
        colors = self.design_manager.get_colors()
        self.configure(bg=colors['button_bg'])
        self.configure(highlightbackground=colors['button_bg'])
        self.entry.configure(
            bg=colors['entry_bg'],
            fg=colors['entry_fg'],
            insertbackground=colors['entry_fg']
        )


class StyledCheckbutton(tk.Frame):
    """Checkbutton estilizado"""
    def __init__(self, parent, text, design_manager, variable=None, command=None, **kwargs):
        self.design_manager = design_manager
        colors = design_manager.get_colors()
        
        super().__init__(parent, bg=colors['bg'])
        
        self.var = variable if variable else tk.BooleanVar()
        
        # Canvas para dibujar el checkbox personalizado
        self.canvas = tk.Canvas(
            self,
            width=20,
            height=20,
            bg=colors['bg'],
            highlightthickness=0
        )
        self.canvas.pack(side=tk.LEFT, padx=(0, 8))
        
        # Label para el texto
        self.label = tk.Label(
            self,
            text=text,
            bg=colors['bg'],
            fg=colors['fg'],
            font=design_manager.get_font('normal')
        )
        self.label.pack(side=tk.LEFT)
        
        # Dibujar checkbox
        self._draw_checkbox()
        
        # Configurar eventos
        self.canvas.bind('<Button-1>', self._toggle)
        self.label.bind('<Button-1>', self._toggle)
        self.bind('<Button-1>', self._toggle)
        
        self.command = command
        
        # Observar cambios en la variable
        if self.var:
            self.var.trace('w', lambda *args: self._draw_checkbox())
    
    def _draw_checkbox(self):
        """Dibuja el checkbox"""
        colors = self.design_manager.get_colors()
        self.canvas.delete('all')
        
        # Dibujar borde
        self.canvas.create_rectangle(
            2, 2, 18, 18,
            outline=colors['button_bg'],
            width=2,
            fill=colors['entry_bg']
        )
        
        # Dibujar check si está marcado
        if self.var.get():
            self.canvas.create_line(
                5, 10, 8, 13, 15, 6,
                width=2,
                fill=colors['select_bg'],
                capstyle='round',
                joinstyle='round'
            )
    
    def _toggle(self, event=None):
        """Alterna el estado del checkbox"""
        self.var.set(not self.var.get())
        if self.command:
            self.command()
    
    def update_theme(self):
        """Actualiza los colores cuando cambia el tema"""
        colors = self.design_manager.get_colors()
        self.configure(bg=colors['bg'])
        self.canvas.configure(bg=colors['bg'])
        self.label.configure(bg=colors['bg'], fg=colors['fg'])
        self._draw_checkbox()


class StyledRadiobutton(tk.Frame):
    """Radiobutton estilizado"""
    def __init__(self, parent, text, design_manager, variable=None, value=None, command=None, **kwargs):
        self.design_manager = design_manager
        colors = design_manager.get_colors()
        
        super().__init__(parent, bg=colors['bg'])
        
        self.var = variable if variable else tk.StringVar()
        self.value = value
        
        # Canvas para dibujar el radio personalizado
        self.canvas = tk.Canvas(
            self,
            width=20,
            height=20,
            bg=colors['bg'],
            highlightthickness=0
        )
        self.canvas.pack(side=tk.LEFT, padx=(0, 8))
        
        # Label para el texto
        self.label = tk.Label(
            self,
            text=text,
            bg=colors['bg'],
            fg=colors['fg'],
            font=design_manager.get_font('normal')
        )
        self.label.pack(side=tk.LEFT)
        
        # Dibujar radio
        self._draw_radio()
        
        # Configurar eventos
        self.canvas.bind('<Button-1>', self._select)
        self.label.bind('<Button-1>', self._select)
        self.bind('<Button-1>', self._select)
        
        self.command = command
        
        # Observar cambios en la variable
        if self.var:
            self.var.trace('w', lambda *args: self._draw_radio())
    
    def _draw_radio(self):
        """Dibuja el radio button"""
        colors = self.design_manager.get_colors()
        self.canvas.delete('all')
        
        # Dibujar círculo exterior
        self.canvas.create_oval(
            2, 2, 18, 18,
            outline=colors['button_bg'],
            width=2,
            fill=colors['entry_bg']
        )
        
        # Dibujar círculo interior si está seleccionado
        if self.var.get() == self.value:
            self.canvas.create_oval(
                6, 6, 14, 14,
                fill=colors['select_bg'],
                outline=''
            )
    
    def _select(self, event=None):
        """Selecciona este radio button"""
        self.var.set(self.value)
        if self.command:
            self.command()
    
    def update_theme(self):
        """Actualiza los colores cuando cambia el tema"""
        colors = self.design_manager.get_colors()
        self.configure(bg=colors['bg'])
        self.canvas.configure(bg=colors['bg'])
        self.label.configure(bg=colors['bg'], fg=colors['fg'])
        self._draw_radio()