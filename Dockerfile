# Applied Bioinformatics Group
# MultiLoc2 Docker Image
#
# Philipp Thiel

FROM ubuntu:18.04

# Update package repository
RUN apt-get update
RUN apt-get -y upgrade

# ----------------------------------------------------------
# Install LibSVM and BLAST
# ----------------------------------------------------------
RUN apt-get install -y libsvm-tools
RUN apt-get install -y ncbi-blast+ ncbi-blast+-legacy


# ----------------------------------------------------------
# Install InterProScan dependencies
# ----------------------------------------------------------
RUN apt-get install -y -q dirmngr software-properties-common \
                          perl python python3 vim wget

RUN add-apt-repository -y ppa:webupd8team/java
RUN apt-get update

#RUN echo oracle-java8-installer shared/accepted-oracle-license-v1-1 select true | debconf-set-selections
#RUN apt-get install -y -q --no-install-recommends oracle-java8-installer
#RUN apt-get install -y -q oracle-java8-set-default

#ENV JAVA_HOME=/usr/lib/jvm/java-8-oracle
#ENV CLASSPATH=/usr/lib/jvm/java-8-oracle/bin


# ----------------------------------------------------------
# Install MultiLoc2
# ----------------------------------------------------------

ADD MultiLoc2 /MultiLoc2

WORKDIR /MultiLoc2

RUN python configureML2.py
RUN chmod +x run_multiloc2.sh


# ----------------------------------------------------------
# Test MultiLoc2
# Also generates BLASTp databases!
# ----------------------------------------------------------

RUN ./run_multiloc2.sh test.fasta animal test.res
