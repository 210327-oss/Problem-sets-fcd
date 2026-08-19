# Problem-sets-fcd
Tareas del curso de "FUNDAMENTOS DE CIENCIA DE DATO"

# Parte 1
En base a estas lecturas, ***explica los aspectos de la plataforma que caen dentro de la metodología CRISP-DM y aquellas que se necesitan mirar desde el paper de Martínez-Plumed***

# $\color{red}{\textbf{De CRISP-DM a las Trayectorias de Ciencia de Datos (DST): El caso de Michelangelo en Uber}}$

## Contenido
 
- [Michelangelo bajo el marco CRISP-DM](#michelangelo-bajo-el-marco-crisp-dm)
- [Los límites de CRISP-DM y la entrada del marco DST](#los-límites-de-crisp-dm-y-la-entrada-del-marco-dst)
- [Conclusión](#conclusión)

La plataforma de Inteligencia Artificial de Uber, Michelangelo, ilustra la transición metodológica desde la minería de datos tradicional hacia las plataformas integradas de Ciencia de Datos a gran escala. A través del análisis de su diseño original en 2017 y su posterior evolución hacia la Inteligencia Artificial Generativa en 2024, es posible identificar qué componentes se ajustan al ciclo tradicional de CRISP-DM y cuáles exigen ser interpretados mediante el marco de **Trayectorias de Ciencia de Datos (DST)** propuesto por Martínez-Plumed et al.

### Michelangelo bajo el marco CRISP-DM
CRISP-DM estructuró la analítica de datos como un ciclo de vida de seis fases jerárquicas e iterativas enfocado en proyectos individuales. El flujo de trabajo original de Michelangelo mapea con precisión estas fases para automatizar la ejecución de modelos predictivos de extremo a extremo.

En la fase de comprensión del negocio y de los datos, Michelangelo traduce necesidades operativas de Uber como la estimación de tiempos de llegada (ETA), tarifas dinámicas, detección de fraude o recomendaciones en Uber Eats en problemas formales de aprendizaje automático, conectándose al Data Lake corporativo (HDFS/Hive) y a flujos en tiempo real (Kafka) para auditar la información antes del entrenamiento.

Para la preparación de datos, la plataforma introdujo el **Feature Store (Palette)**, automatizando la extracción, transformación y limpieza mediante un lenguaje DSL y motores distribuidos (Spark en la capa offline y Samza/Cassandra en la capa online), garantizando consistencia entre el entrenamiento y la inferencia.

En las fases de modelado y evaluación, Michelangelo estandarizó el entrenamiento de modelos tabulares (XGBoost, modelos lineales), series temporales y redes neuronales, automatizando la búsqueda de hiperparámetros y generando reportes de rendimiento (curvas ROC, AUC, RMSE) y pruebas de retroceso (_backtesting_).

Finalmente, el despliegue y monitoreo se resolvieron mediante servicios de inferencia online de baja latencia o procesos batch, cerrando el ciclo con el rastreo continuo de las predicciones para detectar la degradación del modelo y el desplazamiento de variables (_feature drift_).

### Los límites de CRISP-DM y la entrada del marco DST
Aunque CRISP-DM explica con claridad el ciclo procedimental de un modelo aislado, resulta insuficiente para abordar Michelangelo como una plataforma multi-inquilino, evolutiva e interconectada. La metodología DST cubre estas limitaciones al incorporar tres dimensiones: **Gestión de Datos/Infraestructura, Exploración Abierta y Gobernanza Organizacional.**

En la dimensión de gestión de datos e infraestructura, la preparación de datos deja de ser un paso puntual de cada proyecto para convertirse en una trayectoria de valor continua. En Michelangelo, el Feature Store no prepara datos para un único algoritmo, sino que actúa como un catálogo centralizado donde las características son compartidas y reutilizadas por múltiples equipos, gestionando la infraestructura como un producto independiente. Asimismo, en ***Michelangelo 2.0***, la integración de modelos de lenguaje exigió la creación del **Gen AI Gateway**, un componente encargado del enmascaramiento de datos personales (PII), auditoría de peticiones, enrutamiento, cuotas y control de costos, lo cual encaja directamente en la categoría de gestión de riesgos y liberación de datos descrita por Martínez-Plumed et al.

En cuanto a la exploración abierta, CRISP-DM presupone la existencia de metas de negocio fijas y predefinidas antes de iniciar el proyecto. Por el contrario, DST contempla trayectorias inquisitivas donde la prospección de datos genera nuevas oportunidades de producto que no estaban planeadas inicialmente. La evolución de Michelangelo hacia el Deep Learning y la IA Generativa transformó el desarrollo de una tubería rígida a un proceso altamente exploratorio basado en embeddings, fine-tuning, arquitecturas RAG y prompt engineering, donde los desarrolladores investigan capacidades técnicas antes de definir la meta final del producto. Adicionalmente, el paso hacia el paradigma de **"Modelo como Código"**, respaldado por un monorrepositorio, permitió la ramificación (branching), revisión de código e iteraciones no secuenciales, superando la visión unidireccional del estándar del año 2000.

En la gobernanza organizacional, la asignación de recursos dentro de Michelangelo también requiere la perspectiva de DST, la cual modela la interacción entre perfiles técnicos (ingenieros de datos, ingenieros de ML, científicos aplicados) y la jerarquización de proyectos. Michelangelo 2.0 categoriza las iniciativas mediante un sistema de tiering según su impacto en el negocio, garantizando soporte técnico y acuerdos de nivel de servicio (_SLA_) diferenciados. Del mismo modo, la plataforma supera la evaluación técnica puntual de CRISP-DM (centrada en AUC o RMSE) al implementar un sistema de calidad holístico que mide la frescura de los datos, la latencia de inferencia, la reproducibilidad y la observabilidad operativa.

### Conclusión
La trayectoria de Michelangelo demuestra que CRISP-DM resulta plenamente funcional para estructurar el ciclo de vida técnico de un modelo predictivo particular: sus seis fases siguen describiendo con precisión cómo se transforma una necesidad de negocio en un modelo entrenado, evaluado y desplegado. Sin embargo, al observar la plataforma como un todo y no como la suma de proyectos aislados esa estructura lineal deja de capturar buena parte de lo que ocurre dentro de Uber. La administración de un ecosistema industrializado y escalable de Inteligencia Artificial requiere la perspectiva de Martínez-Plumed et al., que integra la gestión de infraestructura, la exploración no lineal y la gobernanza organizacional como elementos insustituibles para el valor continuo de los datos.

Esta distinción tiene implicaciones prácticas: adoptar solo la lógica de CRISP-DM llevaría a tratar cada iniciativa como un proyecto autocontenido, subestimando el Feature Store como activo compartido, la naturaleza exploratoria del desarrollo con modelos de lenguaje y la necesidad de priorizar recursos entre equipos. DST, en cambio, describe cómo las organizaciones maduras operan en dos planos: el técnico, donde CRISP-DM sigue vigente por modelo, y el estratégico, donde infraestructura, exploración y gobernanza determinan si esa capacidad se traduce en valor sostenido. Ambos marcos, entonces, son complementarios y de distinta escala.

---
## Referencias
 
- Wirth, R., & Hipp, J. (2000). *CRISP-DM: Towards a standard process model for data mining*. 
- Martínez-Plumed, F., Contreras-Ochando, L., Ferri, C., Hernández-Orallo, J., Kull, M., Lachiche, N., Ramírez-Quintana, M. J., & Flach, P. (2021). *CRISP-DM twenty years later: From data mining processes to data science trajectories*. 
