"""Controlled vocabularies. The Colombian voice of the dataset lives here.

All lists must stay in deterministic order — they are iterated by position
and any reorder will shift article assignments across a regenerated dataset.
"""
from __future__ import annotations

SECTIONS: list[str] = [
    "actualidad",
    "politica",
    "clima",
    "ciudades",
    "investigacion",
    "cultura",
    "cafe_y_comida",
    "opinion",
]

# 48 topic tags spanning climate, urban, investigations, Colombian politics,
# culture/coffee, and society.
TOPIC_TAGS: list[str] = [
    # climate & environment (12)
    "cambio_climatico", "deforestacion", "mineria_ilegal", "amazonia",
    "paramos", "biodiversidad", "transicion_energetica", "contaminacion_aire",
    "sequia", "rios_contaminados", "proteccion_ambiental", "cop_clima",
    # urban / cities (10)
    "transporte_publico", "metro", "vivienda", "espacio_publico",
    "seguridad_urbana", "movilidad_electrica", "ciclorrutas", "gentrificacion",
    "alcaldias", "servicios_publicos",
    # investigations (6)
    "corrupcion", "contratacion_publica", "narcotrafico", "paramilitares",
    "lavado_activos", "justicia_transicional",
    # Colombian political beats (8)
    "acuerdo_de_paz", "gobierno_petro", "migracion_venezolana",
    "violencia_de_genero", "politica_antidrogas", "eln",
    "elecciones", "ddhh",
    # culture, coffee, food (8)
    "cafe_especial", "festivales", "gastronomia", "literatura",
    "musica", "artesanias", "cine_colombiano", "identidad_regional",
    # health & society (4)
    "salud_publica", "educacion", "pobreza", "indigenas",
]

# Tags that plausibly co-occur within a given section. Drives tag assignment
# in the articles generator so a clima piece doesn't get tagged with
# narcotrafico unless there's overlap reason to.
SECTION_TAG_AFFINITY: dict[str, list[str]] = {
    "actualidad": [
        "gobierno_petro", "elecciones", "acuerdo_de_paz", "migracion_venezolana",
        "ddhh", "seguridad_urbana", "salud_publica", "educacion", "alcaldias",
    ],
    "politica": [
        "gobierno_petro", "elecciones", "acuerdo_de_paz", "politica_antidrogas",
        "eln", "ddhh", "justicia_transicional", "migracion_venezolana",
        "alcaldias", "corrupcion",
    ],
    "clima": [
        "cambio_climatico", "deforestacion", "mineria_ilegal", "amazonia",
        "paramos", "biodiversidad", "transicion_energetica", "contaminacion_aire",
        "sequia", "rios_contaminados", "proteccion_ambiental", "cop_clima",
        "indigenas",
    ],
    "ciudades": [
        "transporte_publico", "metro", "vivienda", "espacio_publico",
        "seguridad_urbana", "movilidad_electrica", "ciclorrutas",
        "gentrificacion", "alcaldias", "servicios_publicos",
        "contaminacion_aire", "pobreza",
    ],
    "investigacion": [
        "corrupcion", "contratacion_publica", "narcotrafico", "paramilitares",
        "lavado_activos", "justicia_transicional", "mineria_ilegal",
        "violencia_de_genero", "politica_antidrogas", "eln", "ddhh",
    ],
    "cultura": [
        "festivales", "literatura", "musica", "artesanias", "cine_colombiano",
        "identidad_regional", "gastronomia",
    ],
    "cafe_y_comida": [
        "cafe_especial", "gastronomia", "identidad_regional", "festivales",
        "artesanias",
    ],
    "opinion": [
        "gobierno_petro", "acuerdo_de_paz", "cambio_climatico",
        "transporte_publico", "vivienda", "educacion", "ddhh",
        "violencia_de_genero", "migracion_venezolana", "corrupcion",
    ],
}

# Beats held by authors, used as the author↔section routing key.
BEATS: list[str] = [
    "editorial", "climate", "urban", "investigations",
    "culture", "politics", "news", "opinion",
]

