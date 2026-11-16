# =======================================================================
#  NODO DE ARRANQUE Y BOOTSTRAP LAN — CONSOLA DE COMANDO MÉDICO (CAPA 4)
# =======================================================================

import atexit
import functools
import queue
import random
import socket
import threading
import time
import webbrowser
from http.server import HTTPServer, SimpleHTTPRequestHandler
from pathlib import Path
import tkinter as tk
from tkinter import ttk, messagebox
import uvicorn

from simulador_misiones.generador_mision_artemis import inicializar_y_poblar_mision
from src.infraestructura.api.servidor import app
from src.presentacion.i18n import set_idioma, t
from src.presentacion.consola_comando.cliente_api import ClienteAPIAstroMed, ErrorClienteAPI
from src.presentacion.consola_comando import tema
from src.presentacion.consola_comando.vistas.panel_control import VentanaPanelControl

_SERVIDOR_WEB_HTTP = None


def obtener_ip_lan() -> str:
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception:
        return "127.0.0.1"


def iniciar_demonios_red() -> None:
    """Inicializa la base de datos de misión y levanta API REST (8000) + HUD Web (8080)."""
    global _SERVIDOR_WEB_HTTP
    inicializar_y_poblar_mision("db/astro_med.db")

    def correr_api():
        config = uvicorn.Config(app, host="0.0.0.0", port=8000, log_level="warning")
        server = uvicorn.Server(config)
        server.run()

    hilo_api = threading.Thread(target=correr_api, daemon=True)
    hilo_api.start()

    ruta_hud = Path(__file__).resolve().parent.parent.parent / "hud_astronauta"
    manejador = functools.partial(SimpleHTTPRequestHandler, directory=str(ruta_hud))

    try:
        _SERVIDOR_WEB_HTTP = HTTPServer(("0.0.0.0", 8080), manejador)
        hilo_web = threading.Thread(target=_SERVIDOR_WEB_HTTP.serve_forever, daemon=True)
        hilo_web.start()
    except OSError:
        pass

    atexit.register(apagar_demonios)
    time.sleep(0.6)


def apagar_demonios() -> None:
    global _SERVIDOR_WEB_HTTP
    if _SERVIDOR_WEB_HTTP:
        try:
            _SERVIDOR_WEB_HTTP.shutdown()
        except Exception:
            pass


