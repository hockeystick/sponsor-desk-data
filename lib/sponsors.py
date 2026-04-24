"""Sponsor folders: profile, press releases, past partnerships, 2026 priorities.

Content is written by hand as static Spanish strings — not templated —
because the four sponsors are a fixed cast and scale-of-one realism
beats scale-of-N generation. A banned-phrase filter runs before every
write; if anything smells like corporate boilerplate or translated LLM
output, the run aborts.
"""
from __future__ import annotations

import random
import unicodedata
from pathlib import Path

_BANNED_PHRASES: tuple[str, ...] = (
    # Spanish corporate-boilerplate tells
    "en el panorama actual en constante evolución",
    "en un mundo en constante cambio",
    "en un entorno cada vez más competitivo",
    "soluciones de última generación",
    "aprovechar sinergias",
    "sinergias estratégicas",
    "cambio de paradigma",
    "a la vanguardia",
    "de vanguardia",
    "sin fisuras",
    "transformar radicalmente",
    "líder indiscutido",
    "hoja de ruta integral",
    "ecosistema disruptivo",
    # English sludge — defensive, in case any helper string slipped through
    "unlock synergies",
    "best-in-class",
    "cutting-edge",
    "game-changing",
    "at the forefront",
    "paradigm shift",
    "in today's rapidly evolving",
    "in an ever-changing world",
)


def _check_banned(text: str, source_label: str) -> None:
    lowered = text.lower()
    hits = [p for p in _BANNED_PHRASES if p in lowered]
    if hits:
        raise RuntimeError(
            f"banned phrase in {source_label}: {hits!r}. "
            "fix the copy — don't weaken the filter."
        )


# ---- Bancolombia Verde ------------------------------------------------------

