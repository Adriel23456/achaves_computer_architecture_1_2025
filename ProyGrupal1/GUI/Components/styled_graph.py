# GUI/Components/styled_graph.py
"""
styled_graph.py - Componente de gráfica estilizada usando matplotlib
"""
import tkinter as tk
from tkinter import ttk
import matplotlib
matplotlib.use('TkAgg')
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
class StyledGraph(tk.Frame):
    """Gráfica estilizada que se adapta al tema de la aplicación."""
    def __init__(self, parent, design_manager, title="", **kwargs):
        self.design_manager = design_manager
        colors = design_manager.get_colors()

        super().__init__(
            parent, bg=colors["bg"],
            relief=tk.SOLID, borderwidth=2, **kwargs
        )
        self.configure(highlightbackground=colors["button_bg"])
        self.configure(highlightcolor=colors["select_bg"])
        self.configure(highlightthickness=1)

        # Título opcional
        if title:
            bar = tk.Frame(self, bg=colors["sidebar_bg"], height=35)
            bar.pack(fill=tk.X)
            bar.pack_propagate(False)
            tk.Label(
                bar, text=title,
                font=design_manager.get_font("bold"),
                bg=colors["sidebar_bg"], fg=colors["sidebar_button_fg"],
                padx=10
            ).pack(side=tk.LEFT, fill=tk.Y)

        # Área para la gráfica
        self.graph_frame = tk.Frame(self, bg=colors["bg"])
        self.graph_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.figure = None
        self.canvas = None
        self.ax     = None
        self._create_figure()

    # ------------------------------------------------------------------
    def _create_figure(self):
        """Crea la figura de matplotlib con estilo del tema."""
        theme = self.design_manager.config["theme"]["current"]
        if theme == "dark":
            bg, fg, grid, face = "#1e1e1e", "#ffffff", "#3a3a3a", "#2d2d2d"
        else:
            bg, fg, grid, face = "#ffffff", "#000000", "#e0e0e0", "#f5f5f5"

        self.figure = Figure(figsize=(8, 6), dpi=100, facecolor=bg)
        self.ax     = self.figure.add_subplot(111, facecolor=face)

        for spine in self.ax.spines.values():
            spine.set_color(fg)
        self.ax.tick_params(colors=fg)
        self.ax.grid(True, color=grid, linestyle="--", alpha=0.5)
        self.ax.xaxis.label.set_color(fg)
        self.ax.yaxis.label.set_color(fg)
        self.ax.title.set_color(fg)

        if self.canvas:
            self.canvas.get_tk_widget().destroy()
        self.canvas = FigureCanvasTkAgg(self.figure, master=self.graph_frame)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
    
    def plot_comparison_bars(self, data, title="", xlabel="", ylabel=""):
        """
        Crea una gráfica de barras para comparación
        data: diccionario con estructura {categoría: {subcategoría: valor}}
        """
        colors = self.design_manager.get_colors()
        
        # Limpiar el axes actual
        self.ax.clear()
        
        # Preparar datos
        categories = list(data.keys())
        subcategories = list(data[categories[0]].keys())
        
        # Configurar posiciones
        x = range(len(categories))
        width = 0.35
        
        # Colores para las barras
        if self.design_manager.config['theme']['current'] == 'dark':
            color1 = '#007ACC'  # Azul
            color2 = '#DC3545'  # Rojo
        else:
            color1 = '#0078D4'  # Azul claro
            color2 = '#E74C3C'  # Rojo claro
        
        # Crear barras
        for i, subcat in enumerate(subcategories):
            values = [data[cat][subcat] for cat in categories]
            offset = width * (i - len(subcategories)/2 + 0.5)
            bars = self.ax.bar([p + offset for p in x], values, width, 
                              label=subcat, color=color1 if i == 0 else color2)
            
            # Añadir valores sobre las barras
            for bar in bars:
                height = bar.get_height()
                self.ax.text(bar.get_x() + bar.get_width()/2., height,
                           f'{height:.3f}',
                           ha='center', va='bottom',
                           color=self.ax.title.get_color())
        
        # Configurar el gráfico
        self.ax.set_xlabel(xlabel)
        self.ax.set_ylabel(ylabel)
        self.ax.set_title(title)
        
        # AGREGAR ESTAS LÍNEAS:
        self.ax.xaxis.label.set_color('red')
        self.ax.xaxis.label.set_weight('bold')
        self.ax.yaxis.label.set_color('red')
        self.ax.yaxis.label.set_weight('bold')
        
        self.ax.set_xticks(x)
        self.ax.set_xticklabels(categories)
        self.ax.legend()
        
        # Actualizar grid
        fg_color = '#ffffff' if self.design_manager.config['theme']['current'] == 'dark' else '#000000'
        grid_color = '#3a3a3a' if self.design_manager.config['theme']['current'] == 'dark' else '#e0e0e0'
        self.ax.grid(True, color=grid_color, linestyle='--', alpha=0.5)
        
        # Redibujar
        self.canvas.draw()
    
    def plot_lines(self, data, title="", xlabel="", ylabel=""):
        """
        Crea una gráfica de líneas
        data: diccionario {nombre_línea: [(x1,y1), (x2,y2),...]}
        """
        # Limpiar el axes actual
        self.ax.clear()
        
        # Colores para las líneas
        line_colors = ['#007ACC', '#DC3545', '#28A745', '#FFC107']
        
        # Plotear cada línea
        for i, (name, points) in enumerate(data.items()):
            x_values = [p[0] for p in points]
            y_values = [p[1] for p in points]
            color = line_colors[i % len(line_colors)]
            self.ax.plot(x_values, y_values, 'o-', label=name, color=color, 
                        linewidth=2, markersize=8)
            
            # Añadir etiquetas en los puntos
            for x, y in points:
                self.ax.annotate(f'{y:.3f}s', (x, y), 
                               textcoords="offset points", 
                               xytext=(0,10), ha='center',
                               color=self.ax.title.get_color(),
                               fontsize=9)
        
        # Configurar el gráfico
        self.ax.set_xlabel(xlabel)
        self.ax.set_ylabel(ylabel)
        self.ax.set_title(title)
        
        # AGREGAR ESTAS LÍNEAS PARA HACER xlabel y ylabel ROJOS Y EN NEGRITA:
        self.ax.xaxis.label.set_color('red')
        self.ax.xaxis.label.set_weight('bold')
        self.ax.yaxis.label.set_color('red')
        self.ax.yaxis.label.set_weight('bold')
        
        self.ax.legend()
        
        # Actualizar grid
        grid_color = '#3a3a3a' if self.design_manager.config['theme']['current'] == 'dark' else '#e0e0e0'
        self.ax.grid(True, color=grid_color, linestyle='--', alpha=0.5)
        
        # Ajustar límites del eje Y
        all_y = []
        for points in data.values():
            all_y.extend([p[1] for p in points])
        if all_y:
            y_min, y_max = min(all_y), max(all_y)
            y_margin = (y_max - y_min) * 0.1
            self.ax.set_ylim(y_min - y_margin, y_max + y_margin)
        
        # Redibujar
        self.canvas.draw()
    
    def update_theme(self):
        colors = self.design_manager.get_colors()
        self.configure(bg=colors["bg"],
                       highlightbackground=colors["button_bg"],
                       highlightcolor=colors["select_bg"])
        self.graph_frame.configure(bg=colors["bg"])
        self._create_figure()  # recrea y el caller vuelve a plotear