#!/bin/bash

#----------------------------------
# Important Settings
#----------------------------------

if [ -z "$ABI_SERVICES_CONTACT_MAIL" ]
then
  contact_email="abi-services@informatik.uni-tuebingen.de"
else
  contact_email="$ABI_SERVICES_CONTACT_MAIL"
fi

if [ -z "$ABI_SERVICES_IMPRINT_URL" ]
then
  imprint_url="https://www-abi.informatik.uni-tuebingen.de/imprint"
else
  imprint_url="$ABI_SERVICES_IMPRINT_URL"
fi

if [ -z "$ABI_SERVICES_GDPR_URL" ]
then
  gdpr_url="https://www-abi.informatik.uni-tuebingen.de/gdpr"
else
  gdpr_url="$ABI_SERVICES_GDPR_URL"
fi

if [ -z "$ABI_SERVICES_MULTILOC2_PORT" ]
then
  multiloc2_port="28020"
else
  multiloc2_port="$ABI_SERVICES_MULTILOC2_PORT"
fi


#----------------------------------
# Start MultiLoc2 Daemon Container
#----------------------------------

# Without an InterProScan installation remove the volume mount flag and
# the flag for the INTERPROSCAN environment variable

docker run --rm -it -d -p $multiloc2_port:80 \
           -e ML_CONTACT_EMAIL="$contact_email" \
           -e ML_IMPRINT_URL="$imprint_url" \
           -e ML_GDPR_URL="$gdpr_url" \
           -e INTERPROSCAN="/interproscan" \
           -v /local/abi_webservices/interproscan-5.29-68.0:/interproscan \
           --name abi_webservice_multiloc2 multiloc2
