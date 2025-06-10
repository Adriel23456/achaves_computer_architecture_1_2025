# styled_console.py - Componente de consola estática
import tkinter as tk
from tkinter import ttk
from GUI.Components.styled_scrollbar import StyledVerticalScrollbar

class StyledCredits(tk.Frame):
    """Creditos estilizada que muestra un texto estático."""
    def __init__(self, parent, design_manager, **kwargs):
        self.design_manager = design_manager
        colors = design_manager.get_colors()
        super().__init__(parent, bg=colors['bg'], relief=tk.SOLID, borderwidth=1, **kwargs)
        self.configure(highlightbackground=colors['button_bg'],
                       highlightcolor=colors['select_bg'],
                       highlightthickness=1)

        # Frame principal para el contenido
        main_frame = tk.Frame(self, bg=colors['bg'])
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Scrollbar vertical estilizado
        self.scrollbar = StyledVerticalScrollbar(main_frame, self.design_manager)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Widget de texto principal (solo lectura)
        self.text_widget = tk.Text(
            main_frame,
            wrap=tk.WORD,
            font=self.design_manager.get_font('normal'),
            bg=colors['entry_bg'],
            fg=colors['entry_fg'],
            insertbackground=colors['entry_fg'],
            selectbackground=colors['select_bg'],
            selectforeground=colors['select_fg'],
            yscrollcommand=self.scrollbar.set,
            state=tk.DISABLED,
            padx=10,
            pady=5,
            borderwidth=0,
            highlightthickness=0
        )
        self.text_widget.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.scrollbar.config(command=self.text_widget.yview)

        # Insertar el texto estático
        self.text_widget.config(state=tk.NORMAL)
        credits = (
                    # Título y contexto
                    "Proyecto Grupal I – Grupo 5\n"
                    "Simulador de CPU Seguro de 64 bits\n"
                    "Instituto Tecnológico de Costa Rica – CE-4301 Arquitectura de Computadores I\n"
                    "Profesor: Dr.-Ing. Jeferson González Gómez | Entrega: 6 jun 2025\n\n"

                    # Objetivo general
                    "Objetivo:\n"
                    "  • Diseñar e implementar, en software, una CPU RISC de 64 bits con\n"
                    "    extensiones de seguridad orientadas a cifrado TEA y bóveda de llaves.\n\n"

                    # Arquitectura en síntesis
                    "Arquitectura y características clave:\n"
                    "  • Conjunto de instrucciones propio, longitud fija de 64 bits (≈140 instrucciones).\n"
                    "  • Microarquitectura pipeline de 5 etapas sin detección de hazards.\n"
                    "  • Banco de 16 registros generales (32 bits) + 9 registros seguros.\n"
                    "  • Memorias especializadas: general (64×32 b), login (8×32 b),\n"
                    "    vault de llaves (16×32 b) y memoria dinámica segura.\n"
                    "  • Flags clásicos (N,Z,C,V) + flags de seguridad (L,S1,S2).\n"
                    "  • Soporte nativo para TEA (32 rondas, Δ = 0x9E3779B9) y gestor de contraseña.\n\n"

                    # Plan de diseño (fases)
                    "Plan de diseño (fases):\n"
                    "  1. Definición completa de la ISA y hoja de referencia.\n"
                    "  2. Modelado de microarquitectura y diagrama de bloques (pipeline).\n"
                    "  3. Implementación del simulador en Python + Tkinter con visualización de registros.\n"
                    "  4. Desarrollo de ensamblador/compilador para cargar binarios.\n"
                    "  5. Validación funcional: cifrado/descifrado TEA y verificación MD5.\n"
                    "  6. Integración de GUI, métricas de ciclos y documentación final.\n\n"

                    # Entregables principales
                    "Entregables:\n"
                    "  • Simulador ejecutable + código fuente y scripts de compilación.\n"
                    "  • Ensamblador y programas de prueba de la ISA.\n"
                    "  • Hoja verde y documento de diseño detallado.\n"
                    "  • Archivos de prueba cifrados/descifrados y hashes respectivos.\n\n"

                    # Integrantes
                    "Integrantes:\n"
                    "  • Adriel S. Chaves Salazar\n"
                    "  • Daniel Duarte Cordero\n"
                    "  • Marco A. Rodríguez Villegas\n"
                    "  • Gonzalo Acuña Madrigal\n"
                )
        self.text_widget.insert(tk.END, credits)
        self.text_widget.config(state=tk.DISABLED)

    def update_theme(self):
        """Actualiza colores cuando cambia el tema."""
        colors = self.design_manager.get_colors()
        self.configure(bg=colors['bg'],
                       highlightbackground=colors['button_bg'],
                       highlightcolor=colors['select_bg'])
        self.text_widget.configure(
            bg=colors['entry_bg'],
            fg=colors['entry_fg'],
            insertbackground=colors['entry_fg'],
            selectbackground=colors['select_bg'],
            selectforeground=colors['select_fg']
        )
        self.scrollbar.update_theme()