#!/bos/usr0/zhuyund/bin/python2.7
import argparse
import twokenizer
import emoticons
from os import listdir
from os.path import isfile, join

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    #parser.add_argument("tweets_hashtag_dir")
    parser.add_argument("output_file", type=argparse.FileType('w'))
    parser.add_argument("threshold", type=int)
    args = parser.parse_args()

    dirs = ['output/hashtag_{0}s'.format(i) for i in range(1, 13)]
    tag_file_paths = []
    for d in dirs:
        tag_file_paths += [(d, f) for f in listdir(d) if isfile(join(d, f))]

    vocab = {}
    for d, p in tag_file_paths:
        with open(join(d, p)) as f:
            for line in f:
                items = line.strip().split('\t')
                for tag in items[1:]:
                    if tag in vocab:
                        vocab[tag] += 1
                    else:
                        vocab[tag] = 1

    n = 0
    for tf, tag in sorted([(tf, tag) for tag, tf in vocab.items()], reverse=True):
        print tag, tf
        if tf < args.threshold:
            break
        args.output_file.write("{0}\t{1}\t{2}\n".format(n, tag, tf))
        n += 1

    args.output_file.close()


