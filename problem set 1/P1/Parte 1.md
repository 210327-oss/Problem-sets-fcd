# Problem-sets-fcd
Tareas del curso de "FUNDAMENTOS DE CIENCIA DE DATO"

# <span style="color:red;">La Evolución de Michelangelo: De CRISP-DM a las Trayectorias de Ciencia de Datos</span>

## Índice

1. [Introducción](#introducción)
2. [Michelangelo bajo la metodología CRISP-DM](#1-michelangelo-bajo-la-metodología-crisp-dm)
3. [Michelangelo bajo el marco de Trayectorias de Ciencia de Datos (DST)](#2-michelangelo-bajo-el-marco-de-trayectorias-de-ciencia-de-datos-dst)
   - [2.1 Gestión de datos e infraestructura central](#21-actividades-de-gestión-de-datos-e-infraestructura-central)
   - [2.2 Actividades exploratorias y evolución del negocio](#22-actividades-exploratorias-y-evolución-del-negocio)
   - [2.3 No linealidad, "Model Iteration as Code" e IA generativa](#23-no-linealidad-model-iteration-as-code-e-ia-generativa)
4. [CRISP-DM vs. DST: cuadro comparativo](#3-crisp-dm-vs-dst-cuadro-comparativo)
5. [Conclusión](#conclusión)
6. [Referencias Bibliográficas](#referencias-bibliográficas)

---

## Introducción

La evolución de **Michelangelo**, la plataforma interna de *Machine Learning as a Service* (MLaaS) de Uber, desde sus inicios en 2016 con modelos predictivos tabulares hasta su estado actual —integrando Inteligencia Artificial Generativa y LLMs a través de un **Gen AI Gateway**— refleja con claridad la propia evolución de las metodologías analíticas en las últimas décadas.

Para analizar la plataforma en toda su dimensión, es necesario diferenciar entre:

- Las capacidades que responden al **ciclo de vida analítico tradicional** (CRISP-DM).
- Aquellas que corresponden a los **ecosistemas modernos de ciencia de datos a gran escala** (Trayectorias de Ciencia de Datos, DST).

---

## 1. Michelangelo bajo la metodología CRISP-DM

La metodología **CRISP-DM** (*CRoss Industry Standard Process for Data Mining*) concibe los proyectos de analítica como un proceso cíclico estructurado en seis fases: Comprensión del Negocio, Comprensión de los Datos, Preparación de Datos, Modelado, Evaluación y Despliegue. Es un enfoque **orientado a objetivos** (*goal-directed*) y guiado por procesos, que asume que se parte de un problema de negocio claro para transformar datos en modelos predictivos.

Los flujos de trabajo clave de Michelangelo —especialmente en sus inicios y en casos de uso predictivos como el ETA de viajes, los tiempos de entrega en UberEats o el cálculo de tarifas dinámicas— se ajustan directamente a esta estructura:

| Fase CRISP-DM | Implementación en Michelangelo |
|---|---|
| **Comprensión del negocio y de los datos** | Traduce métricas operativas en problemas de regresión o clasificación; facilita la recolección y exploración inicial de variables (ej. tiempos de preparación de comida, ubicación del pedido). |
| **Preparación de datos** | Núcleo más estandarizado de la plataforma: el **Feature Store** (Apache Spark, Samza, Cassandra) estandariza pipelines de limpieza, transformación y unión de atributos, tanto en *batch* como en *streaming*. |
| **Modelado** | Automatiza el entrenamiento masivo de algoritmos (XGBoost, modelos lineales, redes neuronales con Horovod). |
| **Evaluación** | Genera informes estandarizados (curvas ROC, precisión-recall, matrices de confusión); incluye **Manifold** para la depuración visual de modelos. |
| **Despliegue** | Publicación en producción con un solo clic, en contenedores de predicción de baja latencia o *offline*, garantizando escalabilidad. |

> **En síntesis:** CRISP-DM explica con precisión la canalización analítica individual de Michelangelo para problemas predictivos cerrados, donde el ciclo *problema de negocio → datos → modelo → despliegue* sigue una secuencia lógica orientada a una meta preconcebida.

---

## 2. Michelangelo bajo el marco de Trayectorias de Ciencia de Datos (DST)

Aunque CRISP-DM es adecuado para proyectos predictivos aislados, resulta **insuficiente** para explicar la complejidad de una plataforma viva e integrada como Michelangelo. Martínez-Plumed et al. (2019) argumentan que la ciencia de datos moderna ha trascendido los procesos rígidamente dirigidos por metas para dar paso a las **Trayectorias de Ciencia de Datos** (*Data Science Trajectories*, DST): un paradigma caracterizado por la exploración no lineal, el uso intensivo de infraestructura y la reusabilidad continua de los activos de datos.

### 2.1 Actividades de gestión de datos e infraestructura central

En CRISP-DM, la base de datos se percibe como un repositorio estático dentro del proceso. En el modelo DST, las actividades de infraestructura son **continuas y transversales** a toda la organización:

| Actividad DST | Aplicación en Michelangelo |
|---|---|
| **Arquitectura e ingesta de datos** | El Feature Store no se construye para un único proyecto: es una arquitectura distribuida que ingiere millones de eventos en tiempo real, compartida por más de **400 proyectos analíticos**. |
| **Simulación de datos** | Aplicada en analítica de percepción y cartografía 3D (vehículos autónomos): genera y procesa simulaciones de entornos complejos para preguntas *what-if* o entrenamiento con escenarios sintéticos. |
| **Publicación de datos** | A través de **Gallery** (registro centralizado de modelos y metadatos) y el Feature Store, los datos y modelos se gestionan como productos reutilizables "publicados" internamente para múltiples equipos. |

### 2.2 Actividades exploratorias y evolución del negocio

El framework DST introduce un ciclo exterior de actividades exploratorias donde la meta no siempre está prefijada y los descubrimientos en los datos pueden redirigir el proyecto:

| Actividad DST | Aplicación en Michelangelo |
|---|---|
| **Exploración de metas y del valor de los datos** | Con la IA Generativa (2023 en adelante), los equipos no siempre parten de una meta predictiva fija; exploran capacidades emergentes como soporte automatizado al cliente, resúmenes de incidencias o asistentes de código interno. |
| **Exploración de resultados y narrativas** | **Manifold** permite explorar el comportamiento del modelo en distintos subconjuntos de datos, detectar sesgos o fallos puntuales y comunicar narrativas explicables a usuarios no técnicos. |
| **Exploración de producto** | Desarrollo de experiencias de usuario complejas y del **Gen AI Gateway**, que gestiona la interacción con LLMs comerciales y modelos de código abierto ajustados (Hugging Face, DeepSpeed). |

### 2.3 No linealidad, "Model Iteration as Code" e IA generativa

Frente a la noción de CRISP-DM de que el "Despliegue" es el paso final del proyecto, Michelangelo opera bajo trayectorias dinámicas e iterativas:

- **Monorrepositorio e iteración como código:** la plataforma adopta metodologías ágiles de ingeniería de software, donde el modelo se itera como código dentro de monorrepositorios. Las pruebas A/B, el *shadow deployment* y el monitoreo de *feature drift* retroalimentan continuamente el ciclo, rompiendo la secuencia rígida tradicional.
- **Gobernanza y Gen AI Gateway:** en la fase de IA Generativa cobran relevancia actividades ausentes en CRISP-DM pero centrales en DST, como la auditoría de peticiones, la redacción automática de datos personales (PII), el control de costes en tiempo real y las políticas de seguridad para LLMs.

---

## 3. CRISP-DM vs. DST: cuadro comparativo

| Dimensión | CRISP-DM | DST (Martínez-Plumed et al.) |
|---|---|---|
| **Naturaleza del proceso** | Cíclico, pero orientado a una meta fija (*goal-directed*) | No lineal, exploratorio, tipo trayectoria |
| **Punto de partida** | Problema de negocio predefinido | Meta y valor de los datos se descubren durante el proceso |
| **Gestión de datos** | Repositorio estático dentro del proyecto | Infraestructura continua y transversal (ej. Feature Store compartido por +400 proyectos) |
| **Fase final** | Despliegue, como cierre del proyecto | Iteración continua ("Model Iteration as Code"), A/B testing, *shadow deployment*, monitoreo de *drift* |
| **Alcance organizacional** | Proyecto individual y acotado | Plataforma transversal y reutilizable (Gallery, Feature Store) |
| **Actividades emergentes (IA Gen.)** | No contempladas | Auditoría, redacción de PII, control de costes, políticas de seguridad LLM (Gen AI Gateway) |

---

## Conclusión

La metodología **CRISP-DM** ofrece un excelente esquema táctico para estructurar el desarrollo paso a paso de un modelo predictivo individual dentro de Michelangelo. Su lógica secuencial —comprensión del negocio, preparación de datos, modelado, evaluación y despliegue— sigue siendo perfectamente vigente para explicar casos de uso acotados y cerrados, como el cálculo de un ETA o una tarifa dinámica, donde existe un objetivo de negocio claro desde el inicio.

Sin embargo, esta misma linealidad es también su principal limitación: CRISP-DM fue concebido para proyectos individuales de minería de datos, no para plataformas que operan como ecosistemas vivos a escala organizacional. Es aquí donde el marco de **Trayectorias de Ciencia de Datos** de Martínez-Plumed et al. resulta indispensable, pues permite capturar tres fenómenos que CRISP-DM simplemente no contempla: (1) la infraestructura de datos como un activo **continuo y transversal** —el Feature Store no pertenece a un proyecto, sino a más de 400 de ellos simultáneamente—; (2) la existencia de un **ciclo exploratorio** donde la meta de negocio no siempre precede al análisis, sino que emerge de él, como ocurre con los casos de uso de IA Generativa; y (3) la **no linealidad** del ciclo de vida del modelo, que se itera como código, se somete a pruebas A/B y *shadow deployment*, y se retroalimenta de forma constante en lugar de "cerrarse" en el despliegue.

En este sentido, ambos marcos no son excluyentes sino complementarios y operan en niveles distintos de análisis: CRISP-DM funciona como una **lente de zoom** para entender el ciclo de vida de un modelo individual dentro de Michelangelo, mientras que las Trayectorias de Ciencia de Datos funcionan como una **lente panorámica** que explica cómo esos ciclos individuales se entrelazan, comparten infraestructura y coexisten con actividades exploratorias, de gobernanza y de gestión de riesgo propias de la era de la IA Generativa. Comprender Michelangelo exige, por tanto, integrar ambas perspectivas: la disciplina metodológica de CRISP-DM para el detalle operativo, y la visión estratégica de DST para entender la plataforma como un organismo evolutivo capaz de escalar desde el aprendizaje supervisado tradicional hasta la integración avanzada de LLMs a nivel global.

---

## Referencias Bibliográficas

- Hermann, J., & Del Balso, M. (2017, 5 de septiembre). *Meet Michelangelo: Uber's Machine Learning Platform*. Uber Engineering Blog. https://www.uber.com/blog/michelangelo-machine-learning-platform/

- Martínez-Plumed, F., Contreras-Ochando, L., Ferri, C., Hernández-Orallo, J., Kull, M., Lachiche, N., Quintana, R. M., & Ramírez-Quintana, M. J. (2021). CRISP-DM Twenty Years Later: From Data Mining Processes to Data Science Trajectories. *IEEE Transactions on Knowledge and Data Engineering*, 33(8), 3048–3061. https://doi.org/10.1109/TKDE.2019.2962680

- Shearer, C. (2000). The CRISP-DM model: the new blueprint for data mining. *Journal of Data Warehousing*, 5(4), 13–22.

- Uber Engineering. (2023). *Generative AI at Uber: Building a Gen AI Gateway*. Uber Engineering Blog. https://www.uber.com/blog/generative-ai-uber/
