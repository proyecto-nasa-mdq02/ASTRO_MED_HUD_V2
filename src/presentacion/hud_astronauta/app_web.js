// ===================================================================================
//  ASTRO-MED HUD · MOTOR ASÍNCRONO SPA
//  Acceso directo sin clave · bilingüe ES/EN · telemetría EveryWear · triage CDSS
//  Sin dependencias de runtime: solo DOM, Fetch API y Canvas 2D.
// ===================================================================================

const HOST_LAN = window.location.hostname || "127.0.0.1";
const API_BASE = `http://${HOST_LAN}:8000/api`;

const SISTEMAS = ["NEURO_PSICO", "CARDIO_RAD", "METABOLICO_INMUNE", "MUSCULO_ESQUELETICO"];

// Los roles y especialidades llegan en español desde la base de datos.
// Solo se traducen sus etiquetas visibles; los datos del backend no se alteran.
const ROLES_EN = {
    "Comandante Medico": "Medical Commander",
    "Oficial Cientifico": "Science Officer",
    "Especialista de Mision": "Mission Specialist",
};

const ESPECIALIDADES_EN = {
    "Medicina Aeroespacial": "Aerospace Medicine",
    "Astrobiología y Dosimetría": "Astrobiology & Dosimetry",
    "Ingeniería de Rover y EVA": "Rover & EVA Engineering",
    "Sistemas de Soporte Vital": "Life Support Systems",
    "Neurociencia y Factores Humanos": "Neuroscience & Human Factors",
    "Telecomunicaciones y Navegación": "Telecommunications & Navigation",
    "Robótica y Mantenimiento de Módulos": "Robotics & Module Maintenance",
};

function normalizarEtiqueta(valor) {
    return String(valor || "")
        .normalize("NFD")
        .replace(/[\u0300-\u036f]/g, "")
        .toLowerCase()
        .trim();
}

const ROLES_EN_NORMALIZADOS = Object.fromEntries(
    Object.entries(ROLES_EN).map(([clave, valor]) => [normalizarEtiqueta(clave), valor])
);

const ESPECIALIDADES_EN_NORMALIZADAS = Object.fromEntries(
    Object.entries(ESPECIALIDADES_EN).map(([clave, valor]) => [normalizarEtiqueta(clave), valor])
);

function localizarRol(valor) {
    if (idiomaActual !== "en") return valor;
    return ROLES_EN[valor] || ROLES_EN_NORMALIZADOS[normalizarEtiqueta(valor)] || valor;
}

function localizarEspecialidad(valor) {
    if (idiomaActual !== "en") return valor;
    return ESPECIALIDADES_EN[valor] || ESPECIALIDADES_EN_NORMALIZADAS[normalizarEtiqueta(valor)] || valor;
}

function tituloTripulante(tripulante) {
    return `${localizarRol(tripulante.rol)} · ${localizarEspecialidad(tripulante.especialidad)}`;
}

const ENTORNOS = {
    "Transito Espacial (0G)": { es: "Tránsito espacial · 0G", en: "Space transit · 0G" },
    "Estacion Espacial": { es: "Estación espacial · microgravedad", en: "Space station · microgravity" },
    "Rover Explorador": { es: "Rover explorador · confinamiento", en: "Rover · confinement" },
    "Base Planetaria": { es: "Base planetaria · EVA", en: "Planetary base · EVA" },
};

const ESTUDIOS = [
    { valor: "everywear_encuesta_diaria.dat", es: "Encuesta EveryWear Sueño/Ánimo", en: "EveryWear Sleep/Mood Survey" },
    { valor: "pulsar_cognition_10tests.dat", es: "Batería Pulsar Cognition (10 pruebas)", en: "Pulsar Cognition Battery (10 tests)" },
    { valor: "actiwatch_spectrum_sleep.dat", es: "Actigrafía Actiwatch Spectrum Plus", en: "Actiwatch Spectrum Plus Actigraphy" },
    { valor: "cinetosis_escala_0_20.dat", es: "Cuestionario Cinetosis (Escala 0-20)", en: "Motion Sickness Questionnaire (0-20)" },
    { valor: "eco_carotida_intima_media.png", es: "Ecografía Carótida (Íntima-Media)", en: "Carotid Ultrasound (Intima-Media)" },
    { valor: "imtp_traccion_isometrica_muslo.dat", es: "Fuerza Isométrica Medio Muslo (IMTP)", en: "Isometric Mid-Thigh Pull (IMTP)" },
    { valor: "sit_to_stand_tandem_walk.mp4", es: "Prueba Sensoriomotora (Sit-to-Stand / Tándem)", en: "Sensorimotor Test (Sit-to-Stand / Tandem)" },
    { valor: "panel_inmune_saliva_microbioma.dat", es: "Muestra Saliva / Microbioma / Tubo ACD", en: "Saliva / Microbiome / ACD Tube Sample" },
];

