#!/bin/bash

#----------------------------------
# Start MultiLoc2 Daemon Container
#----------------------------------

contact_email="abi-services@informatik.uni-tuebingen.de"
imprint_url="https://www-abi.informatik.uni-tuebingen.de/imprint"
gdpr_url="https://www-abi.informatik.uni-tuebingen.de/gdpr"

docker run --rm -it -d -p 28020:80 \
           -e ML_CONTACT_EMAIL="$contact_email" \
           -e ML_IMPRINT_URL="$imprint_url" \
           -e ML_GDPR_URL="$gdpr_url" \
           -e INTERPROSCAN="/interproscan" \
           -v /local/abi_webservices/interproscan-5.29-68.0:/interproscan \
           --name abi_webservice_multiloc2 multiloc2
