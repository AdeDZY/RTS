#!/opt/python27/bin/python

__author__ = 'zhuyund'

# for a partition
# gen jobs for shardFeature

import os, sys
import jobWriter
from os import listdir
from os.path import isfile, join

if __name__ == '__main__':

    inner_files = []
    avg_dirs = []
    tag_files = []
    out_files = []
    for y in range(12, 16):
        avg_dirs += ["output/avgvec/{0}{1:02d}s".format(y, i) for i in range(1, 13)]
        inner_files += ["output/inner_kld/{0}{1:02d}s.inner_kld".format(y, i) for i in range(1, 13)]
        tag_files += ["tags/{0}{1:02d}.tags".format(y, i) for i in range(1, 13)]
        out_files += ["output/tagkld/{0}{1:02d}s.kld".format(y, i) for i in range(1, 13)]

    avg_dirs += ["output/avgvec/160{0}s".format(i) for i in range(1, 6)]
    inner_files += ["output/inner_kld/160{0}s.inner_kld".format(i) for i in range(1, 6)]
    tag_files += ["tags/160{0}.tags".format(i) for i in range(1, 6)]
    out_files += ["output/tagkld/160{0}s.kld".format(i) for i in range(1, 6)]

    job_file = open("get_kld.job", 'w')
    ref = "output/Kmeans/samplingTrial6/50Clusters-10Iters-1/centroids/reference"
    for i in range(len(avg_dirs)):
        execuatable = "./avgvec_kld.py"
        arguments = "{0} {1} {2} {3} {4}".format(avg_dirs[i], tag_files[i], inner_files[i], ref, out_files[i])

        log = "/tmp/zhuyund_kmeans.log"
        out = "tmp/vectors.out"
        err = "tmp/vectors.err"

        job = jobWriter.jobGenerator(execuatable, arguments, log, err, out)
        job_file.write(job + '\n')

job_file.close()



