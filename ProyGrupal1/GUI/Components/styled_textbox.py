# GUI/Components/styled_textbox.py
"""
styled_textbox.py - Componente de caja de texto estilizada para mostrar información importante
"""
import tkinter as tk
from tkinter import ttk
from GUI.Components.styled_scrollbar import StyledVerticalScrollbar

class StyledTextBox(tk.Frame):
    """Caja de texto estilizada para mostrar información teórica con formato rico"""
    def __init__(self, parent, design_manager, title="", **kwargs):
        self.design_manager = design_manager
        colors = design_manager.get_colors()
        
        super().__init__(parent, bg=colors['bg'], relief=tk.SOLID, borderwidth=2, **kwargs)
        self.configure(highlightbackground=colors['button_bg'])
        self.configure(highlightcolor=colors['select_bg'])
        self.configure(highlightthickness=1)
        
        # Frame del título si se proporciona
        if title:
            title_frame = tk.Frame(self, bg=colors['sidebar_bg'], height=35)
            title_frame.pack(fill=tk.X)
            title_frame.pack_propagate(False)
            
            title_label = tk.Label(
                title_frame,
                text=title,
                font=design_manager.get_font('bold'),
                bg=colors['sidebar_bg'],
                fg=colors['sidebar_button_fg'],
                padx=10
            )
            title_label.pack(side=tk.LEFT, fill=tk.Y)
        
        # Frame principal
        main_frame = tk.Frame(self, bg=colors['bg'])
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Scrollbar vertical estilizado
        self.scrollbar = StyledVerticalScrollbar(main_frame, self.design_manager)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Widget de texto principal
        self.text_widget = tk.Text(
            main_frame,
            wrap=tk.WORD,
            font=design_manager.get_font('normal'),
            bg=colors['entry_bg'],
            fg=colors['entry_fg'],
            insertbackground=colors['entry_fg'],
            selectbackground=colors['select_bg'],
            selectforeground=colors['select_fg'],
            yscrollcommand=self.scrollbar.set,
            state=tk.DISABLED,
            padx=15,
            pady=10,
            borderwidth=0,
            highlightthickness=0,
            spacing1=2,  # Espacio antes del párrafo
            spacing2=2,  # Espacio entre líneas
            spacing3=2   # Espacio después del párrafo
        )
        self.text_widget.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.scrollbar.config(command=self.text_widget.yview)
        
        # Configurar tags para formato
        self._configure_tags()
    
    def _configure_tags(self):
        """Configura los tags para diferentes estilos de texto"""
        colors = self.design_manager.get_colors()
        
        # Tag para títulos
        self.text_widget.tag_configure(
            'title',
            font=self.design_manager.get_font('title'),
            foreground=colors['select_bg'],
            spacing3=10
        )
        
        # Tag para subtítulos
        self.text_widget.tag_configure(
            'subtitle',
            font=self.design_manager.get_font('bold'),
            foreground=colors['fg'],
            spacing1=10,
            spacing3=5
        )
        
        # Tag para código/valores
        self.text_widget.tag_configure(
            'code',
            font=('Consolas', self.design_manager.get_font('normal').cget('size')),
            background=colors['button_bg'],
            foreground=colors['sidebar_button_active_bg']
        )
        
        # Tag para énfasis
        self.text_widget.tag_configure(
            'emphasis',
            font=self.design_manager.get_font('bold'),
            foreground=colors['sidebar_button_active_bg']
        )
        
        # Tag para ecuaciones
        self.text_widget.tag_configure(
            'equation',
            font=('Consolas', self.design_manager.get_font('normal').cget('size') + 2),
            foreground=colors['sidebar_button_active_bg'],
            justify=tk.CENTER,
            spacing1=10,
            spacing3=10
        )
        
        # Tag para tablas
        self.text_widget.tag_configure(
            'table_header',
            font=self.design_manager.get_font('bold'),
            background=colors['sidebar_bg'],
            foreground=colors['sidebar_button_fg']
        )
        
        # Tag para notas
        self.text_widget.tag_configure(
            'note',
            font=self.design_manager.get_font('small'),
            foreground=colors['button_hover'],
            lmargin1=20,
            lmargin2=20
        )
    
    def insert_text(self, text, tag=None):
        """Inserta texto con un tag específico"""
        self.text_widget.config(state=tk.NORMAL)
        if tag:
            self.text_widget.insert(tk.END, text, tag)
        else:
            self.text_widget.insert(tk.END, text)
        self.text_widget.config(state=tk.DISABLED)
    
    def insert_formatted_content(self, content_list):
        """
        Inserta contenido con formato.
        content_list es una lista de tuplas (texto, tag)
        """
        self.text_widget.config(state=tk.NORMAL)
        for text, tag in content_list:
            if tag:
                self.text_widget.insert(tk.END, text, tag)
            else:
                self.text_widget.insert(tk.END, text)
        self.text_widget.config(state=tk.DISABLED)
    
    def clear(self):
        """Limpia el contenido del widget"""
        self.text_widget.config(state=tk.NORMAL)
        self.text_widget.delete("1.0", tk.END)
        self.text_widget.config(state=tk.DISABLED)
    
    def update_theme(self):
        """Actualiza los colores cuando cambia el tema"""
        colors = self.design_manager.get_colors()
        
        # Actualizar colores del frame
        self.configure(bg=colors['bg'])
        self.configure(highlightbackground=colors['button_bg'])
        self.configure(highlightcolor=colors['select_bg'])
        
        # Actualizar widget de texto
        self.text_widget.configure(
            bg=colors['entry_bg'],
            fg=colors['entry_fg'],
            insertbackground=colors['entry_fg'],
            selectbackground=colors['select_bg'],
            selectforeground=colors['select_fg']
        )
        
        # Actualizar tags
        self._configure_tags()
        
        # Actualizar scrollbar
        self.scrollbar.update_theme()