const I18N_WEB = {
    es: {
        hero_badge: "NASA HUMAN RESEARCH PROGRAM · ARTEMIS II",
        hero_titulo: "Medicina autónoma para la próxima frontera.",
        hero_sub: "Telemetría biométrica, gemelo digital anatómico y triage CDSS en un solo puesto de control.",
        hero_stat1: "Sistemas monitoreados",
        hero_stat2: "Medidas estándar",
        hero_stat3: "Escenarios de misión",
        hero_list1: "Gemelo digital anatómico con estado por sistema",
        hero_list2: "Triage autónomo NASA HRP · 4 peligros espaciales",
        hero_list3: "Telemetría EveryWear · Medidas estándar",
        chip_admin: "Cmd. López",
        chip_santamaria: "Of. Santamaría",
        chip_saavedra: "Esp. Saavedra",
        chip_bravo: "Esp. Bravo",
        chip_baiz: "Of. Baiz",
        chip_garcia: "Esp. García",
        chip_jauregui: "Esp. Jauregui",
        hero_pie: "HUD v2.0 · Mission Control",
        login_api_ok: "Servidor de misión enlazado",
        login_api_error: "Servidor de misión sin respuesta",
        login_panel_eyebrow: "ACCESO DE TRIPULACIÓN",
        login_titulo: "Identificación de vuelo",
        login_subtitulo: "Terminal biométrica autónoma sin contraseña para tripulación en misión.",
        login_perfil: "Seleccioná tu perfil de astronauta",
        login_entrar: "ABRIR MI HUD BIOMÉTRICO",
        acceso_rapido: "Ingreso 1-Clic:",
        login_seguridad: "◈  Canal local cifrado · Sesión de un solo operador",

        sel_tripulante: "Tripulante monitoreado",
        sel_entorno: "Entorno operativo",
        racha_titulo: "RACHA VITAL",
        dias_sol: "Días Sol",
        btn_salir: "Cambiar Tripulante",
        crew_rol: "Tripulante en seguimiento",
        meta_entorno: "ENTORNO",
        meta_lectura: "ÚLTIMA LECTURA",
        meta_mision: "MISIÓN",
        autonomia: "Autonomía local activa",

        gemelo_titulo: "GEMELO DIGITAL ANATÓMICO",
        gemelo_inst: "Hacé clic en cada zona del cuerpo para inspeccionar las Medidas Estándar NASA, el impacto espacial y el triage autónomo.",
        placa_sitios: "SITIOS ANATÓMICOS DE MEDICIÓN",
        placa_hint: "Seleccioná un sistema",
        estado_nominal: "Nominal",
        estado_precaucion: "Precaución",
        estado_critico: "Crítico",
        leyenda_nota: "Color = estado del backend",
        detalle_evidencia: "EVIDENCIA SSM",

        triage_eyebrow: "EVALUACIÓN AUTÓNOMA",
        triage_titulo: "DIAGNÓSTICO AUTÓNOMO DE MISIÓN",
        resumen_clinico: "RESUMEN CLÍNICO",
        protocolo_guia: "📋 PROTOCOLO PASO A PASO",
        triage_sistema: "SISTEMA AFECTADO",
        triage_nivel: "NIVEL",
        tierra_ok: "🛡️ Autonomía Local Activa",
        tierra_critico: "📡 Enlace prioritario con médicos en tierra",

        vitales_eyebrow: "TELEMETRÍA EN VIVO",
        vitales_titulo: "CONSTANTES FISIOLÓGICAS",
        sub_pa: "PAM {pam} mmHg",
        sub_fc: "Ref. 60–100 lpm",
        sub_glu: "Ref. 70–140 mg/dL",
        sub_temp: "Ref. 36.0–37.4 °C",
        sub_sueno: "Objetivo 7–8 h",
        sub_ejer: "Objetivo ≥ 30 min",

        grafico_eyebrow: "TENDENCIA · 15 DÍAS SOL",
        grafico_titulo: "EVOLUCIÓN TEMPORAL DE INDICADORES",
        metrica_fc: "Frecuencia cardíaca (BPM)",
        metrica_sis: "Presión sistólica (mmHg)",
        metrica_glu: "Glucosa (mg/dL)",
        metrica_sueno: "Sueño (h)",
        metrica_animo: "Ánimo (1–5)",
        chart_ultima: "Última",
        chart_promedio: "Promedio",
        chart_muestras: "Muestras",
        chart_sin_datos: "Sin lecturas registradas para este tripulante.",

        mision_tit: "CAMBIAR MISIÓN ESPACIAL",
        mision_sub: "Conmutá la base de datos entre los tres escenarios interplanetarios.",
        mision_luna_sub: "Luna · 384.400 km",
        mision_marte_sub: "Marte · 225 M km",
        mision_europa_sub: "Europa · 628 M km",
        sim_tit: "SIMULADOR DE PELIGROS",
        sim_sub: "Dispará una anomalía en vivo para evaluar la respuesta del CDSS.",
        sim_rad_tit: "Tormenta Solar",
        sim_rad_sub: "Radiación · 0G",
        sim_psy_tit: "Pulsar / Fatiga",
        sim_psy_sub: "Confinamiento rover",
        sim_met_tit: "Hipoglucemia",
        sim_met_sub: "Fiebre · EVA",
        sim_mus_tit: "Déficit IMTP",
        sim_mus_sub: "Atrofia · 0G",

        ssm_eyebrow: "NASA STANDARD MEASURES",
        ssm_titulo: "MEDIDAS ESTÁNDAR · 4 SISTEMAS",
        ssm_neuro_tit: "Sueño, cognición y ánimo",
        ssm_neuro_sub: "Actiwatch · Pulsar · EveryWear",
        ssm_cardio_tit: "Cardiovascular y radiación",
        ssm_cardio_sub: "PA · FC · Dosimetría",
        ssm_metabolico_tit: "Metabólico e inmune",
        ssm_metabolico_sub: "Glucosa · Fiebre · Microbioma",
        ssm_musculo_tit: "Músculo-esquelético",
        ssm_musculo_sub: "IMTP · ARED · Sensoriomotor",
        ssm_sueno: "Sueño",
        ssm_animo: "Ánimo",
        ssm_pa: "Presión",
        ssm_fc: "Pulso",
        ssm_rad: "Radiación",
        ssm_glu: "Glucosa",
        ssm_temp: "Temperatura",
        ssm_ejer: "Ejercicio",
        ssm_evid: "Evidencia",
        ssm_actigrafia: "Actigrafía",
        ref: "REF",

        registro_eyebrow: "EVERYWEAR · ENTRY",
        form_tit: "REGISTRAR MEDIDAS ESTÁNDAR",
        form_sub: "Cargá la lectura diaria para ejecutar el triage autónomo y actualizar el gemelo digital.",
        form_hemo: "Hemodinámica",
        in_sis: "Sistólica (mmHg)",
        in_dia: "Diastólica (mmHg)",
        in_fc: "Pulso (BPM)",
        form_meta: "Metabólico",
        in_glu: "Glucosa (mg/dL)",
        in_temp: "Temperatura (°C)",
        form_estilo: "Sueño, ánimo y ejercicio",
        in_sueno: "Sueño (h)",
        in_animo: "Ánimo (1–5)",
        in_ejer: "Ejercicio ARED (min)",
        in_rad: "Radiación (mSv)",
        form_registro: "Registro de Medida Estándar",
        in_evid: "Estudio / Medida Estándar",
        in_insumo: "Insumo del botiquín (opcional)",
        btn_submit: "REGISTRAR Y EJECUTAR TRIAGE",
        botiquin_eyebrow: "INVENTARIO A BORDO",
        botiquin_tit: "STOCK DEL BOTIQUÍN",
        botiquin_sub: "Insumos disponibles para el protocolo médico de la misión.",
        kit_none: "— Ninguno —",
        botiquin_vacio: "El botiquín no reporta insumos disponibles.",
        footer_1: "ASTRO-MED · NASA Space Apps · CDSS de vuelo",
        footer_2: "NASA HUMAN RESEARCH PROGRAM · STANDARD MEASURES",

        sin_lecturas: "Sin lecturas registradas para este tripulante.",
        sin_lecturas_sub: "Registrá una lectura EveryWear para ejecutar el primer triage autónomo.",
        sin_resumen: "Sin resumen clínico disponible.",
        sin_instruccion: "Sin acciones correctivas pendientes.",
        registrando: "REGISTRANDO…",
        registro_ok: "Lectura registrada y triage ejecutado.",
        simulando: "Inyectando escenario de crisis…",
        simulacion_ok: "Escenario ejecutado",
        entorno_actualizado: "Entorno operativo: {entorno}",
        mision_ok: "Misión inicializada con éxito.",
        confirmar_mision: "Esta acción reinicia la base de datos de misión con 105 registros. ¿Continuar?",
        error_perfil: "No se encontraron perfiles activos en la misión.",
        error_api: "No se pudo conectar con el servidor de misión.",
        error_generico: "Error inesperado de misión.",
        bienvenida: "Bienvenido/a, {nombre}. HUD sincronizado.",

        estados: { NOMINAL: "Nominal", PRECAUCION: "Precaución", CRITICO: "Crítico" },
        sistemas: {
            NEURO_PSICO: "Neuro-psicológico",
            CARDIO_RAD: "Cardiovascular / radiación",
            METABOLICO_INMUNE: "Metabólico / inmune",
            MUSCULO_ESQUELETICO: "Músculo-esquelético",
            NINGUNO: "Sin sistema afectado",
        },
        misiones: {
            ARTEMIS_LUNA: "Artemis · Luna",
            ARES_MARTE: "Ares · Marte",
            EUROPA_JUPITER: "Crio-Europa · Europa",
        },
        valores: {
            sueno: "Sueño",
            animo: "Ánimo",
            pa: "Presión",
            pam: "PAM",
            fc: "Pulso",
            rad: "Radiación",
            glu: "Glucosa",
            temp: "Temperatura",
            ejer: "Ejercicio ARED",
            evid: "Evidencia",
        },
        organos: {
            NEURO_PSICO: {
                titulo: "Neuro-psicológico",
                peligros: "Medidas Estándar NASA: Pulsar Cognition (10 pruebas) + Actiwatch Spectrum Plus + Cinetosis (0–20).",
                explicacion: "Evalúa aprendizaje visual, memoria de trabajo, atención vigilante y toma de decisiones de riesgo; integra encuestas de sueño y cohesión EveryWear y la escala de cinetosis pos-Crew-8.",
            },
            CARDIO_RAD: {
                titulo: "Cardiovascular y radiación",
                peligros: "Medidas Estándar NASA: ecografía carótida (íntima-media) + analitos cardíacos + bipedestación de 3,5 min.",
                explicacion: "Monitorea presión arterial y MAP, respuesta ortostática y estrés endotelial asociado a radiación cósmica o solar.",
            },
            METABOLICO_INMUNE: {
                titulo: "Metabólico e inmune",
                peligros: "Medidas Estándar NASA: panel bioquímico + inmunidad innata/adaptativa (tubos ACD/saliva) + microbioma.",
                explicacion: "Controla glucosa, respuesta febril y alteraciones del microbioma en hábitats cerrados.",
            },
            MUSCULO_ESQUELETICO: {
                titulo: "Músculo-esquelético",
                peligros: "Medidas Estándar NASA: tracción isométrica a medio muslo (IMTP) + sit-to-stand + caminata en tándem.",
                explicacion: "Evalúa fuerza isométrica, minutos de ejercicio resistivo ARED y equilibrio sensoriomotor pos-aterrizaje.",
            },
        },
    },
    en: {
        hero_badge: "NASA HUMAN RESEARCH PROGRAM · ARTEMIS II",
        hero_titulo: "Autonomous medicine for the next frontier.",
        hero_sub: "Biometric telemetry, an anatomical digital twin, and CDSS triage in a single control station.",
        hero_stat1: "Monitored systems",
        hero_stat2: "Standard measures",
        hero_stat3: "Mission scenarios",
        hero_list1: "Anatomical digital twin with per-system status",
        hero_list2: "Autonomous NASA HRP triage · 4 space hazards",
        hero_list3: "EveryWear telemetry · Standard measures",
        chip_admin: "Cdr. López",
        chip_santamaria: "Ofc. Santamaría",
        chip_saavedra: "Spec. Saavedra",
        chip_bravo: "Spec. Bravo",
        chip_baiz: "Ofc. Baiz",
        chip_garcia: "Spec. García",
        chip_jauregui: "Spec. Jauregui",
        hero_pie: "HUD v2.0 · Mission Control",
        login_api_ok: "Mission server linked",
        login_api_error: "Mission server not responding",
        login_panel_eyebrow: "CREW ACCESS",
        login_titulo: "Flight identification",
        login_subtitulo: "Passwordless autonomous biometric terminal for in-flight crew.",
        login_perfil: "Select your astronaut profile",
        login_entrar: "OPEN MY BIOMETRIC HUD",
        acceso_rapido: "1-Click Access:",
        login_seguridad: "◈  Encrypted local channel · Single-operator session",

        sel_tripulante: "Monitored crew member",
        sel_entorno: "Operational environment",
        racha_titulo: "VITAL STREAK",
        dias_sol: "Sol Days",
        btn_salir: "Switch Crew Member",
        crew_rol: "Monitored crew member",
        meta_entorno: "ENVIRONMENT",
        meta_lectura: "LAST READING",
        meta_mision: "MISSION",
        autonomia: "Local autonomy active",

        gemelo_titulo: "ANATOMICAL DIGITAL TWIN",
        gemelo_inst: "Click each body region to inspect NASA Standard Measures, spaceflight impact, and autonomous triage.",
        placa_sitios: "ANATOMICAL MEASUREMENT SITES",
        placa_hint: "Select a system",
        estado_nominal: "Nominal",
        estado_precaucion: "Caution",
        estado_critico: "Critical",
        leyenda_nota: "Color = backend state",
        detalle_evidencia: "SSM EVIDENCE",

        triage_eyebrow: "AUTONOMOUS ASSESSMENT",
        triage_titulo: "AUTONOMOUS MISSION DIAGNOSIS",
        resumen_clinico: "CLINICAL SUMMARY",
        protocolo_guia: "📋 STEP-BY-STEP PROTOCOL",
        triage_sistema: "AFFECTED SYSTEM",
        triage_nivel: "LEVEL",
        tierra_ok: "🛡️ Local Autonomy Active",
        tierra_critico: "📡 Priority link with flight surgeons",

        vitales_eyebrow: "LIVE TELEMETRY",
        vitales_titulo: "PHYSIOLOGICAL VITALS",
        sub_pa: "MAP {pam} mmHg",
        sub_fc: "Ref. 60–100 bpm",
        sub_glu: "Ref. 70–140 mg/dL",
        sub_temp: "Ref. 36.0–37.4 °C",
        sub_sueno: "Target 7–8 h",
        sub_ejer: "Target ≥ 30 min",

        grafico_eyebrow: "TREND · 15 SOL DAYS",
        grafico_titulo: "TEMPORAL INDICATOR EVOLUTION",
        metrica_fc: "Heart rate (BPM)",
        metrica_sis: "Systolic pressure (mmHg)",
        metrica_glu: "Glucose (mg/dL)",
        metrica_sueno: "Sleep (h)",
        metrica_animo: "Mood (1–5)",
        chart_ultima: "Latest",
        chart_promedio: "Average",
        chart_muestras: "Samples",
        chart_sin_datos: "No readings recorded for this crew member.",

        mision_tit: "SWITCH SPACE MISSION",
        mision_sub: "Switch the database between the three interplanetary scenarios.",
        mision_luna_sub: "Moon · 384,400 km",
        mision_marte_sub: "Mars · 225 M km",
        mision_europa_sub: "Europa · 628 M km",
        sim_tit: "HAZARD SIMULATOR",
        sim_sub: "Trigger a live anomaly to evaluate the CDSS response.",
        sim_rad_tit: "Solar Storm",
        sim_rad_sub: "Radiation · 0G",
        sim_psy_tit: "Pulsar / Fatigue",
        sim_psy_sub: "Rover confinement",
        sim_met_tit: "Hypoglycemia",
        sim_met_sub: "Fever · EVA",
        sim_mus_tit: "IMTP Deficit",
        sim_mus_sub: "Atrophy · 0G",

        ssm_eyebrow: "NASA STANDARD MEASURES",
        ssm_titulo: "STANDARD MEASURES · 4 SYSTEMS",
        ssm_neuro_tit: "Sleep, cognition and mood",
        ssm_neuro_sub: "Actiwatch · Pulsar · EveryWear",
        ssm_cardio_tit: "Cardiovascular and radiation",
        ssm_cardio_sub: "BP · HR · Dosimetry",
        ssm_metabolico_tit: "Metabolic and immune",
        ssm_metabolico_sub: "Glucose · Fever · Microbiome",
        ssm_musculo_tit: "Musculoskeletal",
        ssm_musculo_sub: "IMTP · ARED · Sensorimotor",
        ssm_sueno: "Sleep",
        ssm_animo: "Mood",
        ssm_pa: "Pressure",
        ssm_fc: "Pulse",
        ssm_rad: "Radiation",
        ssm_glu: "Glucose",
        ssm_temp: "Temperature",
        ssm_ejer: "Exercise",
        ssm_evid: "Evidence",
        ssm_actigrafia: "Actigraphy",
        ref: "REF",

        registro_eyebrow: "EVERYWEAR · ENTRY",
        form_tit: "LOG STANDARD MEASURES",
        form_sub: "Enter the daily reading to run autonomous triage and update the digital twin.",
        form_hemo: "Hemodynamics",
        in_sis: "Systolic (mmHg)",
        in_dia: "Diastolic (mmHg)",
        in_fc: "Pulse (BPM)",
        form_meta: "Metabolic",
        in_glu: "Glucose (mg/dL)",
        in_temp: "Temperature (°C)",
        form_estilo: "Sleep, mood and exercise",
        in_sueno: "Sleep (h)",
        in_animo: "Mood (1–5)",
        in_ejer: "ARED exercise (min)",
        in_rad: "Radiation (mSv)",
        form_registro: "Standard Measure Record",
        in_evid: "Study / Standard Measure",
        in_insumo: "Medical kit supply (optional)",
        btn_submit: "LOG & RUN TRIAGE",
        botiquin_eyebrow: "ON-BOARD INVENTORY",
        botiquin_tit: "MEDICAL KIT STOCK",
        botiquin_sub: "Supplies available for the mission medical protocol.",
        kit_none: "— None —",
        botiquin_vacio: "The medical kit reports no available supplies.",
        footer_1: "ASTRO-MED · NASA Space Apps · Flight CDSS",
        footer_2: "NASA HUMAN RESEARCH PROGRAM · STANDARD MEASURES",

        sin_lecturas: "No readings recorded for this crew member.",
        sin_lecturas_sub: "Log an EveryWear reading to run the first autonomous triage.",
        sin_resumen: "No clinical summary available.",
        sin_instruccion: "No corrective actions pending.",
        registrando: "LOGGING…",
        registro_ok: "Reading logged and triage executed.",
        simulando: "Injecting crisis scenario…",
        simulacion_ok: "Scenario executed",
        entorno_actualizado: "Operational environment: {entorno}",
        mision_ok: "Mission initialized successfully.",
        confirmar_mision: "This action resets the mission database with 105 records. Continue?",
        error_perfil: "No active crew profiles found.",
        error_api: "Could not reach the mission server.",
        error_generico: "Unexpected mission error.",
        bienvenida: "Welcome, {nombre}. HUD synchronized.",

        estados: { NOMINAL: "Nominal", PRECAUCION: "Caution", CRITICO: "Critical" },
        sistemas: {
            NEURO_PSICO: "Neuro-psychological",
            CARDIO_RAD: "Cardiovascular / radiation",
            METABOLICO_INMUNE: "Metabolic / immune",
            MUSCULO_ESQUELETICO: "Musculoskeletal",
            NINGUNO: "No affected system",
        },
        misiones: {
            ARTEMIS_LUNA: "Artemis · Moon",
            ARES_MARTE: "Ares · Mars",
            EUROPA_JUPITER: "Cryo-Europa · Europa",
        },
        valores: {
            sueno: "Sleep",
            animo: "Mood",
            pa: "Pressure",
            pam: "MAP",
            fc: "Pulse",
            rad: "Radiation",
            glu: "Glucose",
            temp: "Temperature",
            ejer: "ARED exercise",
            evid: "Evidence",
        },
        organos: {
            NEURO_PSICO: {
                titulo: "Neuro-psychological",
                peligros: "NASA Standard Measures: Pulsar Cognition (10 tests) + Actiwatch Spectrum Plus + Motion Sickness (0–20).",
                explicacion: "Evaluates visual learning, working memory, vigilant attention, and risk decision-making; combines EveryWear sleep/cohesion surveys with the post-Crew-8 motion sickness scale.",
            },
            CARDIO_RAD: {
                titulo: "Cardiovascular and radiation",
                peligros: "NASA Standard Measures: carotid ultrasound (intima-media) + cardiac analytes + 3.5-min stand test.",
                explicacion: "Monitors blood pressure and MAP, orthostatic response, and endothelial stress linked to cosmic or solar radiation.",
            },
            METABOLICO_INMUNE: {
                titulo: "Metabolic and immune",
                peligros: "NASA Standard Measures: biochemistry panel + innate/adaptive immunity (ACD/saliva tubes) + microbiome.",
                explicacion: "Tracks glucose, febrile response, and microbiome shifts inside closed habitats.",
            },
            MUSCULO_ESQUELETICO: {
                titulo: "Musculoskeletal",
                peligros: "NASA Standard Measures: isometric mid-thigh pull (IMTP) + sit-to-stand + tandem walk.",
                explicacion: "Assesses isometric strength, ARED resistive exercise minutes, and post-landing sensorimotor balance.",
            },
        },
    },
};

