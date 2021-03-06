#!/bos/usr0/zhuyund/bin/python2.7
import argparse
from os import listdir, makedirs
from os.path import isfile, join, exists


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("tag_extid_dir")
    parser.add_argument("start_tag", type=int)
    parser.add_argument("end_tag", type=int)
    parser.add_argument("tweet_txt_dir")
    parser.add_argument("tag_txt_file", type=argparse.FileType('r'))
    parser.add_argument("output_dir")
    args = parser.parse_args()

    # read tags
    tags = []
    for line in args.tag_txt_file:
        tags.append(line.strip())

    # read all the hashtag's related tweet extids
    tag_extids = {}
    extid_file_paths = [f for f in listdir(args.tag_extid_dir) if isfile(join(args.tag_extid_dir, f)) and f.isdigit()]
    for p in extid_file_paths:
        tid = int(p)
        if tid < args.start_tag or tid >= args.end_tag: continue 
        with open(join(args.tag_extid_dir, p)) as f:
            for line in f:
                extid = int(line)
                if extid not in tag_extids:
                    tag_extids[extid] = []
                tag_extids[extid].append(tid)

    # output files
    if not exists(args.output_dir):
        makedirs(args.output_dir)
    fouts = [open(join(args.output_dir, str(t)), 'w') for t in range(args.start_tag, args.end_tag)]
    for i, f in enumerate(fouts):
        f.write(tags[i + args.start_tag] + '\n')

    # read each vector file and get the vectors
    txt_file_paths = [f for f in listdir(args.tweet_txt_dir)]

    for p in txt_file_paths:
        vecFile = open(args.tweet_txt_dir + '/' + p)
        for line in vecFile:
            extid, txt = line.split('\t')
            extid = int(extid)
            if extid not in tag_extids:
                continue
            tids = tag_extids[extid]
            for tid in tids:
                fouts[tid - args.start_tag].write(line)

    for f in fouts:
        f.close()




