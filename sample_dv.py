#!/bos/usr0/zhuyund/bin/python2.7
import argparse
from os import listdir
from os.path import isfile, join
import random

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("tweets_dv_dir")
    parser.add_argument("output_file", type=argparse.FileType('w'))
    parser.add_argument("sample_ratio", type=float)
    args = parser.parse_args()

    dv_file_paths = [f for f in listdir(args.tweets_dv_dir) if 'extid' not in f]

    for p in dv_file_paths:
        with open(join(args.tweets_dv_dir, p)) as f:
            for line in f:
                if random.random() < args.sample_ratio:
                    args.output_file.write(line)


