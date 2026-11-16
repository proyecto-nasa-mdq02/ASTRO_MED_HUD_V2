# 🚀 Justificación Analítica del Diseño Arquitectónico — ASTRO_MED_HUD

> 🌐 **[Read in English](./architectural_design.md)**

## 1. Aislamiento del Núcleo Clínico y Operación "Offline-First" (Arquitectura Hexagonal + API REST)

En misiones de espacio profundo (Luna, Marte y Europa en Júpiter), el peligro de **Distancia desde la Tierra** introduce una latencia de comunicación de entre $22$ y $45\text{ minutos}$ por tramo, imposibilitando la telemedicina en tiempo real y el retorno rápido de muestras biológicas a laboratorios terrestres.

* **Autonomía Local (Local-First LAN):** El sistema opera 100% desconectado de Internet. Las capas de **Dominio**, **Aplicación** y **Persistencia (`astro_med.db`)** residen en el nodo servidor local de la nave o base planetaria y exponen contratos JSON sobre HTTP a través de `src/infraestructura/api/`.
* **Ecosistema Multi-Cliente Sincronizado y Bilingüe (`ES` / `EN`):**
  1. **HUD del Astronauta (`src/presentacion/hud_astronauta/` - Puerto 8080):** Aplicación Web de Página Única (SPA) inspirada en la plataforma *EveryWear* de la NASA. Permite el acceso directo sin contraseña para los 7 tripulantes, exhibe un Gemelo Digital Anatómico en SVG interactivo e integra los protocolos de **Medidas Estándar de Vuelos Espaciales (*Standard Measures*)**.
  2. **Consola de Comando Médico (`src/presentacion/consola_comando/` - Puerto 8000):** Estación pesada de escritorio en Tkinter protegida por clave criptográfica (`admin` / `admin123`), con selector de idioma en vivo (`src/presentacion/i18n.py`), conmutador de escenarios interplanetarios, auditoría SQL en caja de arena (*Sandboxing*) y análisis histórico de series temporales biométricas.
* **Inmutabilidad del Dominio:** Ninguna interfaz gráfica accede al motor `sqlite3` ni calcula diagnósticos por su cuenta. Si en el futuro se incorpora un visor de realidad aumentada en el casco del traje espacial (EVA), los directorios `db/`, `src/dominio/`, `src/aplicacion/` y `src/infraestructura/` permanecen **100% intactos (cero líneas modificadas)**.

---

## 2. Evaluación Dinámica de los 5 Peligros mediante el Patrón Estrategia (`evaluador_riesgo_espacial.py`)

Para erradicar las estructuras condicionales anidadas (`if/else`) al evaluar signos vitales en distintos contextos operativos, se implementó el **Patrón de Comportamiento Estrategia (GoF)** en conjunto con el **Principio de Abierto/Cerrado (OCP - S.O.L.I.D.)**:

* **Polimorfismo Ambiental:** Se define la clase abstracta `EstrategiaEntornoEspacial` con el contrato `evaluar(lectura: LecturaBiometrica) -> DiagnosticoTriage`.
* **Estrategias Concretas por Entorno Operativo:**
  * `EstrategiaTransitoCeroG` (Tránsito Espacial / Estación Espacial): Ajusta los umbrales cardiovasculares por redistribución cefálica de fluidos en microgravedad ($0\text{G}$) y exige una cuota estricta de ejercicio resistivo (ARED / tracción isométrica IMTP) para mitigar la pérdida ósea.
  * `EstrategiaRoverExplorador` (Vehículo Presurizado): Endurece los umbrales neuro-psicológicos (horas de sueño registradas por actigrafía *Actiwatch*, estado de ánimo y batería cognitiva *Pulsar Cognition*) debido al peligro extremo de **Aislamiento y Confinamiento**.
  * `EstrategiaBasePlanetaria` (Superficie Lunar $1/6\text{ G}$, Marciana $3/8\text{ G}$ o Crio-Joviana): Contempla la carga física, térmica, metabólica y las pruebas sensoriomotoras posturales (*Sit-to-Stand* y *Tandem Walk*) tras caminatas espaciales (EVA).

---

## 3. Codificación Cromática y Mapeo Anatómico Automático (KISS y Alta Cohesión)

Cada evaluación del dominio retorna un Objeto de Valor (`DiagnosticoTriage`) que alimenta directamente el vector anatómico SVG del HUD sin requerir lógica médica en el cliente:

* **Semáforo Clínico Determinista:** Clasificación automática en tres niveles: `NOMINAL` (Verde `#4CAF50`), `PRECAUCION` (Ámbar `#FF9800`) y `CRITICO` (Rojo `#F44336`).
* **Mapeo de Subsistemas Corporales y *Standard Measures* (Zonas Clicables del SVG):**
  1. `NEURO_PSICO` (Cabeza, Cognición y Sistema Vestibular): Actigrafía de sueño (*Actiwatch Spectrum Plus*), encuestas *EveryWear*, batería *Pulsar Cognition* ($10\text{ pruebas}$) y escala de cinetosis ($0$ a $20$).
  2. `CARDIO_RAD` (Tórax, Sistema Cardiovascular y Dosimetría): Presión arterial sistólica/diastólica, Presión Arterial Media (MAP), pulso (BPM), grosor carotídeo íntima-media por ultrasonido y dosimetría de radiación ($\text{mSv}$).
  3. `METABOLICO_INMUNE` (Abdomen, Bioquímica e Inmunidad): Nivel de glucosa en sangre ($\text{mg/dL}$), temperatura corporal ($^\circ\text{C}$), vigilancia inmunitaria innata/adaptativa y microbioma.
  4. `MUSCULO_ESQUELETICO` (Extremidades y Control Sensoriomotor): Minutos de ejercicio de contramedida diario (ARED), fuerza isométrica a medio muslo (IMTP) y equilibrio pos-vuelo.

---

## 4. Inversión de Dependencias (DIP) y Unidad de Trabajo Atómica (ACID)

* **Principio de Inversión de Dependencias (DIP - S.O.L.I.D.):** Las capas internas (`src/dominio/` y `src/aplicacion/`) no importan librerías externas (`sqlite3`, `bcrypt`, `fastapi`). Dependen exclusivamente de interfaces abstractas (`ABC`) declaradas en `src/dominio/puertos.py`.
* **Unidad de Trabajo (`gestor_sqlite.py`):** Las transacciones sobre el esquema relacional en Tercera Forma Normal (3FN) se encapsulan mediante un Administrador de Contexto (`__enter__` / `__exit__`). Cuando un astronauta registra un chequeo biométrico y consume un suministro del botiquín de a bordo, el gestor garantiza atomicidad ACID: o se confirma el registro clínico junto con el descuento de stock y el incremento de la racha de autocuidado (`commit`), o se revierte toda la operación (`rollback`) ante cualquier anomalía o disparo de *Triggers*.

---

## 5. Estructura de Carpetas del Proyecto

