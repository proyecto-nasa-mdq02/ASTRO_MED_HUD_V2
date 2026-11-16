# 🚀 Analytical Justification of Architectural Design — ASTRO_MED_HUD

> 🌐 **[Leer en Español](./diseño_arquitectonico.md)**

## 1. Clinical Core Isolation & "Offline-First" Operation (Hexagonal Architecture + REST API)

In deep-space missions (Moon, Mars, and Jupiter's icy moon Europa), the **Distance from Earth** hazard introduces a one-way communication latency between $22$ and $45\text{ minutes}$, making real-time telemedicine and rapid sample return to terrestrial laboratories impossible.

* **Local Autonomy (Local-First LAN):** The system operates 100% disconnected from the Internet. The **Domain**, **Application**, and **Persistence (`astro_med.db`)** layers reside on the spacecraft or planetary habitat local server node, exposing JSON contracts over HTTP via `src/infraestructura/api/`.
* **Synchronized & Bilingual Multi-Client Ecosystem (`EN` / `ES`):**
  1. **Astronaut HUD (`src/presentacion/hud_astronauta/` - Port 8080):** Single-Page Web Application (SPA) modeled after NASA's *EveryWear* iPad system. Provides passwordless direct access for all 7 crew members, features an interactive SVG Anatomical Digital Twin, and integrates **NASA Spaceflight Standard Measures**.
  2. **Flight Control Medical Console (`src/presentacion/consola_comando/` - Port 8000):** Desktop Tkinter command station protected by cryptographic credentials (`admin` / `admin123`), featuring a live language selector (`src/presentacion/i18n.py`), interplanetary mission switcher, read-only SQL *Sandboxing*, and historical biometric time-series analytics.
* **Domain Immutability:** Neither graphical interface accesses `sqlite3` directly nor computes diagnoses on its own. If an Augmented Reality visor inside an EVA helmet is added in the future, `db/`, `src/dominio/`, `src/aplicacion/`, and `src/infraestructura/` remain **100% untouched (zero lines modified)**.

---

## 2. Dynamic Evaluation of NASA's 5 Hazards via the Strategy Pattern (`evaluador_riesgo_espacial.py`)

To eliminate nested conditional structures (`if/else`) when evaluating vital signs across different operational contexts, we implemented the **Behavioral Strategy Pattern (GoF)** alongside the **Open/Closed Principle (OCP - S.O.L.I.D.)**:

* **Environmental Polymorphism:** The abstract base class `EstrategiaEntornoEspacial` defines the contract `evaluar(lectura: LecturaBiometrica) -> DiagnosticoTriage`.
* **Concrete Strategies by Operational Environment:**
  * `EstrategiaTransitoCeroG` (Deep-Space Transit / Space Station): Adjusts cardiovascular thresholds for cephalad fluid shifts in microgravity ($0\text{G}$) and enforces strict resistive exercise countermeasures (ARED / IMTP isometric pull) to mitigate bone loss.
  * `EstrategiaRoverExplorador` (Pressurized Rover): Tightens neuro-psychological thresholds (sleep hours logged via *Actiwatch* actigraphy, mood scale, and *Pulsar Cognition* battery) due to extreme **Isolation and Confinement**.
  * `EstrategiaBasePlanetaria` (Lunar $1/6\text{ G}$, Martian $3/8\text{ G}$, or Cryo-Jovian Surface): Accounts for physical, thermal, and metabolic loads as well as post-EVA sensorimotor balance tests (*Sit-to-Stand* and *Tandem Walk*).

---

## 3. Color-Coded Triage & Automatic Anatomical Mapping (KISS & High Cohesion)

Every domain evaluation returns an immutable Value Object (`DiagnosticoTriage`) that directly drives the interactive SVG human body model without requiring medical logic in the frontend:

* **Deterministic Clinical Traffic Light:** Automatic classification into three levels: `NOMINAL` (Green `#4CAF50`), `PRECAUCION` (Amber `#FF9800`), and `CRITICO` (Red `#F44336`).
* **Body Subsystem & *Standard Measures* Mapping (Clickable SVG Regions):**
  1. `NEURO_PSICO` (Head, Cognition & Vestibular System): Sleep actigraphy (*Actiwatch Spectrum Plus*), *EveryWear* behavioral surveys, *Pulsar Cognition* battery ($10\text{ tests}$), and motion sickness scale ($0\text{--}20$).
  2. `CARDIO_RAD` (Thorax, Cardiovascular System & Dosimetry): Systolic/diastolic blood pressure, Mean Arterial Pressure (MAP), heart rate (BPM), carotid intima-media ultrasound thickness, and radiation dosimetry ($\text{mSv}$).
  3. `METABOLICO_INMUNE` (Abdomen, Biochemistry & Immunity): Blood glucose ($\text{mg/dL}$), body temperature ($^\circ\text{C}$), innate/adaptive immune response, and microbiome tracking.
  4. `MUSCULO_ESQUELETICO` (Extremities & Sensorimotor Control): Daily resistive exercise minutes (ARED), Isometric Mid-Thigh Pull (IMTP) strength, and post-landing postural stability.

---

## 4. Dependency Inversion (DIP) & Atomic Unit of Work (ACID)

* **Dependency Inversion Principle (DIP - S.O.L.I.D.):** Inner layers (`src/dominio/` and `src/aplicacion/`) import zero external libraries (`sqlite3`, `bcrypt`, `fastapi`). They depend exclusively on abstract interfaces (`ABC`) declared in `src/dominio/puertos.py`.
* **Unit of Work (`gestor_sqlite.py`):** Transactions over the Third Normal Form (3NF) relational schema are encapsulated via a Context Manager (`__enter__` / `__exit__`). When an astronaut logs a biometric check and consumes an on-board medical supply, the manager guarantees ACID atomicity: either the clinical record, inventory deduction, and self-care streak increment are committed together (`commit`), or the entire operation is reverted (`rollback`) upon any anomaly or database *Trigger* violation.

---

## 5. Project Directory Structure

```text
📂 ASTRO_MED_HUD/
├── 📁 db/                                       # Isolated physical persistence.
│   ├── 📜 esquema.sql                           # 3NF relational DDL, Views, STORED Column, and Triggers.
│   └── 🗄️ astro_med.db                          # Database automatically generated at runtime.
├── 📁 docs/                                     # Bilingual engineering documentation (EN / ES).
│   ├── 📁 fundamentos/
│   │   ├── 📝 architectural_design.md           # English version.
│   │   ├── 📝 diseño_arquitectonico.md          # Spanish version.
│   │   ├── 📝 TDD_construction_plan.md          # English version.
│   │   └── 📝 plan_construccion_guiado_TDD.md   # Spanish version.
│   └── 📁 reportes/
│       ├── 📝 stage_1.md / etapa_1.md
│       ├── 📝 stage_2.md / etapa_2.md
│       ├── 📝 stage_3.md / etapa_3.md
│       └── 📝 stage_4.md / etapa_4.md
├── 📁 simulador_misiones/                       # Interplanetary ETL simulation pipelines (DRY).
│   ├── 🐍 __init__.py
│   ├── 🐍 nucleo_simulacion.py                  # Initializes schema, 7 crew members (AST-001 to AST-007) & medical kit.
│   ├── 🐍 generador_mision_artemis.py           # Scenario 1: Lunar Orbit & Surface (105 readings).
│   ├── 🐍 generador_mision_ares_marte.py        # Scenario 2: Martian Surface & Rover (105 readings).
│   └── 🐍 generador_mision_europa_jupiter.py    # Scenario 3: Jupiter's Icy Moon Europa (105 readings).
│
├── 📁 src/                                      # Production source code.
│   ├── 🐍 __init__.py
│   ├── 📁 dominio/                              # LAYER 1: Clinical-Space Core (Zero external libraries).
│   │   ├── 🐍 __init__.py
│   │   ├── 🐍 entidades.py                      # Tripulante, InsumoMedico, LecturaBiometrica, DiagnosticoTriage.
│   │   ├── 🐍 excepciones.py                    # Business exceptions and biological barriers.
│   │   ├── 🐍 politicas_rbac.py                 # Strategy Pattern for space chain-of-command RBAC.
│   │   ├── 🐍 evaluador_riesgo_espacial.py      # Strategy Pattern: evaluates the 5 hazards by environment.
│   │   └── 🐍 puertos.py                        # Abstract contracts (ABC Interfaces).
│   │
│   ├── 📁 aplicacion/                           # LAYER 2: Use Cases (Pure orchestration).
│   │   ├── 🐍 __init__.py
│   │   ├── 🐍 casos_uso_tripulacion.py          # Authentication, astronaut profile management & gamification streak.
│   │   ├── 🐍 casos_uso_botiquin.py             # Medical supply management & step-by-step protocols.
│   │   └── 🐍 casos_uso_telemetria.py           # Health evaluation, atomic supply consumption & BI analytics.
│   │
│   ├── 📁 infraestructura/                      # LAYER 3: Technical Adapters (SQLite, Bcrypt, FastAPI, Pandas).
│   │   ├── 🐍 __init__.py
│   │   ├── 📁 persistencia/
│   │   │   ├── 🐍 __init__.py
│   │   │   ├── 🐍 gestor_sqlite.py              # ACID Unit of Work (__enter__ / __exit__).
│   │   │   ├── 🐍 utilidades_sql.py             # obtener_o_crear helper for 3NF lookup tables.
│   │   │   ├── 🐍 repositorio_tripulantes_sql.py# Crew, role, and specialty persistence.
│   │   │   ├── 🐍 repositorio_botiquin_sql.py   # Medical supply, status, and module location persistence.
│   │   │   └── 🐍 repositorio_telemetria_sql.py # Biometric persistence and Pandas vector processing.
│   │   ├── 📁 seguridad/
│   │   │   ├── 🐍 __init__.py
│   │   │   └── 🐍 adaptador_bcrypt.py           # Salted cryptographic password hashing.
│   │   └── 📁 api/                              # RESTful Server (Single LAN contact point).
│   │       ├── 🐍 __init__.py
│   │       ├── 🐍 esquemas_validacion.py        # Pydantic input validation DTOs.
│   │       ├── 🐍 inyector_dependencias.py      # IoC Factory & X-Operador-Id header interception.
│   │       ├── 🐍 rutas_tripulacion.py          # Login and crew management endpoints.
│   │       ├── 🐍 rutas_telemetria.py           # Telemetry, language, mission switch, crisis & SQL endpoints.
│   │       └── 🐍 servidor.py                   # FastAPI instance, global exception handlers & CORS.
│   │
│   └── 📁 presentacion/                         # LAYER 4: Primary User Interface Adapters.
│       ├── 🐍 __init__.py
│       ├── 🐍 i18n.py                           # Bilingual internationalization engine (ES / EN).
│       ├── 📁 consola_comando/                  # Adapter 1: Tkinter Medical Command Station.
│       │   ├── 🐍 __init__.py
│       │   ├── 🐍 cliente_api.py                # Centralized HTTP client (requests).
│       │   └── 📁 vistas/
│       │       ├── 🐍 __init__.py
│       │       ├── 🐍 login.py                  # Language selector, Flight Control login & 8000/8080 daemons.
│       │       ├── 🐍 panel_control.py          # Live group monitoring & mission/crisis selector.
│       │       ├── 🐍 analitica.py              # Historical charts with Matplotlib.
│       │       └── 🐍 consola.py                # Read-only Sandbox SQL audit console.
│       └── 📁 hud_astronauta/                   # Adapter 2: Passwordless Web SPA (HTML5 + CSS3 + JS + SVG).
│           ├── 🌐 index.html                    # EveryWear HUD with clickable SVG Twin & Standard Measures.
│           ├── 🎨 estilos.css                   # Aerospace dark theme (NASA Dark HUD) & traffic-light palette.
│           └── 📜 app_web.js                    # Async fetch engine, ES/EN translation, SVG & <canvas> charts.
│
├── 📁 tests/                                    # Automated TDD Suite (15 Pytest tests).
│   ├── 🐍 __init__.py
│   ├── 🐍 conftest.py                           # Isolated in-memory SQLite fixture (:memory:).
│   ├── 📁 unitarios/
│   │   ├── 🐍 __init__.py
│   │   └── 🐍 test_dominio_astromed.py          # Verifies RBAC, Space Risk Evaluator & biological barriers.
│   └── 📁 integracion/
│       ├── 🐍 __init__.py
│       ├── 🐍 test_repositorios_sql.py          # Verifies 3NF transactions, Triggers & ACID Rollback.
│       ├── 🐍 test_api_rest.py                  # Verifies HTTP contracts, solar simulator & SQL Sandboxing.
│       └── 🐍 test_sincronizacion_hud_consola.py# Verifies SVG, mobile LAN CORS & Web <-> Tkinter sync.
│
├── 📄 pytest.ini
├── 📄 requirements.txt
├── 📄 README.md                                 # Primary documentation in English.
└── 📄 README_ESP.md                             # Primary documentation in Spanish.
```