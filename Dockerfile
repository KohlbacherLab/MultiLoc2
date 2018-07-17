# Applied Bioinformatics Group
# MultiLoc2 Docker Image
# Based on Ubuntu 18.04 LTS
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
# Install InterProScan depdendencies
# ----------------------------------------------------------
RUN apt-get install -y -q \
    dirmngr \
    software-properties-common \
    libboost-iostreams-dev libboost-system-dev libboost-filesystem-dev \
    zlibc gcc-multilib apt-utils zlib1g-dev python \
    cmake tcsh build-essential g++ git wget gzip perl

RUN add-apt-repository -y ppa:webupd8team/java && apt-get update

RUN echo oracle-java8-installer shared/accepted-oracle-license-v1-1 select true | /usr/bin/debconf-set-selections
RUN apt-get install -y -q oracle-java8-installer
RUN apt-get install -y -q oracle-java8-set-default

ENV JAVA_HOME=/usr/lib/jvm/java-8-oracle
ENV CLASSPATH=/usr/lib/jvm/java-8-oracle/bin

#RUN wget ftp://ftp.ebi.ac.uk/pub/software/unix/iprscan/5/5.30-69.0/interproscan-5.30-69.0-64-bit.tar.gz
#RUN wget ftp://ftp.ebi.ac.uk/pub/software/unix/iprscan/5/5.30-69.0/interproscan-5.30-69.0-64-bit.tar.gz.md5
#RUN md5sum -c interproscan-5.30-69.0-64-bit.tar.gz.md5
#RUN tar -pxvzf interproscan-5.30-69.0-*-bit.tar.gz
#RUN ln -s /interproscan-5.30-69.0/interproscan.sh /usr/bin/iprscan


# ----------------------------------------------------------
# Install MultiLoc2
# ----------------------------------------------------------

ADD multiloc2 /multiloc2