# Preferred section for an article given its author's beat. The generator
# uses the inverse: for a given section, weight candidate authors by how
# strongly their beat points at that section.
BEAT_SECTION_AFFINITY: dict[str, dict[str, float]] = {
    "editorial":      {"opinion": 0.45, "actualidad": 0.25, "politica": 0.15,
                       "clima": 0.10, "ciudades": 0.05},
    "climate":        {"clima": 0.85, "investigacion": 0.08, "ciudades": 0.05,
                       "opinion": 0.02},
    "urban":          {"ciudades": 0.80, "investigacion": 0.08, "politica": 0.07,
                       "actualidad": 0.05},
    "investigations": {"investigacion": 0.75, "politica": 0.15, "ciudades": 0.06,
                       "clima": 0.04},
    "culture":        {"cultura": 0.55, "cafe_y_comida": 0.35, "opinion": 0.05,
                       "actualidad": 0.05},
    "politics":       {"politica": 0.70, "actualidad": 0.20,
                       "investigacion": 0.08, "opinion": 0.02},
    "news":           {"actualidad": 0.70, "politica": 0.15, "ciudades": 0.10,
                       "clima": 0.05},
    "opinion":        {"opinion": 0.85, "actualidad": 0.05, "politica": 0.05,
                       "cultura": 0.05},
}

# 22 fictional staff. Fields: (name, role, primary_beat, joined_at, is_active).
# Joined dates span the outlet's history from founding (Jan 2018) to recent.
AUTHORS: list[tuple[str, str, str, str, bool]] = [
    ("Carolina Restrepo Arango",    "editora_jefe",              "editorial",      "2018-01-15", True),
    ("Mateo Ochoa Vélez",           "editor_clima",              "climate",        "2018-03-05", True),
    ("Valentina Pérez Mendoza",     "reportera_clima",           "climate",        "2019-07-22", True),
    ("Santiago Gómez Jaramillo",    "reportero_clima",           "climate",        "2021-02-10", True),
    ("Laura Quintero Ríos",         "reportera_clima",           "climate",        "2022-09-01", True),
    ("Andrés Cárdenas Torres",      "editor_ciudades",           "urban",          "2018-06-18", True),
    ("Daniela Hoyos Vargas",        "reportera_ciudades",        "urban",          "2020-01-07", True),
    ("Felipe Correa Salazar",       "reportero_ciudades",        "urban",          "2023-04-03", True),
    ("Juliana Mejía Castaño",       "editora_investigaciones",   "investigations", "2018-09-10", True),
    ("Sebastián Urrego Morales",    "reportero_investigaciones", "investigations", "2020-11-16", True),
    ("Camila Parra Gutiérrez",      "reportera_investigaciones", "investigations", "2022-05-30", True),
    ("Natalia Zapata Osorio",       "editora_cultura",           "culture",        "2019-02-01", True),
    ("Tomás Herrera Londoño",       "reportero_cultura",         "culture",        "2021-08-23", True),
    ("Isabella Acevedo Posada",     "reportera_cultura",         "culture",        "2023-10-12", True),
    ("Diego Montoya Rendón",        "editor_politica",           "politics",       "2019-05-14", True),
    ("Manuela Ramírez Cano",        "reportera_politica",        "politics",       "2021-06-07", True),
    ("Esteban Duque Tobón",         "reportero_politica",        "politics",       "2024-01-22", True),
    ("Alejandra Bedoya Franco",     "reportera_actualidad",      "news",           "2018-11-05", True),
    ("Juan David Gallego Rivas",    "reportero_actualidad",      "news",           "2022-03-14", True),
    ("Paulina Arboleda Giraldo",    "reportera_actualidad",      "news",           "2024-07-01", True),
    ("Ricardo Cuervo Henao",        "columnista",                "opinion",        "2018-01-20", True),
    ("Ana María Vélez Escobar",     "columnista",                "opinion",        "2020-04-18", True),
]

