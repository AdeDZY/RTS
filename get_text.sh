#!/bin/bash

for line in $(cat "list"); do
	condor_run "./get_text.py data/${line} output/text_2/${line}.txt output/hashtag_2/${line}.hashtag"
	echo ${line}
done

