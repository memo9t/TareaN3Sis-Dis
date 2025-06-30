-- ── pig_processing/incidentes.pig ──


SET fs.defaultFS hdfs://localhost:9000;


incidentes_raw = LOAD '/incidentes/clean_incidents.csv'
    USING PigStorage(',')
    AS (
      type:chararray, 
      location:chararray, 
      timestamp:chararray, 
      description:chararray, 
      comuna:chararray
    );

encabezado = FILTER incidentes_raw BY type == 'type';
datos_sin_encabezado = FILTER incidentes_raw BY type != 'type';


separado = FOREACH datos_sin_encabezado GENERATE 
    type, 
    FLATTEN(STRSPLIT(location, ',')) AS (lat:chararray, lon:chararray), 
    timestamp, 
    comuna;

agrupado = GROUP separado BY (comuna, type);


conteo = FOREACH agrupado GENERATE 
    FLATTEN(group) AS (comuna, tipo), 
    COUNT(separado) AS cantidad;

STORE conteo INTO '/incidentes/output/conteo_por_comuna_tipo' USING PigStorage(',');