# Colombia regions + their cities. Outlet is Medellín-based, so Antioquia
# dominates and Bogotá follows.
COLOMBIA_CITIES: list[tuple[str, str]] = [
    ("Medellín", "Antioquia"),
    ("Envigado", "Antioquia"),
    ("Itagüí", "Antioquia"),
    ("Bello", "Antioquia"),
    ("Rionegro", "Antioquia"),
    ("Bogotá", "Bogotá DC"),
    ("Chía", "Cundinamarca"),
    ("Soacha", "Cundinamarca"),
    ("Cali", "Valle del Cauca"),
    ("Palmira", "Valle del Cauca"),
    ("Barranquilla", "Atlántico"),
    ("Bucaramanga", "Santander"),
    ("Cartagena", "Bolívar"),
    ("Pereira", "Risaralda"),
    ("Manizales", "Caldas"),
    ("Armenia", "Quindío"),
]

# Weight per Colombia city. Medellín dominates, Bogotá a strong second.
# Other regions grouped as low-share long tail.
COLOMBIA_CITY_WEIGHTS: dict[str, float] = {
    "Medellín": 0.34, "Bogotá": 0.28,
    "Envigado": 0.055, "Itagüí": 0.045, "Bello": 0.045, "Rionegro": 0.020,
    "Cali": 0.055, "Palmira": 0.010,
    "Barranquilla": 0.035, "Bucaramanga": 0.028, "Cartagena": 0.022,
    "Pereira": 0.020, "Manizales": 0.015, "Armenia": 0.010,
    "Chía": 0.010, "Soacha": 0.010,
}

# Diaspora cities where the outlet has meaningful audience.
DIASPORA_CITIES_BY_COUNTRY: dict[str, list[str]] = {
    "US": ["Miami", "New York", "Houston", "Los Angeles", "Orlando", "Atlanta"],
    "ES": ["Madrid", "Barcelona", "Valencia", "Sevilla"],
    "MX": ["Ciudad de México", "Guadalajara", "Monterrey"],
}

# Coffee domain — used in headlines, culture pieces, and Grupo Éxito Café
# sponsor materials.
COFFEE_VARIETALS: list[str] = [
    "Caturra", "Castillo", "Gesha", "Tabi", "Typica",
    "Bourbon Rosado", "Colombia", "Cenicafé 1", "Maragogipe", "Pacamara",
]

COFFEE_ORIGINS: list[str] = [
    "Huila", "Nariño", "Tolima", "Cauca", "Santander",
    "Antioquia", "Quindío", "Risaralda", "Caldas",
]

DEVICE_WEIGHTS: dict[str, float] = {
    "mobile": 0.72, "desktop": 0.22, "tablet": 0.06,
}

REFERRER_WEIGHTS: dict[str, float] = {
    "search": 0.38, "social": 0.24, "direct": 0.20,
    "newsletter": 0.12, "external": 0.06,
}

# ---- Headline assembly ------------------------------------------------------
# Templates combined with vocab below produce Spanish editorial headlines
# that read Colombian. Do not swap in faker sentence generators — they
# produce genre-less filler.

HEADLINE_TEMPLATES_BY_SECTION: dict[str, list[str]] = {
    "actualidad": [
        "{subject} en {place}: {aspect}",
        "{entity} anuncia {program} tras {trigger}",
        "Lo que dejó {event} en {place}",
        "{entity} responde a {trigger}",
        "Crece la tensión entre {actor_a} y {actor_b} por {issue}",
    ],
    "politica": [
        "{politician} frente a {issue}: {aspect}",
        "El Congreso debate {bill}: quiénes votan a favor y quiénes en contra",
        "Así avanza {reform} bajo el gobierno Petro",
        "Qué hay detrás de la renuncia de {politician}",
        "{institution} prepara {action} para responder a {trigger}",
    ],
    "clima": [
        "La crisis del agua en {place}: cinco claves",
        "{amount} de {resource} bajo amenaza en {region}",
        "Por qué {phenomenon} avanza más rápido en {region}",
        "{community} defiende su {resource} frente a {threat}",
        "El retroceso de los páramos: {region} en cifras",
        "{project} y el costo ambiental que nadie cuenta",
    ],
    "ciudades": [
        "Metro de {city}: {aspect}",
        "Vivienda en {city}: {aspect}",
        "{city} intenta recuperar su espacio público",
        "La nueva cara de {neighborhood}: ¿gentrificación o renovación?",
        "Ciclorrutas en {city}: qué funciona y qué no",
        "El transporte informal que sostiene a {city}",
    ],
    "investigacion": [
        "Seis meses rastreando {subject} en {region}",
        "Los contratos que {entity} firmó con {counterparty}",
        "Quién está detrás de {scheme} en {region}",
        "La red que mueve {asset} entre {region} y {region_b}",
        "Documentos revelan cómo {actor} operó en {place}",
    ],
    "cultura": [
        "{artist} vuelve a {city} con {work}",
        "El mapa de los festivales en {region} este año",
        "{work}: la obra que está marcando el año en {genre}",
        "Cine colombiano: lo imperdible de {year}",
        "{tradition} resiste en {place}",
    ],
    "cafe_y_comida": [
        "{varietal} de {origin}: por qué está ganando taza",
        "La mesa del {region}: {dish} y sus variaciones",
        "Cafés especiales en {city}: {count} lugares para probar",
        "{producer} y el café que cambió su vereda",
        "Del fogón al restaurante: {dish} en clave contemporánea",
    ],
    "opinion": [
        "Columna: {argument}",
        "Lo que no estamos diciendo sobre {issue}",
        "{issue}: tres preguntas incómodas",
        "Por qué {position} (y qué perdemos si insistimos)",
        "Carta abierta a {recipient}",
    ],
}

