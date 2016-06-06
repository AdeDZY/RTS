#!/bos/usr0/zhuyund/bin/python2.7
import argparse
import twokenizer
import emoticons
from os import listdir
from os.path import isfile, join

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("tweets_hashtag_dir")
    parser.add_argument("output_file", type=argparse.FileType('w'))
    parser.add_argument("threshold", type=int)
    args = parser.parse_args()

    tag_file_paths = [f for f in listdir(args.tweets_hashtag_dir) if isfile(join(args.tweets_hashtag_dir, f))]
    vocab = {}
    for p in tag_file_paths:
        with open(join(args.tweets_hashtag_dir, p)) as f:
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


