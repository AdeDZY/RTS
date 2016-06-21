#!/bos/usr0/zhuyund/bin/python2.7
import argparse
from os import listdir, makedirs
from os.path import isfile, join, exists
import numpy as np


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("kld_dir")
    parser.add_argument("output_file", type=argparse.FileType('w'))
    args = parser.parse_args()

    # read in all tags
    all_tags = {}
    with open(join(args.kld_dir, "all.kld")) as f:
        for line in f:
            if not line.strip(): break
            tid, tag, okld, ikld, df = line.split('\t')
            okld = float(okld)
            ikld = float(ikld)
            df = int(df)
            all_tags[tag] = (okld, ikld, df)

    # read each months tags
    m_tags = []
    for m in range(1, 13):
        tmp = {}
        with open(join(args.kld_dir, "{0}.kld".format(m))) as f:
            for line in f:
                if not line.strip(): break
                tid, tag, okld, ikld, df = line.split('\t')
                okld = float(okld)
                ikld = float(ikld)
                df = int(df)
                tmp[tag] = (okld, ikld, df)
        m_tags.append(tmp)

    # for each tag, see whether it is unique to < 3 months
    res = [[] for m in range(0, 12)]
    for tag in all_tags:
        ms = []
        for m in range(0, 12):
            if tag in m_tags[m]:
                ms.append(m + 1)
        if 0 < len(ms) < 3:
            res.append((tag, m_tags[m][tag][-1]))

    for m in range(0, 12):
        print m
        for tag, df in res:
            print tag, df



