#!/bin/bash

LIST=$1
M=$2

for line in $(cat ${LIST}); do
    echo ${line}
    STEM=$(basename "${line}" .gz)
    gunzip -c /bos/data0/twitter/spritzer/${line} > tmp/${STEM}
    ./get_text.py tmp/${STEM} output/text_${M}s/${STEM}.txt output/hashtag_${M}s/${STEM}.hashtag 0.06
    /bin/rm tmp/${STEM}
done