_BANCOLOMBIA_VERDE: dict[str, str] = {
"profile.md": """\
# Bancolombia Verde

Bancolombia Verde es la línea de negocio de banca sostenible del Grupo
Bancolombia, lanzada formalmente en septiembre de 2022 como respuesta
a la creciente demanda de productos financieros alineados con criterios
ambientales, sociales y de gobernanza (ASG). Opera como una unidad con
equipo propio dentro de la estructura del banco y comparte licencia
bancaria con la matriz.

## Qué hacemos

Bancolombia Verde desarrolla y comercializa productos de crédito e
inversión diseñados para reducir el impacto climático del sistema
financiero colombiano. A la fecha operan cuatro líneas activas:

- **Hipoteca Verde**: crédito hipotecario con tasa preferencial para
  vivienda certificada con estándares EDGE o LEED. Lanzada en junio de
  2025 en Medellín y Bogotá; a cierre del primer trimestre de 2026 ha
  desembolsado COP 184.000 millones en 612 operaciones.
- **Crédito MoviEléctrica**: financiación de vehículos eléctricos
  (automóviles, motos, taxis) con tasa inferior a la del mercado
  convencional en 180 puntos básicos. Cartera vigente: COP 96.000
  millones.
- **Empresas Sostenibles**: línea de crédito corporativo para pymes que
  presentan planes de reducción de emisiones verificables por un
  tercero autorizado (Icontec o CTCN).
- **Bonos Verdes Bancolombia**: emisión propia listada en la Bolsa de
  Valores de Colombia. La segunda emisión (septiembre de 2025) colocó
  COP 450.000 millones y fue sobre-demandada 1,8 veces.

## Equipo y liderazgo

- **Paola Andrea Echeverri Villa**, gerente general de Bancolombia
  Verde desde su creación. Ingeniera industrial de la Universidad de
  los Andes con MBA del INSEAD. Trabajó previamente en Bancóldex en
  financiamiento de infraestructura sostenible.
- **Juan Camilo Restrepo Henao**, director de Finanzas Sostenibles.
  Economista de EAFIT, especialista en riesgo climático para el sector
  financiero.
- **Claudia Marcela Ortiz Gómez**, directora de Marca y Comunicación.
  Anteriormente directora de marca de Coltejer y jefa de comunicación
  de Comfama.

## Clientes y alcance

El público objetivo de Bancolombia Verde es el segmento de adultos
profesionales entre 28 y 45 años con ingresos medio-altos, residentes
en las principales ciudades del país (Medellín, Bogotá, Cali,
Barranquilla, Bucaramanga). La estrategia comercial asume que este
grupo combina decisiones de consumo con preocupaciones climáticas y
busca productos financieros que reflejen esa coherencia. En estudios
internos realizados en 2025, un 67% de los clientes activos de la
Hipoteca Verde identifica la reducción de emisiones como motivación
principal del producto.

Bancolombia Verde mantiene alianzas operativas con la Alcaldía de
Medellín para el programa *Vivienda Saludable*, con EPM para
financiamiento de instalaciones solares residenciales, y con la
Cámara Colombiana de la Construcción (Camacol) para estandarizar
criterios de certificación energética en proyectos nuevos. El reporte
de sostenibilidad anual es auditado por KPMG y sigue los estándares
GRI más el marco TCFD para divulgación climática.

## Valores institucionales

La unidad opera bajo tres principios declarados: (1) transparencia en
la medición de impacto, (2) preferencia por inversiones con retorno
medible en reducción de emisiones frente a retorno meramente reputacional,
(3) independencia metodológica para definir criterios de elegibilidad
sin intervención de áreas comerciales de la matriz.
""",

"brand_priorities_2026.md": """\
# Prioridades de marca 2026 — Bancolombia Verde

*Extracto de la presentación de Paola Andrea Echeverri Villa, gerente
general, en el comité ASG del Grupo Bancolombia, febrero de 2026.
Compartido públicamente como parte del reporte de sostenibilidad
preliminar 2025.*

Entramos a 2026 con una agenda concentrada en cinco frentes. No son
aspiracionales — cada uno tiene meta trimestral y responsable
asignado.

## 1. Escalar la Hipoteca Verde

La meta 2026 es desembolsar COP 520.000 millones en al menos 2.100
operaciones. Esto requiere duplicar el número de proyectos de vivienda
con certificación EDGE disponibles en Medellín, Bogotá y extender el
producto a Cali y Barranquilla en el segundo semestre. Trabajamos con
Camacol en una guía estandarizada para constructoras medianas que
reduce el costo de certificación en un 35% frente al proceso actual.

## 2. Llegar a clientes profesionales jóvenes donde leen, no donde
les conviene a los bancos

Nuestra segmentación de clientes (28-45, urbanos, lectores activos de
prensa digital) no se construye bien con la publicidad financiera
tradicional. En 2026 redirigimos el 40% del presupuesto de medios de
Bancolombia Verde hacia contenido editorial patrocinado en medios
independientes con audiencias calificadas en clima y ciudades. La tesis
comercial es que la afinidad se construye en contexto — no interrumpiendo
contexto.

## 3. Cerrar la tercera emisión de bonos verdes

Planeamos una tercera emisión en el tercer trimestre de 2026, con meta
de colocación de COP 600.000 millones. El destino estará ligado
específicamente a financiación de transición energética industrial en
empresas medianas del Valle de Aburrá y Eje Cafetero.

## 4. Ampliar cobertura rural

Durante tres años hemos tenido una presencia urbana dominante. En 2026
abrimos un piloto de crédito para transición productiva en 8 municipios
del suroeste antioqueño, con foco en caficultores que incorporen
prácticas bajas en carbono. Aliados operativos: Comité Departamental de
Cafeteros y Federación Nacional de Cafeteros.

## 5. Publicar métricas de forma pública y trimestral

Pasamos de reporte anual a reporte trimestral a partir del Q2 2026.
Las métricas publicadas incluyen: desembolsos por línea, toneladas de
CO2e mitigadas, tasa de morosidad, % de clientes certificados como
primeros compradores. La decisión responde al estándar de divulgación
TCFD y a la presión legítima de analistas que piden mayor granularidad.

## Lo que no vamos a hacer

Dos cosas que nos han propuesto y rechazamos para 2026: (a) lanzar un
producto de inversión con el sello "verde" sin criterios ASG verificables,
y (b) hacer greenwashing con la marca matriz. Bancolombia Verde mantiene
independencia metodológica justamente para que la unidad no termine
siendo un ejercicio de reputación del grupo.

---

Paola Andrea Echeverri Villa · Gerente General · Bancolombia Verde
""",

"past_media_partnerships.md": """\
# Alianzas con medios — 2024-2025

Bancolombia Verde ha trabajado con medios en formato editorial patrocinado
y panel. No trabajamos con medios bajo modelo de publicidad display
estándar. Listamos aquí las colaboraciones de los últimos 18 meses para
efectos de transparencia ante clientes y para análisis interno de
efectividad.

## Revista Dinero — Sección patrocinada "Finanzas con huella"

Enero-marzo de 2025. Seis artículos originales sobre finanzas sostenibles
escritos por el equipo editorial de Dinero con acceso a datos operativos
de Bancolombia Verde. Temas incluyeron: metodología de medición de
emisiones en cartera hipotecaria, casos de uso de bonos verdes en
Latinoamérica, entrevista a tres clientes MoviEléctrica.

Qué funcionó: el formato respeta el criterio editorial de Dinero,
que garantiza credibilidad del contenido. El engagement por lectura
fue 3,2 veces el de piezas de marca convencionales. Presupuesto: USD
48.000.

## La República — Columna de opinión patrocinada

Julio-diciembre de 2025. Columna quincenal firmada por Juan Camilo
Restrepo Henao, director de Finanzas Sostenibles, sobre temas de
regulación y mercado. La República ejerció revisión editorial estándar
y rechazó dos piezas por considerar que no añadían valor informativo
más allá del mensaje corporativo.

Qué funcionó: reconocimiento de Juan Camilo como voz experta. Ya en
2026 dos columnas independientes de otros medios lo citan. No estamos
renovando este formato para 2026 porque la mecánica de columna firmada
limita la flexibilidad temática.

## Portafolio — Panel presencial "Transición climática y capital privado"

Septiembre de 2025. Panel presencial en Bogotá (Hotel Cosmos 100) con
120 asistentes entre banqueros, reguladores y emisores corporativos.
Panelistas incluyeron a Camilo Sánchez (Fondo Acción), Juanita López
(MinAmbiente), y Paola Echeverri por Bancolombia Verde. Transmisión en
vivo en el sitio de Portafolio alcanzó 4.800 espectadores.

Qué funcionó: el panel generó tres menciones en prensa no compradas
(dos en *La Silla Vacía* y una en *Semana Sostenible*). El formato
presencial corto y enfocado funciona mejor que eventos de día completo.

## Pauta y editoriales que hemos rechazado

Durante 2024-2025 rechazamos nueve propuestas de medios por no cumplir
nuestro estándar mínimo de independencia editorial. La política interna
exige que el medio mantenga derecho a revisar, editar y rechazar piezas
sin intervención nuestra; que toda pieza sea marcada explícitamente
como patrocinada según estándares IAB Colombia; y que no se condicione
el contenido a métricas de marca predefinidas.
""",

"press_releases/2025-06-10-lanzamiento-hipoteca-verde.md": """\
# Bancolombia Verde lanza Hipoteca Verde en Medellín y Bogotá

*Medellín, 10 de junio de 2025.* Bancolombia Verde, la línea de banca
sostenible del Grupo Bancolombia, presentó hoy oficialmente su producto
Hipoteca Verde, un crédito hipotecario con tasa preferencial para
vivienda que cuente con certificación EDGE o LEED. La oferta estará
disponible desde hoy en Medellín y Bogotá y llegará a Cali y
Barranquilla en el segundo semestre de 2025.

"La meta de corto plazo es desembolsar COP 180.000 millones en el
primer año de operación. La meta de largo plazo es que el estándar de
construcción certificada deje de ser la excepción y pase a ser
preferido por el mercado", dijo Paola Andrea Echeverri Villa, gerente
general de Bancolombia Verde, durante el evento de lanzamiento
realizado en el edificio El Cabildo de El Poblado.

El producto aplica una reducción de 90 puntos básicos sobre la tasa
hipotecaria estándar del banco y está disponible para proyectos
entregados desde enero de 2024 en adelante. La elegibilidad se verifica
a través del sello EDGE emitido por IFC o del sello LEED emitido por el
Consejo Colombiano de Construcción Sostenible (CCCS).

Acompañaron el lanzamiento Sandra Forero, presidenta de Camacol
Antioquia, y Juan Sebastián Gómez, director del CCCS, quienes firmaron
con Bancolombia Verde un memorando de entendimiento para simplificar la
ruta de certificación para constructoras medianas. El memorando apunta
a reducir el costo promedio de certificación de COP 52 millones a COP
34 millones por proyecto.

Bancolombia Verde proyecta que la Hipoteca Verde contribuirá a evitar
aproximadamente 12.400 toneladas de CO2 equivalente anuales una vez que
alcance régimen pleno, cálculo realizado sobre el supuesto de 2.100
operaciones anuales con reducción media del 30% en consumo energético
residencial frente al parque construido estándar.

El producto se integra con el simulador hipotecario en línea de
Bancolombia, donde los clientes pueden verificar elegibilidad y
pre-calificación directamente.

### Sobre Bancolombia Verde
Bancolombia Verde es la unidad de banca sostenible del Grupo
Bancolombia, lanzada en septiembre de 2022. Opera cuatro líneas de
producto y ha desembolsado, a mayo de 2025, cerca de COP 280.000
millones en financiación con criterios ambientales verificables.

*Contacto de prensa: Claudia Marcela Ortiz Gómez ·
cortiz@bancolombiaverde.co · +57 (4) 604 0000 ext. 4521*
""",

"press_releases/2025-09-22-reporte-sostenibilidad-2024.md": """\
# Bancolombia Verde publica su segundo reporte anual de sostenibilidad

*Medellín, 22 de septiembre de 2025.* Bancolombia Verde publicó hoy su
segundo reporte anual de sostenibilidad correspondiente al ejercicio
2024. El documento, auditado por KPMG Colombia, reporta un desembolso
acumulado de COP 412.000 millones en productos con criterios ambientales
verificables, un aumento del 68% frente al cierre de 2023.

"El dato que más nos importa este año no es el volumen sino la
diversificación. En 2023 éramos una cartera concentrada en hipoteca
urbana; hoy tenemos cuatro líneas activas y la más pequeña de ellas
(Empresas Sostenibles) ya representa el 14% de la cartera total", dijo
Juan Camilo Restrepo Henao, director de Finanzas Sostenibles, al
presentar el informe.

Entre los hallazgos destacados del reporte:

- Se evitaron 38.200 toneladas de CO2 equivalente durante 2024,
  calculadas bajo metodología PCAF (Partnership for Carbon Accounting
  Financials) y validadas externamente.
- La cartera MoviEléctrica creció 143% y hoy financia 1.840 vehículos,
  principalmente en Medellín y el Valle de Aburrá.
- El 61% de los clientes de Hipoteca Verde son compradores de vivienda
  por primera vez, dato que la unidad interpreta como señal de que el
  producto está ampliando el acceso, no sustituyendo demanda existente.

El reporte también identifica retos pendientes: el producto Empresas
Sostenibles tiene una tasa de rechazo de solicitudes del 47%, lo que
sugiere que los criterios de verificación externa están siendo una
barrera de entrada mayor a lo proyectado. Para 2026, Bancolombia Verde
anunció que simplificará el proceso para pymes de menos de 50
empleados.

Bancolombia Verde adopta por tercer año consecutivo los estándares GRI
y el marco TCFD. El reporte completo está disponible en formato abierto
en el sitio web de la unidad y en el repositorio público de la
Superintendencia Financiera de Colombia.

*Contacto de prensa: Claudia Marcela Ortiz Gómez ·
cortiz@bancolombiaverde.co*
""",

"press_releases/2026-01-15-alianza-movilidad-medellin.md": """\
# Bancolombia Verde y la Alcaldía de Medellín firman alianza para financiar taxis eléctricos

*Medellín, 15 de enero de 2026.* Bancolombia Verde y la Secretaría de
Movilidad de Medellín firmaron hoy un acuerdo de cooperación que
facilita la financiación de taxis eléctricos para conductores afiliados
a las empresas del servicio público individual de pasajeros de la
ciudad. El acuerdo estará vigente hasta diciembre de 2027 y tiene una
meta declarada de 1.200 vehículos financiados.

Bajo el convenio, Bancolombia Verde ofrecerá crédito a 60 meses con
tasa preferencial de 11,8% efectivo anual (230 puntos básicos por
debajo de la tasa comercial estándar) a conductores que acrediten
vinculación activa con una empresa operadora. La Secretaría de
Movilidad aportará un incentivo adicional de COP 6 millones por
vehículo a los primeros 400 beneficiarios bajo el programa *Medellín
Respira*.

"Este acuerdo resuelve el cuello de botella principal de la
electrificación del taxi: el conductor quiere el vehículo, pero la
estructura financiera no le da viabilidad mensual. Lo que hemos hecho
es ajustar esa estructura", dijo Juan Camilo Restrepo Henao, director
de Finanzas Sostenibles, tras la firma en el Centro Administrativo La
Alpujarra.

Por la Alcaldía firmó Carolina Franco, secretaria de Movilidad, quien
señaló que la ciudad proyecta reducir en 16.800 toneladas de CO2e
anuales una vez que la flota cubierta por el acuerdo esté operativa.

La primera cohorte del programa abrirá convocatoria el 1 de febrero de
2026 con 120 cupos disponibles. Los interesados podrán postularse a
través de los puntos de atención de Bancolombia o del portal web de la
Secretaría de Movilidad.

*Contacto de prensa: Claudia Marcela Ortiz Gómez ·
cortiz@bancolombiaverde.co*
""",

"press_releases/2026-03-07-nombramiento-sostenibilidad.md": """\
# Bancolombia Verde nombra a Lorena Quintana Díaz como nueva directora de Producto

*Medellín, 7 de marzo de 2026.* Bancolombia Verde informó hoy el
nombramiento de Lorena Quintana Díaz como directora de Producto,
posición creada este año como parte del ajuste organizativo derivado
del plan estratégico 2026-2028.

Quintana proviene de Davivienda donde ejerció durante cuatro años como
gerente de producto en el área de vivienda, liderando el lanzamiento
del programa *Casa Propia Joven* y la renovación del portafolio de
crédito constructor. Antes de Davivienda trabajó en la IFC en Washington
D.C. en proyectos de financiamiento verde para América Latina.

"Lorena conoce el lado de la construcción, el lado del cliente y el
lado de cómo se diseña el producto para que funcione en los dos. Es un
perfil raro en el mercado y nos alegra mucho que haya aceptado", dijo
Paola Andrea Echeverri Villa, gerente general.

Quintana asume el cargo el 15 de marzo y reportará directamente a la
gerencia general. Su primera prioridad, según el comunicado interno
distribuido al equipo, será la expansión de la Hipoteca Verde a Cali y
Barranquilla en el segundo trimestre de 2026 y el diseño del producto
*Empresas Sostenibles 2.0* para pymes con menos de 50 empleados.

El nombramiento eleva a cuatro el número de directoras mujeres en el
equipo de liderazgo de Bancolombia Verde, que actualmente cuenta con
28 personas.

*Contacto de prensa: Claudia Marcela Ortiz Gómez ·
cortiz@bancolombiaverde.co*
""",
}


