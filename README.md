#  Sistema Distribuido de Análisis de Tráfico con Waze + Big Data

Este proyecto implementa una **arquitectura distribuida modular** para la recolección, almacenamiento, análisis y visualización de eventos de tráfico obtenidos desde la plataforma **Waze**, utilizando tecnologías como **Docker, MongoDB, Apache Pig, Elasticsearch y Kibana**.

## Descripción General

El sistema extrae información georreferenciada en tiempo real desde Waze (vía API GeoRSS), la almacena en MongoDB, y luego la somete a procesos de filtrado, análisis distribuido con Hadoop + Pig y visualización con Kibana, generando métricas clave sobre patrones de tráfico y eficiencia del sistema de caché.

---

## Arquitectura Modular

| Módulo                     | Funcionalidad                                                                 |
|---------------------------|-------------------------------------------------------------------------------|
| `scraper`                 | Recolecta eventos en tiempo real desde Waze (alerts, traffic, users).         |
| `almacenamiento`          | Almacena los eventos crudos en MongoDB.                                       |
| `cache`                   | Simula políticas LRU y LFU con distribución uniforme y Zipf, midiendo hits.   |
| `filtrado`                | Limpia y homogeneiza los datos antes de su análisis.                          |
| `pig_processing`          | Procesa datos de forma distribuida usando Apache Pig sobre Hadoop.            |
| `visualización`           | Indexa métricas en Elasticsearch y genera dashboards con Kibana.              |

---

##  Tecnologías

- **Python 3.10**
- **MongoDB 5**
- **Apache Pig + Hadoop**
- **Elasticsearch 8.6.2**
- **Kibana 8.6.2**
- **Docker + Docker Compose**

---

##  Instalación

### Requisitos previos

- Docker y Docker Compose instalados
- Conexión a internet para consultar la API de Waze

### Clonar el repositorio

```bash
git clone https://github.com/memo9t/TareaN3Sis-Dis.git
cd Tarea2
```
### Levantar los servicios

```bash
sudo docker compose build
sudo docker compose up -d

```

Esto iniciará todos los contenedores necesarios:

- mongo_waze: almacenamiento de eventos
- elasticsearch: motor de búsqueda
- kibana: visualización
- waze_scraper: recolección y simulación de caché
- waze_filter: limpieza de datos
- hadoop_pig: procesamiento distribuido

###  Espera unos minutos mientras se recolectan los eventos y se procesan los datos
Puedes seguir los logs del scraper con:

```bash
sudo docker logs -f waze_scraper
```

##  Acceder a las visualizaciones

Una vez levantado todo, accede a Kibana por tu navegador con :
http://localhost:5601

En Kibana, ve a:
- Ve a Management → Stack Management → Index Patterns
- Crea un nuevo patrón: metricas_cache*
- Define timestamp como el campo de tiempo
- Ahora puedes ir a Visualize → Create visualization → Lens y crear:
- Gráfico de pastel por política (LRU vs LFU)
- Barras comparando hit_rate según distribución (zipf, uniform)
- Líneas de evolución temporal de hits/misses



##  Pruebas del Sistema

Las métricas de cache se envían automáticamente a Elasticsearch después de cada simulación. El procesamiento Pig corre luego del filtrado, y genera resultados que podrían extenderse para análisis más profundos.









