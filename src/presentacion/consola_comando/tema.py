# =============================================================================
#  TEMA VISUAL COMPARTIDO — MISSION CONTROL (CAPA 4 - PRESENTACIÓN)
# =============================================================================
#  Centraliza paleta, tipografías y estilos ttk de la consola de escritorio.
#  No modifica contratos de API ni lógica de negocio: solo presentación.
# =============================================================================

import tkinter as tk
from tkinter import ttk


COLORES = {
    "bg": "#05080f",
    "bg_alt": "#070d18",
    "panel": "#0a1220",
    "panel_2": "#0d1728",
    "panel_3": "#111e32",
    "panel_4": "#16243a",
    "line": "#1b2c44",
    "line_soft": "#142238",
    "text": "#e8f1fb",
    "muted": "#8fa4bb",
    "muted_2": "#647a93",
    "cyan": "#38bdf8",
    "cyan_dark": "#0ea5e9",
    "mint": "#34d399",
    "amber": "#fbbf24",
    "red": "#f87171",
    "violet": "#a78bfa",
    "blue": "#60a5fa",
    "white": "#ffffff",
    "clinical_bg": "#f8fafc",
    "clinical_ink": "#0f1c2e",
    "clinical_muted": "#64748b",
}

FUENTES = {
    "brand": ("Segoe UI", 17, "bold"),
    "title": ("Segoe UI", 14, "bold"),
    "subtitle": ("Segoe UI", 10),
    "body": ("Segoe UI", 9),
    "small": ("Segoe UI", 8),
    "eyebrow": ("Segoe UI", 8, "bold"),
    "mono": ("Consolas", 9),
    "mono_big": ("Consolas", 17, "bold"),
    "kpi": ("Segoe UI", 20, "bold"),
    "kpi_small": ("Segoe UI", 9, "bold"),
    "button": ("Segoe UI", 9, "bold"),
}

COLOR_ALERTA = {
    "NOMINAL": COLORES["mint"],
    "PRECAUCION": COLORES["amber"],
    "CRITICO": COLORES["red"],
}

FONDO_ALERTA = {
    "NOMINAL": "#0c2a24",
    "PRECAUCION": "#2b2110",
    "CRITICO": "#2c1418",
}

COLORES_MISION = {
    "ARTEMIS_LUNA": "#0f766e",
    "ARES_MARTE": "#b45309",
    "EUROPA_JUPITER": "#1d4ed8",
}


