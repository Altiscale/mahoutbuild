#!/bin/bash

# TBD: honor system pre-defined property/variable files from 
# /etc/hadoop/ and other /etc config for spark, hdfs, hadoop, etc

if [ "x${JAVA_HOME}" = "x" ] ; then
  export JAVA_HOME=/usr/java/default
fi
if [ "x${ANT_HOME}" = "x" ] ; then
  export ANT_HOME=/opt/apache-ant
fi
if [ "x${MAVEN_HOME}" = "x" ] ; then
  export MAVEN_HOME=/opt/apache-maven
fi
if [ "x${M2_HOME}" = "x" ] ; then
  export M2_HOME=/opt/apache-maven
fi
if [ "x${MAVEN_OPTS}" = "x" ] ; then
  export MAVEN_OPTS="-Xmx2048m -XX:MaxPermSize=1024m"
fi
if [ "x${SCALA_HOME}" = "x" ] ; then
  export SCALA_HOME=/opt/scala
fi


export PATH=$PATH:$M2_HOME/bin:$SCALA_HOME/bin:$ANT_HOME/bin:$JAVA_HOME/bin

# Define defau;t spark uid:gid and build version
# WARNING: the MAHOUT_VERSION branch name does not align with the Git branch name branch-0.8 / trunk
if [ "x${MAHOUT_USER}" = "x" ] ; then
  export MAHOUT_USER=mahout
fi
if [ "x${MAHOUT_GID}" = "x" ] ; then
  export MAHOUT_GID=411460000
fi
if [ "x${MAHOUT_UID}" = "x" ] ; then
  export MAHOUT_UID=411460025
fi
if [ "x${MAHOUT_VERSION}" = "x" ] ; then
  export MAHOUT_VERSION=trunk_20140328
fi

# Customize build OPTS for MVN
export MAVEN_OPTS="-Xmx2048m -XX:MaxPermSize=1024m"




