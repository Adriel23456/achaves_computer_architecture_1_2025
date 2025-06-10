# creditos.py – Vista de créditos
import tkinter as tk
from GUI.Components.styled_credits import StyledCredits  # ajusta la ruta si tu módulo es distinto


class CreditosView:
    """Vista que muestra únicamente el componente StyledCredits a pantalla completa."""

    def __init__(self, parent, base_dir, config, design_manager, on_config_change, cpu_excel):
        self.parent = parent
        self.base_dir = base_dir
        self.config = config
        self.design_manager = design_manager
        self.on_config_change = on_config_change
        self.cpu_excel = cpu_excel

        self._create_ui()

    # ------------------------------------------------------------------
    # Construcción de la interfaz
    # ------------------------------------------------------------------
    def _create_ui(self):
        colors = self.design_manager.get_colors()

        # Frame contenedor con padding uniforme
        main_frame = tk.Frame(self.parent, bg=colors['bg'])
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        # Permitir que el componente se expanda en ambas direcciones
        main_frame.grid_rowconfigure(0, weight=1)
        main_frame.grid_columnconfigure(0, weight=1)

        # Instanciar y colocar StyledCredits
        self.credits_component = StyledCredits(main_frame, self.design_manager)
        self.credits_component.grid(row=0, column=0, sticky="nsew")

    # ------------------------------------------------------------------
    # Delegar refresco de tema al componente interno
    # ------------------------------------------------------------------
    def update_theme(self):
        if hasattr(self, "credits_component"):
            self.credits_component.update_theme()