```text
📂 ASTRO_MED_HUD/
├── 📁 db/                                       # Persistencia física aislada.
│   ├── 📜 esquema.sql                           # DDL relacional 3FN, Vistas, Columna STORED y Triggers.
│   └── 🗄️ astro_med.db                          # Base de datos generada en tiempo de ejecución.
├── 📁 docs/                                     # Documentación técnica bilingüe (EN / ES).
│   ├── 📁 fundamentos/
│   │   ├── 📝 architectural_design.md          # Versión en inglés.
│   │   ├── 📝 diseño_arquitectonico.md         # Versión en español.
│   │   ├── 📝 TDD_construction_plan.md         # Versión en inglés.
│   │   └── 📝 plan_construccion_guiado_TDD.md  # Versión en español.
│   └── 📁 reportes/
│       ├── 📝 stage_1.md / etapa_1.md
│       ├── 📝 stage_2.md / etapa_2.md
│       ├── 📝 stage_3.md / etapa_3.md
│       └── 📝 stage_4.md / etapa_4.md
├── 📁 simulador_misiones/                       # Pipelines ETL de simulación interplanetaria (DRY).
│   ├── 🐍 __init__.py
│   ├── 🐍 nucleo_simulacion.py                  # Inicializa esquema, 7 tripulantes (AST-001 a AST-007) y botiquín.
│   ├── 🐍 generador_mision_artemis.py           # Escenario 1: Órbita y Superficie Lunar (105 lecturas).
│   ├── 🐍 generador_mision_ares_marte.py        # Escenario 2: Superficie y Rover en Marte (105 lecturas).
│   └── 🐍 generador_mision_europa_jupiter.py    # Escenario 3: Luna Helada Europa en Júpiter (105 lecturas).
│
├── 📁 src/                                      # Código fuente de producción.
│   ├── 🐍 __init__.py
│   ├── 📁 dominio/                              # CAPA 1: Núcleo Clínico-Espacial (Cero librerías externas).
│   │   ├── 🐍 __init__.py
│   │   ├── 🐍 entidades.py                      # Tripulante, InsumoMedico, LecturaBiometrica, DiagnosticoTriage.
│   │   ├── 🐍 excepciones.py                    # Errores de negocio y barreras biológicas.
│   │   ├── 🐍 politicas_rbac.py                 # Patrón Estrategia para cadena de mando espacial.
│   │   ├── 🐍 evaluador_riesgo_espacial.py      # Patrón Estrategia: evalúa los 5 peligros según el entorno.
│   │   └── 🐍 puertos.py                        # Contratos abstractos (Interfaces ABC).
│   │
│   ├── 📁 aplicacion/                           # CAPA 2: Casos de Uso (Orquestación pura).
│   │   ├── 🐍 __init__.py
│   │   ├── 🐍 casos_uso_tripulacion.py          # Autenticación, gestión de astronautas y racha de gamificación.
│   │   ├── 🐍 casos_uso_botiquin.py             # Gestión de insumos médicos y protocolos paso a paso.
│   │   └── 🐍 casos_uso_telemetria.py           # Evaluación de salud, consumo atómico de botiquín y analítica BI.
│   │
│   ├── 📁 infraestructura/                      # CAPA 3: Adaptadores Técnicos (SQLite, Bcrypt, FastAPI, Pandas).
│   │   ├── 🐍 __init__.py
│   │   ├── 📁 persistencia/
│   │   │   ├── 🐍 __init__.py
│   │   │   ├── 🐍 gestor_sqlite.py              # Unidad de Trabajo ACID (__enter__ / __exit__).
│   │   │   ├── 🐍 utilidades_sql.py             # Helper obtener_o_crear para catálogos satélites 3FN.
│   │   │   ├── 🐍 repositorio_tripulantes_sql.py# Persistencia de tripulación, roles y especialidades.
│   │   │   ├── 🐍 repositorio_botiquin_sql.py   # Persistencia de suministros, estados y módulos de ubicación.
│   │   │   └── 🐍 repositorio_telemetria_sql.py # Persistencia biométrica y procesamiento vectorial con Pandas.
│   │   ├── 📁 seguridad/
│   │   │   ├── 🐍 __init__.py
│   │   │   └── 🐍 adaptador_bcrypt.py           # Hashing criptográfico de credenciales con salt.
│   │   └── 📁 api/                              # Servidor RESTful (Punto único de contacto LAN).
│   │       ├── 🐍 __init__.py
│   │       ├── 🐍 esquemas_validacion.py        # DTOs Pydantic de validación de entrada.
│   │       ├── 🐍 inyector_dependencias.py      # Fábrica IoC e intercepción de cabecera X-Operador-Id.
│   │       ├── 🐍 rutas_tripulacion.py          # Endpoints de login y gestión de tripulantes.
│   │       ├── 🐍 rutas_telemetria.py           # Endpoints de telemetría, idioma, misiones, crisis y SQL.
│   │       └── 🐍 servidor.py                   # Instancia FastAPI, manejo global de excepciones y CORS.
│   │
│   └── 📁 presentacion/                         # CAPA 4: Adaptadores Primarios de Interfaz de Usuario.
│       ├── 🐍 __init__.py
│       ├── 🐍 i18n.py                           # Motor de internacionalización bilingüe (ES / EN).
│       ├── 📁 consola_comando/                  # Adaptador 1: Estación de Comando Médico en Tkinter.
│       │   ├── 🐍 __init__.py
│       │   ├── 🐍 cliente_api.py                # Cliente HTTP centralizado (requests).
│       │   └── 📁 vistas/
│       │       ├── 🐍 __init__.py
│       │       ├── 🐍 login.py                  # Selector de idioma, login Control de Vuelo y demonios 8000/8080.
│       │       ├── 🐍 panel_control.py          # Monitoreo grupal en vivo y selector de misiones/crisis.
│       │       ├── 🐍 analitica.py              # Gráficos históricos con Matplotlib.
│       │       └── 🐍 consola.py                # Consola de auditoría SQL en modo Sandbox.
│       └── 📁 hud_astronauta/                   # Adaptador 2: Visor Web SPA sin clave (HTML5 + CSS3 + JS + SVG).
│           ├── 🌐 index.html                    # HUD EveryWear con Gemelo Anatómico SVG y Standard Measures.
│           ├── 🎨 estilos.css                   # Tema oscuro aeroespacial (NASA Dark HUD) y semáforo cromático.
│           └── 📜 app_web.js                    # Motor asíncrono fetch, traducción ES/EN, SVG y gráficos <canvas>.
│
├── 📁 tests/                                    # Suite Automatizada TDD (15 pruebas con Pytest).
│   ├── 🐍 __init__.py
│   ├── 🐍 conftest.py                           # Entorno aislado SQLite en memoria RAM (:memory:).
│   ├── 📁 unitarios/
│   │   ├── 🐍 __init__.py
│   │   └── 🐍 test_dominio_astromed.py          # Verifica RBAC, Evaluador de Riesgo Espacial y barreras biológicas.
│   └── 📁 integracion/
│       ├── 🐍 __init__.py
│       ├── 🐍 test_repositorios_sql.py          # Verifica transacciones 3FN, Triggers y Rollback ACID.
│       ├── 🐍 test_api_rest.py                  # Verifica contratos HTTP, simulador solar y Sandboxing SQL.
│       └── 🐍 test_sincronizacion_hud_consola.py# Verifica SVG, CORS móvil LAN y sincronización Web <-> Tkinter.
│
├── 📄 pytest.ini
├── 📄 requirements.txt
├── 📄 README.md                                 # Documentación principal en inglés.
└── 📄 README_ESP.md                             # Documentación principal en español.
```