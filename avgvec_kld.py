#!/bos/usr0/zhuyund/bin/python2.7
import argparse
from os import listdir, makedirs
from os.path import isfile, join, exists
import numpy as np


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("avgvec_dir")
    parser.add_argument("ref_file", type=argparse.FileType('r'))
    parser.add_argument("output_file", type=argparse.FileType('w'))
    args = parser.parse_args()

    # read ref
    ref = {}
    for line in args.ref_file:
        if ',' not in line:
            continue
        tid, prob = line.split(',')
        tid = int(tid)
        prob = float(prob)
        ref[tid] = prob

    # read avg vec
    vec_file_paths = [f for f in listdir(args.avgvec_dir) if isfile(join(args.avgvec_dir, f)) and f.isdigit()]
    for fname in vec_file_paths:
        with open(join(args.avgvec_dir, fname)) as f:
            kld = 0
            for line in f:
                tid, prob = line.split(',')
                tid = int(tid)
                prob = float(prob)
                kld += prob * np.log(prob/ref.get(tid))
            args.output_file.write('{0} {1}\n'.format(fname, kld))

    args.output_file.close()


