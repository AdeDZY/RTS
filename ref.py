#!/bos/usr0/zhuyund/bin/python2.7
import argparse
from os import listdir, makedirs
import numpy as np
from os.path import isfile, join, exists


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("output_file", type=argparse.FileType('w'))
    args = parser.parse_args()

    # read each vector file and get the vectors
    dirs = ['output/vectors_{0}s'.format(i) for i in range(1, 13)]
    vec_file_paths = []
    for d in dirs:
        vec_file_paths += [(d, f) for f in listdir(d) if isfile(join(d, f)) and 'extid' not in f]

    ref = {}
    n = 0
    for d, p in vec_file_paths:
        vecFile = open(join(d, p))
        for line in vecFile:
            n += 1
            items = line.strip().split(' ')
            nterms = int(items[1])
            for t in items[2:]:
                wid, freq = t.split(':')
                wid = int(wid)
                prob = float(freq)/nterms
                ref[wid] = ref.get(wid, 0) + prob

    for wid, prob in ref.items():
        args.output_file.write("{0},{1}\n".format(wid, prob/n))
    args.output_file.close()





