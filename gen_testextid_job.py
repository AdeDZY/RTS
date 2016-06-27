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
    tag_files = []
    out_files = []
    out_dirs = []
    for y in range(12, 16):
        dirs += ["output/hashtag_{0}{1:02d}s".format(y, i) for i in range(1, 13)]
        tag_files += ["tags/{0}{1:02d}.tags".format(y, i) for i in range(1, 13)]
        out_dirs += ["data/{0}{1:02d}s_extid".format(y, i) for i in range(1, 13)]
    dirs += ["output/hashtag_160{0}s".format(i) for i in range(1, 6)]
    tag_files += ["tags/160{0}.tags".format(i) for i in range(1, 6)]
    out_dirs += ["data/160{0}s_extid".format(i) for i in range(1, 6)]

    job_file = open("get_test_extids.job", 'w')

    for i in range(len(dirs)):
        execuatable = "./get_test_extids.py"
        arguments = "{0} {1} {2}".format(dirs[i], tag_files[i], out_dirs[i])

        log = "/tmp/zhuyund_kmeans.log"
        out = "tmp/vectors.out"
        err = "tmp/vectors.err"

        job = jobWriter.jobGenerator(execuatable, arguments, log, err, out)
        job_file.write(job + '\n')

job_file.close()



