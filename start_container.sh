#!/bin/bash

#----------------------------------
# Important Settings
#----------------------------------

# Enter a valid eMail address that allows to contact the responsible colleague for this webservice
if [ -z "$ABI_SERVICES_CONTACT_MAIL" ]
then
  contact_email="abi-services@informatik.uni-tuebingen.de"
else
  contact_email="$ABI_SERVICES_CONTACT_MAIL"
fi

# Enter a valid URL that leads to the appropriate imprint page
if [ -z "$ABI_SERVICES_IMPRINT_URL" ]
then
  imprint_url="https://www-abi.informatik.uni-tuebingen.de/imprint"
else
  imprint_url="$ABI_SERVICES_IMPRINT_URL"
fi

# Enter a valid URL that leads to the appropriate GDPR declaration page
if [ -z "$ABI_SERVICES_GDPR_URL" ]
then
  gdpr_url="https://www-abi.informatik.uni-tuebingen.de/gdpr"
else
  gdpr_url="$ABI_SERVICES_GDPR_URL"
fi

# Here you can set an upper limit for the number of sequences allowed to be submitted
if [ -z "$ABI_SERVICES_MULTILOC2_MAX_SEQ" ]
then
  multiloc2_max_seq="20"
else
  multiloc2_max_seq="$ABI_SERVICES_MULTILOC2_MAX_SEQ"
fi

# Here you can specify th host port that is bound to port 80 from the container
if [ -z "$ABI_SERVICES_MULTILOC2_PORT" ]
then
  multiloc2_port="28020"
else
  multiloc2_port="$ABI_SERVICES_MULTILOC2_PORT"
fi


#----------------------------------
# Start MultiLoc2 Daemon Container
#----------------------------------

# Without an InterProScan installation remove the volume mount flag

docker run --rm -it -d -p $multiloc2_port:80 \
           -e ML_CONTACT_EMAIL="$contact_email" \
           -e ML_IMPRINT_URL="$imprint_url" \
           -e ML_GDPR_URL="$gdpr_url" \
           -e ML_MAX_SEQ="$multiloc2_max_seq" \
           -v /local/abi_webservices/interproscan-5.29-68.0:/interproscan \
           --name abi_webservice_multiloc2 multiloc2
