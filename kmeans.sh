#!/bin/bash -i
module load python27
module load python27-extras # get additional packages

./kmeans.py $* 
