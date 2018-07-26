## MultiLoc2
### Bioinformatics tool for predicting subcellular localizations of eukaryotic proteins

Travis CI  
[![Build Status](https://travis-ci.org/KohlbacherLab/MultiLoc2.svg?branch=master)](https://travis-ci.org/KohlbacherLab/MultiLoc2)  

This repository mainly provides a containerized installation of MultiLoc2 using Docker.  
In order to install the software elsewhere please read the instructions in the  
[README](MultiLoc2/README) file of the YLoc source folder and have a look in the Dockerfile.  


**Citing & Further Information**  

If you use MultiLoc2 please cite the following publications:

Blum T., Briesemeister S., and Kohlbacher O. (2009)  
[MultiLoc2: integrating phylogeny and Gene Ontology terms improves subcellular protein localization prediction.](https://doi.org/10.1186/1471-2105-10-274)  
BMC Bioinformatics, 10:274
  
  
**Requirements**  

- Linux OS
- Docker


**Installation**

The easiest option is to build the Docker image from this repository using the following steps:  
` $ git clone https://github.com/KohlbacherLab/MultiLoc2.git`  
` $ docker build --no-cache -t <your_image_name> MultiLoc2/`  

**MultiLoc2 Usage (Interactively in container)**  

MultiLoc2 general usage:  
` $ python yloc.py <fasta_file> <model_name> <prediction_id(optional)> <print_result(y/n)(optional)>`  

MultiLoc2 can print the usage description and available models by executing  
` $ python yloc.py`  

**Running MultiLoc2 Using Docker run**  

You can either start your container interactively and run YLoc  
` $ docker run --rm -it <your_image_name> /bin/bash`  
`root@<some_hash>:/YLoc# python yloc.py test.fasta "some_model"`  


