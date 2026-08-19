# Problem-sets-fcd
Tareas del curso de "FUNDAMENTOS DE CIENCIA DE DATO"

# Parte 1
En base a estas lecturas, ***explica los aspectos de la plataforma que caen dentro de la metodología CRISP-DM y aquellas que se necesitan mirar desde el paper de Martínez-Plumed***

## De CRISP-DM a las Trayectorias de Ciencia de Datos (DST): El caso de Michelangelo en Uber  

La plataforma de Inteligencia Artificial de Uber, Michelangelo, ilustra la transición metodológica desde la minería de datos tradicional hacia las plataformas integradas de Ciencia de Datos a gran escala. A través del análisis de su diseño original en 2017 y su posterior evolución hacia la Inteligencia Artificial Generativa en 2024, es posible identificar qué componentes se ajustan al ciclo tradicional de CRISP-DM y cuáles exigen ser interpretados mediante el marco de **Trayectorias de Ciencia de Datos (DST)** propuesto por Martínez-Plumed et al.

### Michelangelo bajo el marco CRISP-DM
CRISP-DM estructuró la analítica de datos como un ciclo de vida de seis fases jerárquicas e iterativas enfocado en proyectos individuales. El flujo de trabajo original de Michelangelo mapea con precisión estas fases para automatizar la ejecución de modelos predictivos de extremo a extremo.

En la fase de comprensión del negocio y de los datos, Michelangelo traduce necesidades operativas de Uber —como la estimación de tiempos de llegada (ETA), tarifas dinámicas, detección de fraude o recomendaciones en Uber Eats— en problemas formales de aprendizaje automático, conectándose al Data Lake corporativo (HDFS/Hive) y a flujos en tiempo real (Kafka) para auditar la información antes del entrenamiento.

Para la preparación de datos, la plataforma introdujo el **Feature Store (Palette)**, automatizando la extracción, transformación y limpieza mediante un lenguaje DSL y motores distribuidos (Spark en la capa offline y Samza/Cassandra en la capa online), garantizando consistencia entre el entrenamiento y la inferencia.

En las fases de modelado y evaluación, Michelangelo estandarizó el entrenamiento de modelos tabulares (XGBoost, modelos lineales), series temporales y redes neuronales, automatizando la búsqueda de hiperparámetros y generando reportes de rendimiento (curvas ROC, AUC, RMSE) y pruebas de retroceso (_backtesting_).

Finalmente, el despliegue y monitoreo se resolvieron mediante servicios de inferencia online de baja latencia o procesos batch, cerrando el ciclo con el rastreo continuo de las predicciones para detectar la degradación del modelo y el desplazamiento de variables (_feature drift_).
