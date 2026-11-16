# 🛰️ Engineering Executive Summary — ASTRO-MED HUD

> 🌐 **Language / Idioma:** **English** | [Leer en Español](./descripcion.md)

## 1. Value Proposition: From Low Earth Orbit (ISS) to Deep Space
NASA's official *Spaceflight Standard Measures* protocol aboard the International Space Station (ISS) relies on freezing serum, saliva, and microbiome swabs or returning ambient ACD blood tubes to Earth laboratories within 48 hours. During missions to the Moon, Mars (22-minute communication delay), or Jupiter's icy moon Europa (>45-minute delay), physical sample return is impossible, requiring autonomous on-board clinical triage.

**ASTRO-MED HUD** converts these protocols into a 100% autonomous, **Offline-First LAN Clinical Decision Support System (CDSS)** that evaluates NASA's 5 Spaceflight Hazards at the point of care.

## 2. Software Architecture & Design Patterns Matrix

| Pattern / Principle | Physical Location | Engineering Purpose |
| :--- | :--- | :--- |
| **Hexagonal Architecture** | `src/dominio/`, `src/aplicacion/` | Isolates clinical rules from SQLite, FastAPI, and UI adapters. |
| **Strategy Pattern (GoF)** | `evaluador_riesgo_espacial.py`, `politicas_rbac.py` | Dynamically adjusts biometric thresholds by environment (0G, Rover, Surface) and RBAC rank. |
| **Unit of Work (ACID)** | `gestor_sqlite.py` | Ensures atomic transactions (`commit`/`rollback`) across telemetry, streak, and medical kit stock. |
| **Repository Pattern (3NF)** | `repositorio_*_sql.py` | Encapsulates SQL queries, views, generated columns (`presion_media`), and safety Triggers. |
| **Dependency Inversion** | `puertos.py`, `inyector_dependencias.py` | Decouples use cases through abstract interfaces (`ABC`) and FastAPI IoC injection. |

## 3. NASA Spaceflight Standard Measures Alignment

* **Neuro-Psychological (`NEURO_PSICO`):** Tracks *Pulsar Cognition* (10 brief tests), *Actiwatch Spectrum Plus* sleep actigraphy, *EveryWear* iPad behavioral surveys, and the post-Crew-8 Motion Sickness scale (0–20).
* **Cardiovascular & Dosimetry (`CARDIO_RAD`):** Monitors Mean Arterial Pressure (MAP), heart rate, carotid intima-media ultrasound, and orthostatic response during the 3.5-minute recovery-from-fall/stand test.
* **Metabolic & Immune (`METABOLICO_INMUNE`):** Evaluates point-of-care blood glucose (mg/dL), febrile innate/adaptive immune reactivation, and closed-habitat microbiome indicators.
* **Musculoskeletal & Sensorimotor (`MUSCULO_ESQUELETICO`):** Audits daily ARED resistive exercise, Isometric Mid-Thigh Pull (IMTP) strength, Sit-to-Stand walk-and-turn (30 cm obstacle), and 10-step Tandem Walk stability.