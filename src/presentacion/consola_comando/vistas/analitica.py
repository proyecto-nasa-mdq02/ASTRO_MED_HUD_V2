# ===========================================================================
#  TABLERO DE ANALÍTICA BIOMÉTRICA Y SERIES TEMPORALES (CAPA 4 - MATPLOTLIB)
# ===========================================================================

import tkinter as tk
from tkinter import ttk

from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from src.presentacion.i18n import t
from src.presentacion.consola_comando.cliente_api import ClienteAPIAstroMed
from src.presentacion.consola_comando import tema


class VentanaAnalitica:
    def __init__(self, master: tk.Toplevel, cliente_api: ClienteAPIAstroMed, id_tripulante_inicial: int = 1):
        self.master = master
        self.api = cliente_api
        self.id_tripulante = id_tripulante_inicial
        self._tripulantes = []
        self._ids_tripulantes = []

        self.master.title(t("bi_titulo_ventana"))
        self.master.configure(bg=tema.COLORES["bg"])
        self.master.minsize(920, 620)
        tema.configurar_estilos(self.master)

        self._construir_ui()

        ancho = min(1100, self.master.winfo_screenwidth() - 80)
        alto = min(740, self.master.winfo_screenheight() - 100)
        tema.centrar_ventana(self.master, ancho, alto)

        self._cargar_tripulantes()
        self.cargar_y_dibujar()

    # ------------------------------------------------------------------
    #  Interfaz
    # ------------------------------------------------------------------
    def _construir_ui(self) -> None:
        self.master.grid_rowconfigure(1, weight=1)
        self.master.grid_columnconfigure(0, weight=1)

        cabecera = tk.Frame(
            self.master,
            bg=tema.COLORES["panel"],
            highlightthickness=1,
            highlightbackground=tema.COLORES["line"],
        )
        cabecera.grid(row=0, column=0, sticky="ew")
        cabecera.grid_columnconfigure(0, weight=1)

        textos = tk.Frame(cabecera, bg=tema.COLORES["panel"])
        textos.grid(row=0, column=0, sticky="w", padx=20, pady=13)

        tk.Label(
            textos,
            text="◔  " + t("bi_titulo_ventana"),
            bg=tema.COLORES["panel"],
            fg=tema.COLORES["text"],
            font=("Segoe UI", 12, "bold"),
            anchor="w",
        ).pack(anchor="w")
        self.lbl_cabecera = tk.Label(
            textos,
            text=t("bi_cabecera", id=self.id_tripulante),
            bg=tema.COLORES["panel"],
            fg=tema.COLORES["cyan"],
            font=("Segoe UI", 8, "bold"),
            anchor="w",
        )
        self.lbl_cabecera.pack(anchor="w", pady=(2, 0))

        selector = tk.Frame(cabecera, bg=tema.COLORES["panel"])
        selector.grid(row=0, column=1, sticky="e", padx=20)

        tk.Label(
            selector,
            text=t("bi_selector"),
            bg=tema.COLORES["panel"],
            fg=tema.COLORES["muted"],
            font=("Segoe UI", 8, "bold"),
        ).pack(side="left", padx=(0, 8))

        self.combo_tripulante = ttk.Combobox(selector, state="readonly", width=34)
        self.combo_tripulante.pack(side="left")
        self.combo_tripulante.bind("<<ComboboxSelected>>", self._cambiar_tripulante)

        cuerpo = tk.Frame(self.master, bg=tema.COLORES["bg"])
        cuerpo.grid(row=1, column=0, sticky="nsew", padx=18, pady=14)
        cuerpo.grid_columnconfigure(0, weight=1)
        cuerpo.grid_rowconfigure(1, weight=1)

        # --- KPIs -------------------------------------------------------
        kpis = tk.Frame(cuerpo, bg=tema.COLORES["bg"])
        kpis.grid(row=0, column=0, sticky="ew", pady=(0, 10))
        for i in range(4):
            kpis.grid_columnconfigure(i, weight=1, uniform="bi_kpi")

        self.kpi_total = self._crear_kpi(kpis, t("bi_total"), tema.COLORES["cyan"], 0)
        self.kpi_fc = self._crear_kpi(kpis, t("bi_prom_fc"), tema.COLORES["amber"], 1)
        self.kpi_glu = self._crear_kpi(kpis, t("bi_prom_glu"), tema.COLORES["mint"], 2)
        self.kpi_rad = self._crear_kpi(kpis, t("bi_prom_rad"), tema.COLORES["violet"], 3)

        panel_grafico = tema.crear_tarjeta(cuerpo, bg=tema.COLORES["panel"])
        panel_grafico.grid(row=1, column=0, sticky="nsew")
        panel_grafico.grid_rowconfigure(0, weight=1)
        panel_grafico.grid_columnconfigure(0, weight=1)

        self.figura = Figure(figsize=(10, 5.6), dpi=100, facecolor=tema.COLORES["panel"])
        self.canvas = FigureCanvasTkAgg(self.figura, master=panel_grafico)
        self.canvas.get_tk_widget().configure(bg=tema.COLORES["panel"], highlightthickness=0)
        self.canvas.get_tk_widget().grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

        self.lbl_error = tk.Label(
            cuerpo,
            text="",
            bg=tema.COLORES["bg"],
            fg=tema.COLORES["red"],
            font=("Segoe UI", 8),
            anchor="w",
        )
        self.lbl_error.grid(row=2, column=0, sticky="ew", pady=(6, 0))

    def _crear_kpi(self, padre: tk.Misc, titulo: str, color: str, columna: int) -> tk.Label:
        tarjeta = tema.crear_tarjeta(padre, bg=tema.COLORES["panel"])
        tarjeta.grid(row=0, column=columna, sticky="ew", padx=(0 if columna == 0 else 8, 0))
        tk.Frame(tarjeta, bg=color, height=3).pack(fill="x")
        tk.Label(
            tarjeta,
            text=titulo.upper(),
            bg=tema.COLORES["panel"],
            fg=tema.COLORES["muted"],
            font=("Segoe UI", 7, "bold"),
            anchor="w",
        ).pack(fill="x", padx=12, pady=(8, 0))
        valor = tk.Label(
            tarjeta,
            text="--",
            bg=tema.COLORES["panel"],
            fg=color,
            font=("Segoe UI", 17, "bold"),
            anchor="w",
        )
        valor.pack(fill="x", padx=12, pady=(0, 8))
        return valor

    # ------------------------------------------------------------------
    #  Datos
    # ------------------------------------------------------------------
    def _cargar_tripulantes(self) -> None:
        try:
            self._tripulantes = self.api.listar_tripulantes()
        except Exception as e:
            self._tripulantes = []
            self.lbl_error.configure(text=t("bi_error", error=e))

        valores = []
        self._ids_tripulantes = []
        for tripulante in self._tripulantes:
            self._ids_tripulantes.append(tripulante["id"])
            valores.append(
                f"{tripulante['codigo_astronauta']} · {tripulante['nombres']} {tripulante['apellidos']}"
            )

        if valores:
            self.combo_tripulante.configure(values=valores)
            indice = 0
            if self.id_tripulante in self._ids_tripulantes:
                indice = self._ids_tripulantes.index(self.id_tripulante)
            self.combo_tripulante.current(indice)
            self.id_tripulante = self._ids_tripulantes[indice]
            self.lbl_cabecera.configure(text=t("bi_cabecera", id=self.id_tripulante))

    def _cambiar_tripulante(self, _evento=None) -> None:
        indice = self.combo_tripulante.current()
        if 0 <= indice < len(self._ids_tripulantes):
            self.id_tripulante = self._ids_tripulantes[indice]
            self.lbl_cabecera.configure(text=t("bi_cabecera", id=self.id_tripulante))
            self.cargar_y_dibujar()

    def _estilizar_eje(self, eje, titulo: str) -> None:
        eje.set_facecolor(tema.COLORES["panel"])
        eje.set_title(
            titulo,
            color=tema.COLORES["text"],
            fontsize=10,
            fontweight="bold",
            loc="left",
            pad=10,
        )
        eje.tick_params(colors=tema.COLORES["muted"], labelsize=8)
        eje.xaxis.label.set_color(tema.COLORES["muted"])
        eje.yaxis.label.set_color(tema.COLORES["muted"])
        for spine in eje.spines.values():
            spine.set_color(tema.COLORES["line"])
        eje.grid(True, color=tema.COLORES["line_soft"], linestyle="--", linewidth=0.7, alpha=0.9)

    @staticmethod
    def _formato_promedio(valor) -> str:
        if isinstance(valor, (int, float)):
            return f"{valor:g}"
        return "--"

    def cargar_y_dibujar(self) -> None:
        try:
            datos = self.api.obtener_analitica(self.id_tripulante)
            self.lbl_error.configure(text="")
        except Exception as e:
            self.lbl_error.configure(text=t("bi_error", error=e))
            datos = {"total_lecturas": 0, "series": {}, "promedios": {}}

        self.datos_actuales = datos
        prom = datos.get("promedios", {}) or {}

        self.kpi_total.configure(text=str(datos.get("total_lecturas", 0)))
        self.kpi_fc.configure(text=self._formato_promedio(prom.get("frecuencia_cardiaca")))
        self.kpi_glu.configure(text=self._formato_promedio(prom.get("glucosa_mg_dl")))
        self.kpi_rad.configure(text=self._formato_promedio(prom.get("radiacion_acumulada_msv")))

        self.figura.clear()
        series = datos.get("series", {}) or {}
        frecuencia = series.get("frecuencia_cardiaca", []) or []
        sistolica = series.get("presion_sistolica", []) or []
        glucosa = series.get("glucosa_mg_dl", []) or []

        if not frecuencia:
            eje = self.figura.add_subplot(111)
            eje.set_facecolor(tema.COLORES["panel"])
            eje.axis("off")
            eje.text(
                0.5,
                0.5,
                t("bi_sin_datos"),
                ha="center",
                va="center",
                color=tema.COLORES["muted"],
                fontsize=11,
            )
            self.canvas.draw()
            return

        ax1 = self.figura.add_subplot(211)
        self._estilizar_eje(ax1, t("bi_graf1_tit"))
        if sistolica:
            x_sis = list(range(1, len(sistolica) + 1))
            ax1.plot(
                x_sis,
                sistolica,
                color=tema.COLORES["cyan"],
                marker="o",
                markersize=4,
                linewidth=2.2,
                label=t("bi_graf1_sis"),
                zorder=3,
            )
            ax1.fill_between(
                x_sis,
                sistolica,
                min(sistolica) - 8,
                color=tema.COLORES["cyan"],
                alpha=0.10,
                zorder=1,
            )
        ax1.set_ylabel(t("bi_graf1_sis"), fontsize=8)

        ax1b = ax1.twinx()
        ax1b.set_facecolor(tema.COLORES["panel"])
        ax1b.plot(
            list(range(1, len(frecuencia) + 1)),
            frecuencia,
            color=tema.COLORES["amber"],
            marker="s",
            markersize=3.5,
            linewidth=2,
            label=t("bi_graf1_fc"),
            zorder=3,
        )
        ax1b.tick_params(colors=tema.COLORES["muted"], labelsize=8)
        ax1b.set_ylabel(t("bi_graf1_fc"), fontsize=8, color=tema.COLORES["muted"])
        for spine in ax1b.spines.values():
            spine.set_color(tema.COLORES["line"])

        lineas = ax1.get_lines() + ax1b.get_lines()
        etiquetas = [linea.get_label() for linea in lineas]
        leyenda = ax1.legend(
            lineas,
            etiquetas,
            loc="upper left",
            fontsize=8,
            facecolor=tema.COLORES["panel_2"],
            edgecolor=tema.COLORES["line"],
            labelcolor=tema.COLORES["text"],
            framealpha=0.95,
        )
        leyenda.get_frame().set_linewidth(0.8)

        ax2 = self.figura.add_subplot(212)
        self._estilizar_eje(ax2, t("bi_graf2_tit"))
        if glucosa:
            x_glu = list(range(1, len(glucosa) + 1))
            ax2.plot(
                x_glu,
                glucosa,
                color=tema.COLORES["mint"],
                marker="^",
                markersize=4,
                linewidth=2.2,
                label=t("bi_graf2_glu"),
                zorder=3,
            )
            ax2.fill_between(
                x_glu,
                glucosa,
                min(glucosa) - 6,
                color=tema.COLORES["mint"],
                alpha=0.10,
                zorder=1,
            )
            leyenda2 = ax2.legend(
                loc="upper left",
                fontsize=8,
                facecolor=tema.COLORES["panel_2"],
                edgecolor=tema.COLORES["line"],
                labelcolor=tema.COLORES["text"],
                framealpha=0.95,
            )
            leyenda2.get_frame().set_linewidth(0.8)
        ax2.set_ylabel(t("bi_graf2_glu"), fontsize=8)
        ax2.set_xlabel(t("bi_eje_lecturas"), fontsize=8)

        self.figura.tight_layout(pad=2.2)
        self.canvas.draw()