# ---------------------------------------------------------------------------
#  Estilos ttk
# ---------------------------------------------------------------------------
def configurar_estilos(root: tk.Misc) -> None:
    """Aplica el tema oscuro de misión a todos los widgets ttk de la ventana."""
    style = ttk.Style(root)
    try:
        style.theme_use("clam")
    except tk.TclError:
        pass

    style.configure(
        ".",
        background=COLORES["bg"],
        foreground=COLORES["text"],
        font=FUENTES["body"],
    )

    # --- Contenedores -----------------------------------------------------
    style.configure("App.TFrame", background=COLORES["bg"])
    style.configure("Sidebar.TFrame", background=COLORES["bg_alt"])
    style.configure("Card.TFrame", background=COLORES["panel"], relief="flat")
    style.configure("CardAlt.TFrame", background=COLORES["panel_2"], relief="flat")
    style.configure("Header.TFrame", background=COLORES["panel"], relief="flat")
    style.configure("Soft.TFrame", background=COLORES["panel_3"], relief="flat")

    # --- Etiquetas --------------------------------------------------------
    style.configure(
        "TLabel",
        background=COLORES["bg"],
        foreground=COLORES["text"],
        font=FUENTES["body"],
    )
    style.configure(
        "Card.TLabel",
        background=COLORES["panel"],
        foreground=COLORES["text"],
        font=FUENTES["body"],
    )
    style.configure(
        "CardMuted.TLabel",
        background=COLORES["panel"],
        foreground=COLORES["muted"],
        font=FUENTES["small"],
    )
    style.configure(
        "Sidebar.TLabel",
        background=COLORES["bg_alt"],
        foreground=COLORES["text"],
        font=FUENTES["body"],
    )
    style.configure(
        "SidebarMuted.TLabel",
        background=COLORES["bg_alt"],
        foreground=COLORES["muted"],
        font=FUENTES["small"],
    )
    style.configure(
        "SidebarBrand.TLabel",
        background=COLORES["bg_alt"],
        foreground=COLORES["cyan"],
        font=FUENTES["brand"],
    )
    style.configure(
        "Title.TLabel",
        background=COLORES["bg"],
        foreground=COLORES["text"],
        font=FUENTES["title"],
    )
    style.configure(
        "Subtitle.TLabel",
        background=COLORES["bg"],
        foreground=COLORES["muted"],
        font=FUENTES["subtitle"],
    )
    style.configure(
        "Muted.TLabel",
        background=COLORES["bg"],
        foreground=COLORES["muted"],
        font=FUENTES["small"],
    )
    style.configure(
        "Cyan.TLabel",
        background=COLORES["bg"],
        foreground=COLORES["cyan"],
        font=FUENTES["body"],
    )
    style.configure(
        "Mint.TLabel",
        background=COLORES["bg"],
        foreground=COLORES["mint"],
        font=FUENTES["body"],
    )
    style.configure(
        "Amber.TLabel",
        background=COLORES["bg"],
        foreground=COLORES["amber"],
        font=FUENTES["body"],
    )
    style.configure(
        "Red.TLabel",
        background=COLORES["bg"],
        foreground=COLORES["red"],
        font=FUENTES["body"],
    )
    style.configure(
        "Violet.TLabel",
        background=COLORES["bg"],
        foreground=COLORES["violet"],
        font=FUENTES["body"],
    )
    style.configure(
        "KPI.TLabel",
        background=COLORES["panel"],
        foreground=COLORES["text"],
        font=FUENTES["kpi"],
    )
    style.configure(
        "KPISmall.TLabel",
        background=COLORES["panel"],
        foreground=COLORES["muted"],
        font=FUENTES["small"],
    )

    # --- Botones ----------------------------------------------------------
    style.configure(
        "TButton",
        background=COLORES["panel_3"],
        foreground=COLORES["text"],
        borderwidth=0,
        focusthickness=0,
        padding=(10, 7),
        font=FUENTES["button"],
    )
    style.map(
        "TButton",
        background=[("active", "#16243a"), ("pressed", "#0f1a2b")],
        foreground=[("disabled", COLORES["muted_2"])],
    )

    for nombre, fondo, activo in (
        ("Accent.TButton", COLORES["cyan_dark"], "#0284c7"),
        ("Success.TButton", "#0f766e", "#0d9488"),
        ("Warning.TButton", "#b45309", "#d97706"),
        ("Danger.TButton", "#b91c1c", "#dc2626"),
        ("Violet.TButton", "#6d28d9", "#7c3aed"),
        ("Ghost.TButton", COLORES["panel_3"], "#16243a"),
    ):
        style.configure(
            nombre,
            background=fondo,
            foreground=COLORES["white"],
            borderwidth=0,
            focusthickness=0,
            padding=(10, 7),
            font=FUENTES["button"],
        )
        style.map(
            nombre,
            background=[("active", activo), ("pressed", activo)],
            foreground=[("disabled", COLORES["muted_2"])],
        )

    # --- Tablas -----------------------------------------------------------
    style.configure(
        "Treeview",
        background=COLORES["panel"],
        fieldbackground=COLORES["panel"],
        foreground=COLORES["text"],
        borderwidth=0,
        rowheight=28,
        font=FUENTES["body"],
    )
    style.configure(
        "Treeview.Heading",
        background=COLORES["panel_3"],
        foreground=COLORES["cyan"],
        relief="flat",
        borderwidth=0,
        padding=(6, 7),
        font=("Segoe UI", 8, "bold"),
    )
    style.map(
        "Treeview",
        background=[("selected", "#12314a")],
        foreground=[("selected", COLORES["white"])],
    )
    style.map(
        "Treeview.Heading",
        background=[("active", "#16243a")],
    )

    # --- Notebook ---------------------------------------------------------
    style.configure(
        "TNotebook",
        background=COLORES["bg"],
        borderwidth=0,
        tabmargins=(0, 0, 0, 0),
    )
    style.configure(
        "TNotebook.Tab",
        background=COLORES["panel"],
        foreground=COLORES["muted"],
        padding=(18, 10),
        borderwidth=0,
        font=("Segoe UI", 9, "bold"),
    )
    style.map(
        "TNotebook.Tab",
        background=[("selected", COLORES["panel_2"]), ("active", "#101b2d")],
        foreground=[("selected", COLORES["cyan"]), ("active", COLORES["text"])],
    )

    # --- Inputs -----------------------------------------------------------
    style.configure(
        "TEntry",
        fieldbackground=COLORES["bg_alt"],
        foreground=COLORES["text"],
        insertcolor=COLORES["text"],
        bordercolor=COLORES["line"],
        lightcolor=COLORES["line"],
        darkcolor=COLORES["line"],
        padding=6,
    )
    style.configure(
        "TCombobox",
        fieldbackground=COLORES["bg_alt"],
        background=COLORES["panel_3"],
        foreground=COLORES["text"],
        arrowcolor=COLORES["cyan"],
        bordercolor=COLORES["line"],
        padding=5,
    )
    style.map(
        "TCombobox",
        fieldbackground=[("readonly", COLORES["bg_alt"])],
        foreground=[("readonly", COLORES["text"])],
    )

    # --- Labelframes y separadores ---------------------------------------
    style.configure(
        "TLabelframe",
        background=COLORES["panel"],
        bordercolor=COLORES["line"],
        lightcolor=COLORES["line"],
        darkcolor=COLORES["line"],
        relief="solid",
    )
    style.configure(
        "TLabelframe.Label",
        background=COLORES["panel"],
        foreground=COLORES["muted"],
        font=("Segoe UI", 9, "bold"),
    )
    style.configure("TSeparator", background=COLORES["line"])

    # --- Scrollbars -------------------------------------------------------
    style.configure(
        "Vertical.TScrollbar",
        background=COLORES["panel_3"],
        troughcolor=COLORES["bg_alt"],
        bordercolor=COLORES["bg_alt"],
        arrowcolor=COLORES["muted"],
        width=10,
    )
    style.configure(
        "Horizontal.TScrollbar",
        background=COLORES["panel_3"],
        troughcolor=COLORES["bg_alt"],
        bordercolor=COLORES["bg_alt"],
        arrowcolor=COLORES["muted"],
        width=10,
    )