const MAPA_IDS = {
    "lbl-hero-badge": "hero_badge",
    "lbl-hero-titulo": "hero_titulo",
    "lbl-hero-sub": "hero_sub",
    "lbl-hero-stat1": "hero_stat1",
    "lbl-hero-stat2": "hero_stat2",
    "lbl-hero-stat3": "hero_stat3",
    "lbl-hero-pie": "hero_pie",
    "lbl-login-panel-eyebrow": "login_panel_eyebrow",
    "lbl-login-titulo": "login_titulo",
    "lbl-login-subtitulo": "login_subtitulo",
    "lbl-login-perfil": "login_perfil",
    "btn-login-entrar": "login_entrar",
    "lbl-acceso-rapido": "acceso_rapido",
    "lbl-login-seguridad": "login_seguridad",
    "lbl-sel-tripulante": "sel_tripulante",
    "lbl-sel-entorno": "sel_entorno",
    "lbl-racha-titulo": "racha_titulo",
    "btn-salir-hud": "btn_salir",
    "lbl-meta-entorno": "meta_entorno",
    "lbl-meta-lectura": "meta_lectura",
    "lbl-meta-mision": "meta_mision",
    "lbl-autonomia": "autonomia",
    "lbl-gemelo-titulo": "gemelo_titulo",
    "lbl-gemelo-inst": "gemelo_inst",
    "lbl-detalle-evidencia": "detalle_evidencia",
    "lbl-triage-eyebrow": "triage_eyebrow",
    "triage-titulo": "triage_titulo",
    "lbl-protocolo-guia": "protocolo_guia",
    "lbl-triage-sistema": "triage_sistema",
    "lbl-triage-nivel": "triage_nivel",
    "lbl-vitales-eyebrow": "vitales_eyebrow",
    "lbl-vitales-titulo": "vitales_titulo",
    "sub-fc": "sub_fc",
    "sub-glucosa": "sub_glu",
    "sub-temp": "sub_temp",
    "sub-sueno": "sub_sueno",
    "sub-ejercicio": "sub_ejer",
    "lbl-grafico-titulo": "grafico_titulo",
    "lbl-mision-activa-tit": "mision_tit",
    "lbl-mision-activa-sub": "mision_sub",
    "lbl-sim-peligros-tit": "sim_tit",
    "lbl-sim-peligros-sub": "sim_sub",
    "lbl-ssm-titulo": "ssm_eyebrow",
    "lbl-ssm-sub": "ssm_titulo",
    "lbl-ssm-neuro-tit": "ssm_neuro_tit",
    "lbl-ssm-neuro-sub": "ssm_neuro_sub",
    "lbl-ssm-sueno": "ssm_sueno",
    "lbl-ssm-animo": "ssm_animo",
    "lbl-ssm-cardio-tit": "ssm_cardio_tit",
    "lbl-ssm-cardio-sub": "ssm_cardio_sub",
    "lbl-ssm-pa": "ssm_pa",
    "lbl-ssm-fc": "ssm_fc",
    "lbl-ssm-rad": "ssm_rad",
    "lbl-ssm-metabolico-tit": "ssm_metabolico_tit",
    "lbl-ssm-metabolico-sub": "ssm_metabolico_sub",
    "lbl-ssm-glu": "ssm_glu",
    "lbl-ssm-temp": "ssm_temp",
    "lbl-ssm-musculo-tit": "ssm_musculo_tit",
    "lbl-ssm-musculo-sub": "ssm_musculo_sub",
    "lbl-ssm-ejer": "ssm_ejer",
    "lbl-ssm-evid": "ssm_evid",
    "lbl-form-tit": "form_tit",
    "lbl-form-sub": "form_sub",
    "lbl-form-hemo": "form_hemo",
    "lbl-in-sis": "in_sis",
    "lbl-in-dia": "in_dia",
    "lbl-in-fc": "in_fc",
    "lbl-form-meta": "form_meta",
    "lbl-in-glu": "in_glu",
    "lbl-in-temp": "in_temp",
    "lbl-form-estilo": "form_estilo",
    "lbl-in-sueno": "in_sueno",
    "lbl-in-animo": "in_animo",
    "lbl-in-ejer": "in_ejer",
    "lbl-in-rad": "in_rad",
    "lbl-form-registro": "form_registro",
    "lbl-in-evid": "in_evid",
    "lbl-in-insumo": "in_insumo",
    "btn-submit-tel": "btn_submit",
    "lbl-botiquin-tit": "botiquin_tit",
    "lbl-botiquin-sub": "botiquin_sub",
};

