#!/bos/usr0/zhuyund/bin/python2.7
import argparse
from os import listdir
from os.path import isfile, join


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("tweets_shardmap_dir")
    parser.add_argument("tag_extid_dir")
    parser.add_argument("n_shard", type=int)
    parser.add_argument("n_test_tags", type=int)
    args = parser.parse_args()

    # read all the hashtag's related tweet extids
    tag_extids = [None for i in range(args.n_test_tags)]
    extid_file_paths = [f for f in listdir(args.tag_extid_dir) if isfile(join(args.tag_extid_dir, f)) and f.isdigit()]
    for p in extid_file_paths:
        tid = int(p)
        tmp = set()
        with open(join(args.tag_extid_dir, p)) as f:
            for line in f:
                extid = int(line)
                tmp.add(extid)

        tag_extids[tid] = tmp

    # read the shardmap and count

    query_shard = [[0 for i in range(args.n_shard)] for j in range(args.n_test_tags)]
    shardmap_file_paths = [f for f in listdir(args.tweets_shardmap_dir) if isfile(args.tweets_shardmap_dir, f) and f.isdigit()]
    for p in shardmap_file_paths:
        shard_extids = set()
        shardid = int(p) - 1
        with open(join(args.tweets_shardmap_dir, p)) as f:
            for line in f:
                extid = int(line)
                shard_extids.add(extid)
        for tid in range(args.n_test_tags):
            for extid in tag_extids[tid]:
                if extid in shard_extids:
                    query_shard[tid][shardid] += 1

    # compute coverage
    avg_coverage = [0 for i in range(args.n_shard)]
    for tid in range(args.n_test_tags):
        n_total = float(sum(query_shard[tid]))
        tmp = sorted(query_shard[tid], reverse=True)
        for i in range(1, len(tmp)):
            tmp[i] += tmp[i - 1]
            tmp[i - 1] /= n_total
            avg_coverage[i - 1] += tmp[i - 1]/args.n_shard

        print tmp
    print avg_coverage

