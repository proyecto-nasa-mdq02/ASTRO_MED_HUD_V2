# 🧪 Test-Driven Development (TDD) Construction Plan — ASTRO_MED_HUD

> 🌐 **[Leer en Español](./plan_construccion_guiado_TDD.md)**

**ASTRO_MED_HUD** is built *Inside-Out*, designing and verifying the clinical rules for NASA's 5 spaceflight hazards, Spaceflight Standard Measures, and transactional integrity before coupling graphical user interface adapters.

---

## Stage 1: Clinical-Space Domain Core & Unit Tests (TDD Cycle 1)

* **Objective:** Model biometric entities, physiological barriers, mission chain-of-command (RBAC), and the polymorphic space risk evaluation engine with zero external dependencies.
* **Built Files:**
  * `requirements.txt` and `pytest.ini`
  * `src/dominio/excepciones.py`
  * `src/dominio/entidades.py`
  * `src/dominio/politicas_rbac.py`
  * `src/dominio/evaluador_riesgo_espacial.py`
  * `src/dominio/puertos.py`
  * `tests/unitarios/test_dominio_astromed.py`
* **TDD Acceptance Criteria:** In-memory execution in $< 1\text{ s}$ verifying that a Mission Specialist cannot deactivate crew members, biological barriers reject impossible vital signs (e.g., diastolic pressure higher than systolic), and identical sleep deprivation triggers `PRECAUCION` on the Space Station but escalates to `CRITICO` inside a confined Explorer Rover.

---

## Stage 2: Use Cases, 3NF SQLite Persistence & Integration Tests (TDD Cycle 2)

* **Objective:** Implement application orchestration, Bcrypt password hashing, and Third Normal Form (3NF) relational repositories over an isolated in-memory database (`:memory:`), validating the computed column (`presion_media`) and survival *Triggers*.
* **Built Files:**
  * `db/esquema.sql`
  * `src/infraestructura/seguridad/adaptador_bcrypt.py`
  * `src/infraestructura/persistencia/utilidades_sql.py`
  * `src/infraestructura/persistencia/repositorio_tripulantes_sql.py`
  * `src/infraestructura/persistencia/repositorio_botiquin_sql.py`
  * `src/infraestructura/persistencia/repositorio_telemetria_sql.py`
  * `src/infraestructura/persistencia/gestor_sqlite.py`
  * `src/aplicacion/casos_uso_tripulacion.py`
  * `src/aplicacion/casos_uso_botiquin.py`
  * `src/aplicacion/casos_uso_telemetria.py`
  * `tests/conftest.py` and `tests/integracion/test_repositorios_sql.py`
* **TDD Acceptance Criteria:** Verification that `trg_proteger_ultimo_comandante_medico` blocks deactivating the last active Medical Commander, atomic medical kit stock deduction and self-care streak increment upon logging a reading, and full transaction `rollback` when medical supplies are insufficient.

---

## Stage 3: RESTful API Adapter (FastAPI), Multi-Mission Simulator & HTTP Tests (TDD Cycle 3)

* **Objective:** Expose use cases via Pydantic-validated RESTful endpoints, incorporate live space anomaly simulation and language synchronization (`/api/idioma`), enforce read-only SQL Sandboxing, and seed the interplanetary scenarios (Moon, Mars, and Europa) with all 7 squadron astronauts and 105 historical records.
* **Built Files:**
  * `src/infraestructura/api/esquemas_validacion.py`
  * `src/infraestructura/api/inyector_dependencias.py`
  * `src/infraestructura/api/rutas_tripulacion.py`
  * `src/infraestructura/api/rutas_telemetria.py`
  * `src/infraestructura/api/servidor.py`
  * `simulador_misiones/nucleo_simulacion.py`
  * `simulador_misiones/generador_mision_artemis.py`
  * `simulador_misiones/generador_mision_ares_marte.py`
  * `simulador_misiones/generador_mision_europa_jupiter.py`
  * `tests/integracion/test_api_rest.py`
* **TDD Acceptance Criteria:** Automated auditing via `TestClient` validating authentication (`200`/`401`), hierarchical RBAC blocking (`403`), solar storm crisis injection (`201` + Pandas time-series), and rejection of destructive statements (`DELETE`/`DROP`) in the SQL console.

---

## Stage 4: Bilingual Presentation Adapters (`hud_astronauta` + `consola_comando`) & LAN Sync (TDD Cycle 4)

* **Objective:** Build the passwordless interactive Web HUD (modeled after *NASA EveryWear*) featuring the clickable SVG human body and *NASA Standard Measures*, alongside the password-protected Tkinter Flight Control Medical Console and bilingual engine (`ES`/`EN`), ensuring real-time bidirectional synchronization across the local area network.
* **Built Files:**
  * `src/presentacion/i18n.py`
  * `src/presentacion/hud_astronauta/index.html`, `estilos.css`, `app_web.js`
  * `src/presentacion/consola_comando/cliente_api.py`
  * `src/presentacion/consola_comando/vistas/login.py`, `panel_control.py`, `analitica.py`, `consola.py`
  * `tests/integracion/test_sincronizacion_hud_consola.py`
* **TDD Acceptance Criteria:** Structural verification of the anatomical SVG and traffic-light CSS variables, validation of mobile LAN *CORS Preflight* (`OPTIONS`) requests, and E2E proof that a critical reading submitted from the Web HUD appears instantaneously in the Tkinter Command Console `Treeview` grid.