let idiomaActual = "es";
let sesionOperador = null;
let tripulantesCache = [];
let botiquinCache = [];
let analiticaActual = null;
let ultimaLecturaGlobal = null;
let ultimoDiagnosticoGlobal = null;
let sistemaSeleccionadoActual = "NEURO_PSICO";
let misionActual = "ARTEMIS_LUNA";
let apiDisponible = false;
let toastTimer = null;
let resizeTimer = null;

const ultimoDiagnosticoSistemas = {
    NEURO_PSICO: "NOMINAL",
    CARDIO_RAD: "NOMINAL",
    METABOLICO_INMUNE: "NOMINAL",
    MUSCULO_ESQUELETICO: "NOMINAL",
};

// ===================================================================================
//  ARRANQUE
// ===================================================================================

if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", iniciarApp);
} else {
    iniciarApp();
}

async function iniciarApp() {
    adjuntarEventos();
    const idioma = await cargarIdiomaRemoto();
    aplicarIdiomaLocal(idioma);
    await cargarTripulantesIniciales();
    verificarApi();
}

function adjuntarEventos() {
    const formLogin = document.getElementById("form-login");
    if (formLogin) {
        formLogin.addEventListener("submit", async (evento) => {
            evento.preventDefault();
            const usuario = document.getElementById("login-usuario").value.trim();
            await ejecutarIngresoHUD(usuario);
        });
    }

    const formTelemetria = document.getElementById("form-telemetria");
    if (formTelemetria) {
        formTelemetria.addEventListener("submit", registrarTelemetria);
    }

    window.addEventListener("resize", () => {
        clearTimeout(resizeTimer);
        resizeTimer = setTimeout(dibujarGraficoEvolucion, 160);
    });
}

// ===================================================================================
//  UTILIDADES
// ===================================================================================

function qs(id) {
    return document.getElementById(id);
}

function setTexto(id, texto) {
    const elemento = qs(id);
    if (elemento) elemento.textContent = texto;
}

function num(valor) {
    if (valor === null || valor === undefined || valor === "") return null;
    const numero = Number(valor);
    return Number.isFinite(numero) ? numero : null;
}

function fmt(valor, decimales = 1) {
    const numero = num(valor);
    if (numero === null) return "—";
    if (Number.isInteger(numero)) return String(numero);
    return numero.toFixed(decimales).replace(/0+$/, "").replace(/\.$/, "");
}

function normalizarEstado(estado) {
    const valor = String(estado || "").trim().toUpperCase();
    if (valor === "PRECAUCIÓN" || valor === "PRECAUCION") return "PRECAUCION";
    if (valor === "CRÍTICO" || valor === "CRITICO") return "CRITICO";
    return "NOMINAL";
}

function claseEstado(estado) {
    return normalizarEstado(estado).toLowerCase();
}

function nombreEstado(estado) {
    return I18N_WEB[idiomaActual].estados[normalizarEstado(estado)];
}

function nombreSistema(codigo) {
    return I18N_WEB[idiomaActual].sistemas[codigo] || codigo;
}

function nombreEntorno(valor) {
    const info = ENTORNOS[valor];
    return info ? info[idiomaActual] : (valor || "—");
}

function entornoCanonico(valor) {
    const buscado = String(valor || "").trim().toUpperCase();
    return Object.keys(ENTORNOS).find((clave) => clave.toUpperCase() === buscado) || "Transito Espacial (0G)";
}

function iniciales(nombres, apellidos) {
    const nombre = String(nombres || "").trim();
    const apellido = String(apellidos || "").trim();
    const letras = `${nombre.charAt(0)}${apellido.charAt(0)}`.toUpperCase();
    return letras || "--";
}

function formatearFecha(fecha) {
    if (!fecha) return "—";
    const texto = String(fecha).replace("T", " ").trim();
    return texto.length >= 16 ? texto.slice(0, 16) : texto;
}

function formatearFechaCorta(fecha) {
    const coincidencia = String(fecha || "").match(/(\d{4})-(\d{2})-(\d{2})/);
    return coincidencia ? `${coincidencia[2]}-${coincidencia[3]}` : "";
}

function posicion(valor, minimo, maximo) {
    const numero = num(valor);
    if (numero === null || maximo === minimo) return 50;
    const porcentaje = ((numero - minimo) / (maximo - minimo)) * 100;
    return Math.max(2, Math.min(98, porcentaje));
}

function mostrarToast(mensaje, tipo = "info") {
    const toast = qs("toast");
    if (!toast) return;
    toast.textContent = mensaje;
    toast.className = `toast visible ${tipo}`;
    clearTimeout(toastTimer);
    toastTimer = setTimeout(() => {
        toast.className = "toast";
    }, 4400);
}

function pintarEstadoApi(ok) {
    const elemento = qs("login-api-estado");
    if (!elemento) return;
    const d = I18N_WEB[idiomaActual];
    elemento.textContent = `● ${ok ? d.login_api_ok : d.login_api_error}`;
    elemento.className = `api-status ${ok ? "ok" : "error"}`;
}

// ===================================================================================
//  IDIOMA
// ===================================================================================

async function cargarIdiomaRemoto() {
    try {
        const respuesta = await fetch(`${API_BASE}/idioma`);
        if (respuesta.ok) {
            const datos = await respuesta.json();
            return datos.idioma === "en" ? "en" : "es";
        }
    } catch (error) {
        // El HUD sigue operativo en español si la API aún no responde.
    }
    return "es";
}

async function cambiarIdiomaHUD(nuevoIdioma) {
    aplicarIdiomaLocal(nuevoIdioma);
    try {
        await fetch(`${API_BASE}/idioma`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ idioma: idiomaActual }),
        });
    } catch (error) {
        // La preferencia local ya quedó aplicada.
    }
}

function aplicarIdiomaLocal(codigo) {
    idiomaActual = codigo === "en" ? "en" : "es";
    const d = I18N_WEB[idiomaActual];

    document.documentElement.lang = idiomaActual;
    const selectorLogin = qs("select-idioma-login");
    const selectorHud = qs("select-idioma-hud");
    if (selectorLogin) selectorLogin.value = idiomaActual;
    if (selectorHud) selectorHud.value = idiomaActual;

    Object.entries(MAPA_IDS).forEach(([id, clave]) => {
        const elemento = qs(id);
        if (elemento && d[clave] !== undefined) elemento.textContent = d[clave];
    });

    document.querySelectorAll("[data-i18n]").forEach((elemento) => {
        const clave = elemento.getAttribute("data-i18n");
        if (clave && d[clave] !== undefined) elemento.textContent = d[clave];
    });

    actualizarOpcionesEntorno();
    reconstruirEstudios();
    poblarSelectorLogin();
    actualizarOperadorLabel();
    actualizarTitulosTripulantes();

    const selectorTripulante = qs("select-tripulante");
    const tripulanteVisible = tripulantesCache.find(
        (tripulante) => String(tripulante.id) === String(selectorTripulante ? selectorTripulante.value : "")
    );
    if (sesionOperador && tripulanteVisible) {
        actualizarIdentidadCrew(tripulanteVisible);
    }

    const racha = qs("lbl-racha");
    if (racha && sesionOperador) {
        racha.textContent = `${sesionOperador.racha_autocuidado ?? 0} ${d.dias_sol}`;
    }

    pintarEstadoApi(apiDisponible);
    actualizarBotonMision(misionActual);

    if (ultimaLecturaGlobal) {
        renderizarUltimaLectura(ultimaLecturaGlobal, ultimoDiagnosticoGlobal, false);
    } else {
        seleccionarSistema(sistemaSeleccionadoActual);
    }

    dibujarGraficoEvolucion();
}

function actualizarOpcionesEntorno() {
    const selector = qs("select-entorno");
    if (!selector) return;
    Array.from(selector.options).forEach((opcion) => {
        const info = ENTORNOS[opcion.value];
        if (info) opcion.textContent = info[idiomaActual];
    });
}

function reconstruirEstudios() {
    const selector = qs("in-evidencia");
    if (!selector) return;
    const seleccionPrevia = selector.value;
    selector.innerHTML = "";
    ESTUDIOS.forEach((estudio) => {
        const opcion = document.createElement("option");
        opcion.value = estudio.valor;
        opcion.textContent = estudio[idiomaActual];
        selector.appendChild(opcion);
    });
    if (ESTUDIOS.some((estudio) => estudio.valor === seleccionPrevia)) {
        selector.value = seleccionPrevia;
    }
}

// ===================================================================================
//  CARGA INICIAL Y LOGIN
// ===================================================================================

async function cargarTripulantesIniciales() {
    try {
        const respuesta = await fetch(`${API_BASE}/tripulantes`);
        if (!respuesta.ok) return;
        const datos = await respuesta.json();
        if (Array.isArray(datos) && datos.length > 0) {
            tripulantesCache = datos;
            poblarSelectorLogin();
        }
    } catch (error) {
        // El formulario conserva sus opciones estáticas hasta que la API responda.
    }
}

function poblarSelectorLogin() {
    if (!tripulantesCache.length) return;
    const selector = qs("login-usuario");
    if (!selector) return;
    const seleccionPrevia = selector.value;
    selector.innerHTML = "";
    tripulantesCache.forEach((tripulante) => {
        const opcion = document.createElement("option");
        opcion.value = tripulante.usuario;
        opcion.textContent = `${tripulante.codigo_astronauta} — ${tripulante.nombres} ${tripulante.apellidos} (${localizarRol(tripulante.rol)})`;
        selector.appendChild(opcion);
    });
    if (Array.from(selector.options).some((opcion) => opcion.value === seleccionPrevia)) {
        selector.value = seleccionPrevia;
    }
}

