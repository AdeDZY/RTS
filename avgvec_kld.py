#!/bos/usr0/zhuyund/bin/python2.7
import argparse
from os import listdir, makedirs
from os.path import isfile, join, exists
import numpy as np


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("avgvec_dir")
    parser.add_argument("tag_txt_file", type=argparse.FileType('r'))
    parser.add_argument("ref_file", type=argparse.FileType('r'))
    parser.add_argument("output_file", type=argparse.FileType('w'))
    args = parser.parse_args()

    # read tags
    tags = []
    for line in args.tag_txt_file:
        tags.append(line.strip())

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
    res = []
    for fname in vec_file_paths:
        with open(join(args.avgvec_dir, fname)) as f:
            kld = 0
            for line in f:
                if ',' not in line:
                    nvec = int(line)
                    continue
                wid, prob = line.split(',')
                wid = int(wid)
                prob = float(prob)
                kld += prob * np.log(prob/ref.get(wid))
            tag = tags[int(fname)]
            res.append((kld, tag, nvec, fname))

    res = sorted(res, reverse=True)
    for kld, tag, nvec, tid in res:
        args.output_file.write('{0}\t{1}\t{2}\t{3}\n'.format(tid, tag, kld, nvec))

    args.output_file.close()


