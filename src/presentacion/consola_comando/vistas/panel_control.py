# =============================================================================
#  PANEL DE CONTROL DE MISIÓN Y MONITOREO GRUPAL (CAPA 4 - CONSOLA DE COMANDO)
# =============================================================================

import datetime
import webbrowser
import tkinter as tk
from tkinter import ttk, messagebox

from src.presentacion.i18n import t
from src.presentacion.consola_comando.cliente_api import ClienteAPIAstroMed, ErrorClienteAPI
from src.presentacion.consola_comando import tema
from src.presentacion.consola_comando.vistas.analitica import VentanaAnalitica
from src.presentacion.consola_comando.vistas.consola import VentanaConsolaSQL


class VentanaPanelControl:
    def __init__(self, master: tk.Toplevel, cliente_api: ClienteAPIAstroMed, al_cerrar=None):
        self.master = master
        self.api = cliente_api
        self.al_cerrar = al_cerrar
        self.op = self.api.operador_actual or {"nombres": "Operador", "rol": "Comandante Medico"}
        self._botones_mision = {}
        self._mision_actual = "ARTEMIS_LUNA"
        self._lecturas_cache = []

        self.master.title(t("pc_titulo_ventana", nombre=self.op["nombres"], rol=self.op["rol"]))
        self.master.configure(bg=tema.COLORES["bg"])
        self.master.minsize(1080, 660)
        tema.configurar_estilos(self.master)

        if self.al_cerrar:
            self.master.protocol("WM_DELETE_WINDOW", self._cerrar)

        self._construir_ui()

        ancho = min(1320, self.master.winfo_screenwidth() - 80)
        alto = min(800, self.master.winfo_screenheight() - 100)
        tema.centrar_ventana(self.master, ancho, alto)

        self._marcar_mision(self._mision_actual)
        self.refrescar_tablero()
        self._actualizar_reloj()

    # ------------------------------------------------------------------
    #  Construcción general
    # ------------------------------------------------------------------
    def _construir_ui(self) -> None:
        self.master.grid_rowconfigure(1, weight=1)
        self.master.grid_columnconfigure(0, weight=1)

        self._construir_topbar()

        cuerpo = tk.Frame(self.master, bg=tema.COLORES["bg"])
        cuerpo.grid(row=1, column=0, sticky="nsew")
        cuerpo.grid_rowconfigure(0, weight=1)
        cuerpo.grid_columnconfigure(1, weight=1)

        self._construir_sidebar(cuerpo)
        self._construir_principal(cuerpo)
        self._construir_statusbar()

    # ------------------------------------------------------------------
    #  Barra superior
    # ------------------------------------------------------------------
    def _construir_topbar(self) -> None:
        barra = tk.Frame(
            self.master,
            bg=tema.COLORES["panel"],
            highlightthickness=1,
            highlightbackground=tema.COLORES["line"],
        )
        barra.grid(row=0, column=0, sticky="ew")
        barra.grid_columnconfigure(1, weight=1)

        marca = tk.Frame(barra, bg=tema.COLORES["panel"])
        marca.grid(row=0, column=0, sticky="w", padx=20, pady=12)

        logo = tk.Label(
            marca,
            text="◈",
            bg=tema.COLORES["panel"],
            fg=tema.COLORES["cyan"],
            font=("Segoe UI Symbol", 21, "bold"),
        )
        logo.pack(side="left", padx=(0, 10))

        textos = tk.Frame(marca, bg=tema.COLORES["panel"])
        textos.pack(side="left")
        tk.Label(
            textos,
            text=t("app_nombre"),
            bg=tema.COLORES["panel"],
            fg=tema.COLORES["text"],
            font=("Segoe UI", 13, "bold"),
            anchor="w",
        ).pack(anchor="w")
        tk.Label(
            textos,
            text=t("app_subtitulo"),
            bg=tema.COLORES["panel"],
            fg=tema.COLORES["muted"],
            font=("Segoe UI", 7, "bold"),
            anchor="w",
        ).pack(anchor="w")

        centro = tk.Frame(barra, bg=tema.COLORES["panel"])
        centro.grid(row=0, column=1, sticky="e", padx=12)

        self.lbl_mision_header = tk.Label(
            centro,
            text="",
            bg=tema.COLORES["panel_2"],
            fg=tema.COLORES["cyan"],
            font=("Segoe UI", 8, "bold"),
            padx=10,
            pady=6,
        )
        self.lbl_mision_header.pack(side="left", padx=(0, 12))

        self.lbl_reloj = tk.Label(
            centro,
            text="--:--:--",
            bg=tema.COLORES["panel"],
            fg=tema.COLORES["muted"],
            font=("Consolas", 9, "bold"),
        )
        self.lbl_reloj.pack(side="left", padx=(0, 14))

        acciones = tk.Frame(barra, bg=tema.COLORES["panel"])
        acciones.grid(row=0, column=2, sticky="e", padx=18, pady=10)

        tema.crear_boton(
            acciones, t("pc_btn_sync"), self.refrescar_tablero, tipo="primary", padx=12, pady=7
        ).pack(side="left", padx=3)
        tema.crear_boton(
            acciones, t("pc_btn_bi"), self.abrir_analitica, tipo="violet", padx=12, pady=7
        ).pack(side="left", padx=3)
        self.btn_consola = tema.crear_boton(
            acciones, t("pc_btn_sql"), self.abrir_consola_sql, tipo="ghost", padx=12, pady=7
        )
        self.btn_consola.pack(side="left", padx=3)
        tema.crear_boton(
            acciones, t("pc_btn_hud"), self._abrir_hud, tipo="success", padx=12, pady=7
        ).pack(side="left", padx=3)
        tema.crear_boton(
            acciones, t("pc_btn_salir"), self._cerrar, tipo="danger", padx=12, pady=7
        ).pack(side="left", padx=3)

        if self.op.get("rol") == "Especialista de Mision":
            self.btn_consola.configure(state="disabled")

    # ------------------------------------------------------------------
    #  Barra lateral
    # ------------------------------------------------------------------
    def _construir_sidebar(self, padre: tk.Misc) -> None:
        sidebar = tk.Frame(padre, bg=tema.COLORES["bg_alt"], width=250)
        sidebar.grid(row=0, column=0, sticky="ns")
        sidebar.grid_propagate(False)
        sidebar.grid_columnconfigure(0, weight=1)
        sidebar.grid_rowconfigure(4, weight=1)

        operador = tema.crear_tarjeta(sidebar, bg=tema.COLORES["panel"])
        operador.grid(row=0, column=0, sticky="ew", padx=14, pady=(16, 12))

        fila_op = tk.Frame(operador, bg=tema.COLORES["panel"])
        fila_op.pack(fill="x", padx=12, pady=12)

        tk.Label(
            fila_op,
            text="◉",
            bg=tema.COLORES["panel"],
            fg=tema.COLORES["cyan"],
            font=("Segoe UI Symbol", 19),
        ).pack(side="left", padx=(0, 10))

        datos_op = tk.Frame(fila_op, bg=tema.COLORES["panel"])
        datos_op.pack(side="left", fill="x", expand=True)
        tk.Label(
            datos_op,
            text=t("pc_operador").upper(),
            bg=tema.COLORES["panel"],
            fg=tema.COLORES["muted_2"],
            font=("Segoe UI", 7, "bold"),
            anchor="w",
        ).pack(anchor="w")
        tk.Label(
            datos_op,
            text=self.op["nombres"],
            bg=tema.COLORES["panel"],
            fg=tema.COLORES["text"],
            font=("Segoe UI", 10, "bold"),
            anchor="w",
        ).pack(anchor="w")
        tk.Label(
            datos_op,
            text=self.op["rol"],
            bg=tema.COLORES["panel"],
            fg=tema.COLORES["mint"],
            font=("Segoe UI", 8),
            anchor="w",
        ).pack(anchor="w")

        separador = tk.Frame(sidebar, bg=tema.COLORES["line_soft"], height=1)
        separador.grid(row=1, column=0, sticky="ew", padx=18, pady=6)

        cabecera = tk.Frame(sidebar, bg=tema.COLORES["bg_alt"])
        cabecera.grid(row=2, column=0, sticky="ew", padx=18, pady=(12, 8))
        tk.Label(
            cabecera,
            text=t("pc_mision_activa").upper(),
            bg=tema.COLORES["bg_alt"],
            fg=tema.COLORES["muted_2"],
            font=("Segoe UI", 7, "bold"),
            anchor="w",
        ).pack(anchor="w")
        tk.Label(
            cabecera,
            text=t("pc_lbl_mision"),
            bg=tema.COLORES["bg_alt"],
            fg=tema.COLORES["muted"],
            font=("Segoe UI", 8),
            anchor="w",
            justify="left",
            wraplength=210,
        ).pack(anchor="w", pady=(2, 0))

        misiones = tk.Frame(sidebar, bg=tema.COLORES["bg_alt"])
        misiones.grid(row=3, column=0, sticky="ew", padx=14)

        for texto, codigo, subclave in (
            (t("pc_mision_luna"), "ARTEMIS_LUNA", "pc_mision_luna_sub"),
            (t("pc_mision_marte"), "ARES_MARTE", "pc_mision_marte_sub"),
            (t("pc_mision_europa"), "EUROPA_JUPITER", "pc_mision_europa_sub"),
        ):
            boton = tema.crear_boton(
                misiones,
                f"{texto}\n{t(subclave)}",
                lambda m=codigo: self.conmutar_mision(m),
                tipo="ghost",
                anchor="w",
                justify="left",
                pady=9,
                padx=12,
                font=("Segoe UI", 8, "bold"),
            )
            boton.pack(fill="x", pady=3)
            self._botones_mision[codigo] = boton

        pie = tk.Frame(sidebar, bg=tema.COLORES["bg_alt"])
        pie.grid(row=5, column=0, sticky="sew", padx=16, pady=14)

        estado = tema.crear_tarjeta(pie, bg=tema.COLORES["panel_2"])
        estado.pack(fill="x")
        fila_estado = tk.Frame(estado, bg=tema.COLORES["panel_2"])
        fila_estado.pack(fill="x", padx=10, pady=9)
        self.dot_sidebar = tk.Label(
            fila_estado,
            text="●",
            bg=tema.COLORES["panel_2"],
            fg=tema.COLORES["muted_2"],
            font=("Segoe UI", 9),
        )
        self.dot_sidebar.pack(side="left", padx=(0, 7))
        self.lbl_sidebar_estado = tk.Label(
            fila_estado,
            text=t("pc_estado_listo"),
            bg=tema.COLORES["panel_2"],
            fg=tema.COLORES["muted"],
            font=("Segoe UI", 8),
            anchor="w",
        )
        self.lbl_sidebar_estado.pack(side="left", fill="x", expand=True)

        tk.Label(
            pie,
            text=t("pc_about"),
            bg=tema.COLORES["bg_alt"],
            fg=tema.COLORES["muted_2"],
            font=("Segoe UI", 7),
            anchor="w",
            justify="left",
            wraplength=210,
        ).pack(fill="x", pady=(10, 0))

    # ------------------------------------------------------------------
    #  Área principal
    # ------------------------------------------------------------------
    def _construir_principal(self, padre: tk.Misc) -> None:
        principal = tk.Frame(padre, bg=tema.COLORES["bg"])
        principal.grid(row=0, column=1, sticky="nsew", padx=(18, 18), pady=(16, 0))
        principal.grid_columnconfigure(0, weight=1)
        principal.grid_rowconfigure(3, weight=1)

        cabecera = tk.Frame(principal, bg=tema.COLORES["bg"])
        cabecera.grid(row=0, column=0, sticky="ew")
        tk.Label(
            cabecera,
            text=t("pc_titulo_panel"),
            bg=tema.COLORES["bg"],
            fg=tema.COLORES["text"],
            font=("Segoe UI", 18, "bold"),
            anchor="w",
        ).pack(anchor="w")
        tk.Label(
            cabecera,
            text=t("pc_subtitulo_panel"),
            bg=tema.COLORES["bg"],
            fg=tema.COLORES["muted"],
            font=("Segoe UI", 9),
            anchor="w",
        ).pack(anchor="w", pady=(2, 0))

        kpis = tk.Frame(principal, bg=tema.COLORES["bg"])
        kpis.grid(row=1, column=0, sticky="ew", pady=(14, 12))
        for i in range(5):
            kpis.grid_columnconfigure(i, weight=1, uniform="kpi")

        self.kpi_trip = self._crear_kpi(kpis, t("pc_kpi_tripulacion"), tema.COLORES["cyan"], 0)
        self.kpi_lect = self._crear_kpi(kpis, t("pc_kpi_lecturas"), tema.COLORES["violet"], 1)
        self.kpi_nom = self._crear_kpi(kpis, t("pc_kpi_nominal"), tema.COLORES["mint"], 2)
        self.kpi_pre = self._crear_kpi(kpis, t("pc_kpi_precaucion"), tema.COLORES["amber"], 3)
        self.kpi_cri = self._crear_kpi(kpis, t("pc_kpi_critico"), tema.COLORES["red"], 4)

        self.notebook = ttk.Notebook(principal)
        self.notebook.grid(row=3, column=0, sticky="nsew")

        self._construir_tab_resumen()
        self._construir_tab_telemetria()
        self._construir_tab_herramientas()

    def _crear_kpi(self, padre: tk.Misc, titulo: str, color: str, columna: int):
        tarjeta = tema.crear_tarjeta(padre, bg=tema.COLORES["panel"])
        tarjeta.grid(row=0, column=columna, sticky="ew", padx=(0 if columna == 0 else 8, 0))
        tarjeta.grid_columnconfigure(0, weight=1)

        tk.Frame(tarjeta, bg=color, height=3).pack(fill="x")
        tk.Label(
            tarjeta,
            text=titulo.upper(),
            bg=tema.COLORES["panel"],
            fg=tema.COLORES["muted"],
            font=("Segoe UI", 7, "bold"),
            anchor="w",
        ).pack(fill="x", padx=12, pady=(9, 0))

        valor = tk.Label(
            tarjeta,
            text="--",
            bg=tema.COLORES["panel"],
            fg=color,
            font=("Segoe UI", 19, "bold"),
            anchor="w",
        )
        valor.pack(fill="x", padx=12)
        return valor

    def _construir_tab_resumen(self) -> None:
        tab = tk.Frame(self.notebook, bg=tema.COLORES["bg"])
        tab.grid_columnconfigure(0, weight=3)
        tab.grid_columnconfigure(1, weight=2)
        tab.grid_rowconfigure(0, weight=1)

        # --- Nómina -----------------------------------------------------
        panel_equipo = tema.crear_tarjeta(tab, bg=tema.COLORES["panel"])
        panel_equipo.grid(row=0, column=0, sticky="nsew", padx=(0, 8), pady=8)
        panel_equipo.grid_columnconfigure(0, weight=1)
        panel_equipo.grid_rowconfigure(1, weight=1)

        encabezado = tk.Frame(panel_equipo, bg=tema.COLORES["panel"])
        encabezado.grid(row=0, column=0, sticky="ew", padx=14, pady=(12, 8))
        tk.Label(
            encabezado,
            text=t("pc_seccion_escuadron"),
            bg=tema.COLORES["panel"],
            fg=tema.COLORES["text"],
            font=("Segoe UI", 11, "bold"),
            anchor="w",
        ).pack(anchor="w")
        tk.Label(
            encabezado,
            text=t("pc_seccion_escuadron_sub"),
            bg=tema.COLORES["panel"],
            fg=tema.COLORES["muted"],
            font=("Segoe UI", 8),
            anchor="w",
        ).pack(anchor="w")

        contenedor = tk.Frame(panel_equipo, bg=tema.COLORES["panel"])
        contenedor.grid(row=1, column=0, sticky="nsew", padx=12, pady=(0, 12))
        contenedor.grid_rowconfigure(0, weight=1)
        contenedor.grid_columnconfigure(0, weight=1)

        cols_t = ("id", "codigo", "nombre", "rol", "especialidad", "racha")
        self.tabla_tripulantes = ttk.Treeview(
            contenedor, columns=cols_t, show="headings", height=9, selectmode="browse"
        )
        encabezados_t = {
            "id": ("ID", 45),
            "codigo": (t("pc_col_codigo"), 100),
            "nombre": (t("pc_col_nombre"), 205),
            "rol": (t("pc_col_rol"), 155),
            "especialidad": (t("pc_col_esp"), 195),
            "racha": (t("pc_col_racha"), 125),
        }
        for col, (texto, ancho) in encabezados_t.items():
            self.tabla_tripulantes.heading(col, text=texto)
            self.tabla_tripulantes.column(col, width=ancho, anchor="center")

        scroll_t = ttk.Scrollbar(contenedor, orient="vertical", command=self.tabla_tripulantes.yview)
        self.tabla_tripulantes.configure(yscrollcommand=scroll_t.set)
        self.tabla_tripulantes.grid(row=0, column=0, sticky="nsew")
        scroll_t.grid(row=0, column=1, sticky="ns")
        self.tabla_tripulantes.bind("<<TreeviewSelect>>", self._actualizar_seleccion)

        # --- Crisis -----------------------------------------------------
        panel_crisis = tema.crear_tarjeta(tab, bg=tema.COLORES["panel"])
        panel_crisis.grid(row=0, column=1, sticky="nsew", padx=(8, 0), pady=8)

        tk.Label(
            panel_crisis,
            text=t("pc_seccion_crisis"),
            bg=tema.COLORES["panel"],
            fg=tema.COLORES["text"],
            font=("Segoe UI", 11, "bold"),
            anchor="w",
        ).pack(fill="x", padx=14, pady=(12, 0))
        tk.Label(
            panel_crisis,
            text=t("pc_seccion_crisis_sub"),
            bg=tema.COLORES["panel"],
            fg=tema.COLORES["muted"],
            font=("Segoe UI", 8),
            anchor="w",
            justify="left",
            wraplength=320,
        ).pack(fill="x", padx=14, pady=(2, 10))

        self.lbl_trip_sel = tk.Label(
            panel_crisis,
            text=t("pc_sin_seleccion"),
            bg=tema.COLORES["panel_2"],
            fg=tema.COLORES["cyan"],
            font=("Segoe UI", 8, "bold"),
            anchor="w",
            padx=10,
            pady=7,
        )
        self.lbl_trip_sel.pack(fill="x", padx=14, pady=(0, 12))

        for etiqueta, subclave, codigo, tipo in (
            ("pc_crisis_rad", "pc_crisis_rad_sub", "TORMENTA_SOLAR", "danger"),
            ("pc_crisis_psy", "pc_crisis_psy_sub", "CONFINAMIENTO_ROVER", "violet"),
            ("pc_crisis_met", "pc_crisis_met_sub", "HIPOGLUCEMIA_EVA", "warning"),
            ("pc_crisis_mus", "pc_crisis_mus_sub", "ATROFIA_CERO_G", "success"),
        ):
            tema.crear_boton(
                panel_crisis,
                f"{t(etiqueta)}\n{t(subclave)}",
                lambda c=codigo: self.disparar_simulacion(c),
                tipo=tipo,
                anchor="w",
                justify="left",
                pady=9,
                padx=12,
                font=("Segoe UI", 8, "bold"),
            ).pack(fill="x", padx=14, pady=3)

        self.notebook.add(tab, text=t("pc_tab_resumen"))

    def _construir_tab_telemetria(self) -> None:
        tab = tk.Frame(self.notebook, bg=tema.COLORES["bg"])
        tab.grid_columnconfigure(0, weight=1)
        tab.grid_rowconfigure(0, weight=1)

        panel = tema.crear_tarjeta(tab, bg=tema.COLORES["panel"])
        panel.grid(row=0, column=0, sticky="nsew", padx=8, pady=8)
        panel.grid_columnconfigure(0, weight=1)
        panel.grid_rowconfigure(1, weight=1)

        encabezado = tk.Frame(panel, bg=tema.COLORES["panel"])
        encabezado.grid(row=0, column=0, sticky="ew", padx=14, pady=(12, 8))
        tk.Label(
            encabezado,
            text=t("pc_tab_telemetria"),
            bg=tema.COLORES["panel"],
            fg=tema.COLORES["text"],
            font=("Segoe UI", 11, "bold"),
            anchor="w",
        ).pack(anchor="w")
        tk.Label(
            encabezado,
            text=t("pc_seccion_telemetria_sub"),
            bg=tema.COLORES["panel"],
            fg=tema.COLORES["muted"],
            font=("Segoe UI", 8),
            anchor="w",
        ).pack(anchor="w")

        contenedor = tk.Frame(panel, bg=tema.COLORES["panel"])
        contenedor.grid(row=1, column=0, sticky="nsew", padx=12, pady=(0, 12))
        contenedor.grid_rowconfigure(0, weight=1)
        contenedor.grid_columnconfigure(0, weight=1)

        cols_l = (
            "id",
            "fecha",
            "tripulante",
            "entorno",
            "pa",
            "fc",
            "glucosa",
            "sueno",
            "alerta",
            "sistema",
            "diagnostico",
        )
        self.tabla_telemetria = ttk.Treeview(
            contenedor, columns=cols_l, show="headings", height=14
        )
        encabezados_l = {
            "id": ("ID", 40),
            "fecha": (t("pc_col_fecha"), 135),
            "tripulante": (t("pc_col_trip"), 60),
            "entorno": (t("pc_col_entorno"), 145),
            "pa": (t("pc_col_pa"), 110),
            "fc": (t("pc_col_fc"), 70),
            "glucosa": (t("pc_col_glu"), 80),
            "sueno": (t("pc_col_sueno"), 60),
            "alerta": (t("pc_col_alerta"), 95),
            "sistema": (t("pc_col_sis"), 135),
            "diagnostico": (t("pc_col_diag"), 360),
        }
        for col, (texto, ancho) in encabezados_l.items():
            self.tabla_telemetria.heading(col, text=texto)
            self.tabla_telemetria.column(col, width=ancho, anchor="center")

        self.tabla_telemetria.tag_configure(
            "NOMINAL", background=tema.FONDO_ALERTA["NOMINAL"], foreground="#6ee7b7"
        )
        self.tabla_telemetria.tag_configure(
            "PRECAUCION", background=tema.FONDO_ALERTA["PRECAUCION"], foreground="#fcd34d"
        )
        self.tabla_telemetria.tag_configure(
            "CRITICO", background=tema.FONDO_ALERTA["CRITICO"], foreground="#fca5a5"
        )

        scroll_y = ttk.Scrollbar(contenedor, orient="vertical", command=self.tabla_telemetria.yview)
        scroll_x = ttk.Scrollbar(contenedor, orient="horizontal", command=self.tabla_telemetria.xview)
        self.tabla_telemetria.configure(yscrollcommand=scroll_y.set, xscrollcommand=scroll_x.set)
        self.tabla_telemetria.grid(row=0, column=0, sticky="nsew")
        scroll_y.grid(row=0, column=1, sticky="ns")
        scroll_x.grid(row=1, column=0, sticky="ew")

        self.notebook.add(tab, text=t("pc_tab_telemetria"))

    def _construir_tab_herramientas(self) -> None:
        tab = tk.Frame(self.notebook, bg=tema.COLORES["bg"])
        tab.grid_columnconfigure(0, weight=1)
        tab.grid_columnconfigure(1, weight=1)
        tab.grid_columnconfigure(2, weight=1)
        tab.grid_rowconfigure(0, weight=1)

        self.btn_sql_tool = self._crear_herramienta(
            tab,
            "▥",
            t("pc_herramienta_sql"),
            t("pc_herramienta_sql_sub"),
            t("pc_btn_sql"),
            self.abrir_consola_sql,
            "ghost",
            0,
        )
        self._crear_herramienta(
            tab,
            "◔",
            t("pc_herramienta_bi"),
            t("pc_herramienta_bi_sub"),
            t("pc_btn_bi"),
            self.abrir_analitica,
            "violet",
            1,
        )
        self._crear_herramienta(
            tab,
            "◈",
            t("pc_herramienta_hud"),
            t("pc_herramienta_hud_sub"),
            t("pc_btn_hud"),
            self._abrir_hud,
            "primary",
            2,
        )

        if self.op.get("rol") == "Especialista de Mision":
            self.btn_sql_tool.configure(state="disabled")

        self.notebook.add(tab, text=t("pc_tab_herramientas"))

    def _crear_herramienta(
        self,
        padre: tk.Misc,
        icono: str,
        titulo: str,
        descripcion: str,
        texto_boton: str,
        comando,
        tipo: str,
        columna: int,
    ) -> tk.Button:
        panel = tema.crear_tarjeta(padre, bg=tema.COLORES["panel"])
        panel.grid(
            row=0,
            column=columna,
            sticky="nsew",
            padx=(0 if columna == 0 else 8, 0),
            pady=8,
        )

        tk.Label(
            panel,
            text=icono,
            bg=tema.COLORES["panel"],
            fg=tema.COLORES["cyan"],
            font=("Segoe UI Symbol", 24),
            anchor="w",
        ).pack(fill="x", padx=16, pady=(18, 6))
        tk.Label(
            panel,
            text=titulo,
            bg=tema.COLORES["panel"],
            fg=tema.COLORES["text"],
            font=("Segoe UI", 11, "bold"),
            anchor="w",
        ).pack(fill="x", padx=16)
        tk.Label(
            panel,
            text=descripcion,
            bg=tema.COLORES["panel"],
            fg=tema.COLORES["muted"],
            font=("Segoe UI", 8),
            anchor="w",
            justify="left",
            wraplength=280,
        ).pack(fill="x", padx=16, pady=(5, 16))

        boton = tema.crear_boton(panel, texto_boton, comando, tipo=tipo, padx=14, pady=8)
        boton.pack(fill="x", padx=16, pady=(0, 18))
        return boton

    # ------------------------------------------------------------------
    #  Barra de estado
    # ------------------------------------------------------------------
    def _construir_statusbar(self) -> None:
        barra = tk.Frame(self.master, bg=tema.COLORES["bg_alt"])
        barra.grid(row=2, column=0, sticky="ew")
        barra.grid_columnconfigure(1, weight=1)

        self.dot_estado = tk.Label(
            barra,
            text="●",
            bg=tema.COLORES["bg_alt"],
            fg=tema.COLORES["muted_2"],
            font=("Segoe UI", 9),
        )
        self.dot_estado.grid(row=0, column=0, padx=(18, 6), pady=6)
        self.lbl_estado = tk.Label(
            barra,
            text=t("pc_estado_listo"),
            bg=tema.COLORES["bg_alt"],
            fg=tema.COLORES["muted"],
            font=("Segoe UI", 8),
            anchor="w",
        )
        self.lbl_estado.grid(row=0, column=1, sticky="w")

        self.lbl_ultima_sync = tk.Label(
            barra,
            text="",
            bg=tema.COLORES["bg_alt"],
            fg=tema.COLORES["muted_2"],
            font=("Consolas", 8),
            anchor="e",
        )
        self.lbl_ultima_sync.grid(row=0, column=2, sticky="e", padx=18)

    # ------------------------------------------------------------------
    #  Estado
    # ------------------------------------------------------------------
    def _set_estado(self, ok: bool, mensaje: str) -> None:
        color = tema.COLORES["mint"] if ok else tema.COLORES["red"]
        for widget in (self.dot_estado, self.dot_sidebar):
            try:
                widget.configure(fg=color)
            except tk.TclError:
                pass
        for widget in (self.lbl_estado, self.lbl_sidebar_estado):
            try:
                widget.configure(text=mensaje, fg=color if not ok else tema.COLORES["muted"])
            except tk.TclError:
                pass

    def _actualizar_reloj(self) -> None:
        try:
            if not self.master.winfo_exists():
                return
            self.lbl_reloj.configure(text=datetime.datetime.now().strftime("%H:%M:%S"))
            self.master.after(1000, self._actualizar_reloj)
        except tk.TclError:
            pass

    # ------------------------------------------------------------------
    #  Datos
    # ------------------------------------------------------------------
    def obtener_id_tripulante_seleccionado(self) -> int:
        sel = self.tabla_tripulantes.selection()
        if sel:
            valores = self.tabla_tripulantes.item(sel[0], "values")
            return int(valores[0])
        items = self.tabla_tripulantes.get_children()
        if items:
            return int(self.tabla_tripulantes.item(items[0], "values")[0])
        return 1

    def refrescar_tablero(self) -> None:
        seleccion_previa = None
        if self.tabla_tripulantes.selection():
            seleccion_previa = self.tabla_tripulantes.item(
                self.tabla_tripulantes.selection()[0], "values"
            )[0]

        try:
            tripulantes = self.api.listar_tripulantes()
            lecturas = self.api.listar_telemetria()
        except Exception as e:
            self._set_estado(False, f"{t('pc_estado_error')} · {e}")
            return

        self._lecturas_cache = lecturas

        for item in self.tabla_tripulantes.get_children():
            self.tabla_tripulantes.delete(item)
        for item in self.tabla_telemetria.get_children():
            self.tabla_telemetria.delete(item)

        for t_row in tripulantes:
            self.tabla_tripulantes.insert(
                "",
                "end",
                values=(
                    t_row["id"],
                    t_row["codigo_astronauta"],
                    f"{t_row['nombres']} {t_row['apellidos']}",
                    t_row["rol"],
                    t_row["especialidad"],
                    f"{t_row['racha_autocuidado']} Sol",
                ),
            )

        for l in lecturas[:45]:
            alerta = l["nivel_alerta"]
            self.tabla_telemetria.insert(
                "",
                "end",
                values=(
                    l["id"],
                    l["fecha"],
                    f"AST-00{l['id_tripulante']}",
                    l["entorno"],
                    f"{l['presion_sistolica']}/{l['presion_diastolica']} ({l['presion_media']})",
                    f"{l['frecuencia_cardiaca']} bpm",
                    f"{l['glucosa_mg_dl']} mg/dL",
                    f"{l['horas_sueno']} h",
                    alerta,
                    l["sistema_afectado"],
                    l["instruccion_accion"],
                ),
                tags=(alerta,),
            )

        self._actualizar_kpis(tripulantes, lecturas)

        items = self.tabla_tripulantes.get_children()
        if items:
            objetivo = items[0]
            if seleccion_previa is not None:
                for item in items:
                    if str(self.tabla_tripulantes.item(item, "values")[0]) == str(seleccion_previa):
                        objetivo = item
                        break
            self.tabla_tripulantes.selection_set(objetivo)
            self.tabla_tripulantes.focus(objetivo)

        self._actualizar_seleccion()
        self._set_estado(True, t("pc_estado_listo"))
        self.lbl_ultima_sync.configure(
            text=t("pc_ultima_sync", hora=datetime.datetime.now().strftime("%H:%M:%S"))
        )

    def _actualizar_kpis(self, tripulantes, lecturas) -> None:
        self.kpi_trip.configure(text=str(len(tripulantes)))
        self.kpi_lect.configure(text=str(len(lecturas)))
        conteo = {"NOMINAL": 0, "PRECAUCION": 0, "CRITICO": 0}
        for lectura in lecturas:
            nivel = lectura.get("nivel_alerta", "NOMINAL")
            if nivel in conteo:
                conteo[nivel] += 1
        self.kpi_nom.configure(text=str(conteo["NOMINAL"]))
        self.kpi_pre.configure(text=str(conteo["PRECAUCION"]))
        self.kpi_cri.configure(text=str(conteo["CRITICO"]))

    def _actualizar_seleccion(self, _evento=None) -> None:
        sel = self.tabla_tripulantes.selection()
        if not sel:
            self.lbl_trip_sel.configure(text=t("pc_sin_seleccion"))
            return
        valores = self.tabla_tripulantes.item(sel[0], "values")
        nombre = valores[2] if len(valores) > 2 else valores[0]
        self.lbl_trip_sel.configure(text=t("pc_tripulante_sel", nombre=nombre))

    # ------------------------------------------------------------------
    #  Acciones
    # ------------------------------------------------------------------
    def _marcar_mision(self, codigo_mision: str) -> None:
        for codigo, boton in self._botones_mision.items():
            try:
                if codigo == codigo_mision:
                    boton.configure(
                        bg=tema.COLORES_MISION.get(codigo, tema.COLORES["cyan_dark"]),
                        fg=tema.COLORES["white"],
                        activebackground=tema.COLORES_MISION.get(codigo, tema.COLORES["cyan_dark"]),
                        activeforeground=tema.COLORES["white"],
                    )
                else:
                    boton.configure(
                        bg=tema.COLORES["panel_3"],
                        fg=tema.COLORES["muted"],
                        activebackground=tema.COLORES["panel_4"],
                        activeforeground=tema.COLORES["text"],
                    )
            except tk.TclError:
                pass

        nombres = {
            "ARTEMIS_LUNA": t("pc_mision_luna"),
            "ARES_MARTE": t("pc_mision_marte"),
            "EUROPA_JUPITER": t("pc_mision_europa"),
        }
        self.lbl_mision_header.configure(
            text=f"{t('pc_mision_activa').upper()} · {nombres.get(codigo_mision, codigo_mision)}"
        )

    def conmutar_mision(self, codigo_mision: str) -> None:
        try:
            self.api.cambiar_mision(codigo_mision)
            self._mision_actual = codigo_mision
            self._marcar_mision(codigo_mision)
            self.refrescar_tablero()
            messagebox.showinfo(t("pc_msg_mision_tit"), t("pc_msg_mision_txt", mision=codigo_mision))
        except Exception as e:
            self._set_estado(False, f"{t('pc_estado_error')} · {e}")
            messagebox.showerror("Error", str(e))

    def disparar_simulacion(self, escenario: str) -> None:
        id_t = self.obtener_id_tripulante_seleccionado()
        try:
            res = self.api.simular_crisis(id_t, escenario)
            diag = res["diagnostico"]
            self.refrescar_tablero()
            messagebox.showwarning(
                t("pc_msg_triage_tit", nivel=diag["nivel_alerta_global"]),
                f"{t('pc_msg_triage_sis')}: {diag['sistema_afectado_principal']}\n\n"
                f"{t('pc_msg_triage_diag')}: {diag['resumen_clinico']}\n\n"
                f"{t('pc_msg_triage_prot')}: {diag['instruccion_paso_a_paso']}",
            )
        except Exception as e:
            self._set_estado(False, f"{t('pc_estado_error')} · {e}")
            messagebox.showerror("Error", str(e))

    def abrir_analitica(self) -> None:
        id_t = self.obtener_id_tripulante_seleccionado()
        top = tk.Toplevel(self.master)
        VentanaAnalitica(top, self.api, id_tripulante_inicial=id_t)

    def abrir_consola_sql(self) -> None:
        if self.op.get("rol") == "Especialista de Mision":
            messagebox.showinfo(t("sql_err_titulo"), t("pc_rol_restriccion"))
            return
        top = tk.Toplevel(self.master)
        VentanaConsolaSQL(top, self.api)

    def _abrir_hud(self) -> None:
        webbrowser.open("http://127.0.0.1:8080")

    def _cerrar(self) -> None:
        self.master.destroy()
        if self.al_cerrar:
            self.al_cerrar()
