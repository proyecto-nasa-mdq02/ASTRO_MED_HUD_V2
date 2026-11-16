# 📄 Execution Report - Stage 2: Use Cases, 3NF Persistence & SQL Integration Tests

> 🌐 **[Leer en Español](./etapa_2.md)**

## 📌 Stage Summary
The **Application Layer (Layer 2)** and **Third Normal Form (3NF) Persistence Adapters (Layer 3)** were implemented and verified over in-memory SQLite (`:memory:`), guaranteeing ACID atomicity and database-level *Trigger* protection.

## ⚙️ Developed Components
* **`db/esquema.sql`**: Normalized relational schema with lookup catalogs (`roles`, `entornos_mision`, `modulos_ubicacion`, `estados_insumo`, `especialidades`), computed column `presion_media` (`GENERATED ALWAYS AS ... STORED`), `vista_tripulacion_activa` view, and physical deletion / last Medical Commander survival *Triggers*.
* **`src/infraestructura/persistencia/`**: ACID Unit of Work (`GestorSQLite`), decoupled catalog helper (`obtener_o_crear`), and concrete repositories (`RepositorioTripulantesSQL`, `RepositorioBotiquinSQL`, `RepositorioTelemetriaSQL`).
* **`src/aplicacion/`**: Orchestrating services (`ServicioTripulacion`, `ServicioBotiquin`, `ServicioTelemetria`) unifying biometric evaluation, medical supply stock deduction, and self-care streak gamification into a single atomic transaction.

## 🚀 Console Execution Results
```text
collected 8 items

tests/integracion/test_repositorios_sql.py::test_alta_tripulante_y_proteccion_trigger_ultimo_comandante PASSED [ 12%]
tests/integracion/test_repositorios_sql.py::test_transaccion_atomica_telemetria_descuenta_botiquin_y_suma_racha PASSED [ 25%]
tests/integracion/test_repositorios_sql.py::test_rollback_atomico_si_stock_botiquin_es_insuficiente PASSED [ 37%]
tests/unitarios/test_dominio_astromed.py::test_rbac_especialista_no_puede_dar_baja PASSED    [ 50%]
tests/unitarios/test_dominio_astromed.py::test_rbac_oficial_cientifico_no_modifica_comandante_medico PASSED [ 62%]
tests/unitarios/test_dominio_astromed.py::test_evaluador_detecta_hipoglucemia_critica_y_asigna_sistema PASSED [ 75%]
tests/unitarios/test_dominio_astromed.py::test_mismo_sueno_es_precaucion_en_estacion_pero_critico_en_rover PASSED [ 87%]
tests/unitarios/test_dominio_astromed.py::test_barrera_biologica_rechaza_valores_imposibles PASSED [100%]

======================================== 8 passed in 2.05s ========================================
```