async function verificarApi() {
    const controlador = new AbortController();
    const temporizador = setTimeout(() => controlador.abort(), 5000);
    try {
        const respuesta = await fetch(`${API_BASE}/tripulantes`, { signal: controlador.signal });
        apiDisponible = respuesta.ok;
        if (respuesta.ok) {
            const datos = await respuesta.json();
            if (Array.isArray(datos) && datos.length > 0) {
                tripulantesCache = datos;
                poblarSelectorLogin();
            }
        }
    } catch (error) {
        apiDisponible = false;
    } finally {
        clearTimeout(temporizador);
        pintarEstadoApi(apiDisponible);
    }
}

async function ingresoDirecto(usuarioSeleccionado) {
    const selector = qs("login-usuario");
    if (selector) selector.value = usuarioSeleccionado;
    await ejecutarIngresoHUD(usuarioSeleccionado);
}

async function ejecutarIngresoHUD(usuario) {
    const errorLogin = qs("login-error");
    const boton = qs("btn-login-entrar");
    const d = I18N_WEB[idiomaActual];
    if (errorLogin) errorLogin.textContent = "";
    if (boton) boton.disabled = true;

    try {
        if (!tripulantesCache.length) {
            const respuesta = await fetch(`${API_BASE}/tripulantes`);
            if (!respuesta.ok) throw new Error(d.error_api);
            const datos = await respuesta.json();
            if (Array.isArray(datos)) tripulantesCache = datos;
        }

        const perfil = tripulantesCache.find((tripulante) => tripulante.usuario === usuario) ||
            tripulantesCache.find((tripulante) => String(tripulante.id) === String(usuario)) ||
            (tripulantesCache.length === 1 ? tripulantesCache[0] : null);

        if (!perfil) throw new Error(d.error_perfil);

        sesionOperador = perfil;
        apiDisponible = true;
        pintarEstadoApi(true);

        const vistaLogin = qs("vista-login");
        const vistaHud = qs("vista-hud");
        if (vistaLogin) vistaLogin.classList.add("oculto");
        if (vistaHud) vistaHud.classList.remove("oculto");
        window.scrollTo(0, 0);

        actualizarOperadorLabel();
        await inicializarDatosHUD();
        requestAnimationFrame(dibujarGraficoEvolucion);
        mostrarToast(d.bienvenida.replace("{nombre}", perfil.nombres), "ok");
    } catch (error) {
        if (errorLogin) errorLogin.textContent = error.message || d.error_generico;
        const vistaLogin = qs("vista-login");
        const vistaHud = qs("vista-hud");
        if (vistaLogin) vistaLogin.classList.remove("oculto");
        if (vistaHud) vistaHud.classList.add("oculto");
    } finally {
        if (boton) boton.disabled = false;
    }
}

function actualizarOperadorLabel() {
    const elemento = qs("lbl-operador");
    if (!elemento) return;
    if (sesionOperador) {
        elemento.textContent = `${sesionOperador.nombres} ${sesionOperador.apellidos} · ${localizarRol(sesionOperador.rol)}`;
    } else {
        elemento.textContent = "—";
    }
}

function cerrarSesion() {
    sesionOperador = null;
    ultimaLecturaGlobal = null;
    ultimoDiagnosticoGlobal = null;
    analiticaActual = null;

    const vistaHud = qs("vista-hud");
    const vistaLogin = qs("vista-login");
    if (vistaHud) vistaHud.classList.add("oculto");
    if (vistaLogin) vistaLogin.classList.remove("oculto");

    const errorLogin = qs("login-error");
    if (errorLogin) errorLogin.textContent = "";
    const selector = qs("login-usuario");
    if (selector) selector.focus();
    window.scrollTo(0, 0);
}

// ===================================================================================
//  DATOS DE MISIÓN
// ===================================================================================

async function inicializarDatosHUD() {
    try {
        await cargarTripulantes();
    } catch (error) {
        mostrarToast(error.message || I18N_WEB[idiomaActual].error_api, "error");
    }

    try {
        await cargarBotiquin();
    } catch (error) {
        mostrarToast(error.message || I18N_WEB[idiomaActual].error_api, "error");
    }

    const selector = qs("select-tripulante");
    if (selector) {
        if (sesionOperador && tripulantesCache.some((tripulante) => tripulante.id === sesionOperador.id)) {
            selector.value = String(sesionOperador.id);
        } else if (tripulantesCache.length > 0) {
            selector.value = String(tripulantesCache[0].id);
        }
    }

    actualizarBotonMision(misionActual);
    await cambiarTripulanteActivo(true);
}

async function cargarTripulantes() {
    const respuesta = await fetch(`${API_BASE}/tripulantes`);
    if (!respuesta.ok) throw new Error(I18N_WEB[idiomaActual].error_api);
    const datos = await respuesta.json();
    if (!Array.isArray(datos)) throw new Error(I18N_WEB[idiomaActual].error_generico);
    tripulantesCache = datos;

    if (sesionOperador) {
        const actualizado = tripulantesCache.find((tripulante) => tripulante.usuario === sesionOperador.usuario) ||
            tripulantesCache.find((tripulante) => tripulante.codigo_astronauta === sesionOperador.codigo_astronauta);
        if (actualizado) {
            sesionOperador = actualizado;
            actualizarOperadorLabel();
        }
    }

    const selector = qs("select-tripulante");
    if (!selector) return;
    const seleccionPrevia = selector.value;
    selector.innerHTML = "";
    tripulantesCache.forEach((tripulante) => {
        const opcion = document.createElement("option");
        opcion.value = tripulante.id;
        opcion.textContent = `${tripulante.codigo_astronauta} — ${tripulante.nombres} ${tripulante.apellidos}`;
        opcion.title = tituloTripulante(tripulante);
        selector.appendChild(opcion);
    });
    if (seleccionPrevia && tripulantesCache.some((tripulante) => String(tripulante.id) === String(seleccionPrevia))) {
        selector.value = seleccionPrevia;
    }
}

function actualizarTitulosTripulantes() {
    const selector = qs("select-tripulante");
    if (!selector) return;
    Array.from(selector.options).forEach((opcion) => {
        const tripulante = tripulantesCache.find(
            (item) => String(item.id) === String(opcion.value)
        );
        if (tripulante) opcion.title = tituloTripulante(tripulante);
    });
}

async function cargarBotiquin() {
    const d = I18N_WEB[idiomaActual];
    const respuesta = await fetch(`${API_BASE}/botiquin`);
    if (!respuesta.ok) throw new Error(d.error_api);
    const datos = await respuesta.json();
    if (!Array.isArray(datos)) throw new Error(d.error_generico);
    botiquinCache = datos;

    const selector = qs("in-insumo");
    if (selector) {
        const seleccionPrevia = selector.value;
        selector.innerHTML = "";
        const ninguna = document.createElement("option");
        ninguna.value = "";
        ninguna.textContent = d.kit_none;
        selector.appendChild(ninguna);
        botiquinCache.forEach((insumo) => {
            const opcion = document.createElement("option");
            opcion.value = insumo.id;
            opcion.textContent = `${insumo.codigo} — ${insumo.nombre} (${fmt(insumo.stock_actual, 1)} ${insumo.unidad_medida})`;
            selector.appendChild(opcion);
        });
        if (seleccionPrevia && botiquinCache.some((insumo) => String(insumo.id) === String(seleccionPrevia))) {
            selector.value = seleccionPrevia;
        }
    }

    const lista = qs("lista-botiquin");
    if (!lista) return;
    lista.innerHTML = "";
    if (!botiquinCache.length) {
        const vacio = document.createElement("li");
        vacio.className = "kit-empty";
        vacio.textContent = d.botiquin_vacio;
        lista.appendChild(vacio);
        return;
    }

    botiquinCache.forEach((insumo) => {
        const item = document.createElement("li");
        const bajo = num(insumo.stock_actual) !== null && num(insumo.stock_minimo) !== null &&
            Number(insumo.stock_actual) <= Number(insumo.stock_minimo);
        item.className = `kit-item${bajo ? " bajo" : ""}`;
        item.title = [insumo.modulo_ubicacion, insumo.instrucciones_uso].filter(Boolean).join(" · ");

        const principal = document.createElement("div");
        principal.className = "kit-item-main";
        const codigo = document.createElement("strong");
        codigo.textContent = insumo.codigo;
        const nombre = document.createElement("span");
        nombre.textContent = insumo.nombre;
        principal.append(codigo, nombre);

        const stock = document.createElement("div");
        stock.className = "kit-stock";
        const cantidad = document.createElement("b");
        cantidad.textContent = fmt(insumo.stock_actual, 1);
        const unidad = document.createElement("small");
        unidad.textContent = insumo.unidad_medida;
        stock.append(cantidad, unidad);

        item.append(principal, stock);
        lista.appendChild(item);
    });
}

async function cambiarTripulanteActivo(autoSeleccionar = true) {
    const selector = qs("select-tripulante");
    if (!selector) return;
    const idTripulante = parseInt(selector.value, 10);
    if (!Number.isFinite(idTripulante)) return;

    const tripulante = tripulantesCache.find((item) => item.id === idTripulante);
    const d = I18N_WEB[idiomaActual];

    if (tripulante) {
        actualizarIdentidadCrew(tripulante);
        setTexto("lbl-racha", `${tripulante.racha_autocuidado ?? 0} ${d.dias_sol}`);
    }

    let historial = [];
    try {
        const [respuestaHistorial, respuestaAnalitica] = await Promise.all([
            fetch(`${API_BASE}/telemetria/tripulante/${idTripulante}?limite=15`),
            fetch(`${API_BASE}/analitica/${idTripulante}`),
        ]);

        if (respuestaHistorial.ok) {
            const datos = await respuestaHistorial.json();
            if (Array.isArray(datos)) historial = datos;
        }
        if (respuestaAnalitica.ok) {
            analiticaActual = await respuestaAnalitica.json();
        }
    } catch (error) {
        mostrarToast(d.error_api, "error");
    }

    if (historial.length > 0) {
        renderizarUltimaLectura(historial[0], null, autoSeleccionar);
    } else {
        limpiarLectura();
    }

    dibujarGraficoEvolucion();
}