# ---- Fundación Andes --------------------------------------------------------

_FUNDACION_ANDES: dict[str, str] = {
"profile.md": """\
# Fundación Andes

Fundación Andes es una organización sin ánimo de lucro con sede en
Bogotá (Colombia) y oficina regional en Lima (Perú), dedicada al
fortalecimiento de la participación ciudadana y el periodismo
independiente en los países andinos. Constituida en 2012 por un grupo
mixto de donantes colombianos y peruanos, opera hoy con una plantilla
de 34 personas y un presupuesto anual de aproximadamente USD 6,4
millones.

## Ámbito

Fundación Andes trabaja en cuatro países: Colombia, Ecuador, Perú y
Bolivia. Su enfoque geográfico responde a la tesis de que los
ecosistemas democráticos de la región andina comparten retos
estructurales comunes (debilidad institucional local, concentración de
poder mediático, conflictos socioambientales recurrentes) y que
intervenciones coordinadas producen efectos mayores que esfuerzos
aislados por país.

La fundación no opera en política partidista ni hace advocacy directo.
Canaliza su trabajo a través de tres líneas: (1) becas de reportaje
periodístico, (2) investigación aplicada sobre ecosistemas de
información, y (3) pilotos de cívica digital con organizaciones locales.

## Programas activos

- **Beca Andes**: beca anual de reportaje para periodistas menores de 35
  años. Cohorte 2025: 18 becarios de cuatro países, cada uno financiado
  con USD 18.000 para seis meses de trabajo investigativo. Las piezas se
  publican en medios aliados o en el sitio propio de la fundación.
- **Observatorio Andino de Medios**: línea de investigación que publica
  un informe regional anual sobre pluralismo mediático. El informe 2024
  fue citado por la CIDH en su relatoría sobre libertad de expresión.
- **Laboratorio Andino de Cívica**: financia pilotos tecnológicos de
  participación ciudadana local (rendición de cuentas municipal,
  veedurías digitales, herramientas de acceso a datos públicos). En
  2025 financió 9 pilotos con COP 120 millones promedio cada uno.
- **Red de Editoras Investigativas**: espacio formativo cerrado para
  editoras de investigación de medios andinos, realizado dos veces al
  año desde 2022.

## Equipo directivo

- **Dra. Elena Mercedes Cárdenas Restrepo**, directora ejecutiva desde
  2019. Antes dirigió el programa de derechos humanos de la Fundación
  Ford para América Latina. PhD en Ciencia Política por la Universidad
  de los Andes.
- **Tomás Iriarte Montoya**, director del programa de periodismo.
  Ex-editor de investigaciones de *El Espectador*. Dirige el programa
  desde 2020.
- **Sofía Vargas Prieto**, directora del Observatorio Andino de Medios.
  Socióloga de la Universidad Nacional Mayor de San Marcos (Lima), con
  maestría en la LSE.
- **Camilo Iván Paredes**, gerente de operaciones en Bogotá.

## Financiamiento y transparencia

Fundación Andes recibe financiamiento de tres fuentes: donantes
internacionales institucionales (Ford Foundation, Open Society, Luminate,
NED), aportes de cooperación bilateral (Suecia, Alemania, Unión
Europea), y aportes de un pequeño grupo de donantes privados
individuales. El presupuesto completo y los estados financieros
auditados se publican anualmente en el sitio web. Los donantes no
tienen influencia sobre las decisiones editoriales de los becarios ni
sobre los temas del Observatorio.

## Lo que no hacemos

Fundación Andes no subsidia la operación de medios de comunicación.
Financia periodistas individuales y proyectos específicos, pero no
asume gastos recurrentes de redacciones. Esta política existe desde
2015 y se mantiene porque el equipo considera que subsidiar operación
corriente distorsiona la relación de dependencia entre medio y donante.
""",

"brand_priorities_2026.md": """\
# Prioridades 2026 — Fundación Andes

*Documento institucional aprobado por la Junta Directiva el 28 de enero
de 2026. Este extracto se comparte con aliados y medios con los que la
Fundación sostiene conversación activa.*

Fundación Andes concentra su trabajo de 2026 en tres apuestas
programáticas y una reforma interna. Cada apuesta tiene un indicador
de resultado público.

## 1. Beca Andes: doblar la cohorte para 2026

Cumplimos diez años del programa Beca Andes. La próxima cohorte (enero
2026) pasa de 18 a 36 becarios con financiamiento complementario de la
Fundación Ford y la Luminate Group. El criterio de selección prioriza
proyectos de investigación sobre (a) crimen organizado y finanzas
ilícitas, (b) conflictos socioambientales en zonas de frontera
extractiva, y (c) captura institucional en gobiernos subnacionales.

Meta pública: 30 de las 36 investigaciones publicadas en medios
aliados o en el sitio de la fundación antes del 31 de diciembre de
2026.

## 2. Fortalecimiento del periodismo local

Identificamos que el cuello de botella del periodismo investigativo en
la región no es el periodista individual — hay talento — sino la
ausencia de redacciones pequeñas con músculo editorial para sostener
investigaciones largas. En 2026 lanzamos el programa *Ráfaga* que
financia estancias editoriales de tres meses para periodistas
provenientes de redacciones pequeñas en redacciones más grandes
(*Connectas*, *Ojo Público*, *La Silla Vacía*, *Cuestión Pública*).

Presupuesto: USD 480.000 para 16 estancias en 2026.

## 3. Investigación sobre ecosistemas de información regionales

El Observatorio Andino de Medios publica en octubre de 2026 la tercera
edición de su informe regional, con foco en la concentración de
propiedad mediática y el papel de plataformas digitales en la economía
de los medios locales. Ya comenzó la fase de levantamiento de datos en
los cuatro países.

Socios de investigación 2026: Instituto Prensa y Sociedad (Perú),
Fundación Gabo (Colombia), Fundación Jubileo (Bolivia), Fundamedios
(Ecuador).

## 4. Reforma interna: política de transparencia donante

Durante 2025 recibimos cuestionamientos legítimos sobre la composición
de nuestro portafolio de donantes. En 2026 adoptamos un estándar
público de transparencia que incluye: (a) publicación trimestral de
nuevos aportes por encima de USD 50.000, (b) declaración pública de
conflictos potenciales cuando un donante tenga intereses materiales en
un tema de investigación financiado por la fundación, (c) política
renovada sobre aportes corporativos.

## Lo que estamos observando sin intervenir todavía

- Concentración regional de plataformas de distribución (Google, Meta,
  TikTok) y su impacto en la economía de medios locales.
- Uso de inteligencia artificial generativa en redacciones pequeñas.
  Estamos estudiando si conviene desarrollar lineamientos o si es
  prematuro dado que el campo se mueve muy rápido.

---

Junta Directiva · Fundación Andes · Bogotá, febrero de 2026
""",

"past_media_partnerships.md": """\
# Alianzas con medios — Fundación Andes

Fundación Andes no compra publicidad. Trabaja con medios bajo tres
formatos: publicación de piezas producidas por becarios del programa
Beca Andes, co-producción de investigaciones con redacciones aliadas,
y organización conjunta de eventos públicos. Listamos aquí las
colaboraciones más relevantes de los últimos 18 meses.

## Connectas — Proyecto "Fronteras Invisibles"

Una serie investigativa de ocho entregas sobre economías ilícitas en
zonas de frontera en los cuatro países andinos, producida conjuntamente
por Connectas (red regional) y cuatro becarios Andes durante el primer
semestre de 2025. La serie fue replicada en *El Espectador* (Colombia),
*El Comercio* (Perú), *La Razón* (Bolivia) y *Plan V* (Ecuador). Una de
las piezas resultó en una citación del Congreso colombiano al
subdirector del INPEC.

Presupuesto total: USD 180.000. Contribución Fundación Andes: USD 95.000.

## Ojo Público — Serie "Contratos al margen"

Producción de una serie de seis entregas sobre contratación irregular
en gobiernos regionales del sur peruano, publicada por Ojo Público
durante el segundo semestre de 2025. El proyecto recibió financiamiento
de la Beca Andes extendida y del Pulitzer Center for Crisis Reporting.
Fundación Andes aportó financiamiento semilla de USD 45.000.

## CIPER Chile y La Silla Vacía — Intercambio editorial

En octubre de 2025 cofinanciamos con la Fundación Luminate un
intercambio editorial de seis semanas entre CIPER Chile y La Silla
Vacía, en el que editoras de ambos medios trabajaron en proyectos
compartidos. No fue una alianza de publicación sino de formación
editorial.

## La Silla Vacía — Foro público "La independencia editorial en tiempos
de crisis mediática"

Octubre de 2025, Bogotá. Copatrocinamos con La Silla Vacía un foro
público con 180 asistentes presenciales y 3.200 conectados en línea.
Panelistas: Patricia Janiot (periodista independiente), Juanita León
(La Silla Vacía), Daniela Mohor (CIPER Chile), Ricardo Uceda (IPYS,
Perú). El registro del panel está disponible públicamente en el sitio
de La Silla Vacía.

## Cuestión Pública — Investigación sobre Hidroituango

Aporte de la Fundación Andes a la investigación de largo aliento
publicada por Cuestión Pública sobre la toma de decisiones financieras
y técnicas alrededor del proyecto Hidroituango. Fundación Andes no tuvo
intervención editorial alguna; el aporte fue USD 38.000 al Fondo de
Investigaciones del medio.

## Criterios para futuras colaboraciones

Fundación Andes no financia a medios que tengan conflictos patrimoniales
no declarados con el tema de la investigación. No publica como
"alianza" trabajo que en realidad es publicidad institucional de la
fundación. Prefiere estructuras donde el medio mantiene control
editorial completo y la fundación aparece en los créditos, no en el
control.
""",

"press_releases/2024-11-05-becarios-2025.md": """\
# Fundación Andes anuncia los 18 becarios del programa Beca Andes 2025

*Bogotá, 5 de noviembre de 2024.* Fundación Andes dio a conocer hoy la
cohorte 2025 de su programa anual Beca Andes, que financia
investigaciones periodísticas de largo aliento en Colombia, Ecuador,
Perú y Bolivia. La cohorte está compuesta por 18 periodistas
seleccionados entre 423 postulantes.

"Este año recibimos un número récord de postulaciones. Lo más
significativo no es el volumen sino la calidad temática: más de la
mitad de los proyectos propone investigaciones en territorios de
difícil acceso — Putumayo, Madre de Dios, Morona Santiago, Beni", dijo
Tomás Iriarte Montoya, director del programa de periodismo, durante
el anuncio realizado en las instalaciones de la fundación en Chapinero.

Los 18 becarios seleccionados recibirán USD 18.000 cada uno para cubrir
seis meses de trabajo investigativo, además de apoyo editorial de
mentores asignados y acceso a recursos de verificación de datos a
través de alianzas con el Instituto Poynter y Data Journalism Asia.

Entre los proyectos seleccionados destacan una investigación de
Alejandra Tapia (Perú) sobre redes de tráfico de madera entre Loreto
y Acre (Brasil); un trabajo de Sebastián Lozano (Colombia) sobre
contratación irregular en secretarías de salud del Caribe; y una
investigación de Gabriela Murillo (Ecuador) sobre la explotación
minera en áreas protegidas de la Amazonía.

La cohorte está compuesta por nueve mujeres y nueve hombres, con
edades entre 24 y 34 años. Ocho becarios provienen de redacciones
pequeñas fuera de capitales (Cali, Arequipa, Cuenca, Santa Cruz). Los
proyectos serán publicados a lo largo de 2025 en los sitios de los
medios aliados o en el portal de la fundación.

La selección fue realizada por un comité editorial externo compuesto
por Javier Lafuente (*El País*), Gabriela Wiener (escritora y
periodista), y Ignacio Escolar (*elDiario.es*), sin participación del
equipo de la Fundación Andes en la decisión final.

*Contacto: Tomás Iriarte Montoya · tiriarte@fundacionandes.org*
""",

"press_releases/2025-04-18-informe-participacion-civica.md": """\
# Fundación Andes publica informe sobre participación cívica digital en la región andina

*Bogotá, 18 de abril de 2025.* El Observatorio Andino de Medios,
programa de investigación de Fundación Andes, publicó hoy el informe
*Participación cívica digital en los Andes: diagnóstico regional
2024*, un documento de 184 páginas que mapea herramientas, organizaciones
y prácticas de cívica digital en Colombia, Ecuador, Perú y Bolivia.

El informe, liderado por la directora del Observatorio Sofía Vargas
Prieto, identifica 312 iniciativas de cívica digital activas en la
región, de las cuales 61% tienen presupuestos anuales inferiores a
USD 25.000 y 82% operan con personal voluntario o mixto. El documento
sostiene que el ecosistema cívico digital andino es más amplio y
disperso de lo que revelan los mapeos anteriores, pero enfrenta una
crisis de sostenibilidad financiera.

"Una conclusión incómoda: muchas de las herramientas cívicas más
usadas en la región están a un donante de distancia de desaparecer.
Esa fragilidad tiene que ser parte de la conversación sobre
modernización democrática", señaló Vargas Prieto en la presentación
realizada en el auditorio del Centro Cultural Gabriel García Márquez.

El informe fue elaborado entre enero de 2024 y marzo de 2025 con
participación de 74 investigadores locales en los cuatro países.
Incluye estudios de caso de ocho herramientas — entre ellas Veeduría
Ciudadana (Colombia), Fiscalizadores (Perú), y Observatorio Urbano de
La Paz (Bolivia) — y un conjunto de recomendaciones de política
pública para gobiernos locales.

El informe está disponible en acceso abierto en el sitio del
Observatorio y bajo licencia Creative Commons Atribución-No Comercial.
Una versión resumida de 20 páginas será distribuida a más de 600
formuladores de política pública de la región en las próximas semanas.

*Contacto: Sofía Vargas Prieto · svargas@fundacionandes.org*
""",

"press_releases/2025-10-30-convocatoria-investigativa.md": """\
# Fundación Andes abre convocatoria extraordinaria por USD 2 millones para
investigaciones sobre crimen organizado

*Bogotá, 30 de octubre de 2025.* Fundación Andes y la Fundación Ford
anunciaron hoy una convocatoria extraordinaria dotada con USD 2
millones para financiar investigaciones periodísticas sobre
economías ilegales y crimen organizado transnacional en la región
andina. La convocatoria estará abierta hasta el 15 de diciembre de
2025 y los proyectos seleccionados se ejecutarán durante 2026.

La bolsa de recursos financiará entre 8 y 12 investigaciones, con
apoyo individual que oscilará entre USD 80.000 y USD 220.000 por
proyecto. El programa priorizará investigaciones de al menos seis
meses de duración, con enfoque transfronterizo, y que vinculen
datos de flujos financieros con trabajo de campo en territorio.

"La convocatoria responde a una preocupación compartida con nuestros
aliados: el periodismo que rastrea el dinero es el periodismo que
mejor explica cómo operan estas economías, y es justamente el que más
recursos requiere. Queremos que los proyectos tengan tiempo y
músculo", explicó Tomás Iriarte Montoya, director del programa de
periodismo.

Los proyectos serán seleccionados por un comité externo integrado por
editores de *The Washington Post*, *Le Monde*, *La Nación* (Argentina)
y *El Faro* (El Salvador). El proceso de evaluación se realizará en
dos rondas: preselección por país y selección final regional.

Los interesados podrán acceder a los términos completos en el sitio de
la fundación (fundacionandes.org/crimen2026) y a una sesión
informativa virtual el 18 de noviembre de 2025.

*Contacto: Tomás Iriarte Montoya · tiriarte@fundacionandes.org*
""",

"press_releases/2026-02-12-panel-sostenibilidad.md": """\
# Fundación Andes convoca panel sobre sostenibilidad del periodismo en los Andes

*Bogotá, 12 de febrero de 2026.* Fundación Andes realizará el próximo
26 de febrero el panel anual *Sostenibilidad del periodismo en los
Andes: modelos viables, modelos frágiles*, con la participación de
editores de medios de los cuatro países en los que opera la fundación.

El panel se realizará de forma híbrida: presencial en la Universidad
de los Andes (Bogotá) con 220 cupos y transmisión en vivo para
participantes remotos. Los panelistas confirmados son: Juanita León
(La Silla Vacía, Colombia), Ricardo Uceda (IPYS, Perú), Fernanda Torres
(Plan V, Ecuador), y Raúl Peñaranda (Página Siete, Bolivia). Moderará
Elena Mercedes Cárdenas Restrepo, directora ejecutiva de la fundación.

"Esta va a ser la conversación más difícil que hemos tenido en el
programa. Hay medios que llevan tres años sin alcanzar punto de
equilibrio. No tiene sentido convocar este panel para repetir buenas
intenciones. Vamos a exponer los números", dijo Cárdenas Restrepo.

Fundación Andes publicará la grabación completa del panel en acceso
abierto y un documento de síntesis de 12 páginas a mediados de marzo
de 2026. Ambos estarán disponibles bajo licencia Creative Commons.

La inscripción es gratuita y se puede realizar desde el sitio web de
la fundación (fundacionandes.org/panel2026). El programa del evento
incluye una cena de trabajo cerrada el 25 de febrero para 40
directores de medios invitados de los cuatro países.

*Contacto: Elena Mercedes Cárdenas Restrepo · ecardenas@fundacionandes.org*
""",
}


