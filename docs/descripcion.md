# 🛰️ Resumen Ejecutivo de Ingeniería — ASTRO-MED HUD

> 🌐 **Language / Idioma:** [Read in English](./description.md) | **Español**

## 1. Propuesta de Valor: De la EEI al Espacio Profundo
El protocolo oficial *Spaceflight Standard Measures* de la NASA en la Estación Espacial Internacional (EEI) depende de congelar suero, saliva e hisopados de microbioma o enviar tubos de sangre ACD a la Tierra en menos de 48 horas. En la Luna, Marte (22 min de latencia) o Europa en Júpiter (>45 min), el retorno físico inmediato es inviable y obliga a procesar el diagnóstico a bordo.

**ASTRO-MED HUD** transforma ese protocolo en un Sistema de Soporte a la Decisión Clínica (CDSS) 100% autónomo (*Offline-First LAN*) que evalúa los 5 Peligros de la NASA en el punto de atención.

## 2. Matriz de Arquitectura y Patrones de Diseño

| Patrón / Principio | Ubicación Física | Propósito Técnico |
| :--- | :--- | :--- |
| **Arquitectura Hexagonal** | `src/dominio/`, `src/aplicacion/` | Aísla las reglas clínicas de SQLite, FastAPI y las vistas gráficas. |
| **Patrón Estrategia (GoF)** | `evaluador_riesgo_espacial.py`, `politicas_rbac.py` | Evalúa umbrales biométricos según el entorno (0G, Rover, Superficie) y jerarquías RBAC. |
| **Unidad de Trabajo (ACID)** | `gestor_sqlite.py` | Garantiza transacciones atómicas (`commit`/`rollback`) entre telemetría, racha y stock médico. |
| **Patrón Repositorio (3FN)** | `repositorio_*_sql.py` | Abstrae consultas SQL, vistas, columnas calculadas (`presion_media`) y *Triggers*. |
| **Inversión de Dependencias** | `puertos.py`, `inyector_dependencias.py` | Desacopla los casos de uso mediante contratos abstractos (`ABC`) e inyección IoC. |

## 3. Cobertura de Medidas Estándar de la NASA (Standard Measures)

* **Neuro-Psicológico (`NEURO_PSICO`):** Integra métricas de la batería *Pulsar Cognition* (10 pruebas), actigrafía de sueño (*Actiwatch Spectrum Plus*), encuestas *EveryWear* y escala de cinetosis pos-Crew-8 (0 a 20).
* **Cardiovascular y Dosimetría (`CARDIO_RAD`):** Monitorea presión arterial media (MAP), frecuencia cardíaca, ecografía carotídea (grosor íntima-media) y tolerancia ortostática en prueba de bipedestación de 3,5 minutos.
* **Metabólico e Inmunitario (`METABOLICO_INMUNE`):** Controla perfil bioquímico (glucosa mg/dL), respuesta febril inmunitaria (innata/adaptativa) y vigilancia de microbioma en entornos cerrados.
* **Músculo-Esquelético y Sensoriomotor (`MUSCULO_ESQUELETICO`):** Registra contramedidas en máquina ARED, tracción isométrica a medio muslo (IMTP), prueba *Sit-to-Stand* (obstáculo de 30 cm) y caminata en tándem (10 pasos talón-punta).