function actualizarIdentidadCrew(tripulante) {
    const d = I18N_WEB[idiomaActual];
    setTexto("crew-avatar", iniciales(tripulante.nombres, tripulante.apellidos));
    setTexto("crew-nombre", `${tripulante.nombres} ${tripulante.apellidos}`);
    const rol = [localizarRol(tripulante.rol), localizarEspecialidad(tripulante.especialidad)].filter(Boolean).join(" · ");
    setTexto("lbl-crew-rol", rol || d.crew_rol);
}

async function recargarAnalitica(idTripulante) {
    try {
        const respuesta = await fetch(`${API_BASE}/analitica/${idTripulante}`);
        if (respuesta.ok) analiticaActual = await respuesta.json();
    } catch (error) {
        // El gráfico conserva los datos previos disponibles.
    }
    dibujarGraficoEvolucion();
}

// ===================================================================================
//  RENDERIZADO CLÍNICO
// ===================================================================================

function renderizarUltimaLectura(lectura, diagnostico = null, autoSeleccionar = false) {
    if (!lectura) return;
    ultimaLecturaGlobal = lectura;
    ultimoDiagnosticoGlobal = diagnostico;
    const d = I18N_WEB[idiomaActual];

    const estadoGlobal = normalizarEstado(
        diagnostico && diagnostico.nivel_alerta_global ? diagnostico.nivel_alerta_global : lectura.nivel_alerta
    );
    const sistemaPrincipal = (diagnostico && diagnostico.sistema_afectado_principal) ||
        lectura.sistema_afectado || "NINGUNO";

    aplicarEstadosSistemas(lectura, diagnostico);
    pintarBadgeGlobal(estadoGlobal);
    renderizarTriage(lectura, diagnostico, estadoGlobal, sistemaPrincipal);
    actualizarGauges(lectura);
    actualizarTarjetasSSM(lectura);

    if (lectura.entorno) {
        const entornoLectura = entornoCanonico(lectura.entorno);
        const selectorEntorno = qs("select-entorno");
        if (selectorEntorno) selectorEntorno.value = entornoLectura;
        actualizarOpcionesEntorno();
        setTexto("meta-entorno", nombreEntorno(entornoLectura));
    }
    setTexto("meta-lectura", formatearFecha(lectura.fecha));

    if (autoSeleccionar && SISTEMAS.includes(sistemaPrincipal)) {
        sistemaSeleccionadoActual = sistemaPrincipal;
    }
    if (autoSeleccionar && !SISTEMAS.includes(sistemaSeleccionadoActual)) {
        sistemaSeleccionadoActual = "NEURO_PSICO";
    }
    seleccionarSistema(sistemaSeleccionadoActual);
}

function aplicarEstadosSistemas(lectura, diagnostico) {
    const explicitos = diagnostico && diagnostico.estado_sistemas &&
        Object.keys(diagnostico.estado_sistemas).length > 0
        ? diagnostico.estado_sistemas
        : null;

    SISTEMAS.forEach((sistema) => {
        let estado = "NOMINAL";
        if (explicitos && explicitos[sistema]) {
            estado = normalizarEstado(explicitos[sistema]);
        } else if (lectura.sistema_afectado === sistema) {
            estado = normalizarEstado(lectura.nivel_alerta);
        }
        ultimoDiagnosticoSistemas[sistema] = estado;

        const zona = qs(`zona-${sistema}`);
        if (zona) {
            zona.setAttribute(
                "class",
                `zona-sistema ${claseEstado(estado)}${sistema === sistemaSeleccionadoActual ? " zona-activa" : ""}`
            );
        }

        const pildora = qs(`estado-${sistema}`);
        if (pildora) {
            pildora.textContent = nombreEstado(estado);
            pildora.className = `mini-pill ${claseEstado(estado)}`;
        }

        const tarjeta = document.querySelector(`.measure-item[data-system="${sistema}"]`);
        if (tarjeta) tarjeta.className = `measure-item ${claseEstado(estado)}`;
    });
}

function pintarBadgeGlobal(estado) {
    const badge = qs("badge-global");
    if (!badge) return;
    badge.textContent = nombreEstado(estado);
    badge.className = `status-pill ${claseEstado(estado)}`;
}

function renderizarTriage(lectura, diagnostico, estadoGlobal, sistemaPrincipal) {
    const d = I18N_WEB[idiomaActual];
    const panel = qs("panel-protocolo");
    if (panel) panel.className = `triage-panel ${claseEstado(estadoGlobal)}`;

    const resumen = (diagnostico && diagnostico.resumen_clinico) ||
        lectura.diagnostico_resumen || d.sin_resumen;
    const instruccion = (diagnostico && diagnostico.instruccion_paso_a_paso) ||
        lectura.instruccion_accion || d.sin_instruccion;

    setTexto("triage-resumen", resumen);
    setTexto("triage-instruccion", instruccion);
    setTexto("triage-sistema", nombreSistema(sistemaPrincipal));
    setTexto("triage-nivel", nombreEstado(estadoGlobal));

    const requiereTierra = diagnostico
        ? Boolean(diagnostico.requiere_atencion_tierra) || estadoGlobal === "CRITICO"
        : estadoGlobal === "CRITICO";
    const etiqueta = qs("triage-tierra");
    if (etiqueta) {
        etiqueta.textContent = requiereTierra ? d.tierra_critico : d.tierra_ok;
        etiqueta.className = `tag-tierra${requiereTierra ? " alerta" : ""}`;
    }
}

function actualizarGauges(lectura) {
    const sistolica = num(lectura.presion_sistolica);
    const diastolica = num(lectura.presion_diastolica);
    const pam = num(lectura.presion_media);
    const d = I18N_WEB[idiomaActual];

    setTexto(
        "kpi-presion",
        sistolica === null || diastolica === null ? "-- / --" : `${fmt(sistolica, 0)} / ${fmt(diastolica, 0)}`
    );
    setTexto("sub-pa", d.sub_pa.replace("{pam}", pam === null ? "—" : fmt(pam, 1)));
    setTexto("kpi-fc", fmt(lectura.frecuencia_cardiaca, 0));
    setTexto("kpi-glucosa", fmt(lectura.glucosa_mg_dl, 1));
    setTexto("kpi-temp", fmt(lectura.temperatura_c, 1));
    setTexto("kpi-sueno", fmt(lectura.horas_sueno, 1));
    setTexto("kpi-ejercicio", fmt(lectura.minutos_ejercicio, 0));

    pintarGauge("gauge-pa", "CARDIO_RAD", sistolica, 50, 210);
    pintarGauge("gauge-fc", "CARDIO_RAD", num(lectura.frecuencia_cardiaca), 30, 170);
    pintarGauge("gauge-glucosa", "METABOLICO_INMUNE", num(lectura.glucosa_mg_dl), 40, 300);
    pintarGauge("gauge-temp", "METABOLICO_INMUNE", num(lectura.temperatura_c), 34, 41);
    pintarGauge("gauge-sueno", "NEURO_PSICO", num(lectura.horas_sueno), 0, 12);
    pintarGauge("gauge-ejercicio", "MUSCULO_ESQUELETICO", num(lectura.minutos_ejercicio), 0, 120);
}

function pintarGauge(idTarjeta, sistema, valor, minimo, maximo) {
    const tarjeta = qs(idTarjeta);
    if (!tarjeta) return;
    const estado = ultimoDiagnosticoSistemas[sistema] || "NOMINAL";
    tarjeta.className = `ruler-card ${claseEstado(estado)}`;
    const pista = tarjeta.querySelector(".ruler-track");
    if (pista) pista.style.setProperty("--pct", `${posicion(valor, minimo, maximo)}%`);
}

function actualizarTarjetasSSM(lectura) {
    const sistolica = num(lectura.presion_sistolica);
    const diastolica = num(lectura.presion_diastolica);
    const evidencia = lectura.evidencia_adjunta || "—";

    setTexto("ssm-sueno", `${fmt(lectura.horas_sueno, 1)} h`);
    setTexto("ssm-animo", `${fmt(lectura.estado_animo, 0)} / 5`);
    setTexto(
        "ssm-pa",
        sistolica === null || diastolica === null ? "-- / --" : `${fmt(sistolica, 0)} / ${fmt(diastolica, 0)}`
    );
    setTexto("ssm-fc", fmt(lectura.frecuencia_cardiaca, 0));
    setTexto("ssm-rad", fmt(lectura.radiacion_msv, 2));
    setTexto("ssm-glu", fmt(lectura.glucosa_mg_dl, 1));
    setTexto("ssm-temp", fmt(lectura.temperatura_c, 1));
    setTexto("ssm-ejer", fmt(lectura.minutos_ejercicio, 0));

    ["ssm-evid-neuro", "ssm-evid-cardio", "ssm-evid-metabolico", "ssm-evid-musculo"].forEach((id) => {
        setTexto(id, evidencia);
        const elemento = qs(id);
        if (elemento) elemento.title = evidencia === "—" ? "" : evidencia;
    });
}

function seleccionarSistema(codigoSistema) {
    if (!SISTEMAS.includes(codigoSistema)) return;
    sistemaSeleccionadoActual = codigoSistema;
    const d = I18N_WEB[idiomaActual];
    const info = d.organos[codigoSistema];
    if (!info) return;

    SISTEMAS.forEach((sistema) => {
        const zona = qs(`zona-${sistema}`);
        if (zona) zona.classList.toggle("zona-activa", sistema === codigoSistema);
    });

    const estado = ultimoDiagnosticoSistemas[codigoSistema] || "NOMINAL";
    const pildora = qs("estado-organo");
    if (pildora) {
        pildora.textContent = nombreEstado(estado);
        pildora.className = `mini-pill ${claseEstado(estado)}`;
    }

    setTexto("titulo-organo", info.titulo);

    let descripcion = `<strong>${info.peligros}</strong><br>${info.explicacion}`;
    if (ultimaLecturaGlobal &&
        ultimaLecturaGlobal.sistema_afectado === codigoSistema &&
        normalizarEstado(ultimaLecturaGlobal.nivel_alerta) !== "NOMINAL" &&
        ultimaLecturaGlobal.diagnostico_resumen) {
        descripcion += `<br><span class="detalle-backend">⚠ ${escaparHtml(ultimaLecturaGlobal.diagnostico_resumen)}</span>`;
    }
    const descripcionElemento = qs("desc-organo");
    if (descripcionElemento) descripcionElemento.innerHTML = descripcion;

    const contenedor = qs("detalle-valores");
    if (contenedor) {
        contenedor.innerHTML = "";
        const valores = valoresDelSistema(codigoSistema);
        if (!valores.length) {
            const vacio = document.createElement("div");
            vacio.className = "detalle-vacio";
            vacio.textContent = d.sin_lecturas;
            contenedor.appendChild(vacio);
        } else {
            valores.forEach((valor) => {
                const celda = document.createElement("div");
                const etiqueta = document.createElement("span");
                etiqueta.textContent = valor.etiqueta;
                const dato = document.createElement("strong");
                dato.textContent = valor.dato;
                celda.append(etiqueta, dato);
                contenedor.appendChild(celda);
            });
        }
    }

    setTexto("detalle-evidencia", ultimaLecturaGlobal ? (ultimaLecturaGlobal.evidencia_adjunta || "—") : "—");
    const detalleEvidencia = qs("detalle-evidencia");
    if (detalleEvidencia) {
        detalleEvidencia.title = ultimaLecturaGlobal ? (ultimaLecturaGlobal.evidencia_adjunta || "") : "";
    }
}

