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
    vec_dirs = []
    avg_dirs = []
    for y in range(12, 16):
        vec_dirs += ["output/vectors_{0}{1:02d}s".format(y, i) for i in range(1, 13)]
        avg_dirs += ["output/avgvec/{0}{1:02d}s".format(y, i) for i in range(1, 13)]
        dirs += ["data/{0}{1:02d}s_extid".format(y, i) for i in range(1, 13)]
        out_files += ["output/tagkld/{0}{1:02d}s.inner_kld".format(y, i) for i in range(1, 13)]
    vec_dirs += ["output/vectors_160{0}s".format(i) for i in range(1, 6)]
    avg_dirs += ["output/avgvec/160{0}s".format(i) for i in range(1, 6)]
    dirs += ["data/160{0}s_extid".format(i) for i in range(1, 6)]
    out_files += ["output/tagkld/160{0}s.inner_kld".format(i) for i in range(1, 6)]

    job_file = open("get_innerkld.job", 'w')

    for i in range(len(dirs)):
        execuatable = "./inner_kld.py"
        arguments = "{0} {1} {2} {3}".format(avg_dirs[i], dirs[i], vec_dirs[i], out_files[i])

        log = "/tmp/zhuyund_kmeans.log"
        out = "tmp/vectors.out"
        err = "tmp/vectors.err"

        job = jobWriter.jobGenerator(execuatable, arguments, log, err, out)
        job_file.write(job + '\n')

job_file.close()



