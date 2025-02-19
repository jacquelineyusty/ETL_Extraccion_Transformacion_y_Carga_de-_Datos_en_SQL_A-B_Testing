ETL: Extracción, Transformación y Carga de Datos en SQL

📚 Descripción del Proyecto

Este proyecto implementa un proceso ETL (Extract, Transform, Load) para la extracción, limpieza, transformación y carga de datos en una base de datos SQL, facilitando su acceso y consulta para futuros análisis. El objetivo es estructurar los datos de manera eficiente para mejorar la toma de decisiones y optimizar el rendimiento de consultas.

⚙️ Tecnologías Utilizadas

Python: Pandas, NumPy, Seaborn, Matplotlib

Machine Learning: Scikit-learn (SimpleImputer, IterativeImputer, KNNImputer)

Bases de Datos: MySQL

Conectividad: MySQL Connector

🔄 Flujo del Proceso ETL

1. Extracción (Extract)

Se obtienen datos desde:

Archivos CSV

Se utilizan conectores como Pandas, MySQL Connector para acceder a la información.

2. Transformación y Limpieza (Transform)

Una vez extraídos los datos, se aplican los siguientes procesos:

Gestón de valores nulos: Imputación usando SimpleImputer, IterativeImputer, KNNImputer.

Normalización y estandarización: Ajuste de formatos y unidades.

Conversión de tipos de datos: Garantiza compatibilidad con SQL.

Codificación de variables categóricas.

Visualización y análisis exploratorio con Seaborn y Matplotlib.

3. Carga en Base de Datos (Load)

Los datos procesados se almacenan en una base de datos MySQL, asegurando:

Estructura optimizada mediante esquemas relacionales.

Creación de índices y claves foráneas para mejorar el rendimiento.

Carga incremental o completa usando scripts de automatización.

📊 Visualización de Datos

Para validar la calidad de los datos y el impacto de las transformaciones, se generan:

Gráficos de distribución de datos.

Matrices de correlación entre variables.

Reportes de calidad de datos.

🚀 Futuras Mejoras

✨ Implementación de pipelines con Apache Airflow.

✨ Optimización del almacenamiento mediante particionamiento.

✨ Integración con herramientas como Power BI o Tableau.

✨ Implementación de un sistema de monitoreo de calidad de datos.


🔗 Instalación y Uso

Requisitos

Python 3.x

MySQL

Librerías: Pandas, NumPy, Seaborn, Matplotlib, Scikit-learn, MySQL Connector

Instalación

Clona el repositorio 

git clone https://github.com/jacquelineyusty/analisis_datos_A-B

Ejecución del Proceso ETL

Ejecuta el script principal para iniciar el proceso ETL:

python etl.py

📂 Estructura del Repositorio

<img src="https://github.com/jacquelineyusty/recursos/blob/main/estructura.PNG" width="250" />


🎬 Autor

Jacqueline Yusty Espinosa - www.linkedin.com/in/jacquelineyusti
