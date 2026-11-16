# 🚀 ASTRO-MED HUD | Sistema Autónomo de Monitoreo Biométrico y Triage Espacial

> 🌐 **[Read this documentation in English (Main README)](./README.md)**

> **Desafío NASA Space Apps / Human Research Program (HRP):** Creación de software de monitorización de la salud, Medidas Estándar de Vuelos Espaciales (*Spaceflight Standard Measures*) y soporte a la decisión clínica (CDSS) para astronautas en misiones de larga duración (Estación Espacial, Luna, Marte y Europa - Júpiter).

---

## 👨‍🚀 Equipo de Desarrollo (Tripulación de Misión)

Proyecto desarrollado por estudiantes de la **Tecnicatura Superior en Análisis de Sistemas**:

| Código NASA | Integrante | Rol en la Misión Simulada | Especialidad en el Sistema |
| :--- | :--- | :--- | :--- |
| **`AST-001`** | **Alicia López** | Comandante Médico | Medicina Aeroespacial y Auditoría General |
| **`AST-002`** | **Marcos Santamaría** | Oficial Científico | Astrobiología y Dosimetría de Radiación |
| **`AST-003`** | **Jazmín Saavedra** | Especialista de Misión | Ingeniería de Rover y Operaciones EVA |
| **`AST-004`** | **David Bravo** | Especialista de Misión | Arquitectura de Software y Soporte Vital |
| **`AST-005`** | **Zoe Baiz** | Oficial Científico | Neurociencia, UX/UI y Factores Humanos |
| **`AST-006`** | **David García** | Especialista de Misión | Telecomunicaciones, Redes LAN y Navegación |
| **`AST-007`** | **Iván Jauregui** | Especialista de Misión | Robótica y Mantenimiento de Módulos |

---

## 🌌 El Problema que Resolvemos: Los 5 Peligros de la NASA y las Medidas Estándar (Standard Measures)

En misiones hacia la Luna (Programa Artemis), Marte y las lunas heladas del sistema solar exterior (Europa en Júpiter), los astronautas se enfrentan a **cinco peligros que interactúan entre sí**:
1. **Radiación Espacial:** Incrementa el riesgo cardiovascular y de daño celular agudo ante tormentas solares o cinturones magnetosféricos como el de Júpiter.
2. **Aislamiento y Confinamiento:** Altera los ciclos circadianos, degrada el sueño y afecta el estado de ánimo y la atención cognitiva.
3. **Distancia desde la Tierra:** Con una latencia de comunicación de hasta **$22\text{ minutos}$ por tramo en Marte** y **más de $45\text{ minutos}$ en Júpiter**, la tripulación no puede depender de médicos en Tierra ni de enviar muestras congeladas de sangre o saliva de regreso a laboratorios terrestres en $48\text{ horas}$ como se hace hoy en la Estación Espacial Internacional (EEI).
4. **Campos Gravitatorios Alterados:** En microgravedad ($0\text{G}$) o gravedad parcial ($1/6\text{ G}$ en la Luna, $3/8\text{ G}$ en Marte), los fluidos migran hacia la cabeza y se acelera la pérdida de masa ósea y muscular.
5. **Entornos Hostiles y Cerrados:** La alteración del ecosistema interno impacta sobre el sistema inmunitario, el microbioma y el metabolismo.

### 💡 Nuestra Solución
**ASTRO-MED HUD** es un ecosistema **100% Offline-First (Local-First LAN)** y **Bilingüe (Español / Inglés)** construido bajo **Arquitectura Hexagonal**. Combina dos interfaces sincronizadas en tiempo real sobre una única base de datos transaccional (`SQLite3` en 3FN):

1. **📱 HUD Interactivo del Astronauta (`src/presentacion/hud_astronauta/` - Puerto `8080`):**
   * **Acceso Directo sin Contraseña (Estilo NASA EveryWear):** Siguiendo el estándar de las tablets iPad con *EveryWear* de la EEI, los astronautas ingresan a su terminal con un solo clic sin fricción de claves criptográficas durante maniobras operativas o emergencias.
   * **Gemelo Digital Anatómico (SVG Clicable):** Figura humana interactiva dividida en 4 subsistemas (`NEURO_PSICO`, `CARDIO_RAD`, `METABOLICO_INMUNE`, `MUSCULO_ESQUELETICO`) que cambian de color automáticamente (**Verde = Nominal**, **Ámbar = Precaución**, **Rojo = Crítico**).
   * **Integración con *Spaceflight Standard Measures* de la NASA:** Incorpora trazabilidad para la batería cognitiva **Pulsar Cognition** ($10\text{ pruebas}$), actigrafía de sueño **Actiwatch Spectrum Plus**, **Cuestionario de Cinetosis** pos-Crew-8 (escala $0$ a $20$), **Ecografía Carotídea** (espesor íntima-media), **Tracción Isométrica a Medio Muslo (IMTP)** y pruebas sensoriomotoras posturales (*Sit-to-Stand* y *Tandem Walk*).
   * **Simulador Multi-Misión Interplanetario (`simulador_misiones/`):** Permite conmutar en tiempo real entre **🌕 Misión Artemis (Luna)**, **🔴 Misión Ares (Marte)** y **❄️ Misión Crio-Europa (Luna Helada de Júpiter)** con $105$ lecturas biométricas históricas.
   * **Protocolos Paso a Paso y Gamificación:** Guía a tripulantes sin formación médica, descuenta atómicamente suministros del **Botiquín de a Bordo** e incrementa la **Racha Vital de Autocuidado (🔥)**.