# ---- MoviMed Colombia -------------------------------------------------------

_MOVIMED_COLOMBIA: dict[str, str] = {
"profile.md": """\
# MoviMed Colombia

MoviMed Colombia es una empresa de tecnología en salud fundada en 2021
en Bogotá. Su operación combina unidades móviles de atención primaria
con una plataforma digital de teleconsulta, orientada a poblaciones
urbanas y periurbanas con acceso limitado al sistema de salud
tradicional.

## Qué hacemos

MoviMed opera tres servicios integrados:

- **Unidades móviles de atención primaria**: flota de 11 vehículos
  equipados para consulta médica general, toma de muestras de
  laboratorio, ecografía obstétrica, y vacunación. Operan en rutas
  fijas en Soacha, Bello, Itagüí, Ciudad Bolívar (Bogotá), Kennedy
  (Bogotá) y Bosa. Cada unidad atiende entre 60 y 90 pacientes por día.
- **Teleconsulta general**: plataforma web y app móvil con
  disponibilidad 12 horas al día. Cuenta con un equipo médico propio de
  38 profesionales.
- **Gestión de medicamentos crónicos**: programa de seguimiento y
  entrega domiciliaria para pacientes con hipertensión, diabetes tipo 2
  y enfermedad pulmonar obstructiva crónica. Cuenta con 4.200 pacientes
  activos.

A diciembre de 2025 MoviMed ha atendido a 148.000 pacientes únicos, de
los cuales un 68% reside en áreas clasificadas como estrato
socioeconómico 1 o 2.

## Modelo operativo

MoviMed trabaja principalmente bajo dos modalidades: (1) contratos de
capitación con EPS del régimen contributivo y subsidiado para
atenciones específicas (consulta primaria, toma de laboratorio,
atenciones de baja complejidad); (2) convenios con secretarías de
salud municipales para operar programas focalizados (jornadas de
vacunación, seguimiento a gestantes adolescentes, tamizaje de
enfermedades no transmisibles).

La empresa no atiende población exclusivamente privada; el 93% de su
facturación proviene de contratos con pagadores públicos o mixtos.

## Equipo directivo

- **Dr. Andrés Vargas Ospina**, cofundador y CEO. Médico de la
  Universidad del Rosario con maestría en salud pública de la Escuela
  de Salud Pública de Harvard. Antes trabajó en Fundación Santa Fe de
  Bogotá y como consultor del Banco Interamericano de Desarrollo en
  proyectos de fortalecimiento de atención primaria.
- **Laura Restrepo Piedrahíta**, cofundadora y COO. Ingeniera de
  sistemas de la Universidad Nacional, con trayectoria previa en Rappi
  liderando operaciones de última milla.
- **Dra. Camilo Fernández Lozano**, director médico. Internista y
  especialista en medicina familiar. Coordinó durante ocho años los
  programas de atención primaria en el Hospital Pablo Tobón Uribe.

MoviMed cuenta con una plantilla total de 184 personas, de las cuales
68% son personal asistencial (médicos, enfermeras, auxiliares,
tecnólogos).

## Inversionistas y financiamiento

MoviMed ha cerrado dos rondas de financiación: una ronda semilla de
USD 1,8 millones en 2022 (lidereada por Polymath Ventures) y una serie
A de USD 6,2 millones en 2023 (lidereada por Kaszek Ventures con
participación de Acumen). En 2026 cerró una serie B de USD 14 millones
destinada a expansión geográfica y desarrollo de la línea de
cronicidad.

## Lo que MoviMed no hace

MoviMed no opera servicios de alta complejidad, no tiene camas de
hospitalización, no realiza cirugías. El modelo está deliberadamente
focalizado en atención primaria y ambulatoria. La empresa remite a los
pacientes a la red hospitalaria del sistema cuando se requieren
servicios de mayor complejidad, siguiendo los protocolos del Sistema
General de Seguridad Social en Salud.
""",

"brand_priorities_2026.md": """\
# Prioridades 2026 — MoviMed Colombia

*Documento interno compartido con prensa aliada y socios comerciales
tras el cierre de la serie B de USD 14 millones en febrero de 2026.
Redactado por el equipo directivo.*

La serie B cambia lo que podemos hacer en 2026. El equipo directivo
definió cuatro prioridades estratégicas, con responsable asignado y
meta medible para cada una.

## 1. Expansión geográfica a Barranquilla y el área metropolitana

MoviMed opera hoy en Bogotá, Medellín (área metropolitana) y el sur
del Valle de Aburrá. En 2026 abrimos operación en Barranquilla
(ciudad + municipios de Soledad y Malambo) con una flota inicial de 3
unidades móviles y equipo médico contratado localmente. La operación
arranca en junio con meta de 18.000 pacientes únicos atendidos en el
primer semestre de operación.

*Responsable: Laura Restrepo Piedrahíta (COO)*

## 2. Lanzamiento del programa de cronicidad ampliado

Pasamos de 4.200 a 12.000 pacientes activos en gestión de cronicidad
para fin de año. Esto requiere contratar 22 auxiliares de enfermería
adicionales, integrar 3 nuevas EPS al modelo de capitación, y
desplegar la versión 3.0 de la app de paciente con recordatorios
automatizados y telemetría básica (medición de presión arterial y
glicemia desde dispositivos del hogar).

El programa de cronicidad es el corazón de nuestro caso de impacto.
Un paciente con hipertensión bien controlada cuesta al sistema entre
40% y 55% menos que uno con control inestable.

*Responsable: Dr. Camilo Fernández Lozano (Director Médico)*

## 3. Comunicación sobre resultados en salud

Uno de nuestros retos de 2025 fue que los resultados en salud (control
metabólico, adherencia a medicación, reducción de hospitalizaciones)
no están llegando a las comunidades que podrían beneficiarse. Las
poblaciones que atendemos no llegan a MoviMed por publicidad; llegan
por recomendación de otros pacientes, líderes comunitarios o juntas de
acción comunal.

En 2026 reorientamos nuestra comunicación externa con dos premisas:
hablar donde estas audiencias leen (radio comunitaria, medios
digitales con audiencia local, prensa local) y hacerlo con evidencia
específica (una pieza sobre control de diabetes en Ciudad Bolívar, no
una campaña nacional de marca). Incluso cuando la inversión es más
fragmentada, creemos que este camino genera más valor que una campaña
masiva.

*Responsable: Ana María Herrera (Jefa de Comunicación)*

## 4. Integración de datos clínicos con el sistema público

Una meta técnica y política: integrar nuestra historia clínica
electrónica con el Sistema Integrado de Información de la Protección
Social (SISPRO) para que los pacientes que atendemos tengan continuidad
cuando son referidos al sistema hospitalario. Esto requiere trabajo
normativo con el Ministerio de Salud y desarrollo técnico en los dos
sentidos (extracción e importación).

Meta 2026: integración productiva con al menos tres hospitales
aliados en Bogotá y Medellín, con derivaciones electrónicas por parte
de MoviMed en lugar de referenciación en papel.

*Responsable: Juan Manuel Prieto (CTO)*

## Riesgos que estamos mirando

- La reforma a la salud en curso puede alterar las condiciones del
  contrato de capitación bajo las que operamos. Mantenemos escenarios
  de contingencia.
- La tasa de rotación del personal asistencial en el sector sigue
  siendo alta. Nuestra tasa actual (31%) es peor que nuestra meta
  (menos del 22%).

---

Dr. Andrés Vargas Ospina · CEO · MoviMed Colombia
""",

"past_media_partnerships.md": """\
# Alianzas con medios — MoviMed Colombia

MoviMed trabaja con medios bajo dos premisas: hablar a las audiencias
donde viven (medios locales, radio comunitaria, prensa con audiencia
focalizada) y evitar campañas masivas genéricas que no llegan a las
poblaciones que atendemos. Listamos aquí las colaboraciones más
relevantes de los últimos 18 meses.

## El Espectador — Sección patrocinada "Salud en la cotidianidad"

Agosto-octubre de 2025. Ocho artículos originales producidos por el
equipo editorial de El Espectador, con temas sugeridos por MoviMed
pero control editorial pleno del medio. Los artículos cubrieron:
atención primaria en barrios periféricos de Bogotá, cronicidad en
poblaciones desplazadas, salud mental comunitaria, acceso a salud
para poblaciones LGBTIQ+ en Soacha, entre otros.

Qué funcionó: el formato respetó la línea editorial del medio y produjo
contenido que el equipo de MoviMed no habría escrito bajo una
identidad de marca. La audiencia lectora coincide en geografía con
nuestras zonas de operación.

Qué no funcionó: la medición de impacto directo sobre uso del servicio
MoviMed es débil; las lecturas no se traducen uno a uno en consultas.
Aceptamos esta limitación como costo razonable del formato.

Presupuesto: COP 72 millones (aprox. USD 17.500).

## Semana — Serie especial "Salud mental en Colombia"

Marzo-mayo de 2025. Serie coeditada con Semana sobre salud mental en
zonas urbanas y periurbanas, incluyendo un análisis de acceso a
servicios de salud mental en Medellín y un reportaje sobre el programa
de MoviMed en Itagüí. Semana ejerció control editorial pleno. MoviMed
aportó financiamiento parcial (COP 48 millones) y facilitó acceso a
fuentes y pacientes que aceptaron ser entrevistados (con consentimiento
informado documentado).

## Radio Nacional de Colombia — Cuñas informativas "Cuide su corazón"

Enero-diciembre de 2025. Patrocinio de cuñas de 30 segundos sobre
prevención cardiovascular en emisoras regionales de la RCN y la Radio
Nacional Pública. Este formato tradicional sigue funcionando en
audiencias adultas de estratos 2 y 3 que son el núcleo de nuestro
programa de cronicidad. Presupuesto anual: COP 180 millones.

## La Silla Vacía — Informe sobre cumplimiento normativo en teleconsulta

Junio de 2025. La Silla Vacía publicó un informe sobre el estado
regulatorio de la teleconsulta en Colombia. MoviMed proporcionó datos
operativos y entrevistas con el equipo médico. No hubo pago de por
medio; la colaboración fue de acceso a fuente.

## Criterios para alianzas futuras

- Preferencia por medios con audiencia geográfica coincidente con
  nuestras zonas de operación.
- Rechazo de formatos donde MoviMed pueda ejercer control editorial
  sobre el contenido.
- Disposición a aceptar que la medición de impacto directo es débil en
  formatos editoriales. Aceptamos esa debilidad porque creemos que la
  construcción de confianza es importante y no se mide en clics.
""",

"press_releases/2025-05-20-lanzamiento-soacha-bello.md": """\
# MoviMed amplía operación a Soacha y Bello con servicios de atención primaria móvil

*Bogotá, 20 de mayo de 2025.* MoviMed, empresa de tecnología en salud
con sede en Bogotá, anunció hoy la expansión de su operación a los
municipios de Soacha (Cundinamarca) y Bello (Antioquia), con dos
unidades móviles adicionales por municipio que atenderán a partir del
2 de junio de 2025.

"Soacha y Bello son dos de los municipios con mayor brecha de acceso a
atención primaria de Colombia. En Soacha la disponibilidad de
consulta general tiene un tiempo de espera promedio de 22 días. En
Bello la situación es similar en los barrios periféricos. Nuestra
propuesta es simple: acercar los servicios, no esperar que los
pacientes viajen", dijo el Dr. Andrés Vargas Ospina, CEO de MoviMed.

La operación en Soacha cubrirá inicialmente cinco sectores (Altos de
Cazucá, Compartir, Ciudad Verde, Terreros, San Mateo) y la operación
en Bello cubrirá Niquía, Paris, Zamora y Cabañas. Cada unidad móvil
atenderá entre 50 y 80 pacientes por día, con capacidad para consulta
médica general, toma de muestras de laboratorio, ecografía
obstétrica y vacunación básica.

El lanzamiento incluye un acuerdo con la Secretaría de Salud de
Soacha para priorizar atención a gestantes adolescentes identificadas
por el programa municipal *Soacha Cuida*. MoviMed atenderá en este
marco hasta 1.800 gestantes durante 2025 sin costo adicional para las
pacientes.

"La alianza con MoviMed nos permite llegar con servicios a territorios
donde el hospital municipal no alcanza. Es una complementariedad
operativa, no un reemplazo del sistema", señaló María Elena Torres,
secretaria de Salud de Soacha, durante el acto en la casa de justicia
de Compartir.

MoviMed tiene previsto alcanzar 24.000 pacientes únicos atendidos en
las dos operaciones durante el resto de 2025.

*Contacto: Ana María Herrera · aherrera@movimed.co · (+57) 300 555 4421*
""",

"press_releases/2025-08-14-convenio-salud-bogota.md": """\
# MoviMed firma convenio con la Secretaría Distrital de Salud de Bogotá para atención a poblaciones migrantes

*Bogotá, 14 de agosto de 2025.* MoviMed y la Secretaría Distrital de
Salud de Bogotá firmaron hoy un convenio de cooperación interadministrativa
por valor de COP 3.200 millones que permitirá atender hasta 18.000
pacientes en condición de migración o no regularizada en las
localidades de Kennedy, Bosa y Ciudad Bolívar durante los próximos
doce meses.

El convenio cubre consulta médica general, atención de primera vez,
seguimiento a enfermedades crónicas no transmisibles y atención
obstétrica básica. MoviMed desplegará cuatro unidades móviles
adicionales durante el período del contrato, con cobertura de lunes a
sábado en puntos fijos rotativos.

"Tenemos aproximadamente 280.000 personas en condición de migración
residiendo en Bogotá. Muchas de ellas no han podido afiliarse al
sistema de salud por condiciones administrativas que son ajenas a su
situación clínica. Este convenio cierra parte de esa brecha", dijo
Alejandro Gómez López, secretario Distrital de Salud, durante la
firma realizada en la sede de la Secretaría.

Por MoviMed firmó la Dra. Carolina Fernández Lozano, directora médica.
"Este tipo de convenios requieren claridad sobre qué hace el Estado y
qué hace el operador. Nuestro rol es operativo: poner las unidades, el
personal, los sistemas de información. La rectoría en salud y la
decisión de dónde atender son de la Secretaría", señaló.

El convenio contempla un mecanismo de medición de resultados que será
publicado trimestralmente en el portal de datos abiertos de la
Secretaría. Los indicadores incluyen: pacientes únicos atendidos,
cobertura de vacunación en la población objetivo, y tasa de remisión
efectiva a la red hospitalaria.

La operación bajo este convenio comenzará el 1 de septiembre de 2025.

*Contacto: Ana María Herrera · aherrera@movimed.co*
""",

"press_releases/2025-12-03-reporte-impacto-2025.md": """\
# MoviMed publica su primer reporte anual de impacto: 148.000 pacientes atendidos en 2025

*Bogotá, 3 de diciembre de 2025.* MoviMed publicó hoy su primer reporte
anual de impacto correspondiente al año 2025. El documento, auditado
por Deloitte Colombia, reporta 148.000 pacientes únicos atendidos a
través de unidades móviles y teleconsulta, un crecimiento del 78%
frente al cierre de 2024.

Entre los hallazgos principales del reporte:

- **Control de cronicidad**: de los 4.200 pacientes activos en el
  programa de cronicidad a diciembre de 2025, el 68% alcanzó control
  metabólico según los indicadores clínicos de la Guía de Práctica
  Clínica del Ministerio de Salud (control de presión arterial en
  hipertensión, HbA1c por debajo de 7% en diabetes tipo 2).
- **Acceso**: el 68% de los pacientes atendidos reside en áreas
  clasificadas como estrato 1 o 2, y un 12% adicional como estrato 3.
- **Tiempo de espera**: la mediana del tiempo de espera para consulta
  primaria en los sectores donde opera MoviMed bajó de 22 días (línea
  base enero 2024) a 3 días (diciembre 2025).
- **Retos**: la tasa de deserción del programa de cronicidad se
  mantiene alta (41% al primer año). MoviMed identifica como causa
  principal la movilidad residencial de los pacientes y no factores
  clínicos o de servicio.

"El dato del tiempo de espera es el que más nos motiva a continuar. Y
el de la deserción es el que más nos confronta. Ninguno de los dos se
resuelve con tecnología solamente; requieren trabajo más cercano con
las comunidades", dijo el Dr. Andrés Vargas Ospina, CEO de MoviMed, al
presentar el reporte.

El reporte completo está disponible en el sitio web de MoviMed en
formato abierto. Una síntesis de 16 páginas fue distribuida a las 12
secretarías de salud con las que MoviMed tiene convenio activo y a sus
EPS contratantes.

*Contacto: Ana María Herrera · aherrera@movimed.co*
""",

"press_releases/2026-02-28-ronda-serie-b.md": """\
# MoviMed cierra ronda Serie B de USD 14 millones para expansión regional

*Bogotá, 28 de febrero de 2026.* MoviMed anunció hoy el cierre de una
ronda de financiación Serie B de USD 14 millones, liderada por General
Atlantic con participación de los inversionistas existentes Kaszek
Ventures, Polymath Ventures y Acumen, así como de los nuevos
inversionistas BID Lab y Banistmo Impact Ventures.

Los recursos estarán destinados principalmente a tres usos: expansión
geográfica (apertura de operación en Barranquilla y su área
metropolitana durante 2026), ampliación del programa de gestión de
enfermedades crónicas a 12.000 pacientes activos antes de fin de año, e
integración tecnológica con el Sistema Integrado de Información de la
Protección Social (SISPRO).

"Esta ronda nos permite pasar de operar en dos ciudades principales
(Bogotá y el área metropolitana del Valle de Aburrá) a operar en tres
y consolidar nuestro modelo de cronicidad, que es la línea que más
impacto clínico genera por peso invertido", dijo el Dr. Andrés Vargas
Ospina, CEO y cofundador de MoviMed.

Con esta ronda, MoviMed ha levantado USD 22 millones en capital de
riesgo desde su fundación en 2021. La empresa tiene hoy 184 empleados
directos y 46 profesionales de salud contratistas.

General Atlantic, la firma líder de la ronda, invierte en MoviMed a
través de su fondo de América Latina. "MoviMed es un caso raro en la
región: tiene tanto indicadores clínicos verificables como un modelo
comercial sostenible. Esa combinación no se encuentra fácil", dijo
Martín Escobari, co-presidente de General Atlantic, en un comunicado.

MoviMed tendrá su junta directiva ampliada a nueve miembros con la
llegada de dos nuevos representantes de los inversionistas entrantes.

*Contacto: Ana María Herrera · aherrera@movimed.co*
""",
}


