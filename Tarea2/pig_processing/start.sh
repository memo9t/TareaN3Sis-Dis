#!/bin/bash
set -e


export HDFS_NAMENODE_USER=root
export HDFS_DATANODE_USER=root
export HDFS_SECONDARYNAMENODE_USER=root
export YARN_RESOURCEMANAGER_USER=root
export YARN_NODEMANAGER_USER=root

echo "[pig_processing] Formateando namenode..."
hdfs namenode -format -force

echo "[pig_processing] Iniciando HDFS..."
start-dfs.sh

echo "[pig_processing] Iniciando YARN..."
start-yarn.sh

echo "[pig_processing] Esperando archivo /data/clean_incidents.csv..."
while [ ! -f /data/clean_incidents.csv ]; do
  sleep 5
done

echo "[pig_processing] Copiando CSV limpio a HDFS..."
hdfs dfs -mkdir -p /incidentes
hdfs dfs -put -f /data/clean_incidents.csv /incidentes/clean_incidents.csv

echo "[pig_processing] Ejecutando Pig..."
pig -x mapreduce /scripts/incidentes.pig

echo "[pig_processing] Pig finalizó. Manteniendo contenedor activo para revisar logs."
tail -f /dev/null
