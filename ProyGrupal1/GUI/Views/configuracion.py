# GUI/Views/configuracion.py  (archivo completo reemplazado)

import tkinter as tk
from tkinter import ttk, messagebox

from GUI.Components.styled_widgets import (
    StyledLabel,
    StyledCheckbutton,
    StyledRadiobutton,
)
from GUI.Components.styled_scrollbar import ScrollableFrame
from GUI.Components.styled_button import StyledButton
from GUI.Components.styled_combobox import StyledCombobox


class ConfiguracionView:
    PRESET_SIZES = [
        "1024x600",
        "1280x720",
        "1366x768",
        "1440x900",
        "1920x1080",
        "2560x1440",
    ]

    def __init__(self, parent, base_dir, config, design_manager, on_config_change, cpu_excel, controller):
        self.parent = parent
        self.base_dir = base_dir
        self.config = config
        self.design_manager = design_manager
        self.on_config_change = on_config_change
        self.cpu_excel = cpu_excel
        self.controller = controller

        # --- variables de control ---
        self.font_size_var = tk.IntVar(value=config["theme"]["font_size"])
        self.fullscreen_var = tk.BooleanVar(value=config["window"]["fullscreen"])
        self.theme_var = tk.StringVar(value=config["theme"]["current"])
        self.size_var = tk.StringVar(
            value=f'{config["window"]["width"]}x{config["window"]["height"]}'
        )

        self._create_ui()

        # --- sincronía con cambios globales ---
        root = self.parent.winfo_toplevel()
        root.bind("<<FullscreenToggled>>", self._sync_fullscreen_checkbox)

    # ---------- UI ----------
    def _create_ui(self):
        root_frame = self.design_manager.create_styled_frame(self.parent)
        root_frame.pack(fill=tk.BOTH, expand=True)

        StyledLabel(
            root_frame, "CONFIGURACIÓN", self.design_manager, font_type="title"
        ).pack(pady=(0, 15))

        scroll = ScrollableFrame(root_frame, self.design_manager)
        scroll.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        self._create_window_size_section(scroll.interior)
        ttk.Separator(scroll.interior, orient="horizontal").pack(fill=tk.X, pady=20)

        self._create_font_size_section(scroll.interior)
        ttk.Separator(scroll.interior, orient="horizontal").pack(fill=tk.X, pady=20)

        self._create_fullscreen_section(scroll.interior)
        ttk.Separator(scroll.interior, orient="horizontal").pack(fill=tk.X, pady=20)

        self._create_theme_section(scroll.interior)

    # ---------- secciones ----------
    def _create_window_size_section(self, parent):
        section = ttk.LabelFrame(parent, text="Tamaño de Ventana", padding=10)
        section.pack(fill=tk.X, pady=10)
        section.columnconfigure(1, weight=1)

        StyledLabel(section, "Presets:", self.design_manager).grid(
            row=0, column=0, sticky="w"
        )

        size_combo = StyledCombobox(
            section,
            self.design_manager,
            textvariable=self.size_var,
            values=self.PRESET_SIZES,
            state="readonly",
        )
        size_combo.grid(row=0, column=1, sticky="ew", padx=5, pady=2)

        StyledButton(
            section, "Aplicar", self._apply_window_size, self.design_manager
        ).grid(row=1, column=0, columnspan=2, sticky="ew", pady=8)

    def _create_font_size_section(self, parent):
        section = ttk.LabelFrame(parent, text="Tamaño de Fuente", padding=10)
        section.pack(fill=tk.X, pady=10)
        section.columnconfigure(0, weight=1)

        value_lbl = StyledLabel(
            section, f"Tamaño: {self.font_size_var.get()}pt", self.design_manager
        )
        value_lbl.grid(row=0, column=0, sticky="w")

        scale = ttk.Scale(
            section,
            from_=10,
            to=16,
            orient=tk.HORIZONTAL,
            variable=self.font_size_var,
            command=lambda v: value_lbl.config(text=f"Tamaño: {int(float(v))}pt"),
        )
        scale.grid(row=1, column=0, sticky="ew", pady=5)

        StyledButton(
            section,
            "Aplicar tamaño de fuente",
            self._apply_font_size,
            self.design_manager,
        ).grid(row=2, column=0, sticky="ew", pady=8)

    def _create_fullscreen_section(self, parent):
        section = ttk.LabelFrame(parent, text="Modo Pantalla Completa", padding=10)
        section.pack(fill=tk.X, pady=10)

        StyledCheckbutton(
            section,
            "Activar pantalla completa",
            self.design_manager,
            variable=self.fullscreen_var,
            command=self._toggle_fullscreen,
        ).pack(anchor="w", pady=5)

        StyledLabel(
            section,
            "Nota: usa F11 o ESC para alternar pantalla completa",
            self.design_manager,
            font_type="small",
        ).pack(anchor="w", pady=5)

    def _create_theme_section(self, parent):
        section = ttk.LabelFrame(parent, text="Tema de la Aplicación", padding=10)
        section.pack(fill=tk.X, pady=10)

        radio_frame = ttk.Frame(section)
        radio_frame.pack(anchor="w", pady=5)

        StyledRadiobutton(
            radio_frame,
            "Tema Oscuro",
            self.design_manager,
            variable=self.theme_var,
            value="dark",
            command=self._change_theme,
        ).pack(side=tk.LEFT, padx=10)

        StyledRadiobutton(
            radio_frame,
            "Tema Claro",
            self.design_manager,
            variable=self.theme_var,
            value="light",
            command=self._change_theme,
        ).pack(side=tk.LEFT, padx=10)

    # ---------- acciones ----------
    def _apply_window_size(self):
        """Aplica el tamaño y centra la ventana en la pantalla."""
        try:
            width, height = map(int, self.size_var.get().split("x"))

            root = self.parent.winfo_toplevel()
            screen_w, screen_h = root.winfo_screenwidth(), root.winfo_screenheight()

            # Coordenadas para centrar
            x = max((screen_w - width) // 2, 0)
            y = max((screen_h - height) // 2, 0)

            root.geometry(f"{width}x{height}+{x}+{y}")

            # Persistir en configuración
            self.config["window"].update({"width": width, "height": height, "x": x, "y": y})

            messagebox.showinfo("Éxito", "Tamaño de ventana actualizado")
        except Exception:
            messagebox.showerror("Error", "Formato de tamaño inválido")

    def _apply_font_size(self):
        self.on_config_change("font_size", self.font_size_var.get())
        messagebox.showinfo("Éxito", "Tamaño de fuente actualizado")

    def _toggle_fullscreen(self):
        self.on_config_change("fullscreen", self.fullscreen_var.get())

    def _change_theme(self):
        self.on_config_change("theme", self.theme_var.get())

    # ---------- sincronía ----------
    def _sync_fullscreen_checkbox(self, *_):
        """Actualiza la casilla cuando el modo cambia externamente (F11/Esc)."""
        root = self.parent.winfo_toplevel()
        self.fullscreen_var.set(root.attributes("-fullscreen"))
