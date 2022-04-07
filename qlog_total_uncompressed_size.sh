#!/bin/bash

find ./data -name '*.qlog.gz' -exec sh -c "gzip -l {} | grep -oP '\d.*'" \; | awk '{s+=$2} END {print s}'