# ---- Grupo Éxito Café -------------------------------------------------------

_GRUPO_EXITO_CAFE: dict[str, str] = {
"profile.md": """\
# Grupo Éxito Café

Grupo Éxito Café es la línea especializada en café de origen del Grupo
Éxito, lanzada en 2020 como una unidad independiente dentro de la
vertical de marcas propias del conglomerado retail colombiano. Opera
tiendas físicas dedicadas, una línea de suscripción de café tostado, y
abastecimiento directo desde fincas en el Eje Cafetero, Huila, Nariño y
Tolima.

## Operaciones

- **Tiendas físicas**: 14 tiendas en Medellín, Bogotá, Cali,
  Barranquilla y Cartagena. Cinco son tiendas insignia con barras de
  servicio de especialidad; las otras nueve funcionan como puntos de
  venta con servicio simplificado.
- **Tostión**: planta de tostión en Envigado (Antioquia) con capacidad
  de 180 toneladas anuales, certificada SCA (Specialty Coffee
  Association) y con operación bajo estándares ISO 22000.
- **Línea de suscripción Origen Único**: servicio mensual de café de
  origen único, con cohortes cuatrimestrales de producto rotando
  orígenes (Huila, Nariño, Tolima, Antioquia). Lanzada en marzo de
  2025; cuenta con 8.200 suscriptores activos a febrero de 2026.
- **Programa de abastecimiento directo**: relación comercial con 62
  caficultores en seis departamentos, con precios al menos 18% sobre el
  precio de mercado y contratos anuales renovables.

## Equipo directivo

- **Juan Diego Arango Restrepo**, director general. Antes de Grupo
  Éxito Café dirigió la línea de productos frescos de Almacenes Éxito
  durante siete años. Administrador de empresas de EAFIT con MBA del
  IESE (Barcelona).
- **Isabella Márquez Hoyos**, directora de Abastecimiento y Sourcing.
  Ingeniera agrónoma de la Universidad Nacional de Colombia, sede
  Medellín. Q-Grader certificada por la SCA desde 2018. Antes trabajó
  en Nespresso en el programa AAA Sustainable Quality.
- **Felipe Zuluaga Torres**, director de Marca y Experiencia. Antes
  fue jefe de mercadeo de Juan Valdez Café; diseñador industrial de
  la Universidad Pontificia Bolivariana.

El equipo total de Grupo Éxito Café suma 148 personas, incluyendo
personal de tiendas, tostión, abastecimiento, y administrativos.

## Producto y calidad

La propuesta de valor de Grupo Éxito Café se construye sobre tres
elementos: (1) trazabilidad completa desde finca hasta taza, visible al
cliente mediante código QR en el empaque; (2) relación directa con
caficultores sin intermediarios comerciales, lo que permite pagar
precios superiores al mercado C; (3) curación de microlotes de
especialidad con puntaje SCA mínimo de 84.

La línea regular de supermercado (café molido para cafetera de goteo)
sigue operando bajo la marca Surtimax del Grupo Éxito y no pertenece a
Grupo Éxito Café.

## Relación con el Grupo Éxito

Grupo Éxito Café opera con autonomía operativa y marca separada, pero
comparte con la matriz: (a) infraestructura logística de distribución,
(b) canales digitales (sitio web, e-commerce), (c) servicios
compartidos administrativos. La matriz mantiene el 100% de la propiedad
y sus decisiones estratégicas se validan con el comité de marcas
propias del Grupo.

## Lo que no hacemos

Grupo Éxito Café no produce café instantáneo ni cápsulas compatibles con
sistemas cerrados. No ofrece servicio de catering corporativo ni
máquinas de oficina. La operación se concentra en venta de grano tostado
y experiencias de consumo en tienda física.
""",

"brand_priorities_2026.md": """\
# Prioridades 2026 — Grupo Éxito Café

*Extracto del plan estratégico presentado por Juan Diego Arango
Restrepo al comité de marcas propias del Grupo Éxito en enero de 2026.
Compartido con socios comerciales y medios aliados.*

En 2025 pasamos de ser un piloto interesante a ser una línea de negocio
con músculo propio. En 2026 queremos tres cosas: crecer donde tiene
sentido, cerrar el círculo con los caficultores que nos abastecen, y
evitar errores típicos de escalamiento en tiendas físicas.

## 1. Apertura en Bucaramanga y Cartagena

Abrimos dos tiendas nuevas en 2026: una en Cabecera de Bucaramanga
(segundo trimestre) y otra en el casco histórico de Cartagena (tercer
trimestre). Son ciudades donde estudios de demanda nos dicen que hay
audiencia para café de especialidad sin la competencia saturada de
Medellín y Bogotá. Meta de rentabilidad: punto de equilibrio en el
décimo mes de operación.

*Responsable: Luisa Fernanda Montes (Gerente de Operaciones Retail)*

## 2. Suscripción Origen Único: triplicar base

Pasamos de 8.200 suscriptores activos (febrero 2026) a 25.000
suscriptores al cierre del año. Este crecimiento requiere tres ajustes:
expansión de capacidad de tostión en Envigado (obra ya iniciada),
revisión del empaque para reducir gramos desperdiciados en envío (dato
que recibimos de clientes recurrentes), y ampliación de los canales de
adquisición fuera del ecosistema digital del Grupo Éxito.

*Responsable: Felipe Zuluaga Torres (Director de Marca)*

## 3. Programa "Vereda a Taza" para 2027

Durante 2026 desarrollamos el programa *Vereda a Taza*, que en 2027
permitirá a clientes suscritos visitar las fincas de los productores de
su cohorte y participar en una cosecha guiada. Estamos trabajando con
ocho productores aliados en Huila, Nariño y Antioquia para definir
logística, capacidad y certificación sanitaria.

Inversión 2026: COP 380 millones para infraestructura receptiva en
fincas y capacitación de productores como anfitriones.

## 4. Comunicación: salir de la burbuja del café especializado

Un reto honesto: nuestro marketing de 2024-2025 habló bien a la
audiencia que ya sabía de café de origen, pero mal a audiencias que
todavía consumen café comercial y podrían apreciar el producto. En
2026 rediseñamos la comunicación con foco en tres mensajes: (a) la
historia del productor específico (no del país en abstracto), (b) la
diferencia real de taza sin jerga técnica, (c) el precio. No queremos
ocultar que cuesta más.

Presupuesto de medios 2026: COP 1.650 millones, distribuido 35% en
medios de estilo de vida (Revista Semana, Revista Diners), 30% en
prensa gastronómica especializada (La Barra, Axioma), 25% en medios
regionales de las ciudades donde abrimos tiendas, 10% en redes
sociales.

## 5. Reducir desperdicio en tienda

Medimos por primera vez en 2025 el desperdicio diario de café preparado
en las cinco tiendas insignia: 6,8% del café tostado consumido se
desperdicia (café preparado no servido, mermas de extracción, granos
vencidos). La meta 2026 es bajar a 3,5%.

*Responsable: Luisa Fernanda Montes*

## Lo que no vamos a hacer

- No vamos a lanzar cápsulas compatibles con sistemas cerrados en
  2026, aunque nos lo han propuesto. Creemos que la curva de consumo
  colombiano de café de especialidad todavía está en grano y molido, y
  las cápsulas introducen tensiones de sostenibilidad que no queremos
  gestionar ahora.
- No vamos a abrir tiendas en centros comerciales tipo *food court*
  sin barras de preparación. La experiencia en tienda es parte de la
  promesa de marca.

---

Juan Diego Arango Restrepo · Director General · Grupo Éxito Café
""",

"past_media_partnerships.md": """\
# Alianzas con medios — Grupo Éxito Café

Grupo Éxito Café ha trabajado con medios durante 2024-2025
principalmente bajo formato editorial patrocinado y con foco en
audiencias de estilo de vida premium. Listamos aquí las colaboraciones
relevantes del último ciclo para efectos de análisis interno y
transparencia con socios nuevos.

## Revista Diners — Columna mensual "Del grano a la taza"

Enero-diciembre de 2025. Doce piezas publicadas, una por mes, escritas
por periodistas gastronómicos de la revista con acceso al programa de
abastecimiento de Grupo Éxito Café y a cuatro productores aliados del
programa. Las piezas incluyeron: perfil de Doña Amparo (caficultora de
Salgar, Antioquia), análisis del perfil sensorial del Gesha de Huila,
historia del Bourbon Rosado en Nariño, reportaje sobre barismo femenino
en Medellín.

Qué funcionó: Diners tiene una audiencia exactamente coincidente con
nuestro cliente objetivo. El formato de columna mensual mantuvo la
marca presente sin saturar. Las piezas generaron 1.600 clics
cualificados al sitio de la suscripción Origen Único.

Presupuesto: COP 68 millones.

## Revista Semana — Serie "Café Colombia 2025"

Agosto-noviembre de 2025. Serie de seis artículos en Semana sobre el
estado actual de la caficultura colombiana, con foco en sostenibilidad,
relevo generacional y cambio climático. Grupo Éxito Café aportó
financiamiento parcial (COP 52 millones) y facilitó acceso a
productores de su red. Semana ejerció control editorial pleno y publicó
dos piezas que fueron críticas con prácticas estándar del sector
cafetero colombiano — prácticas en las que Grupo Éxito Café no
participa.

## La Barra — Patrocinio del Concurso Nacional de Baristas 2025

Agosto-octubre de 2025. Patrocinio principal del Concurso Nacional de
Baristas organizado por la revista La Barra y la Cámara Colombiana de
Café. El evento reunió a 38 baristas finalistas en Bogotá y fue
transmitido en vivo. Grupo Éxito Café aportó el premio mayor (viaje de
formación a Specialty Coffee Expo en Estados Unidos, valor COP 22
millones) y los microlotes usados en la ronda final.

Qué funcionó: el concurso visibiliza un oficio que es central a nuestra
propuesta de marca. El retorno en reconocimiento dentro de la
comunidad barista profesional justifica la inversión.

## Axioma — Contenidos técnicos sobre procesos post-cosecha

Febrero-mayo de 2025. Serie de cuatro artículos en la revista técnica
Axioma sobre nuevas variedades y procesos post-cosecha en Colombia.
Audiencia profesional (caficultores, tostadores, baristas). La serie
fue coeditada con tres investigadores de Cenicafé y produjo contenido
técnico que Grupo Éxito Café no habría producido sola.

## Decisiones editoriales que hemos rechazado

En 2024-2025 rechazamos tres propuestas de medios: un reality show
sobre un barista de Éxito Café por considerarlo poco alineado con la
marca; una pauta display estándar en un portal gastronómico con
tráfico comprado; y una columna firmada en un medio de turismo que
habría requerido opinar sobre política pública cafetera, terreno que
consideramos no nos corresponde.
""",

"press_releases/2025-03-15-lanzamiento-origen-unico.md": """\
# Grupo Éxito Café lanza suscripción Origen Único con café de cuatro departamentos

*Medellín, 15 de marzo de 2025.* Grupo Éxito Café anunció hoy el
lanzamiento de Origen Único, un servicio mensual de suscripción de
café tostado que cada cuatro meses rota el origen departamental del
producto. La primera cohorte, disponible desde hoy, incluye café Gesha
de la finca La Esperanza en Acevedo (Huila), perfilado con proceso
natural.

"La propuesta no es simplemente un club de café. Es una invitación a
seguir a un productor específico durante un ciclo completo de cosecha
y a tomar café con historia trazable. Nos tomó tres años de trabajo
con los productores llegar al estándar de volumen y calidad que este
producto requiere", dijo Juan Diego Arango Restrepo, director general
de Grupo Éxito Café, durante el lanzamiento en la tienda insignia de
El Poblado.

La suscripción está disponible en dos formatos: 250 gramos mensuales
(COP 58.000) y 500 gramos mensuales (COP 108.000). Cada envío incluye
una ficha técnica con información del productor, variedad, altura,
proceso, perfil sensorial, y un código QR que enlaza al video de
presentación del productor.

Las cuatro cohortes del primer año rotarán: Huila (marzo-junio),
Nariño (julio-octubre), Antioquia (noviembre-febrero) y Tolima
(marzo-junio 2026). Los productores de cada cohorte reciben el 100% del
sobreprecio de especialidad pagado por Grupo Éxito Café, sin
intermediación de exportadores comerciales.

Isabella Márquez Hoyos, directora de abastecimiento, explicó los
criterios de selección: "Trabajamos solo con microlotes que alcanzan
mínimo 84 puntos SCA, con fincas que cumplen con los estándares del
programa de abastecimiento directo que construimos desde 2022. No
buscamos el café más caro; buscamos el más honesto en su trazabilidad".

La suscripción inicia con una capacidad de 3.000 suscriptores y
escalará gradualmente según la capacidad de tostión en la planta de
Envigado, que opera actualmente al 62% de su capacidad instalada.

*Contacto: Catalina Ruiz · cruiz@grupoexitocafe.co · (+57) 4 604 0000
ext. 2283*
""",

"press_releases/2025-09-10-apertura-poblado.md": """\
# Grupo Éxito Café abre su tercera tienda insignia en El Poblado

*Medellín, 10 de septiembre de 2025.* Grupo Éxito Café inauguró hoy su
tercera tienda insignia, ubicada en la carrera 43A con calle 7 sur en
El Poblado (Medellín). La nueva tienda, de 340 metros cuadrados,
incluye barra de preparación de especialidad, espacio de tostión en
sitio para lotes pequeños, y zona de cata abierta al público con
capacidad para 18 personas.

"Abrir en El Poblado es una decisión deliberada. No es por accesibilidad
al cliente premium; es por accesibilidad a gente que trabaja en café
profesionalmente. Queríamos una tienda donde un barista, un tostador o
un Q-Grader pueda entrar sin pedirle permiso a nadie", dijo Juan Diego
Arango Restrepo, director general.

La tienda integra dos elementos nuevos frente a las insignias anteriores
en Bogotá y Cali: una tostadora Probat de 5 kilos visible desde la
barra que permite que los clientes presencien tostión en vivo los
martes y jueves; y un programa de cupping gratuito los sábados por la
mañana, con cupo limitado a 12 asistentes por sesión y moderado por
Isabella Márquez Hoyos, directora de abastecimiento y Q-Grader
certificada.

El diseño interior fue realizado por el estudio Taller Síntesis
(Medellín) con materiales locales: paneles de madera de tabla reciclada
de construcción antioqueña, mesas de concreto pulido fabricadas en
Envigado, y luminarias hechas por el taller Toro en la comuna 13.

La tienda empleará 14 personas en planta — 8 baristas, 2 tostadores, 1
Q-Grader, 2 de caja y 1 gerente — con una rotación prevista por turno
que permite operar desde las 7:00 am hasta las 9:30 pm.

Con esta apertura, Grupo Éxito Café alcanza 14 tiendas a nivel nacional
y emplea 148 personas en toda su operación.

*Contacto: Catalina Ruiz · cruiz@grupoexitocafe.co*
""",

"press_releases/2025-11-25-alianza-jerico.md": """\
# Grupo Éxito Café firma acuerdo con 12 caficultores del suroeste antioqueño

*Jericó, 25 de noviembre de 2025.* Grupo Éxito Café y la Asociación de
Caficultores de Jericó (ASCAFÉ-Jericó) firmaron hoy un acuerdo de
abastecimiento directo por tres años que cubre a 12 caficultores
certificados bajo el programa de Grupo Éxito Café. El acuerdo, firmado
en la sede de la Cooperativa de Caficultores de Andes en Jericó, prevé
una compra anual mínima de 14.800 kilogramos de café verde de alta
especialidad.

"Este tipo de acuerdos son los que permiten planear la finca a tres
años. No es solo el precio — que ayuda — es saber cuánto se va a
vender. Eso cambia desde cómo se maneja el lote hasta cómo se planea
la renovación del cultivo", dijo Don Hernando Velásquez, presidente de
ASCAFÉ-Jericó y caficultor en la vereda La Pintada desde hace 34 años.

El acuerdo reconoce un sobreprecio del 22% sobre el precio interno del
mercado colombiano al momento de cada cosecha, con prima adicional por
puntaje SCA: 84 puntos mínimo (precio base), 85-86 puntos (+6%), 87+
puntos (+12%). Isabella Márquez Hoyos, directora de abastecimiento de
Grupo Éxito Café, indicó que esta estructura de incentivos busca
remunerar la calidad sin castigar a productores que no alcanzan el
puntaje máximo.

El acuerdo incluye acompañamiento técnico anual por parte del equipo
agronómico de Grupo Éxito Café en prácticas de manejo post-cosecha
(beneficio, secado, almacenamiento), áreas donde la Asociación
identificó oportunidades de mejora durante el diagnóstico inicial
realizado en enero de 2025.

Los cafés del acuerdo aparecerán en la cohorte Antioquia de la
suscripción Origen Único durante la temporada noviembre 2025 -
febrero 2026, y selectivamente en la barra de las tiendas insignia de
Grupo Éxito Café.

*Contacto: Catalina Ruiz · cruiz@grupoexitocafe.co*
""",

"press_releases/2026-02-18-concurso-baristas.md": """\
# Grupo Éxito Café convoca el Concurso Nacional de Baristas 2026

*Medellín, 18 de febrero de 2026.* Grupo Éxito Café anunció hoy la
convocatoria oficial del Concurso Nacional de Baristas 2026, que se
realizará en Bogotá del 28 al 30 de mayo en la sede de la Cámara
Colombiana de Café. La convocatoria está abierta hasta el 15 de
abril.

"Este es el segundo año que organizamos el concurso con La Barra. En
2025 recibimos 142 postulaciones; este año esperamos superar los 180.
La calidad viene subiendo y ya hay baristas jóvenes que se preparan
todo el año para este momento", dijo Felipe Zuluaga Torres, director
de marca de Grupo Éxito Café, en el anuncio realizado en la tienda
insignia de El Poblado.

El concurso tendrá tres categorías: latte art, preparación manual
(V60, Chemex, prensa francesa, Aeropress), y creación libre con
producto Origen Único. Cada categoría premia al primer lugar con COP
8 millones y al segundo con COP 4 millones. El ganador absoluto de la
categoría de creación libre obtiene un viaje de formación a la
Specialty Coffee Expo 2026 en Portland, Oregón.

Los 18 finalistas del concurso serán seleccionados por un jurado
técnico compuesto por tres Q-Graders certificados (dos colombianos y
uno mexicano, que se confirma en marzo) a partir de videos enviados
durante la fase de postulación. La ronda final será evaluada por
jurado ampliado y transmitida en vivo por los canales de redes
sociales de La Barra y Grupo Éxito Café.

La convocatoria está abierta a cualquier barista residente en
Colombia con mínimo un año de experiencia profesional verificable. La
postulación es gratuita y se realiza a través del formulario del sitio
web de La Barra.

*Contacto: Catalina Ruiz · cruiz@grupoexitocafe.co · (+57) 4 604 0000
ext. 2283*
""",
}