function valoresDelSistema(codigoSistema) {
    const lectura = ultimaLecturaGlobal;
    if (!lectura) return [];
    const d = I18N_WEB[idiomaActual];

    switch (codigoSistema) {
        case "NEURO_PSICO":
            return [
                { etiqueta: d.valores.sueno, dato: `${fmt(lectura.horas_sueno, 1)} h` },
                { etiqueta: d.valores.animo, dato: `${fmt(lectura.estado_animo, 0)} / 5` },
            ];
        case "CARDIO_RAD":
            return [
                {
                    etiqueta: d.valores.pa,
                    dato: `${fmt(lectura.presion_sistolica, 0)} / ${fmt(lectura.presion_diastolica, 0)}`,
                },
                { etiqueta: d.valores.pam, dato: `${fmt(lectura.presion_media, 1)} mmHg` },
                { etiqueta: d.valores.fc, dato: `${fmt(lectura.frecuencia_cardiaca, 0)} lpm` },
                { etiqueta: d.valores.rad, dato: `${fmt(lectura.radiacion_msv, 2)} mSv` },
            ];
        case "METABOLICO_INMUNE":
            return [
                { etiqueta: d.valores.glu, dato: `${fmt(lectura.glucosa_mg_dl, 1)} mg/dL` },
                { etiqueta: d.valores.temp, dato: `${fmt(lectura.temperatura_c, 1)} °C` },
            ];
        case "MUSCULO_ESQUELETICO":
            return [
                { etiqueta: d.valores.ejer, dato: `${fmt(lectura.minutos_ejercicio, 0)} min` },
                { etiqueta: d.valores.evid, dato: lectura.evidencia_adjunta || "—" },
            ];
        default:
            return [];
    }
}

function escaparHtml(texto) {
    return String(texto ?? "").replace(/[&<>"']/g, (caracter) => {
        const mapa = { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" };
        return mapa[caracter];
    });
}

function limpiarLectura() {
    ultimaLecturaGlobal = null;
    ultimoDiagnosticoGlobal = null;
    const d = I18N_WEB[idiomaActual];

    [
        "kpi-presion", "kpi-fc", "kpi-glucosa", "kpi-temp", "kpi-sueno", "kpi-ejercicio",
        "ssm-sueno", "ssm-animo", "ssm-pa", "ssm-fc", "ssm-rad", "ssm-glu", "ssm-temp", "ssm-ejer",
        "ssm-evid-neuro", "ssm-evid-cardio", "ssm-evid-metabolico", "ssm-evid-musculo",
        "meta-lectura", "detalle-evidencia", "triage-sistema", "triage-nivel",
    ].forEach((id) => setTexto(id, "—"));

    ["ssm-evid-neuro", "ssm-evid-cardio", "ssm-evid-metabolico", "ssm-evid-musculo", "detalle-evidencia"]
        .forEach((id) => {
            const elemento = qs(id);
            if (elemento) elemento.title = "";
        });

    setTexto("sub-pa", d.sub_pa.replace("{pam}", "—"));
    setTexto("meta-entorno", nombreEntorno(qs("select-entorno") ? qs("select-entorno").value : ""));

    SISTEMAS.forEach((sistema) => {
        ultimoDiagnosticoSistemas[sistema] = "NOMINAL";
        const zona = qs(`zona-${sistema}`);
        if (zona) {
            zona.setAttribute(
                "class",
                `zona-sistema nominal${sistema === sistemaSeleccionadoActual ? " zona-activa" : ""}`
            );
        }
        const pildora = qs(`estado-${sistema}`);
        if (pildora) {
            pildora.textContent = nombreEstado("NOMINAL");
            pildora.className = "mini-pill nominal";
        }
        const tarjeta = document.querySelector(`.measure-item[data-system="${sistema}"]`);
        if (tarjeta) tarjeta.className = "measure-item nominal";
    });

    ["gauge-pa", "gauge-fc", "gauge-glucosa", "gauge-temp", "gauge-sueno", "gauge-ejercicio"].forEach((id) => {
        const tarjeta = qs(id);
        if (!tarjeta) return;
        tarjeta.className = "ruler-card nominal";
        const pista = tarjeta.querySelector(".ruler-track");
        if (pista) pista.style.setProperty("--pct", "50%");
    });

    const badge = qs("badge-global");
    if (badge) {
        badge.textContent = nombreEstado("NOMINAL");
        badge.className = "status-pill nominal";
    }

    const panel = qs("panel-protocolo");
    if (panel) panel.className = "triage-panel nominal";
    setTexto("triage-resumen", d.sin_lecturas);
    setTexto("triage-instruccion", d.sin_lecturas_sub);
    setTexto("triage-sistema", "—");

    const etiqueta = qs("triage-tierra");
    if (etiqueta) {
        etiqueta.textContent = d.tierra_ok;
        etiqueta.className = "tag-tierra";
    }

    seleccionarSistema(sistemaSeleccionadoActual);
}

// ===================================================================================
//  OPERACIONES
// ===================================================================================

function actualizarInfoEntorno() {
    const selector = qs("select-entorno");
    if (!selector) return;
    const entorno = selector.value;
    setTexto("meta-entorno", nombreEntorno(entorno));
    mostrarToast(I18N_WEB[idiomaActual].entorno_actualizado.replace("{entorno}", nombreEntorno(entorno)), "info");
    seleccionarSistema(sistemaSeleccionadoActual);
}

async function cambiarMision(codigoMision) {
    const d = I18N_WEB[idiomaActual];
    if (!window.confirm(d.confirmar_mision)) return;

    const botones = document.querySelectorAll(".mission-btn");
    botones.forEach((boton) => {
        boton.disabled = true;
    });

    try {
        const respuesta = await fetch(`${API_BASE}/telemetria/cargar-mision`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ mision: codigoMision }),
        });
        const datos = await respuesta.json().catch(() => ({}));
        if (!respuesta.ok) throw new Error(datos.detalle || datos.detail || d.error_generico);

        misionActual = codigoMision;
        actualizarBotonMision(codigoMision);
        await inicializarDatosHUD();
        mostrarToast(datos.mensaje || d.mision_ok, "ok");
    } catch (error) {
        mostrarToast(error.message || d.error_generico, "error");
    } finally {
        botones.forEach((boton) => {
            boton.disabled = false;
        });
    }
}

function actualizarBotonMision(codigoMision) {
    const mapa = {
        ARTEMIS_LUNA: "btn-mision-luna",
        ARES_MARTE: "btn-mision-marte",
        EUROPA_JUPITER: "btn-mision-europa",
    };
    document.querySelectorAll(".mission-btn").forEach((boton) => {
        boton.classList.remove("activa");
    });
    const activo = qs(mapa[codigoMision]);
    if (activo) activo.classList.add("activa");

    const d = I18N_WEB[idiomaActual];
    setTexto("meta-mision", d.misiones[codigoMision] || codigoMision);
}

async function simularCrisis(escenario) {
    const selector = qs("select-tripulante");
    if (!selector) return;
    const idTripulante = parseInt(selector.value, 10);
    if (!Number.isFinite(idTripulante)) return;

    const d = I18N_WEB[idiomaActual];
    const botones = document.querySelectorAll(".hazard-btn");
    botones.forEach((boton) => {
        boton.disabled = true;
    });
    mostrarToast(d.simulando, "warn");

    try {
        const respuesta = await fetch(`${API_BASE}/telemetria/simular-crisis`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "X-Operador-Id": sesionOperador ? String(sesionOperador.id) : "1",
            },
            body: JSON.stringify({ id_tripulante: idTripulante, escenario }),
        });
        const datos = await respuesta.json().catch(() => ({}));
        if (!respuesta.ok) throw new Error(datos.detalle || datos.detail || d.error_generico);

        actualizarRacha(datos.racha_actualizada, idTripulante);
        renderizarUltimaLectura(datos.lectura, datos.diagnostico, true);
        await recargarAnalitica(idTripulante);

        const nivel = datos.diagnostico ? normalizarEstado(datos.diagnostico.nivel_alerta_global) : "NOMINAL";
        mostrarToast(`${d.simulacion_ok} · ${nombreEstado(nivel)}`, nivel === "CRITICO" ? "error" : "warn");
    } catch (error) {
        mostrarToast(error.message || d.error_generico, "error");
    } finally {
        botones.forEach((boton) => {
            boton.disabled = false;
        });
    }
}

function actualizarRacha(nuevaRacha, idTripulante) {
    const d = I18N_WEB[idiomaActual];
    const tripulante = tripulantesCache.find((item) => item.id === idTripulante);
    if (tripulante) tripulante.racha_autocuidado = nuevaRacha;
    if (sesionOperador && sesionOperador.id === idTripulante) sesionOperador.racha_autocuidado = nuevaRacha;
    setTexto("lbl-racha", `${nuevaRacha ?? 0} ${d.dias_sol}`);
}

// ===================================================================================
//  REGISTRO EVERYWEAR
// ===================================================================================

