#!/bos/usr0/zhuyund/bin/python2.7
import argparse
from os import listdir, makedirs
import numpy as np
from os.path import isfile, join, exists


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("avgvec_dir")
    parser.add_argument("tag_extid_dir")
    parser.add_argument("tweet_vector_dir")
    parser.add_argument("output_file", type=argparse.FileType('w'))
    args = parser.parse_args()

    # read all the hashtag's related tweet extids
    tag_extids = {}
    extid_file_paths = [f for f in listdir(args.tag_extid_dir) if isfile(join(args.tag_extid_dir, f)) and f.isdigit()]
    for p in extid_file_paths:
        tid = int(p)
        with open(join(args.tag_extid_dir, p)) as f:
            for line in f:
                extid = int(line)
                if extid not in tag_extids:
                    tag_extids[extid] = []
                tag_extids[extid].append(tid)

    # read avg vec
    vec_file_paths = [f for f in listdir(args.avgvec_dir) if isfile(join(args.avgvec_dir, f)) and f.isdigit()]
    avg_vecs = {}
    n_vecs = {}
    for fname in vec_file_paths:
        with open(join(args.avgvec_dir, fname)) as f:
            vec = {}
            for line in f:
                if ',' not in line:
                    nvec = int(line)
                    continue
                wid, prob = line.split(',')
                wid = int(wid)
                prob = float(prob)
                vec[wid] = prob
            avg_vecs[int(fname)] = vec
            n_vecs[int(fname)] = nvec

    # read each vector file and get the vectors
    extid_file_paths = [f for f in listdir(args.tweet_vector_dir) if isfile(join(args.tweet_vector_dir, f)) and 'extid' in f]
    vec_file_paths = [f for f in listdir(args.tweet_vector_dir) if 'extid' not in f]
    inner_klds = {}

    for p in extid_file_paths:
        name = p.replace('.extid', '')
        extidFile = open(args.tweet_vector_dir + '/' + p)
        vecFile = open(args.tweet_vector_dir + '/' + name)

        nLine = 0
        for line in vecFile:
            extid = int(extidFile.readline().strip())
            nLine += 1
            if extid not in tag_extids:
                continue
            tids = tag_extids[extid]
            items = line.strip().split(' ')
            for tid in tids:
                kld = 0
                nterms = int(items[1])
                for t in items[2:]:
                    wid, freq = t.split(':')
                    wid = int(wid)
                    prob = float(freq)/nterms
                    kld += prob * np.log(prob/avg_vecs[tid][wid])
                inner_klds[tid] = inner_klds.get(tid, 0.0) + kld

    for tid in inner_klds:
        nvec = n_vecs[tid]
        args.output_file.write('{0}\t{1}\n'.format(tid, inner_klds[tid]/nvec))
    args.output_file.close()