SPONSORS: dict[str, dict[str, str]] = {
    "bancolombia-verde":  _BANCOLOMBIA_VERDE,
    "fundacion-andes":    _FUNDACION_ANDES,
    "movimed-colombia":   _MOVIMED_COLOMBIA,
    "grupo-exito-cafe":   _GRUPO_EXITO_CAFE,
}


def write_all_sponsors(rng: random.Random, sponsors_dir: Path) -> int:
    """Write every sponsor's markdown files under sponsors_dir/<slug>/.

    `rng` is accepted for parity with other generators; sponsor content
    is static per run so it isn't used. Returns the total file count
    written.
    """
    del rng
    count = 0
    for slug in sorted(SPONSORS.keys()):
        files = SPONSORS[slug]
        base = sponsors_dir / slug
        for rel_path in sorted(files.keys()):
            content = files[rel_path]
            _check_banned(content, f"{slug}/{rel_path}")
            # Sanity: every press release must contain at least one
            # quoted speaker. Catches silent template regressions.
            if "press_releases/" in rel_path and '"' not in content and "dijo" not in content.lower():
                raise RuntimeError(
                    f"press release {slug}/{rel_path} is missing a quoted speaker"
                )
            target = base / rel_path
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(content, encoding="utf-8")
            count += 1
    return count


# Characters like fancy quotes/dashes can slip through when copy-pasting;
# keep a smoke test that the filter only uses ASCII lowercase in phrases.
assert all(unicodedata.is_normalized("NFC", p) for p in _BANNED_PHRASES)
