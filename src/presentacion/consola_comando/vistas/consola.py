# =================================================================
#  CONSOLA DE AUDITORÍA SQL EN CAJA DE ARENA (SANDBOXING - CAPA 4)
# =================================================================

import tkinter as tk
from tkinter import ttk, messagebox

from src.presentacion.i18n import t
from src.presentacion.consola_comando.cliente_api import ClienteAPIAstroMed, ErrorClienteAPI
from src.presentacion.consola_comando import tema


class VentanaConsolaSQL:
    def __init__(self, master: tk.Toplevel, cliente_api: ClienteAPIAstroMed):
        self.master = master
        self.api = cliente_api

        self.master.title(t("sql_titulo_ventana"))
        self.master.configure(bg=tema.COLORES["bg"])
        self.master.minsize(820, 540)
        tema.configurar_estilos(self.master)

        self._construir_ui()

        ancho = min(1040, self.master.winfo_screenwidth() - 100)
        alto = min(680, self.master.winfo_screenheight() - 120)
        tema.centrar_ventana(self.master, ancho, alto)

    def _construir_ui(self) -> None:
        self.master.grid_rowconfigure(2, weight=1)
        self.master.grid_columnconfigure(0, weight=1)

        cabecera = tk.Frame(
            self.master,
            bg=tema.COLORES["panel"],
            highlightthickness=1,
            highlightbackground=tema.COLORES["line"],
        )
        cabecera.grid(row=0, column=0, sticky="ew")

        textos = tk.Frame(cabecera, bg=tema.COLORES["panel"])
        textos.pack(side="left", padx=20, pady=13)
        tk.Label(
            textos,
            text="▥  " + t("sql_titulo_ventana"),
            bg=tema.COLORES["panel"],
            fg=tema.COLORES["text"],
            font=("Segoe UI", 12, "bold"),
            anchor="w",
        ).pack(anchor="w")
        tk.Label(
            textos,
            text=t("sql_subtitulo"),
            bg=tema.COLORES["panel"],
            fg=tema.COLORES["muted"],
            font=("Segoe UI", 8),
            anchor="w",
        ).pack(anchor="w", pady=(2, 0))

        tk.Label(
            cabecera,
            text="SELECT ONLY · SANDBOX",
            bg=tema.COLORES["panel_2"],
            fg=tema.COLORES["cyan"],
            font=("Consolas", 8, "bold"),
            padx=10,
            pady=6,
        ).pack(side="right", padx=20)

        consulta = tema.crear_tarjeta(self.master, bg=tema.COLORES["panel"])
        consulta.grid(row=1, column=0, sticky="ew", padx=18, pady=(14, 8))
        consulta.grid_columnconfigure(0, weight=1)

        tk.Label(
            consulta,
            text=t("sql_instruccion"),
            bg=tema.COLORES["panel"],
            fg=tema.COLORES["muted"],
            font=("Segoe UI", 8, "bold"),
            anchor="w",
        ).grid(row=0, column=0, sticky="ew", padx=14, pady=(11, 6))

        self.txt_query = tk.Entry(
            consulta,
            font=("Consolas", 10),
            bg=tema.COLORES["bg_alt"],
            fg=tema.COLORES["text"],
            insertbackground=tema.COLORES["cyan"],
            relief="flat",
            bd=0,
            highlightthickness=1,
            highlightbackground=tema.COLORES["line"],
            highlightcolor=tema.COLORES["cyan"],
        )
        self.txt_query.insert(
            0,
            "SELECT codigo_astronauta, nombres, apellidos, rol, racha_autocuidado FROM vista_tripulacion_activa",
        )
        self.txt_query.grid(row=1, column=0, sticky="ew", padx=14, pady=(0, 10), ipady=7)
        self.txt_query.bind("<Return>", lambda _e: self.ejecutar_consulta())

        tema.crear_boton(
            consulta,
            t("sql_btn_ejecutar"),
            self.ejecutar_consulta,
            tipo="success",
            padx=16,
            pady=8,
        ).grid(row=1, column=1, padx=(0, 14), pady=(0, 10))

        panel = tema.crear_tarjeta(self.master, bg=tema.COLORES["panel"])
        panel.grid(row=2, column=0, sticky="nsew", padx=18, pady=(0, 14))
        panel.grid_rowconfigure(0, weight=1)
        panel.grid_columnconfigure(0, weight=1)

        contenedor = tk.Frame(panel, bg=tema.COLORES["panel"])
        contenedor.grid(row=0, column=0, sticky="nsew", padx=12, pady=12)
        contenedor.grid_rowconfigure(0, weight=1)
        contenedor.grid_columnconfigure(0, weight=1)

        self.tabla = ttk.Treeview(contenedor, show="headings")
        scroll_y = ttk.Scrollbar(contenedor, orient="vertical", command=self.tabla.yview)
        scroll_x = ttk.Scrollbar(contenedor, orient="horizontal", command=self.tabla.xview)
        self.tabla.configure(yscrollcommand=scroll_y.set, xscrollcommand=scroll_x.set)
        self.tabla.grid(row=0, column=0, sticky="nsew")
        scroll_y.grid(row=0, column=1, sticky="ns")
        scroll_x.grid(row=1, column=0, sticky="ew")

        self.lbl_resultado = tk.Label(
            self.master,
            text="",
            bg=tema.COLORES["bg"],
            fg=tema.COLORES["muted"],
            font=("Segoe UI", 8),
            anchor="w",
        )
        self.lbl_resultado.grid(row=3, column=0, sticky="ew", padx=20, pady=(0, 10))

    def ejecutar_consulta(self) -> bool:
        query = self.txt_query.get().strip()
        try:
            res = self.api.ejecutar_sql_sandbox(query)
            columnas = res.get("columnas", [])
            filas = res.get("filas", [])

            self.tabla.delete(*self.tabla.get_children())
            self.tabla["columns"] = columnas
            for columna in columnas:
                self.tabla.heading(columna, text=columna)
                self.tabla.column(columna, width=130, anchor="center")

            for fila in filas:
                self.tabla.insert("", "end", values=[fila.get(c) for c in columnas])

            if filas:
                self.lbl_resultado.configure(
                    text=f"● {t('sql_resultado', filas=len(filas))}",
                    fg=tema.COLORES["mint"],
                )
            else:
                self.lbl_resultado.configure(
                    text=f"● {t('sql_sin_resultados')}",
                    fg=tema.COLORES["muted"],
                )
            return True
        except ErrorClienteAPI as e:
            self.lbl_resultado.configure(text=f"● {t('sql_error', error=e)}", fg=tema.COLORES["red"])
            messagebox.showerror(t("sql_err_titulo"), str(e))
            return False
        except Exception as e:
            self.lbl_resultado.configure(text=f"● {t('sql_error', error=e)}", fg=tema.COLORES["red"])
            messagebox.showerror(t("sql_err_titulo"), str(e))
            return False