class VentanaLogin:
    """Puesto de acceso del operador de vuelo, con estética Mission Control."""

    def __init__(self, root: tk.Tk, cliente_api: ClienteAPIAstroMed):
        self.root = root
        self.api = cliente_api
        self.ip_lan = obtener_ip_lan()
        self._fondo_size = (0, 0)
        self._cola_estado_api: queue.Queue[bool] = queue.Queue()
        self._intentos_api = 0
        self._verificando_api = False

        self.root.title("ASTRO-MED | NASA HRP Flight Control")
        self.root.configure(bg=tema.COLORES["bg"])
        self.root.minsize(980, 640)
        tema.configurar_estilos(self.root)

        self._construir_fondo()
        self._construir_ui()
        tema.centrar_ventana(self.root, 1120, 710)

        self.root.bind("<Return>", self._atajo_ingresar)
        self.root.after(450, self._verificar_api)

    # ------------------------------------------------------------------
    #  Fondo espacial decorativo
    # ------------------------------------------------------------------
    def _construir_fondo(self) -> None:
        self.canvas_fondo = tk.Canvas(
            self.root,
            bg=tema.COLORES["bg"],
            highlightthickness=0,
            bd=0,
        )
        self.canvas_fondo.place(x=0, y=0, relwidth=1, relheight=1)
        self.canvas_fondo.bind("<Configure>", self._dibujar_fondo)

    @staticmethod
    def _interpolar_color(c1: str, c2: str, factor: float) -> str:
        factor = max(0.0, min(1.0, factor))
        a = tuple(int(c1[i : i + 2], 16) for i in (1, 3, 5))
        b = tuple(int(c2[i : i + 2], 16) for i in (1, 3, 5))
        return "#" + "".join(f"{round(x + (y - x) * factor):02x}" for x, y in zip(a, b))

    def _dibujar_fondo(self, evento=None) -> None:
        ancho = self.canvas_fondo.winfo_width()
        alto = self.canvas_fondo.winfo_height()
        if ancho < 50 or alto < 50:
            return
        if (ancho, alto) == self._fondo_size:
            return
        self._fondo_size = (ancho, alto)

        self.canvas_fondo.delete("fondo")
        for y in range(0, alto, 3):
            color = self._interpolar_color("#05080f", "#0a1d34", y / max(alto, 1))
            self.canvas_fondo.create_rectangle(
                0, y, ancho, y + 3, fill=color, outline=color, tags="fondo"
            )

        rnd = random.Random(11)
        for _ in range(max(70, ancho // 14)):
            x = rnd.randrange(0, ancho)
            y = rnd.randrange(0, alto)
            r = rnd.choice((0, 0, 1))
            color = rnd.choice(("#1e3a5f", "#2f5e86", "#7dd3fc", "#334155"))
            self.canvas_fondo.create_oval(
                x, y, x + r, y + r, fill=color, outline="", tags="fondo"
            )

        cx, cy = ancho * 0.23, alto * 0.52
        for radio, color in ((310, "#0e2a44"), (430, "#0b2035"), (560, "#081726")):
            self.canvas_fondo.create_oval(
                cx - radio,
                cy - radio * 0.62,
                cx + radio,
                cy + radio * 0.62,
                outline=color,
                width=1,
                tags="fondo",
            )
        self.canvas_fondo.create_arc(
            cx - 380,
            cy - 240,
            cx + 380,
            cy + 240,
            start=18,
            extent=116,
            style="arc",
            outline="#0f3b5c",
            width=2,
            tags="fondo",
        )
        self.canvas_fondo.create_oval(
            cx + 236,
            cy - 168,
            cx + 244,
            cy - 160,
            fill="#38bdf8",
            outline="",
            tags="fondo",
        )
        self.canvas_fondo.create_text(
            ancho - 34,
            alto - 24,
            text="ORBITAL FLIGHT CONTROL · 2026",
            fill="#12314a",
            font=("Consolas", 8),
            anchor="e",
            tags="fondo",
        )
        self.canvas_fondo.tag_lower("fondo")

    # ------------------------------------------------------------------
    #  Interfaz principal
    # ------------------------------------------------------------------
    def _construir_ui(self) -> None:
        self.tarjeta = tk.Frame(
            self.canvas_fondo,
            bg=tema.COLORES["panel"],
            highlightthickness=1,
            highlightbackground=tema.COLORES["line"],
            bd=0,
        )
        self.tarjeta.place(
            relx=0.5, rely=0.5, anchor="center", relwidth=0.92, relheight=0.86
        )
        self.tarjeta.grid_columnconfigure(0, weight=1, uniform="login_col")
        self.tarjeta.grid_columnconfigure(1, weight=1, uniform="login_col")
        self.tarjeta.grid_rowconfigure(0, weight=1)

        self._construir_hero()
        self._construir_formulario()

    def _construir_hero(self) -> None:
        hero = tk.Frame(self.tarjeta, bg=tema.COLORES["panel_2"])
        hero.grid(row=0, column=0, sticky="nsew")
        hero.grid_columnconfigure(0, weight=1)

        contenido = tk.Frame(hero, bg=tema.COLORES["panel_2"])
        contenido.pack(fill="both", expand=True, padx=40, pady=38)

        fila_marca = tk.Frame(contenido, bg=tema.COLORES["panel_2"])
        fila_marca.pack(fill="x")
        tk.Label(
            fila_marca,
            text="◈",
            bg=tema.COLORES["panel_2"],
            fg=tema.COLORES["cyan"],
            font=("Segoe UI Symbol", 19, "bold"),
        ).pack(side="left", padx=(0, 10))

        self.lbl_hero_badge = tk.Label(
            fila_marca,
            text=t("login_hero_badge"),
            bg=tema.COLORES["panel_2"],
            fg=tema.COLORES["cyan"],
            font=("Segoe UI", 8, "bold"),
            anchor="w",
            justify="left",
        )
        self.lbl_hero_badge.pack(side="left", fill="x", expand=True)

        tk.Label(
            contenido,
            text="ASTRO-MED",
            bg=tema.COLORES["panel_2"],
            fg=tema.COLORES["text"],
            font=("Segoe UI", 30, "bold"),
            anchor="w",
        ).pack(fill="x", pady=(28, 0))

        linea = tk.Frame(contenido, bg=tema.COLORES["cyan"], height=3, width=58)
        linea.pack(anchor="w", pady=(10, 14))

        self.lbl_hero_titulo = tk.Label(
            contenido,
            text=t("login_hero_titulo"),
            bg=tema.COLORES["panel_2"],
            fg=tema.COLORES["text"],
            font=("Segoe UI", 14, "bold"),
            anchor="w",
            justify="left",
            wraplength=390,
        )
        self.lbl_hero_titulo.pack(fill="x")

        self.lbl_hero_sub = tk.Label(
            contenido,
            text=t("login_hero_sub"),
            bg=tema.COLORES["panel_2"],
            fg=tema.COLORES["muted"],
            font=("Segoe UI", 10),
            anchor="w",
            justify="left",
            wraplength=390,
        )
        self.lbl_hero_sub.pack(fill="x", pady=(10, 24))

        stats = tk.Frame(contenido, bg=tema.COLORES["panel_2"])
        stats.pack(fill="x")

        self._stat_1 = self._crear_stat(stats, "04", t("login_hero_stat1"))
        self._stat_2 = self._crear_stat(stats, "08", t("login_hero_stat2"))
        self._stat_3 = self._crear_stat(stats, "03", t("login_hero_stat3"))

        caracteristicas = tk.Frame(contenido, bg=tema.COLORES["panel_2"])
        caracteristicas.pack(fill="x", pady=(30, 0))
        for texto in (
            "Gemelo digital anatómico con estado por sistema",
            "Triage autónomo NASA HRP · 4 peligros espaciales",
            "Telemetría EveryWear · Medidas estándar",
        ):
            fila = tk.Frame(caracteristicas, bg=tema.COLORES["panel_2"])
            fila.pack(fill="x", pady=3)
            tk.Label(
                fila,
                text="▸",
                bg=tema.COLORES["panel_2"],
                fg=tema.COLORES["mint"],
                font=("Segoe UI", 9, "bold"),
            ).pack(side="left", padx=(0, 9))
            tk.Label(
                fila,
                text=texto,
                bg=tema.COLORES["panel_2"],
                fg=tema.COLORES["muted"],
                font=("Segoe UI", 9),
                anchor="w",
            ).pack(side="left", fill="x", expand=True)

        pie = tk.Frame(contenido, bg=tema.COLORES["panel_2"])
        pie.pack(side="bottom", fill="x", pady=(28, 0))
        self.lbl_hero_pie = tk.Label(
            pie,
            text=t("login_hero_pie"),
            bg=tema.COLORES["panel_2"],
            fg=tema.COLORES["muted_2"],
            font=("Segoe UI", 8, "bold"),
            anchor="w",
        )
        self.lbl_hero_pie.pack(side="left")
        self.lbl_api = tk.Label(
            pie,
            text="● API 8000",
            bg=tema.COLORES["panel_2"],
            fg=tema.COLORES["muted_2"],
            font=("Segoe UI", 8, "bold"),
            anchor="e",
        )
        self.lbl_api.pack(side="right")

    def _crear_stat(self, padre: tk.Misc, valor: str, etiqueta: str) -> tk.Frame:
        tarjeta = tk.Frame(
            padre,
            bg=tema.COLORES["panel"],
            highlightthickness=1,
            highlightbackground=tema.COLORES["line"],
            bd=0,
        )
        tarjeta.pack(side="left", fill="x", expand=True, padx=(0, 8))
        tk.Label(
            tarjeta,
            text=valor,
            bg=tema.COLORES["panel"],
            fg=tema.COLORES["cyan"],
            font=("Consolas", 18, "bold"),
            anchor="w",
        ).pack(fill="x", padx=12, pady=(10, 0))
        lbl = tk.Label(
            tarjeta,
            text=etiqueta,
            bg=tema.COLORES["panel"],
            fg=tema.COLORES["muted"],
            font=("Segoe UI", 8),
            anchor="w",
            justify="left",
            wraplength=105,
        )
        lbl.pack(fill="x", padx=12, pady=(0, 10))
        tarjeta.etiqueta = lbl  # type: ignore[attr-defined]
        return tarjeta

    def _construir_formulario(self) -> None:
        panel = tk.Frame(self.tarjeta, bg=tema.COLORES["panel"])
        panel.grid(row=0, column=1, sticky="nsew")
        panel.grid_columnconfigure(0, weight=1)
        panel.grid_rowconfigure(0, weight=1)

        contenido = tk.Frame(panel, bg=tema.COLORES["panel"])
        contenido.pack(fill="both", expand=True, padx=38, pady=32)

        fila_idioma = tk.Frame(contenido, bg=tema.COLORES["panel"])
        fila_idioma.pack(fill="x", pady=(0, 24))

        self.lbl_idioma = tk.Label(
            fila_idioma,
            text=t("login_idioma"),
            fg=tema.COLORES["muted"],
            bg=tema.COLORES["panel"],
            font=("Segoe UI", 8, "bold"),
        )
        self.lbl_idioma.pack(side="left")

        self.combo_idioma = ttk.Combobox(
            fila_idioma,
            values=["Español (ES)", "English (EN)"],
            state="readonly",
            width=15,
        )
        self.combo_idioma.current(0)
        self.combo_idioma.pack(side="right")
        self.combo_idioma.bind("<<ComboboxSelected>>", self.cambiar_idioma_ui)

        self.lbl_panel_eyebrow = tk.Label(
            contenido,
            text=t("login_panel_eyebrow"),
            bg=tema.COLORES["panel"],
            fg=tema.COLORES["cyan"],
            font=("Segoe UI", 8, "bold"),
            anchor="w",
        )
        self.lbl_panel_eyebrow.pack(fill="x")

        self.lbl_titulo = tk.Label(
            contenido,
            text=t("login_panel_titulo"),
            fg=tema.COLORES["text"],
            bg=tema.COLORES["panel"],
            font=("Segoe UI", 19, "bold"),
            anchor="w",
        )
        self.lbl_titulo.pack(fill="x", pady=(4, 4))

        self.lbl_sub = tk.Label(
            contenido,
            text=t("login_sub"),
            fg=tema.COLORES["muted"],
            bg=tema.COLORES["panel"],
            font=("Segoe UI", 9),
            anchor="w",
        )
        self.lbl_sub.pack(fill="x", pady=(0, 12))

        self.lbl_lan = tk.Label(
            contenido,
            text=f"{t('login_lan')} http://{self.ip_lan}:8080",
            fg=tema.COLORES["mint"],
            bg=tema.COLORES["panel_2"],
            font=("Consolas", 8, "bold"),
            anchor="w",
            padx=10,
            pady=7,
        )
        self.lbl_lan.pack(fill="x", pady=(0, 20))

        self.lbl_usr = tk.Label(
            contenido,
            text=t("login_usuario"),
            fg=tema.COLORES["muted"],
            bg=tema.COLORES["panel"],
            font=("Segoe UI", 9),
            anchor="w",
        )
        self.lbl_usr.pack(fill="x")
        self.ent_usuario = self._crear_entry(contenido)
        self.ent_usuario.insert(0, "admin")
        self.ent_usuario.pack(fill="x", pady=(5, 14), ipady=7)

        self.lbl_pwd = tk.Label(
            contenido,
            text=t("login_clave"),
            fg=tema.COLORES["muted"],
            bg=tema.COLORES["panel"],
            font=("Segoe UI", 9),
            anchor="w",
        )
        self.lbl_pwd.pack(fill="x")
        self.ent_password = self._crear_entry(contenido, show="*")
        self.ent_password.insert(0, "admin123")
        self.ent_password.pack(fill="x", pady=(5, 18), ipady=7)

        self.btn_ingresar = tema.crear_boton(
            contenido,
            t("login_btn_iniciar"),
            self.autenticar,
            tipo="primary",
            font=("Segoe UI", 10, "bold"),
            pady=11,
        )
        self.btn_ingresar.pack(fill="x", pady=(0, 8))

        self.btn_hud = tema.crear_boton(
            contenido,
            t("login_btn_hud"),
            lambda: webbrowser.open("http://127.0.0.1:8080"),
            tipo="ghost",
            bg=tema.COLORES["panel_2"],
            fg=tema.COLORES["cyan"],
            activeforeground=tema.COLORES["cyan"],
            pady=9,
        )
        self.btn_hud.pack(fill="x")

        self.lbl_error = tk.Label(
            contenido,
            text="",
            fg=tema.COLORES["red"],
            bg=tema.COLORES["panel"],
            font=("Segoe UI", 8),
            anchor="w",
            justify="left",
            wraplength=410,
        )
        self.lbl_error.pack(fill="x", pady=(10, 0))

        self.lbl_seguridad = tk.Label(
            contenido,
            text=f"◈  {t('login_seguridad')}",
            fg=tema.COLORES["muted_2"],
            bg=tema.COLORES["panel"],
            font=("Segoe UI", 8),
            anchor="w",
        )
        self.lbl_seguridad.pack(side="bottom", fill="x", pady=(18, 0))

    def _crear_entry(self, padre: tk.Misc, show: str = "") -> tk.Entry:
        return tk.Entry(
            padre,
            font=("Segoe UI", 11),
            bg=tema.COLORES["bg_alt"],
            fg=tema.COLORES["text"],
            insertbackground=tema.COLORES["cyan"],
            show=show,
            relief="flat",
            bd=0,
            highlightthickness=1,
            highlightbackground=tema.COLORES["line"],
            highlightcolor=tema.COLORES["cyan"],
        )

    # ------------------------------------------------------------------
    #  Comportamiento
    # ------------------------------------------------------------------
    def _atajo_ingresar(self, _evento=None):
        self.autenticar()
        return "break"

    def _verificar_api(self) -> None:
        if self._verificando_api:
            return

        def tarea():
            try:
                self.api.listar_tripulantes()
                ok = True
            except Exception:
                ok = False
            self._cola_estado_api.put(ok)

        self._verificando_api = True
        self._intentos_api += 1
        threading.Thread(target=tarea, daemon=True).start()
        try:
            self.root.after(150, self._revisar_estado_api)
        except tk.TclError:
            pass

    def _revisar_estado_api(self) -> None:
        """Consume desde el hilo de Tk el resultado de la comprobación de red."""
        try:
            ok = self._cola_estado_api.get_nowait()
        except queue.Empty:
            try:
                self.root.after(150, self._revisar_estado_api)
            except tk.TclError:
                pass
            return
        self._verificando_api = False
        self._pintar_estado_api(ok)
        # Uvicorn puede tardar en arrancar: reintentamos con calma mientras
        # la ventana siga abierta, sin bloquear el hilo de Tk.
        if not ok and self._intentos_api < 40:
            try:
                self.root.after(1200, self._verificar_api)
            except tk.TclError:
                pass

    def _pintar_estado_api(self, ok: bool) -> None:
        try:
            self.lbl_api.configure(
                text=("● " + t("login_api_ok")) if ok else ("● " + t("login_api_error")),
                fg=tema.COLORES["mint"] if ok else tema.COLORES["red"],
            )
        except tk.TclError:
            pass

    def cambiar_idioma_ui(self, _evento=None) -> None:
        seleccion = self.combo_idioma.get()
        cod = "en" if "EN" in seleccion else "es"
        set_idioma(cod)
        try:
            self.api.cambiar_idioma(cod)
        except Exception:
            # La preferencia local ya quedó aplicada aunque la API no responda.
            pass

        self.lbl_idioma.configure(text=t("login_idioma"))
        self.lbl_sub.configure(text=t("login_sub"))
        self.lbl_titulo.configure(text=t("login_panel_titulo"))
        self.lbl_panel_eyebrow.configure(text=t("login_panel_eyebrow"))
        self.lbl_lan.configure(text=f"{t('login_lan')} http://{self.ip_lan}:8080")
        self.lbl_usr.configure(text=t("login_usuario"))
        self.lbl_pwd.configure(text=t("login_clave"))
        self.btn_ingresar.configure(text=t("login_btn_iniciar"))
        self.btn_hud.configure(text=t("login_btn_hud"))
        self.lbl_hero_badge.configure(text=t("login_hero_badge"))
        self.lbl_hero_titulo.configure(text=t("login_hero_titulo"))
        self.lbl_hero_sub.configure(text=t("login_hero_sub"))
        self.lbl_hero_pie.configure(text=t("login_hero_pie"))
        self.lbl_seguridad.configure(text=f"◈  {t('login_seguridad')}")
        self._stat_1.etiqueta.configure(text=t("login_hero_stat1"))  # type: ignore[attr-defined]
        self._stat_2.etiqueta.configure(text=t("login_hero_stat2"))  # type: ignore[attr-defined]
        self._stat_3.etiqueta.configure(text=t("login_hero_stat3"))  # type: ignore[attr-defined]

    def autenticar(self) -> bool:
        usuario = self.ent_usuario.get().strip()
        password = self.ent_password.get().strip()
        self.lbl_error.configure(text="")
        self.btn_ingresar.configure(state="disabled")

        try:
            datos = self.api.login(usuario, password)
            messagebox.showinfo(
                t("login_ok_titulo"),
                t("login_ok_msg", nombre=f"{datos['nombres']} {datos['apellidos']}", rol=datos["rol"]),
            )
            self.abrir_panel_control()
            return True
        except ErrorClienteAPI as e:
            self.lbl_error.configure(text=str(e))
            messagebox.showerror(t("login_err_titulo"), str(e))
            return False
        except Exception:
            mensaje = t("login_err_red")
            self.lbl_error.configure(text=mensaje)
            messagebox.showerror(t("login_err_titulo"), mensaje)
            # Reintentamos la comprobación de enlace por si el servidor tardó en arrancar.
            self._intentos_api = 0
            self._verificar_api()
            return False
        finally:
            try:
                self.btn_ingresar.configure(state="normal")
            except tk.TclError:
                pass

    def abrir_panel_control(self) -> None:
        top = tk.Toplevel(self.root)
        self.root.withdraw()
        VentanaPanelControl(top, self.api, al_cerrar=self.root.deiconify)


if __name__ == "__main__":
    iniciar_demonios_red()
    raiz = tk.Tk()
    cliente = ClienteAPIAstroMed("http://127.0.0.1:8000/api")
    app_login = VentanaLogin(raiz, cliente)
    raiz.mainloop()
