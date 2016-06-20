#!/bos/usr0/zhuyund/bin/python2.7
import argparse
from os import listdir, makedirs
from os.path import isfile, join, exists


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("tag_extid_dir")
    parser.add_argument("tweet_vector_dir")
    parser.add_argument("n_test_tags", type=int)
    parser.add_argument("output_dir")
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

    # read each vector file and get the vectors
    extid_file_paths = [f for f in listdir(args.tweet_vector_dir) if isfile(join(args.tweet_vector_dir, f)) and 'extid' in f]
    vec_file_paths = [f for f in listdir(args.tweet_vector_dir) if 'extid' not in f]
    avg_vecs = {}
    n_vecs = {}

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
                if tid not in avg_vecs:
                    avg_vecs[tid] = {}
                    n_vecs[tid] = 0
                nterms = int(items[1])
                for t in items[2:]:
                    wid, freq = t.split(':')
                    wid = int(wid)
                    freq = int(freq)
                    prob = freq/float(nterms) 
                    avg_vecs[tid][wid] = avg_vecs[tid].get(wid, 0) + prob 

                n_vecs[tid] += 1

    if not exists(args.output_dir):
        makedirs(args.output_dir)
    for tid in avg_vecs:
        fout = open(join(args.output_dir, str(tid)), 'w')
        nvec = n_vecs[tid]
        for wid, prob in avg_vecs[tid].items():
            fout.write("{0},{1}\n".format(wid, prob/nvec))
        fout.write(str(nvec))
        fout.close()





