#!/bin/bash

if [ -z "$INTERPROSCAN" ]; then
  python /MultiLoc2/src/multiloc2_prediction.py -fasta=$1 -origin=$2 -result=$3
else
  $INTERPROSCAN/interproscan.sh -cli -i $1 -o interpro.out -format raw -goterms -iprlookup
  python /MultiLoc2/src/multiloc2_prediction.py -fasta=$1 -origin=$2 -result=$3 -go=interpro.out
fi
