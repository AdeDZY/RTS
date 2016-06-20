#!/bin/bash

LIST=$1
M=$2

for line in $(cat ${LIST}); do
    echo ${line}
    STEM=$(basename "${line}" .gz)
    condor_run "gunzip -c /bos/data0/twitter/spritzer/${line} > tmp/${STEM}"
    condor_run "./get_text.py tmp/${STEM} output/text_${M}s/${STEM}.txt output/hashtag_${M}s/${STEM}.hashtag"
    condor_run "/bin/rm tmp/${STEM}"
done