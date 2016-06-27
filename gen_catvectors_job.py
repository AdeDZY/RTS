#!/opt/python27/bin/python

__author__ = 'zhuyund'

# for a partition
# gen jobs for shardFeature

import os, sys
import jobWriter
from os import listdir, makedirs
from os.path import isfile, join, exists

if __name__ == '__main__':

    dirs = []
    tag_dirs = []
    out_dirs = []
    for y in range(12, 16):
        dirs += ["output/vectors_{0}{1:02d}s".format(y, i) for i in range(1, 13)]
        tag_dirs += ["output/hashtag_{0}{1:02d}s".format(y, i) for i in range(1, 13)]
        out_dirs += ["output/vectors_withtag_{0}{1:02d}s".format(y, i) for i in range(1, 13)]
    dirs += ["output/vectors_160{0}s".format(i) for i in range(1, 6)]
    tag_dirs += ["output/hashtag_160{0}s".format(i) for i in range(1, 6)]
    out_dirs += ["output/vectors_withtag_160{0}s".format(i) for i in range(1, 6)]

    job_file = open("cat_vectors.job", 'w')

    for d in out_dirs:
        if not exists(d):
            makedirs(d)

    for i in range(len(dirs)):
        execuatable = "./cat_vector_with_hashtag.py"
        arguments = "{0} {1} {2}".format(dirs[i], tag_dirs[i], out_dirs[i],
                                         "hash_vocab_4year", "vocab_4year")

        log = "/tmp/zhuyund_kmeans.log"
        out = "tmp/vectors.out"
        err = "tmp/vectors.err"

        job = jobWriter.jobGenerator(execuatable, arguments, log, err, out)
        job_file.write(job + '\n')

    job_file.close()



