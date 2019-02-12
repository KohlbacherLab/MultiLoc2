# Applied Bioinformatics Group
# MultiLoc2 Docker Image
#
# Philipp Thiel

FROM ubuntu:14.04

# Update package repository
RUN apt-get update
#RUN apt-get -y upgrade


# ----------------------------------------------------------
# Install some useful and required stuff
# ----------------------------------------------------------
RUN apt-get install -y dirmngr software-properties-common vim wget


# ----------------------------------------------------------
# Install LibSVM and BLAST
# ----------------------------------------------------------
RUN apt-get install -y libsvm-tools ncbi-blast+


# ----------------------------------------------------------
# Install InterProScan dependencies
# ----------------------------------------------------------
RUN apt-get install -y libgnutls28

RUN add-apt-repository -y ppa:webupd8team/java
RUN apt-get update

RUN echo oracle-java8-installer shared/accepted-oracle-license-v1-1 select true | debconf-set-selections
RUN apt-get install -y -q --no-install-recommends oracle-java8-installer
RUN apt-get install -y -q oracle-java8-set-default

ENV JAVA_HOME=/usr/lib/jvm/java-8-oracle
ENV CLASSPATH=/usr/lib/jvm/java-8-oracle/bin


# ----------------------------------------------------------
# Setup MultiLoc2 Webservice
# ----------------------------------------------------------
RUN apt-get -y install python-biopython apache2
RUN a2enmod cgid
ADD webservice/apache2.conf         /etc/apache2/apache2.conf
ADD webservice/serve-cgi-bin.conf   /etc/apache2/conf-available/serve-cgi-bin.conf

COPY webservice/webloc.cgi   /var/www/html/cgi-bin/
COPY webservice/downloads/   /var/www/html/cgi-bin/downloads/
COPY webservice/images/      /var/www/html/cgi-bin/images/
COPY MultiLoc2/data/multiloc2_datasets.tar.bz2 /var/www/html/cgi-bin/downloads/multiloc2_datasets.tar.bz2

RUN mkdir /webservice
ADD webservice/ml2setup.py  /webservice/ml2setup.py
ADD webservice/multiloc2_entrypoint.sh  /webservice/multiloc2_entrypoint.sh

RUN mkdir /ml2jobs
RUN chmod 777 /ml2jobs

# ----------------------------------------------------------
# Install MultiLoc2
# ----------------------------------------------------------
COPY MultiLoc2 /MultiLoc2
WORKDIR /MultiLoc2
RUN python configureML2.py
RUN chmod +x run_multiloc2.sh

# Generate the reusable BLAST databases!
#RUN ./run_multiloc2.sh test.fasta animal test.res

WORKDIR /
RUN  chown -R www-data:www-data /MultiLoc2
RUN  chmod -R 775 /MultiLoc2


EXPOSE 80

CMD ["sh", "/webservice/multiloc2_entrypoint.sh"]
