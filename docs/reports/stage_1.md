# 📄 Execution Report - Stage 1: Clinical-Space Domain Core & Unit Tests

> 🌐 **[Leer en Español](./etapa_1.md)**

## 📌 Stage Summary
The **Domain Layer (Layer 1)** was built and validated under Hexagonal Architecture and S.O.L.I.D. principles. The core models biometric entities and evaluates the impact of **NASA's 5 Hazards of Human Spaceflight** 100% isolated in RAM, with zero database or web framework dependencies.

## ⚙️ Developed Components
* **`src/dominio/entidades.py`**: Implementation of `Tripulante`, `InsumoMedico`, `DiagnosticoTriage`, and `LecturaBiometrica`, including Mean Arterial Pressure (MAP) calculation and physiological barriers against impossible sensor readings.
* **`src/dominio/excepciones.py`**: Business exception hierarchy (`ErrorJerarquiaRBAC`, `ErrorInsumoInsuficiente`, `ErrorBiometriaFueraDeRangoFisico`).
* **`src/dominio/politicas_rbac.py`**: **Strategy Pattern** implementation for `Comandante Medico`, `Oficial Cientifico`, and `Especialista de Mision` ranks.
* **`src/dominio/evaluador_riesgo_espacial.py`**: Polymorphic rule engine adjusting sleep, mood, blood pressure, heart rate, glucose, temperature, radiation, and exercise thresholds according to the operational environment (`Transito Espacial (0G)`, `Estacion Espacial`, `Rover Explorador`, `Base Planetaria`).
* **`src/dominio/puertos.py`**: Abstract contracts (`ABC`) enforcing Dependency Inversion (DIP).

## 🚀 Console Execution Results
```text
collected 5 items

tests/unitarios/test_dominio_astromed.py::test_rbac_especialista_no_puede_dar_baja PASSED    [ 20%]
tests/unitarios/test_dominio_astromed.py::test_rbac_oficial_cientifico_no_modifica_comandante_medico PASSED [ 40%]
tests/unitarios/test_dominio_astromed.py::test_evaluador_detecta_hipoglucemia_critica_y_asigna_sistema PASSED [ 60%]
tests/unitarios/test_dominio_astromed.py::test_mismo_sueno_es_precaucion_en_estacion_pero_critico_en_rover PASSED [ 80%]
tests/unitarios/test_dominio_astromed.py::test_barrera_biologica_rechaza_valores_imposibles PASSED [100%]

======================================== 5 passed in 0.98s ========================================
```