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
    out_dirs = []
    for y in range(12, 16):
        dirs += ["output/text_{0}{1:02d}s".format(y, i) for i in range(1, 13)]
        out_dirs += ["output/vectors_{0}{1:02d}s".format(y, i) for i in range(1, 13)]
    dirs += ["output/text_160{0}s".format(i) for i in range(1, 6)]
    out_dirs += ["output/vectors_160{0}s".format(i) for i in range(1, 6)]

    job_file = open("get_vectors.job", 'w')

    for d, od in zip(dirs, out_dirs):
        execuatable = "./get_vectors.py"
        arguments = "{0} {1} {2}".format(d,
                                         "vocab_4year",
                                         od)

        log = "/tmp/zhuyund_kmeans.log"
        out = "tmp/vectors.out"
        err = "tmp/vectors.err"

        job = jobWriter.jobGenerator(execuatable, arguments, log, err, out)
        job_file.write(job + '\n')

job_file.close()



