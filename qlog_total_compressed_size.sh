#!/bin/bash

find ./data -name '*.qlog.gz' -exec sh -c "gzip -l {} | grep -oP '\d.*'" \; | awk '{s+=$1} END {print s}'