# ---------------------------------------------------------------------------
#  Helpers de widgets tk (para no repetir opciones en cada vista)
# ---------------------------------------------------------------------------
_BOTONES = {
    "primary": (COLORES["cyan_dark"], "#0284c7", COLORES["white"]),
    "success": ("#0f766e", "#0d9488", COLORES["white"]),
    "warning": ("#b45309", "#d97706", COLORES["white"]),
    "danger": ("#b91c1c", "#dc2626", COLORES["white"]),
    "violet": ("#6d28d9", "#7c3aed", COLORES["white"]),
    "ghost": (COLORES["panel_3"], "#16243a", COLORES["text"]),
    "subtle": (COLORES["bg_alt"], "#101b2d", COLORES["muted"]),
}


def crear_boton(parent: tk.Misc, texto: str, comando, tipo: str = "ghost", **kwargs) -> tk.Button:
    """Crea un botón plano consistente con la paleta de misión."""
    fondo, activo, texto_color = _BOTONES.get(tipo, _BOTONES["ghost"])
    opciones = {
        "text": texto,
        "command": comando,
        "bg": fondo,
        "fg": texto_color,
        "activebackground": activo,
        "activeforeground": texto_color,
        "disabledforeground": COLORES["muted_2"],
        "font": FUENTES["button"],
        "relief": "flat",
        "bd": 0,
        "highlightthickness": 0,
        "padx": 12,
        "pady": 8,
        "cursor": "hand2",
    }
    opciones.update(kwargs)
    return tk.Button(parent, **opciones)


def crear_tarjeta(parent: tk.Misc, **kwargs) -> tk.Frame:
    """Crea un contenedor con borde sutil, usado como tarjeta de panel."""
    opciones = {
        "bg": COLORES["panel"],
        "bd": 0,
        "highlightthickness": 1,
        "highlightbackground": COLORES["line"],
        "highlightcolor": COLORES["line"],
    }
    opciones.update(kwargs)
    return tk.Frame(parent, **opciones)


def crear_etiqueta(parent: tk.Misc, texto: str, tipo: str = "body", **kwargs) -> tk.Label:
    """Crea una etiqueta con la tipografía y el color semántico indicado."""
    estilos = {
        "body": (FUENTES["body"], COLORES["text"]),
        "small": (FUENTES["small"], COLORES["muted"]),
        "muted": (FUENTES["small"], COLORES["muted"]),
        "eyebrow": (FUENTES["eyebrow"], COLORES["cyan"]),
        "title": (FUENTES["title"], COLORES["text"]),
        "subtitle": (FUENTES["subtitle"], COLORES["muted"]),
        "mono": (FUENTES["mono"], COLORES["text"]),
        "kpi": (FUENTES["kpi"], COLORES["text"]),
        "mint": (FUENTES["body"], COLORES["mint"]),
        "amber": (FUENTES["body"], COLORES["amber"]),
        "red": (FUENTES["body"], COLORES["red"]),
        "violet": (FUENTES["body"], COLORES["violet"]),
        "cyan": (FUENTES["body"], COLORES["cyan"]),
    }
    fuente, color = estilos.get(tipo, estilos["body"])
    opciones = {
        "text": texto,
        "bg": COLORES["panel"],
        "fg": color,
        "font": fuente,
        "anchor": "w",
        "justify": "left",
    }
    opciones.update(kwargs)
    return tk.Label(parent, **opciones)


def centrar_ventana(ventana: tk.Misc, ancho: int, alto: int) -> None:
    """Centra una ventana Tk en la pantalla actual."""
    ventana.update_idletasks()
    pantalla_ancho = ventana.winfo_screenwidth()
    pantalla_alto = ventana.winfo_screenheight()
    x = max(0, (pantalla_ancho - ancho) // 2)
    y = max(0, (pantalla_alto - alto) // 2)
    ventana.geometry(f"{ancho}x{alto}+{x}+{y}")
