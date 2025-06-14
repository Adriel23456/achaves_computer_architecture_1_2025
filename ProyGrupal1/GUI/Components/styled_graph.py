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
    """Gráfica estilizada que se adapta al tema de la aplicación"""
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
        
        # Frame principal para la gráfica
        self.graph_frame = tk.Frame(self, bg=colors['bg'])
        self.graph_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Crear figura de matplotlib
        self.figure = None
        self.canvas = None
        self.ax = None
        
        self._create_figure()
    
    def _create_figure(self):
        """Crea la figura de matplotlib con el tema actual"""
        colors = self.design_manager.get_colors()
        
        # Determinar colores según el tema
        if self.design_manager.config['theme']['current'] == 'dark':
            bg_color = '#1e1e1e'
            fg_color = '#ffffff'
            grid_color = '#3a3a3a'
            face_color = '#2d2d2d'
        else:
            bg_color = '#ffffff'
            fg_color = '#000000'
            grid_color = '#e0e0e0'
            face_color = '#f5f5f5'
        
        # Crear figura
        self.figure = Figure(figsize=(8, 6), dpi=100, facecolor=bg_color)
        self.ax = self.figure.add_subplot(111, facecolor=face_color)
        
        # Configurar estilo del axes
        self.ax.spines['bottom'].set_color(fg_color)
        self.ax.spines['top'].set_color(fg_color)
        self.ax.spines['left'].set_color(fg_color)
        self.ax.spines['right'].set_color(fg_color)
        self.ax.tick_params(colors=fg_color, which='both')
        
        # Configurar grid
        self.ax.grid(True, color=grid_color, linestyle='--', alpha=0.5)
        
        # Configurar etiquetas
        self.ax.xaxis.label.set_color(fg_color)
        self.ax.yaxis.label.set_color(fg_color)
        self.ax.title.set_color(fg_color)
        
        # Crear canvas
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
        """Actualiza los colores cuando cambia el tema"""
        colors = self.design_manager.get_colors()
        
        # Actualizar frame
        self.configure(bg=colors['bg'])
        self.configure(highlightbackground=colors['button_bg'])
        self.configure(highlightcolor=colors['select_bg'])
        
        self.graph_frame.configure(bg=colors['bg'])
        
        # Recrear la figura con los nuevos colores
        self._create_figure()
        
        # Si hay datos, volver a plotear (esto debería manejarlo la vista)