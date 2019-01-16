#!/bin/bash

if [ -z "$INTERPROSCAN" ]; then
  python /MultiLoc2/src/multiloc2_prediction.py -fasta=$1 -origin=$2 -predictor=$3 -result=$4
else
  $INTERPROSCAN/interproscan.sh -i $1 -o $5 -format TSV -goterms -iprlookup --tempdir $7
  python /MultiLoc2/src/multiloc2_prediction.py -fasta=$1 -origin=$2 -predictor=$3 -result=$4 -go=$5
fi

echo "Done" > $6
