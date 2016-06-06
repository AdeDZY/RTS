#!/bos/usr0/zhuyund/bin/python2.7
import argparse
from os import listdir
from os.path import isfile, join

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("tweets_hashtag_dir")
    parser.add_argument("test_tag_file", type=argparse.FileType('r'))
    parser.add_argument("output_dir")
    parser.add_argument("threshold", type=int)
    args = parser.parse_args()

    tag_file_paths = [f for f in listdir(args.tweets_hashtag_dir) if isfile(join(args.tweets_hashtag_dir, f))]
    test_tags = []
    tag2extid = {}
    for line in args.test_tag_file:
        test_tags.append(line.strip())
        tag2extid[line.strip()] = []

    for p in tag_file_paths:
        with open(join(args.tweets_hashtag_dir, p)) as f:
            for line in f:
                items = line.strip().split('\t')
                extid = int(items[0])
                for tag in items[1:]:
                    if tag in tag2extid:
                        tag2extid[tag].append(extid)

    for i in range(len(test_tags)):
        with open(join(args.output_dir, str(i)), 'w') as fout:
            for extid in tag2extid[test_tags[i]]:
                fout.write(str(extid) + '\n')
