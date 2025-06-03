# GUI/Components/styled_combobox.py  (archivo completo reemplazado)

from tkinter import ttk


class StyledCombobox(ttk.Combobox):
    """
    Combobox clásico: fondo blanco y texto negro,
    idéntico para tema claro u oscuro.
    No cambia con el tema → solución simple y estable.
    """

    STYLE_NAME = "Simple.TCombobox"

    def __init__(self, parent, design_manager, **kwargs):
        self._configure_style()
        super().__init__(parent, style=self.STYLE_NAME, **kwargs)

    @staticmethod
    def _configure_style():
        style = ttk.Style()

        # Configuración estática: blanco + negro
        style.configure(
            StyledCombobox.STYLE_NAME,
            fieldbackground="#ffffff",
            background="#ffffff",
            foreground="#000000",
            arrowcolor="#000000",
            relief="flat",
            padding=4,
            borderwidth=1,
        )

        style.map(
            StyledCombobox.STYLE_NAME,
            fieldbackground=[("readonly", "#ffffff")],
            background=[("active", "#f0f0f0")],
            arrowcolor=[("active", "#000000")],
            foreground=[("active", "#000000")],
        )

    # Sin soporte de tema dinámico (no se necesita)
    def update_theme(self):
        pass
