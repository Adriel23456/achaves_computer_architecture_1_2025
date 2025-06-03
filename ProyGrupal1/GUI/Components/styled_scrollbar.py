"""
styled_scrollbar.py - Componentes de scrollbar estilizados
"""
import tkinter as tk
from tkinter import ttk

class StyledVerticalScrollbar(ttk.Scrollbar):
    def __init__(self, parent, design_manager, **kwargs):
        super().__init__(parent, orient='vertical', **kwargs)
        self.design_manager = design_manager
        self._configure_style()
    
    def _configure_style(self):
        """Configura el estilo del scrollbar"""
        colors = self.design_manager.get_colors()
        style = ttk.Style()
        
        # Configurar estilo para scrollbar vertical
        style.configure(
            'Vertical.TScrollbar',
            background=colors['button_bg'],
            troughcolor=colors['bg'],
            bordercolor=colors['bg'],
            arrowcolor=colors['fg'],
            lightcolor=colors['button_bg'],
            darkcolor=colors['button_bg']
        )
        
        # Configurar el comportamiento al pasar el mouse
        style.map(
            'Vertical.TScrollbar',
            background=[('active', colors['button_hover'])],
            arrowcolor=[('active', colors['fg'])]
        )
        
        self.configure(style='Vertical.TScrollbar')
    
    def update_theme(self):
        """Actualiza el estilo cuando cambia el tema"""
        self._configure_style()


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