2. **🖥️ Consola de Comando Médico (`src/presentacion/consola_comando/` - Conectada al Puerto `8000`):**
   * **Selector de Idioma Global (`ES` / `EN`):** Al iniciar `login.py`, permite elegir entre Español e Inglés, traduciendo toda la consola de escritorio y sincronizando automáticamente el idioma del HUD Web a través de la red LAN (`/api/idioma`).
   * **Seguridad Criptográfica para Control de Vuelo:** Protegida con hashing `Bcrypt` exclusivamente para la estación de mando médico.
   * **Analítica Científica y Consola SQL Sandbox:** Monitoreo en vivo de los 7 tripulantes, gráficos con `Pandas` y `Matplotlib`, y auditoría SQL en modo de solo lectura.

---

## 🛠️ Requisitos e Instalación Rápida (Paso a Paso)

El proyecto utiliza exclusivamente librerías con binarios precompilados (*wheels*) para ejecutarse en menos de $2\text{ minutos}$ en **Windows, Linux o macOS**.

### 1. Clonar el repositorio e ingresar a la carpeta
```bash
git clone <URL_DEL_REPOSITORIO>
cd ASTRO_MED_HUD
```

### 2. Crear y activar el entorno virtual de Python (Recomendado Python 3.10+)

* **En Windows (CMD o PowerShell):**
  ```powershell
  python -m venv .venv
  .venv\Scripts\activate
  ```
* **En Linux / macOS:**
  ```bash
  python3 -m venv .venv
  source .venv/bin/activate
  ```

### 3. Instalar las dependencias
```bash
pip install -r requirements.txt
```

---

## ▶️ Cómo Ejecutar la Aplicación (Un Solo Comando)

Ejecutá desde la raíz del proyecto:

```bash
python -m src.presentacion.consola_comando.vistas.login
```

### ¿Qué hace este comando automáticamente?
1. Crea e inicializa la base de datos `db/astro_med.db` aplicando el esquema en 3FN y los *Triggers* de seguridad.
2. Siembra automáticamente los **7 astronautas del equipo**, el **Botiquín Médico de la nave** y **105 registros históricos ($15\text{ días Sol}$ por tripulante)**.
3. Enciende en segundo plano el servidor **API RESTful FastAPI** en `http://0.0.0.0:8000` (Swagger UI en `http://127.0.0.1:8000/docs`).
4. Enciende el servidor del **HUD Interactivo del Astronauta** en `http://0.0.0.0:8080`.
5. Abre la ventana de **Control de Vuelo**, donde podés elegir el idioma (**Español / English**), ingresar a la consola médica o abrir el **HUD sin contraseña en el navegador**.

### 🔑 Esquema de Acceso (Control de Vuelo vs. HUD Astronauta)

| Interfaz | Método de Autenticación | Usuario / Perfil | Clave | Rol Operativo |
| :--- | :--- | :--- | :--- | :--- |
| **🖥️ Consola Control de Vuelo (Tkinter)** | Clave Criptográfica (`Bcrypt`) | `admin` | `admin123` | **Alicia López (`AST-001`)** — Comandante Médico |
| **📱 HUD Astronauta (Web Puerto 8080)** | **Acceso Directo sin Clave (EveryWear)** | Selección en 1 clic (`AST-001` a `AST-007`) | *Sin clave* | Toda la tripulación (Autochequeo y Triage) |

---

## 🧪 Cómo Ejecutar la Suite de Pruebas Automatizadas (TDD)

El proyecto cuenta con **15 pruebas automatizadas** (Unitarias de Dominio, Integración SQL 3FN/Triggers en RAM `:memory:`, Contratos HTTP FastAPI y Sincronización E2E entre el HUD Web y la Consola Tkinter):

```bash
pytest tests/ -v
```

---

## 📚 Documentación de Ingeniería del Proyecto

* [🚀 Justificación Analítica del Diseño Arquitectónico](./docs/fundamentos/diseño_arquitectonico.md) | [English Version](./docs/fundamentos/architectural_design.md)
* [🧪 Plan de Construcción Guiado por Pruebas (TDD)](./docs/fundamentos/plan_construccion_guiado_TDD.md) | [English Version](./docs/fundamentos/TDD_construction_plan.md)
* **Reportes de Auditoría por Etapa:**
  * [📄 Etapa 1: Núcleo de Dominio Clínico-Espacial y Tests Unitarios](./docs/reportes/etapa_1.md) | [English](./docs/reportes/stage_1.md)
  * [📄 Etapa 2: Casos de Uso, Persistencia 3FN y Tests de Integración SQL](./docs/reportes/etapa_2.md) | [English](./docs/reportes/stage_2.md)
  * [📄 Etapa 3: Adaptador API RESTful, Simulador de Misiones y Pruebas HTTP](./docs/reportes/etapa_3.md) | [English](./docs/reportes/stage_3.md)
  * [📄 Etapa 4: Adaptadores de Presentación (`hud_astronauta` + `consola_comando`) y Sincronización E2E](./docs/reportes/etapa_4.md) | [English](./docs/reportes/stage_4.md)