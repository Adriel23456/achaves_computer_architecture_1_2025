"""
styled_scrollbar.py - Componentes de scrollbar estilizados
"""
import tkinter as tk
from tkinter import ttk

class StyledVerticalScrollbar(tk.Frame):
    """Scrollbar vertical personalizado con mejor soporte de temas"""
    def __init__(self, parent, design_manager, **kwargs):
        self.design_manager = design_manager
        colors = design_manager.get_colors()
        
        # Frame contenedor
        super().__init__(parent, bg=colors['bg'], width=12)
        
        # Canvas para dibujar el scrollbar
        self.canvas = tk.Canvas(
            self,
            width=12,
            bg=colors['bg'],
            highlightthickness=0,
            borderwidth=0
        )
        self.canvas.pack(fill=tk.BOTH, expand=True)
        
        # Variables de estado
        self.thumb_pos = 0
        self.thumb_size = 0.1
        self.is_dragging = False
        self.command = None
        
        # Dibujar elementos
        self._create_elements()
        
        # Configurar eventos
        self.canvas.bind('<Button-1>', self._on_click)
        self.canvas.bind('<B1-Motion>', self._on_drag)
        self.canvas.bind('<ButtonRelease-1>', self._on_release)
        self.canvas.bind('<Enter>', self._on_enter)
        self.canvas.bind('<Leave>', self._on_leave)
        self.canvas.bind('<Configure>', self._on_configure)
        
    def _create_elements(self):
        """Crea los elementos visuales del scrollbar"""
        colors = self.design_manager.get_colors()
        
        # Limpiar canvas
        self.canvas.delete('all')
        
        # Fondo (trough)
        self.trough = self.canvas.create_rectangle(
            2, 2, 10, self.canvas.winfo_height() - 2,
            fill=colors['button_bg'],
            outline='',
            tags='trough'
        )
        
        # Thumb (parte que se mueve)
        self.thumb = self.canvas.create_rectangle(
            2, 2, 10, 50,
            fill=colors['button_hover'],
            outline='',
            tags='thumb'
        )
    
    def set(self, first, last):
        """Actualiza la posición del scrollbar"""
        first = float(first)
        last = float(last)
        
        height = self.canvas.winfo_height()
        if height <= 1:
            return
            
        # Margen superior e inferior
        margin = 2
        available_height = height - (2 * margin)
        
        # Tamaño del thumb proporcional al contenido visible
        thumb_ratio = last - first
        thumb_height = max(20, int(thumb_ratio * available_height))
        
        # Posición del thumb
        # Cuando first=0, thumb está arriba (margin)
        # Cuando first=1-thumb_ratio, thumb está abajo (height-margin-thumb_height)
        max_top = available_height - thumb_height
        thumb_top = margin + int(first * max_top / (1.0 - thumb_ratio) if thumb_ratio < 1.0 else 0)
        
        # Actualizar posición del thumb
        self.canvas.coords(
            self.thumb,
            2, thumb_top,
            10, thumb_top + thumb_height
        )
        
        # Guardar valores
        self.thumb_pos = first
        self.thumb_size = thumb_ratio
    
    def config(self, **kwargs):
        """Configura el scrollbar"""
        if 'command' in kwargs:
            self.command = kwargs.pop('command')
        # No pasar 'command' al Frame padre
        if kwargs:
            super().configure(**kwargs)
    
    def configure(self, **kwargs):
        """Alias para config"""
        self.config(**kwargs)
    
    def _on_click(self, event):
        """Maneja clicks en el scrollbar"""
        if self.command is None:
            return
            
        # Verificar si se hizo click en el thumb
        clicked_item = self.canvas.find_closest(event.x, event.y)[0]
        
        if clicked_item == self.thumb:
            self.is_dragging = True
            # Guardar offset del click dentro del thumb
            thumb_coords = self.canvas.coords(self.thumb)
            self.drag_offset = event.y - thumb_coords[1]
        else:
            # Click en el trough - página arriba/abajo
            thumb_coords = self.canvas.coords(self.thumb)
            if thumb_coords:
                if event.y < thumb_coords[1]:
                    self.command('scroll', -1, 'pages')
                elif event.y > thumb_coords[3]:
                    self.command('scroll', 1, 'pages')
    
    def _on_drag(self, event):
        """Maneja el arrastre del thumb"""
        if not self.is_dragging or self.command is None:
            return
            
        height = self.canvas.winfo_height()
        if height <= 1:
            return
            
        margin = 2
        available_height = height - (2 * margin)
        thumb_height = max(20, int(self.thumb_size * available_height))
        max_top = available_height - thumb_height
        
        # Posición deseada del top del thumb (considerando el offset)
        desired_top = event.y - self.drag_offset
        desired_top = max(margin, min(desired_top, margin + max_top))
        
        # Convertir a posición normalizada
        if max_top > 0 and self.thumb_size < 1.0:
            normalized_pos = (desired_top - margin) / max_top
            new_pos = normalized_pos * (1.0 - self.thumb_size)
            new_pos = max(0, min(new_pos, 1.0 - self.thumb_size))
            
            # Mover a la nueva posición
            self.command('moveto', new_pos)
    
    def _on_release(self, event):
        """Maneja cuando se suelta el click"""
        self.is_dragging = False
    
    def _on_enter(self, event):
        """Maneja cuando el mouse entra al scrollbar"""
        colors = self.design_manager.get_colors()
        self.canvas.itemconfig(self.thumb, fill=colors['button_active'])
    
    def _on_leave(self, event):
        """Maneja cuando el mouse sale del scrollbar"""
        if not self.is_dragging:
            colors = self.design_manager.get_colors()
            self.canvas.itemconfig(self.thumb, fill=colors['button_hover'])
    
    def _on_configure(self, event):
        """Maneja cuando se redimensiona el canvas"""
        # Actualizar el tamaño del trough
        self.canvas.coords(
            self.trough,
            2, 2, 10, event.height - 2
        )
        # Redibujar el thumb con los nuevos cálculos
        if hasattr(self, 'thumb_pos') and hasattr(self, 'thumb_size'):
            self.set(self.thumb_pos, self.thumb_pos + self.thumb_size)
    
    def update_theme(self):
        """Actualiza los colores cuando cambia el tema"""
        colors = self.design_manager.get_colors()
        
        # Actualizar colores
        self.configure(bg=colors['bg'])
        self.canvas.configure(bg=colors['bg'])
        self.canvas.itemconfig(self.trough, fill=colors['button_bg'])
        self.canvas.itemconfig(self.thumb, fill=colors['button_hover'])


