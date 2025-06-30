FROM ubuntu:20.04

ENV DEBIAN_FRONTEND=noninteractive
ENV HADOOP_VERSION=3.3.6
ENV PIG_VERSION=0.17.0


RUN apt-get update && \
    apt-get install -y openjdk-8-jdk wget ssh rsync python3 procps && \
    rm -rf /var/lib/apt/lists/*


RUN wget https://downloads.apache.org/hadoop/common/hadoop-${HADOOP_VERSION}/hadoop-${HADOOP_VERSION}.tar.gz && \
    tar -xzf hadoop-${HADOOP_VERSION}.tar.gz && \
    mv hadoop-${HADOOP_VERSION} /opt/hadoop && \
    rm hadoop-${HADOOP_VERSION}.tar.gz


RUN wget https://downloads.apache.org/pig/pig-${PIG_VERSION}/pig-${PIG_VERSION}.tar.gz && \
    tar -xzf pig-${PIG_VERSION}.tar.gz && \
    mv pig-${PIG_VERSION} /opt/pig && \
    rm pig-${PIG_VERSION}.tar.gz


ENV JAVA_HOME=/usr/lib/jvm/java-8-openjdk-amd64
ENV HADOOP_HOME=/opt/hadoop
ENV HADOOP_CONF_DIR=$HADOOP_HOME/etc/hadoop
ENV PATH=$PATH:$HADOOP_HOME/bin:$HADOOP_HOME/sbin:$HADOOP_HOME/jars
ENV PIG_HOME=/opt/pig
ENV PATH=$PATH:$PIG_HOME/bin


RUN echo "export JAVA_HOME=$JAVA_HOME" >> $HADOOP_CONF_DIR/hadoop-env.sh

# Configuración mínima de Hadoop
RUN sed -i 's@<configuration>@<configuration> \
    <property><name>fs.defaultFS</name><value>hdfs://localhost:9000</value></property> \
    <property><name>dfs.replication</name><value>1</value></property>@' $HADOOP_CONF_DIR/core-site.xml

RUN sed -i 's@<configuration>@<configuration> \
    <property><name>dfs.name.dir</name><value>/var/hadoop/hdfs/namenode</value></property> \
    <property><name>dfs.data.dir</name><value>/var/hadoop/hdfs/datanode</value></property>@' $HADOOP_CONF_DIR/hdfs-site.xml

RUN echo "export HADOOP_OPTS=\"-Djava.net.preferIPv4Stack=true\"" >> $HADOOP_CONF_DIR/hadoop-env.sh


RUN mkdir -p /var/hadoop/hdfs/namenode && \
    mkdir -p /var/hadoop/hdfs/datanode


RUN mkdir /var/run/sshd && \
    echo 'root:root' | chpasswd && \
    sed -i 's/#PermitRootLogin prohibit-password/PermitRootLogin yes/' /etc/ssh/sshd_config && \
    echo "StrictHostKeyChecking no" >> /etc/ssh/ssh_config && \
    ssh-keygen -t rsa -P "" -f ~/.ssh/id_rsa && \
    cat ~/.ssh/id_rsa.pub >> ~/.ssh/authorized_keys && \
    chmod 600 ~/.ssh/authorized_keys


WORKDIR /scripts
COPY pig_processing/incidentes.pig /scripts/
COPY pig_processing/start.sh /scripts/
RUN chmod +x /scripts/start.sh


VOLUME ["/data"]


EXPOSE 22 9000 50070 9870 8088

CMD service ssh start && /scripts/start.sh

