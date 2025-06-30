# Tarea2
Este proyecto corresponde al segundo entregable del curso de Sistemas Distribuidos. En esta etapa se realiza el procesamiento distribuido de eventos de tráfico obtenidos desde Waze, utilizando un enfoque modular basado en contenedores Docker.

## Estructura del Proyecto
├── docker-compose.yml

├── data/

│ └── clean_incidents.csv

├── filtering/

│ ├── Dockerfile

│ └── filter.py

├── pig_processing/

│ ├── Dockerfile

│ ├── incidentes.pig

│ └── start.sh

├── scraper/

│ ├── Dockerfile

│ └── scraper.py


##  Tecnologías utilizadas

- Python (para scraping y filtrado)
- Apache Pig (para procesamiento distribuido)
- Docker y Docker Compose (para orquestación de servicios)
- Hadoop (como entorno de ejecución de Pig)
- CSV (formato de almacenamiento intermedio)

Para ejecutar el sistema, asegúrate de tener Docker y Docker Compose instalados en tu máquina. Luego, sigue los siguientes pasos:

##Clona este repositorio:
```sql
git clone https://github.com/tu_usuario/tu_repositorio.git
cd tu_repositorio
```
## Instrucciones de Ejecución

1. **Construir los contenedores**
```sql
    docker compose build
```
3. **Ejecutar el Scraper**
 ```sql
   docker compose run scraper
```
4. **Ejecutar el filtrado y homogeneización**
```sql
    docker compose run filtering
   ```
6. **Ejecutar el procesamiento distribuido con Apache Pig**
```sql
   docker compose run pig_processing
   ```
## Descripción de los Módulos
scraper/: Extrae los eventos de tráfico desde Waze (mapa en vivo).

filtering/: Elimina duplicados, normaliza datos y agrupa incidentes similares.

pig_processing/: Realiza análisis distribuido utilizando scripts en Apache Pig (conteos por comuna, tipo, análisis temporal, etc.).

data/: Contiene archivos intermedios o resultados, como clean_incidents.csv.