async function registrarTelemetria(evento) {
    evento.preventDefault();
    const formulario = qs("form-telemetria");
    if (!formulario || !formulario.reportValidity()) return;

    const d = I18N_WEB[idiomaActual];
    const boton = qs("btn-submit-tel");
    const textoOriginal = boton ? boton.textContent : "";
    if (boton) {
        boton.disabled = true;
        boton.textContent = d.registrando;
    }

    const idTripulante = parseInt(qs("select-tripulante").value, 10);
    const idInsumo = qs("in-insumo").value;

    const payload = {
        id_tripulante: idTripulante,
        entorno: qs("select-entorno").value,
        presion_sistolica: parseInt(qs("in-sistolica").value, 10),
        presion_diastolica: parseInt(qs("in-diastolica").value, 10),
        frecuencia_cardiaca: parseInt(qs("in-fc").value, 10),
        glucosa_mg_dl: parseFloat(qs("in-glucosa").value),
        temperatura_c: parseFloat(qs("in-temp").value),
        horas_sueno: parseFloat(qs("in-sueno").value),
        estado_animo: parseInt(qs("in-animo").value, 10),
        minutos_ejercicio: parseInt(qs("in-ejercicio").value, 10),
        radiacion_msv: parseFloat(qs("in-rad").value),
        evidencia_adjunta: qs("in-evidencia").value,
        id_insumo_aplicado: idInsumo ? parseInt(idInsumo, 10) : null,
        cantidad_insumo: parseFloat(qs("in-cant-insumo").value || "0"),
    };

    try {
        const respuesta = await fetch(`${API_BASE}/telemetria`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "X-Operador-Id": sesionOperador ? String(sesionOperador.id) : "1",
            },
            body: JSON.stringify(payload),
        });
        const datos = await respuesta.json().catch(() => ({}));
        if (!respuesta.ok) throw new Error(datos.detalle || datos.detail || d.error_generico);

        actualizarRacha(datos.racha_actualizada, idTripulante);
        await Promise.all([cargarTripulantes(), cargarBotiquin()]);

        const selector = qs("select-tripulante");
        if (selector) selector.value = String(idTripulante);
        const tripulante = tripulantesCache.find((item) => item.id === idTripulante);
        if (tripulante) actualizarIdentidadCrew(tripulante);

        renderizarUltimaLectura(datos.lectura, datos.diagnostico, true);
        await recargarAnalitica(idTripulante);
        mostrarToast(d.registro_ok, "ok");
    } catch (error) {
        mostrarToast(error.message || d.error_generico, "error");
    } finally {
        if (boton) {
            boton.disabled = false;
            boton.textContent = textoOriginal;
        }
    }
}

// ===================================================================================
//  GRÁFICO CANVAS
// ===================================================================================

const UNIDADES_GRAFICO = {
    frecuencia_cardiaca: "BPM",
    presion_sistolica: "mmHg",
    glucosa_mg_dl: "mg/dL",
    horas_sueno: "h",
    estado_animo: "/5",
};

function dibujarGraficoEvolucion() {
    const canvas = qs("canvas-evolucion");
    if (!canvas || !canvas.parentElement) return;
    const contenedor = canvas.parentElement;
    const ancho = contenedor.clientWidth;
    const alto = contenedor.clientHeight;
    if (ancho < 20 || alto < 20) return;

    const d = I18N_WEB[idiomaActual];
    const dpr = window.devicePixelRatio || 1;
    canvas.width = Math.round(ancho * dpr);
    canvas.height = Math.round(alto * dpr);
    const ctx = canvas.getContext("2d");
    ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
    ctx.clearRect(0, 0, ancho, alto);

    const selectorMetrica = qs("select-metrica-grafico");
    const metrica = selectorMetrica ? selectorMetrica.value : "frecuencia_cardiaca";
    const series = analiticaActual && analiticaActual.series ? analiticaActual.series : {};
    const crudos = Array.isArray(series[metrica]) ? series[metrica] : [];
    const fechas = Array.isArray(series.fechas) ? series.fechas : [];
    const puntos = crudos
        .map((valor, indice) => ({ valor: Number(valor), fecha: fechas[indice] }))
        .filter((punto) => Number.isFinite(punto.valor));

    const leyenda = qs("chart-legend");
    if (leyenda) leyenda.innerHTML = "";

    if (!puntos.length) {
        ctx.fillStyle = "#647a93";
        ctx.font = "12px 'Segoe UI', sans-serif";
        ctx.textAlign = "center";
        ctx.textBaseline = "middle";
        ctx.fillText(d.chart_sin_datos, ancho / 2, alto / 2);
        return;
    }

    const padL = 46;
    const padR = 14;
    const padT = 16;
    const padB = 24;
    const anchoTrazo = Math.max(10, ancho - padL - padR);
    const altoTrazo = Math.max(10, alto - padT - padB);
    const valores = puntos.map((punto) => punto.valor);
    let minimo = Math.min(...valores);
    let maximo = Math.max(...valores);
    if (Math.abs(maximo - minimo) < 0.0001) {
        minimo -= 1;
        maximo += 1;
    }
    const margen = (maximo - minimo) * 0.12;
    minimo -= margen;
    maximo += margen;

    ctx.font = "10px 'Segoe UI', sans-serif";
    ctx.lineWidth = 1;
    for (let indice = 0; indice <= 4; indice += 1) {
        const y = padT + (altoTrazo / 4) * indice;
        ctx.strokeStyle = "rgba(27, 44, 68, 0.9)";
        ctx.beginPath();
        ctx.moveTo(padL, y);
        ctx.lineTo(padL + anchoTrazo, y);
        ctx.stroke();

        const valorEje = maximo - ((maximo - minimo) / 4) * indice;
        ctx.fillStyle = "#647a93";
        ctx.textAlign = "right";
        ctx.textBaseline = "middle";
        const etiqueta = Math.abs(maximo - minimo) < 6 ? valorEje.toFixed(1) : String(Math.round(valorEje));
        ctx.fillText(etiqueta, padL - 7, y);
    }

    const coordenadaX = (indice) => padL + (puntos.length === 1
        ? anchoTrazo / 2
        : (indice / (puntos.length - 1)) * anchoTrazo);
    const coordenadaY = (valor) => padT + (1 - (valor - minimo) / (maximo - minimo)) * altoTrazo;
    const xs = puntos.map((punto, indice) => coordenadaX(indice));
    const ys = puntos.map((punto) => coordenadaY(punto.valor));

    ctx.save();
    ctx.beginPath();
    ctx.rect(padL, padT, anchoTrazo, altoTrazo);
    ctx.clip();

    const relleno = ctx.createLinearGradient(0, padT, 0, padT + altoTrazo);
    relleno.addColorStop(0, "rgba(56, 189, 248, 0.26)");
    relleno.addColorStop(1, "rgba(56, 189, 248, 0)");
    ctx.beginPath();
    ctx.moveTo(xs[0], padT + altoTrazo);
    xs.forEach((x, indice) => ctx.lineTo(x, ys[indice]));
    ctx.lineTo(xs[xs.length - 1], padT + altoTrazo);
    ctx.closePath();
    ctx.fillStyle = relleno;
    ctx.fill();

    const trazo = ctx.createLinearGradient(padL, 0, padL + anchoTrazo, 0);
    trazo.addColorStop(0, "#38bdf8");
    trazo.addColorStop(1, "#a78bfa");
    ctx.beginPath();
    xs.forEach((x, indice) => {
        if (indice === 0) ctx.moveTo(x, ys[indice]);
        else ctx.lineTo(x, ys[indice]);
    });
    ctx.strokeStyle = trazo;
    ctx.lineWidth = 2.4;
    ctx.lineJoin = "round";
    ctx.lineCap = "round";
    ctx.stroke();

    const promedio = valores.reduce((acumulado, valor) => acumulado + valor, 0) / valores.length;
    const yPromedio = coordenadaY(promedio);
    ctx.setLineDash([4, 4]);
    ctx.strokeStyle = "rgba(251, 191, 36, 0.55)";
    ctx.lineWidth = 1;
    ctx.beginPath();
    ctx.moveTo(padL, yPromedio);
    ctx.lineTo(padL + anchoTrazo, yPromedio);
    ctx.stroke();
    ctx.setLineDash([]);

    puntos.forEach((punto, indice) => {
        const esUltimo = indice === puntos.length - 1;
        ctx.beginPath();
        ctx.arc(xs[indice], ys[indice], esUltimo ? 4 : 2.6, 0, Math.PI * 2);
        ctx.fillStyle = esUltimo ? "#fbbf24" : "#38bdf8";
        ctx.fill();
        if (esUltimo) {
            ctx.beginPath();
            ctx.arc(xs[indice], ys[indice], 8, 0, Math.PI * 2);
            ctx.strokeStyle = "rgba(251, 191, 36, 0.5)";
            ctx.lineWidth = 1.2;
            ctx.stroke();
        }
    });
    ctx.restore();

    ctx.fillStyle = "#647a93";
    ctx.font = "10px 'Segoe UI', sans-serif";
    ctx.textAlign = "center";
    ctx.textBaseline = "top";
    const indicesEje = Array.from(new Set([0, Math.floor((puntos.length - 1) / 2), puntos.length - 1]));
    indicesEje.forEach((indice) => {
        const fecha = formatearFechaCorta(puntos[indice].fecha) || `#${indice + 1}`;
        ctx.fillText(fecha, xs[indice], padT + altoTrazo + 7);
    });

    if (leyenda) {
        const unidad = UNIDADES_GRAFICO[metrica] || "";
        crearChipLeyenda(leyenda, "#fbbf24", d.chart_ultima, `${fmt(valores[valores.length - 1], 1)} ${unidad}`);
        crearChipLeyenda(leyenda, "#38bdf8", d.chart_promedio, `${fmt(promedio, 1)} ${unidad}`);
        crearChipLeyenda(leyenda, "#a78bfa", d.chart_muestras, String(valores.length));
    }
}

function crearChipLeyenda(contenedor, color, etiqueta, valor) {
    const chip = document.createElement("span");
    const punto = document.createElement("i");
    punto.style.background = color;
    chip.appendChild(punto);
    chip.appendChild(document.createTextNode(`${etiqueta} `));
    const dato = document.createElement("b");
    dato.textContent = valor;
    chip.appendChild(dato);
    contenedor.appendChild(chip);
}
