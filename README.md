# 🚀 ASTRO-MED HUD | Autonomous Biometric Monitoring & Space Triage System

> 🌐 **[Leer esta documentación en Español](./README_ESP.md)**

> **NASA Space Apps / Human Research Program (HRP) Challenge:** Health monitoring software, *Spaceflight Standard Measures* integration, and autonomous Clinical Decision Support System (CDSS) for astronauts on long-duration missions (International Space Station, Moon, Mars, and Europa - Jupiter).

---

## 👨‍🚀 Development Team (Mission Crew)

Developed by students of the **Higher Technical Degree in Systems Analysis**:

| NASA Code | Team Member | Simulated Mission Role | System Specialty |
| :--- | :--- | :--- | :--- |
| **`AST-001`** | **Alicia López** | Medical Commander | Aerospace Medicine & General Auditing |
| **`AST-002`** | **Marcos Santamaría** | Science Officer | Astrobiology & Radiation Dosimetry |
| **`AST-003`** | **Jazmín Saavedra** | Mission Specialist | Rover Engineering & EVA Operations |
| **`AST-004`** | **David Bravo** | Mission Specialist | Software Architecture & Life Support Systems |
| **`AST-005`** | **Zoe Baiz** | Science Officer | Neuroscience, UX/UI & Human Factors |
| **`AST-006`** | **David García** | Mission Specialist | Telecommunications, LAN Networks & Navigation |
| **`AST-007`** | **Iván Jauregui** | Mission Specialist | Robotics & Habitat Module Maintenance |

---

## 🌌 The Problem We Solve: NASA's 5 Hazards & Spaceflight Standard Measures

On missions to the Moon (Artemis Program), Mars, and the icy moons of the outer solar system (Europa at Jupiter), astronauts face **five interacting hazards**:
1. **Space Radiation:** Increases cardiovascular risk and acute cellular damage during solar particle events or within magnetospheric belts such as Jupiter's.
2. **Isolation and Confinement:** Disrupts circadian rhythms, degrades sleep architecture, and impacts mood, team cohesion, and cognitive attention.
3. **Distance from Earth:** With one-way communication latency reaching **$22\text{ minutes}$ on Mars** and **over $45\text{ minutes}$ at Jupiter**, the crew cannot rely on real-time Earth flight surgeons or return ambient ACD blood tubes within $48\text{ hours}$ and frozen serum/saliva samples to terrestrial laboratories as currently done on the ISS.
4. **Altered Gravity Fields:** In microgravity ($0\text{G}$) or partial gravity ($1/6\text{ G}$ on the Moon, $3/8\text{ G}$ on Mars), bodily fluids shift cephalad and bone/muscle atrophy accelerates.
5. **Hostile/Closed Environments:** Altered internal habitat ecosystems impact immune function, microbiome stability, and metabolism.

### 💡 Our Solution
**ASTRO-MED HUD** is a **100% Offline-First (Local-First LAN)** and **Bilingual (English / Spanish)** ecosystem built under **Hexagonal Architecture**. It synchronizes two real-time interfaces over a single transactional database (`SQLite3` in 3NF):

