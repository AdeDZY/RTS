#!/bos/usr0/zhuyund/bin/python2.7
import argparse
from os import listdir, makedirs
from os.path import isfile, join, exists
import numpy as np


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("avgvec_dir")
    parser.add_argument("tag_txt_file", type=argparse.FileType('r'))
    parser.add_argument("inner_kld_file", type=argparse.FileType('r'))
    parser.add_argument("ref_file", type=argparse.FileType('r'))
    parser.add_argument("output_file", type=argparse.FileType('w'))
    args = parser.parse_args()

    # read inner kld
    inner_klds = {}
    for line in args.inner_kld_file:
         tid, ikld = line.split('\t')
         inner_klds[int(tid)] = float(ikld)
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
                if wid in ref:
                    kld += prob * np.log(prob/ref.get(wid))
            tag = tags[int(fname)]
            res.append((kld, tag, nvec, fname, inner_klds.get(int(fname), 0)))

    res = sorted(res, reverse=True)
    for kld, tag, nvec, tid , ikld in res:
        if ikld > 3:
            args.output_file.write('{0}\t{1}\t{2}\t{3}\t{4}\n'.format(tid, tag, kld, ikld, nvec))

    args.output_file.write('\n')
    for kld, tag, nvec, tid , ikld in res:
        if ikld <= 3:
            args.output_file.write('{0}\t{1}\t{2}\t{3}\t{4}\n'.format(tid, tag, kld, ikld, nvec))

    args.output_file.close()


