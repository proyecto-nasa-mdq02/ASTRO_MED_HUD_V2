# 📄 Execution Report - Stage 3: RESTful API Adapter, Multi-Mission Simulator & HTTP Tests

> 🌐 **[Leer en Español](./etapa_3.md)**

## 📌 Stage Summary
The clinical-space core was exposed through a **FastAPI RESTful Server**, integrating Pydantic schema validation, automatic domain-exception-to-HTTP translation, language synchronization (`/api/idioma`), live space hazard simulation with *Standard Measures* traceability, and the interplanetary simulation engine for the Moon, Mars, and Europa (Jupiter).

## ⚙️ Developed Components
* **`src/infraestructura/api/`**: DTO contracts (`esquemas_validacion.py`), IoC container (`inyector_dependencias.py`), controllers (`rutas_tripulacion.py`, `rutas_telemetria.py`), and central ASGI server with CORS and global error handlers (`servidor.py`).
* **`simulador_misiones/` (`nucleo_simulacion.py`, `generador_mision_artemis.py`, `generador_mision_ares_marte.py`, `generador_mision_europa_jupiter.py`)**: DRY ETL pipelines initializing `db/astro_med.db` with all 7 squadron members (`AST-001` Alicia López to `AST-007` Iván Jauregui), step-by-step medical supplies, and 105 historical readings ($15\text{ Sol days}$ per astronaut) tailored to each celestial body's hostility.
* **`tests/integracion/test_api_rest.py`**: HTTP contract tests using `TestClient` and `dependency_overrides`.

## 🚀 Console Execution Results
```text
collected 12 items

tests/integracion/test_api_rest.py::test_api_login_exitoso_y_credenciales_invalidas PASSED   [  8%]
tests/integracion/test_api_rest.py::test_api_bloqueo_rbac_especialista_intentando_crear_tripulante PASSED [ 16%]
tests/integracion/test_api_rest.py::test_api_registro_telemetria_y_simulador_crisis_solar PASSED [ 25%]
tests/integracion/test_api_rest.py::test_api_consola_sql_bloquea_borrado_y_permite_select PASSED [ 33%]
tests/integracion/test_repositorios_sql.py::test_alta_tripulante_y_proteccion_trigger_ultimo_comandante PASSED [ 41%]
tests/integracion/test_repositorios_sql.py::test_transaccion_atomica_telemetria_descuenta_botiquin_y_suma_racha PASSED [ 50%]
tests/integracion/test_repositorios_sql.py::test_rollback_atomico_si_stock_botiquin_es_insuficiente PASSED [ 58%]
tests/unitarios/test_dominio_astromed.py::test_rbac_especialista_no_puede_dar_baja PASSED    [ 66%]
tests/unitarios/test_dominio_astromed.py::test_rbac_oficial_cientifico_no_modifica_comandante_medico PASSED [ 75%]
tests/unitarios/test_dominio_astromed.py::test_evaluador_detecta_hipoglucemia_critica_y_asigna_sistema PASSED [ 83%]
tests/unitarios/test_dominio_astromed.py::test_mismo_sueno_es_precaucion_en_estacion_pero_critico_en_rover PASSED [ 91%]
tests/unitarios/test_dominio_astromed.py::test_barrera_biologica_rechaza_valores_imposibles PASSED [100%]

================================== 12 passed, 1 warning in 8.06s ==================================
```