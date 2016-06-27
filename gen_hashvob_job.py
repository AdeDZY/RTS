#!/opt/python27/bin/python

__author__ = 'zhuyund'

# for a partition
# gen jobs for shardFeature

import os, sys
import jobWriter
from os import listdir
from os.path import isfile, join

if __name__ == '__main__':

    dirs = []
    out_files = []
    for y in range(12, 16):
        dirs += ["output/hashtag_{0}{1:02d}s".format(y, i) for i in range(1, 13)]
        out_files += ["tags/{0}{1:02d}.vocab".format(y, i) for i in range(1, 13)]
    dirs += ["output/hashtag_160{0}s".format(i) for i in range(1, 6)]
    out_files += ["tags/160{0}.vocab".format(i) for i in range(1, 6)]

    job_file = open("get_vectors.job", 'w')

    for d, of in zip(dirs, out_files):
        execuatable = "./get_vectors.py"
        arguments = "{0} {1} {2}".format(d, of, 10)

        log = "/tmp/zhuyund_kmeans.log"
        out = "tmp/vectors.out"
        err = "tmp/vectors.err"

        job = jobWriter.jobGenerator(execuatable, arguments, log, err, out)
        job_file.write(job + '\n')

job_file.close()



