#!/opt/python27/bin/python
import string
from os import listdir
from os.path import isfile, join
import argparse


__author__ = 'zhuyund'

import argparse
import os
import jobWriter

parser = argparse.ArgumentParser()
parser.add_argument("dv_dir")
parser.add_argument("kmeans_dir")
parser.add_argument("n_clusters")
parser.add_argument("job_dir", help="write condor jobs into here")
parser.add_argument("lamda")
parser.add_argument("--ref_threshold","-r", type=float, help="ignore terms with ref > threshold", default=1.0)
args = parser.parse_args()

executable = '/bos/tmp11/zhuyund/partition/Inference-field/inference'

log_file = "/tmp/zhuyund_infernce.log"
log_dir = "./log/"
err_file = log_dir + "inference.err"
out_file = log_dir + "inference.out"

if not os.path.exists(log_dir):
    os.makedirs(log_dir)

if not os.path.exists(args.kmeans_dir + "/inference"):
    os.makedirs(args.kmeans_dir + "/inference")

txt_file_paths = [f for f in listdir(args.dv_dir) if isfile(join(args.dv_dir, f)) and 'extid' not in f]

job_file = open('tmp.f', "w")



for i in range(len(txt_file_paths)):
    if i%20 == 0:
        job_file.close()
        job_file = open(args.job_dir + '/' + str(i/20) + '.job', 'w')
    arguments = "{0}/{1}  {2}/centroids/ {2}/inference/{1}.inference {3} {5} 1 1 field {4} ".format(args.dv_dir,
                                                                                txt_file_paths[i],
                                                                                args.kmeans_dir,
                                                                                args.n_clusters, args.ref_threshold, args.lamda)

    job = jobWriter.jobGenerator(executable, arguments, log_file, err_file, out_file)

    job_file.write(job)

job_file.close()

