#!/bin/bash

cd /ml2jobs

find . -mtime +14 -type f -delete
find . -mtime +14 -type d -exec rm -Rf {} +