# Filler vocabulary the templates pull from. Kept here (not faker) so output
# stays deterministic and Colombian-flavoured.
HEADLINE_FILLERS: dict[str, list[str]] = {
    "subject": [
        "la crisis de la salud pública", "la disputa por el agua",
        "la llegada del metro", "el debate sobre la reforma pensional",
        "la ola migratoria", "la contratación sospechosa",
        "el retorno de los desplazados", "la protesta estudiantil",
        "el alza de la gasolina", "la inseguridad urbana",
    ],
    "aspect": [
        "qué dice el informe", "lo que funcionó y lo que no",
        "la letra pequeña", "cinco claves para entenderlo",
        "voces desde el territorio", "los vacíos que quedan",
        "qué sigue ahora", "la cronología", "tres preguntas pendientes",
    ],
    "entity": [
        "La Alcaldía de Medellín", "El Ministerio de Ambiente",
        "La Gobernación de Antioquia", "La Contraloría",
        "La Procuraduría", "El DANE", "EPM", "La ANLA",
        "La Defensoría del Pueblo", "La Fiscalía",
    ],
    "program": [
        "un nuevo plan de acción", "medidas de emergencia",
        "un proceso de consulta", "una estrategia de mitigación",
        "una mesa de diálogo", "una auditoría externa",
    ],
    "trigger": [
        "las denuncias de la comunidad", "el fallo de la Corte",
        "las lluvias de abril", "la presión internacional",
        "el paro de transportadores", "los hallazgos del informe",
    ],
    "event": [
        "el paro camionero", "la consulta popular",
        "la cumbre climática", "la audiencia pública",
        "la marcha del 21N", "el debate en el Concejo",
    ],
    "place": [
        "Medellín", "el Valle de Aburrá", "Bogotá", "Urabá",
        "el Catatumbo", "La Guajira", "el Chocó", "el Putumayo",
        "Antioquia", "la ruralidad antioqueña",
    ],
    "actor_a": ["la Alcaldía", "el Ministerio", "la Gobernación", "el sindicato"],
    "actor_b": ["la ciudadanía", "los gremios", "la oposición", "el Gobierno Nacional"],
    "issue": [
        "el cobro de valorización", "el POT", "la tarifa de EPM",
        "la política antidrogas", "la reforma tributaria",
        "el manejo del río Medellín", "el sistema de salud",
    ],
    "politician": [
        "el presidente Petro", "la vicepresidenta Márquez",
        "el alcalde Gutiérrez", "el gobernador Rendón",
        "la ministra Muhamad", "la senadora Valencia",
    ],
    "bill": [
        "la reforma a la salud", "la reforma pensional",
        "la ley de sometimiento", "el proyecto de paz total",
        "la ley estatutaria de educación",
    ],
    "reform": [
        "la reforma agraria", "la reforma a la salud",
        "la paz total", "la transición energética",
        "la reforma laboral",
    ],
    "institution": [
        "La Registraduría", "El Consejo de Estado", "La Corte Constitucional",
        "El Banco de la República", "El Consejo Nacional Electoral",
    ],
    "action": [
        "un pronunciamiento", "una investigación formal",
        "una medida cautelar", "un llamado a sesión extraordinaria",
    ],
    "amount": [
        "30 mil hectáreas", "el 40% del caudal", "tres especies endémicas",
        "12 mil familias", "18 cuencas", "seis municipios",
    ],
    "resource": [
        "bosque seco tropical", "páramo", "humedal", "agua potable",
        "cobertura vegetal", "biodiversidad",
    ],
    "region": [
        "Antioquia", "La Guajira", "el Chocó", "el Amazonas",
        "el Magdalena Medio", "el Cauca", "el Putumayo",
        "Norte de Santander", "el Valle del Cauca",
    ],
    "phenomenon": [
        "la deforestación", "la sequía", "el retroceso glaciar",
        "la contaminación del aire", "la pérdida de biodiversidad",
    ],
    "community": [
        "La comunidad wayuu", "Campesinos de Urabá",
        "Pescadores del Magdalena", "Líderes sociales del Catatumbo",
        "Consejos comunitarios del Pacífico",
    ],
    "threat": [
        "la minería ilegal", "un proyecto de hidrocarburos",
        "la expansión ganadera", "una concesión cuestionada",
    ],
    "project": [
        "Hidroituango", "el proyecto Quebradona",
        "la ampliación del puerto de Buenaventura", "el bloque del Yarí",
    ],
    "city": ["Medellín", "Bogotá", "Cali", "Bucaramanga", "Barranquilla", "Pereira"],
    "neighborhood": [
        "El Poblado", "Laureles", "Chapinero", "Usaquén",
        "Granada", "Manga", "Prado", "San Antonio de Prado",
    ],
    "counterparty": [
        "contratistas del sector salud", "empresas de fachada",
        "intermediarios del PAE", "operadores logísticos",
    ],
    "scheme": [
        "el desvío de regalías", "el cartel de la hemofilia",
        "la red de contratos sin licitar", "el esquema de testaferros",
    ],
    "asset": ["oro de aluvión", "madera fina", "cocaína", "divisas"],
    "region_b": ["el sur de Bolívar", "la frontera con Venezuela", "el Pacífico"],
    "actor": [
        "un contratista recurrente", "una fundación pantalla",
        "un exalcalde", "un alto funcionario",
    ],
    "artist": [
        "Adriana Lucía", "Juanes", "Carlos Vives", "Shakira",
        "Totó la Momposina", "Lido Pimienta", "Herencia de Timbiquí",
    ],
    "work": [
        "un nuevo álbum", "una obra de teatro", "un documental",
        "una exposición fotográfica", "una gira por el país",
    ],
    "genre": ["literatura", "cine", "música popular", "artes visuales"],
    "year": ["2024", "2025"],
    "tradition": [
        "La marimba de chonta", "El sombrero vueltiao",
        "Las fiestas de San Pacho", "La cumbia",
    ],
    "varietal": [
        "Caturra", "Castillo", "Gesha", "Tabi", "Bourbon Rosado", "Pacamara",
    ],
    "origin": ["Huila", "Nariño", "Tolima", "Cauca", "Antioquia"],
    "dish": [
        "la bandeja paisa", "el sancocho trifásico", "la arepa de chócolo",
        "el ajiaco santafereño", "la lechona tolimense",
    ],
    "count": ["ocho", "doce", "quince", "veinte"],
    "producer": [
        "Doña Amparo, caficultora de Salgar",
        "Don Ernesto, caficultor de Jardín",
        "La Asociación de Cafeteras de Andes",
        "Ramiro Estrada, productor de Betulia",
    ],
    "argument": [
        "La paz total no puede ser un cheque en blanco",
        "El metro de Bogotá nos cuesta más caro sin él",
        "La transición energética tiene que empezar por los territorios",
        "No hay periodismo local sin política pública",
    ],
    "position": [
        "el POT de Medellín no resiste otra prórroga",
        "la reforma a la salud necesita más debate público",
        "la política antidrogas actual ya fracasó",
    ],
    "recipient": [
        "la ministra de Ambiente", "el alcalde de Medellín",
        "los candidatos a la Gobernación", "el director del SENA",
    ],
}