class StyledHorizontalScrollbar(ttk.Scrollbar):
    def __init__(self, parent, design_manager, **kwargs):
        super().__init__(parent, orient='horizontal', **kwargs)
        self.design_manager = design_manager
        self._configure_style()
    
    def _configure_style(self):
        """Configura el estilo del scrollbar"""
        colors = self.design_manager.get_colors()
        style = ttk.Style()
        
        # Configurar estilo para scrollbar horizontal
        style.configure(
            'Horizontal.TScrollbar',
            background=colors['button_bg'],
            troughcolor=colors['bg'],
            bordercolor=colors['bg'],
            arrowcolor=colors['fg'],
            lightcolor=colors['button_bg'],
            darkcolor=colors['button_bg']
        )
        
        # Configurar el comportamiento al pasar el mouse
        style.map(
            'Horizontal.TScrollbar',
            background=[('active', colors['button_hover'])],
            arrowcolor=[('active', colors['fg'])]
        )
        
        self.configure(style='Horizontal.TScrollbar')
    
    def update_theme(self):
        """Actualiza el estilo cuando cambia el tema"""
        self._configure_style()


class ScrollableFrame(tk.Frame):
    """Frame con scroll automático y centrado cuando no es necesario."""
    def __init__(self, parent, design_manager, orientation="vertical", **kwargs):
        colors = design_manager.get_colors()
        super().__init__(parent, bg=colors["bg"], **kwargs)

        self.design_manager = design_manager
        self.orientation = orientation

        # --- canvas --------------------------------------------------------
        self.canvas = tk.Canvas(self, bg=colors["bg"], highlightthickness=0)

        # --- scrollbar -----------------------------------------------------
        if orientation == "vertical":
            self.scrollbar = StyledVerticalScrollbar(self, design_manager)
            self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
            self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
            self.canvas.configure(yscrollcommand=self.scrollbar.set)
            self.scrollbar.configure(command=self.canvas.yview)
        else:
            self.scrollbar = StyledHorizontalScrollbar(self, design_manager)
            self.scrollbar.pack(side=tk.BOTTOM, fill=tk.X)
            self.canvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
            self.canvas.configure(xscrollcommand=self.scrollbar.set)
            self.scrollbar.configure(command=self.canvas.xview)

        # --- frame interior -----------------------------------------------
        self.interior = tk.Frame(self.canvas, bg=colors["bg"])
        self.interior_id = self.canvas.create_window(0, 0, window=self.interior, anchor=tk.NW)

        # --- eventos -------------------------------------------------------
        self.interior.bind("<Configure>", self._configure_interior)
        self.canvas.bind("<Configure>", self._configure_canvas)
        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)

    # ----------------------------------------------------------------------
    def _configure_interior(self, _=None):
        """Actualiza scrollregion y visibilidad de scrollbars."""
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        if self.orientation == "horizontal":
            need_bar = self.interior.winfo_reqwidth() > self.canvas.winfo_width()
            self.scrollbar.pack_forget() if not need_bar else self.scrollbar.pack(side=tk.BOTTOM, fill=tk.X)

    def _configure_canvas(self, event=None):
        """
        Ajusta el ancho del interior y deja un gap fijo de 10 px con el scrollbar.
        También centra verticalmente el contenido cuando todo cabe.
        """
        if self.orientation == "vertical":
            GAP = 10  # espacio mínimo entre contenido y barra
            canvas_width = max(event.width - GAP, 0)
            self.canvas.itemconfig(self.interior_id, width=canvas_width)

            # centrado vertical si el contenido es más bajo que el canvas
            interior_h = self.interior.winfo_reqheight()
            y_offset = max((event.height - interior_h) // 2, 0)
            self.canvas.coords(self.interior_id, 0, y_offset)
        else:
            # comportamiento original para orientación horizontal
            interior_w = self.interior.winfo_reqwidth()
            x_offset = max((event.width - interior_w) // 2, 0)
            self.canvas.coords(self.interior_id, x_offset, 0)

    # ----------------------------------------------------------------------
    def _on_mousewheel(self, event):
        """
        Desplaza SOLO cuando el contenido excede el área visible.
        Si todo cabe (no se necesita scroll), ignora la rueda del mouse.
        """
        region = self.canvas.bbox("all")
        if not region:
            return  # no hay contenido aún

        if self.orientation == "vertical":
            content_h = region[3] - region[1]
            if content_h > self.canvas.winfo_height():
                self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
        else:  # horizontal
            content_w = region[2] - region[0]
            if content_w > self.canvas.winfo_width():
                self.canvas.xview_scroll(int(-1 * (event.delta / 120)), "units")

    # ----------------------------------------------------------------------
    def update_theme(self):
        colors = self.design_manager.get_colors()
        self.configure(bg=colors["bg"])
        self.canvas.configure(bg=colors["bg"])
        self.interior.configure(bg=colors["bg"])
        self.scrollbar.update_theme()