#!/bos/usr0/zhuyund/bin/python2.7
import argparse
from os import listdir, makedirs
from os.path import isfile, join, exists
import numpy as np


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("kld_dir")
    parser.add_argument("year", type=int, hlep="12,13,14,15,16")
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
            all_tags[tag] = (tid, okld, ikld, df)

    # read each months tags of the year
    m_tags = []
    n_month = 12
    if args.year == 16:
        n_month = 5
    for m in range(1, n_month + 1):
        tmp = {}
        with open(join(args.kld_dir, "{1}{0}s.kld".format(m, args.year))) as f:
            for line in f:
                if not line.strip(): break
                tid, tag, okld, ikld, df = line.split('\t')
                okld = float(okld)
                ikld = float(ikld)
                df = int(df)
                tmp[tag] = (tid, okld, ikld, df)
        m_tags.append(tmp)

    # for each tag, see whether it is unique to < 3 months
    res = [[] for m in range(0, n_month)]
    res2 = []
    for tag in all_tags:
        ms = []
        for m in range(0, n_month):
            if tag in m_tags[m]:
                ms.append(m)
        if 0 < len(ms) < 3:
            for m in ms:
                res[m].append((m_tags[m][tag][-1], tag, m_tags[m][tag][0]))
        elif len(ms) > n_month - 2:
            res2.append((all_tags[tag][-1], tag, all_tags[tag][0]))

    for m in range(0, n_month):
        print m + 1
        for df, tag, tid in sorted(res[m], reverse=True):
            print m+1, tid, tag, df
        print ''
    for df, tag, tid in sorted(res2, reverse=True):
        print tid, tag, df



