"""
styled_button.py - Componente de botón estilizado
"""
import tkinter as tk

class StyledButton(tk.Frame):
    def __init__(self, parent, text, command, design_manager, style_type='default', **kwargs):
        # Obtener colores del tema
        colors = design_manager.get_colors()
        
        # Configurar frame contenedor
        super().__init__(parent, bg=colors.get('sidebar_bg', colors['bg']), **kwargs)
        
        self.design_manager = design_manager
        self.command = command
        self.style_type = style_type
        self.is_active = False
        
        # Determinar colores según el tipo de estilo
        if style_type == 'sidebar':
            self.normal_bg = colors['sidebar_button_bg']
            self.normal_fg = colors['sidebar_button_fg']
            self.hover_bg = colors['button_hover']
            self.active_bg = colors['sidebar_button_active_bg']
            self.active_fg = colors['sidebar_button_active_fg']
        else:
            self.normal_bg = colors['button_bg']
            self.normal_fg = colors['button_fg']
            self.hover_bg = colors['button_hover']
            self.active_bg = colors['button_active']
            self.active_fg = colors['button_fg']
        
        # Crear el botón usando tk.Label para mejor control
        self.button = tk.Label(
            self,
            text=text,
            bg=self.normal_bg,
            fg=self.normal_fg,
            font=design_manager.get_font('normal'),
            pady=12,
            padx=15,
            anchor='w',
            cursor='hand2'
        )
        self.button.pack(fill=tk.BOTH, expand=True)
        
        # Configurar eventos
        self.button.bind('<Button-1>', self._on_click)
        self.button.bind('<Enter>', self._on_enter)
        self.button.bind('<Leave>', self._on_leave)
    
    def _on_click(self, event=None):
        """Maneja el click del botón"""
        if self.command:
            self.command()
    
    def _on_enter(self, event=None):
        """Maneja cuando el mouse entra al botón"""
        if not self.is_active:
            self.button.configure(bg=self.hover_bg)
    
    def _on_leave(self, event=None):
        """Maneja cuando el mouse sale del botón"""
        if not self.is_active:
            self.button.configure(bg=self.normal_bg)
    
    def set_active(self, active=True):
        """Establece el estado activo del botón"""
        self.is_active = active
        if active:
            self.button.configure(bg=self.active_bg, fg=self.active_fg)
        else:
            self.button.configure(bg=self.normal_bg, fg=self.normal_fg)
    
    def update_theme(self):
        """Actualiza los colores cuando cambia el tema"""
        colors = self.design_manager.get_colors()
        
        # Actualizar colores según el tipo
        if self.style_type == 'sidebar':
            self.normal_bg = colors['sidebar_button_bg']
            self.normal_fg = colors['sidebar_button_fg']
            self.hover_bg = colors['button_hover']
            self.active_bg = colors['sidebar_button_active_bg']
            self.active_fg = colors['sidebar_button_active_fg']
            self.configure(bg=colors['sidebar_bg'])
        else:
            self.normal_bg = colors['button_bg']
            self.normal_fg = colors['button_fg']
            self.hover_bg = colors['button_hover']
            self.active_bg = colors['button_active']
            self.active_fg = colors['button_fg']
            self.configure(bg=colors['bg'])
        
        # Aplicar nuevos colores
        if self.is_active:
            self.button.configure(bg=self.active_bg, fg=self.active_fg)
        else:
            self.button.configure(bg=self.normal_bg, fg=self.normal_fg)