1. **📱 Interactive Astronaut HUD (`src/presentacion/hud_astronauta/` - Port `8080`):**
   * **Passwordless Direct Access (NASA EveryWear Style):** Modeled after NASA's *EveryWear* iPad application used on the ISS, crew members open their personal biometric HUD with a single click—eliminating password friction during EVA preparation or medical contingencies.
   * **Anatomical Digital Twin (Clickable SVG):** Interactive human body model divided into 4 subsystems (`NEURO_PSICO`, `CARDIO_RAD`, `METABOLICO_INMUNE`, `MUSCULO_ESQUELETICO`) dynamically color-coded (**Green = Nominal**, **Amber = Caution**, **Red = Critical**).
   * **NASA *Spaceflight Standard Measures* Integration:** Built-in support and clinical encyclopedia for the **Pulsar Cognition** battery ($10\text{ tests}$), **Actiwatch Spectrum Plus** sleep actigraphy, post-Crew-8 **Motion Sickness Questionnaire** ($0\text{--}20\text{ scale}$), **Carotid Intima-Media Ultrasound**, **Isometric Mid-Thigh Pull (IMTP)** lower-body strength tests, and post-landing sensorimotor tests (*Sit-to-Stand with walk-and-turn* and *Tandem Walk*).
   * **Interplanetary Multi-Mission Simulator (`simulador_misiones/`):** Hot-swaps in real time between **🌕 Artemis Mission (Moon)**, **🔴 Ares Mission (Mars)**, and **❄️ Cryo-Europa Mission (Jupiter's Icy Moon)** with $105$ historical biometric records.
   * **Step-by-Step Guided Protocols & Gamification:** Provides clear medical instructions for non-physician crew members, atomically deducts supplies from the **On-Board Medical Kit**, and tracks the **Vital Self-Care Streak (🔥)**.

2. **🖥️ Flight Control Medical Console (`src/presentacion/consola_comando/` - Connected to Port `8000`):**
   * **Global Language Selector (`EN` / `ES`):** At startup in `login.py`, operators choose between English and Spanish, translating the entire desktop console and automatically synchronizing the Web HUD language across the LAN (`/api/idioma`).
   * **Cryptographic Security for Flight Control:** Protected via `Bcrypt` password hashing exclusively for the Flight Surgeon / Medical Commander station.
   * **Scientific Analytics & SQL Sandbox Console:** Live telemetry monitoring for all 7 astronauts, multi-variable time-series charts with `Pandas` and `Matplotlib`, and a read-only SQL audit sandbox.

---

## 🛠️ Requirements & Quick Installation (Step-by-Step)

The project uses pre-compiled binary wheels exclusively so any team member or judge can run it in under $2\text{ minutes}$ on **Windows, Linux, or macOS**.

### 1. Clone the repository and enter the directory
```bash
git clone <REPOSITORY_URL>
cd ASTRO_MED_HUD
```

### 2. Create and activate the Python virtual environment (Python 3.10+ recommended)

* **On Windows (CMD or PowerShell):**
  ```powershell
  python -m venv .venv
  .venv\Scripts\activate
  ```
* **On Linux / macOS:**
  ```bash
  python3 -m venv .venv
  source .venv/bin/activate
  ```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

---

## ▶️ How to Run the Application (Single Command)

Run from the project root directory:

```bash
python -m src.presentacion.consola_comando.vistas.login
```

### What does this command do automatically?
1. Creates and initializes `db/astro_med.db`, applying the 3NF relational schema and safety *Triggers*.
2. Seeds all **7 squadron astronauts**, the **On-Board Medical Kit**, and **105 historical biometric readings ($15\text{ Sol days}$ per crew member)**.
3. Starts the background **FastAPI RESTful Server** at `http://0.0.0.0:8000` (Swagger UI available at `http://127.0.0.1:8000/docs`).
4. Starts the **Astronaut Web HUD Server** at `http://0.0.0.0:8080`.
5. Opens the **Flight Control Login Window**, where you can select the interface language (**Español / English**), log into the desktop medical console, or launch the **Passwordless Astronaut HUD** in your browser (or from any smartphone/tablet on the same Wi-Fi LAN).

### 🔑 Access Matrix (Flight Control vs. Astronaut HUD)

| Interface | Authentication Method | User / Profile | Password | Operational Role |
| :--- | :--- | :--- | :--- | :--- |
| **🖥️ Flight Control Console (Tkinter)** | Cryptographic Key (`Bcrypt`) | `admin` | `admin123` | **Alicia López (`AST-001`)** — Medical Commander |
| **📱 Astronaut Web HUD (Port 8080)** | **Passwordless Direct Access (EveryWear)** | 1-Click Profile Selector (`AST-001` to `AST-007`) | *No password* | All 7 Crew Members (Self-Check & Autonomous Triage) |

---

## 🧪 How to Run the Automated Test Suite (TDD)

The project includes **15 automated tests** (Domain Unit Tests, In-Memory `:memory:` 3NF SQL & Trigger Integration Tests, FastAPI HTTP Contract Tests, and E2E Synchronization between the Web HUD and Tkinter Console):

```bash
pytest tests/ -v
```

---

## 📚 Project Engineering Documentation

* [🚀 Analytical Justification of Architectural Design](./docs/fundamentos/architectural_design.md) | [Versión en Español](./docs/fundamentos/diseño_arquitectonico.md)
* [🧪 Test-Driven Development (TDD) Construction Plan](./docs/fundamentos/TDD_construction_plan.md) | [Versión en Español](./docs/fundamentos/plan_construccion_guiado_TDD.md)
* **Stage Execution Reports:**
  * [📄 Stage 1: Clinical-Space Domain Core & Unit Tests](./docs/reportes/stage_1.md) | [Español](./docs/reportes/etapa_1.md)
  * [📄 Stage 2: Use Cases, 3NF SQLite Persistence & SQL Integration Tests](./docs/reportes/stage_2.md) | [Español](./docs/reportes/etapa_2.md)
  * [📄 Stage 3: FastAPI RESTful Adapter, Multi-Mission Simulator & HTTP Tests](./docs/reportes/stage_3.md) | [Español](./docs/reportes/etapa_3.md)
  * [📄 Stage 4: Bilingual Presentation Adapters (`hud_astronauta` + `consola_comando`) & E2E Sync](./docs/reportes/stage_4.md) | [Español](./docs/reportes/etapa_4.md)