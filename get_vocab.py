import argparse
import twokenizer
import emoticons
from os import listdir
from os.path import isfile, join

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("tweets_txt_dir")
    parser.add_argument("output_vocab_file", type=argparse.FileType('w'))
    parser.add_argument("threshold", type=int)
    parser.add_argument("stoplist", type=argparse.FileType('r'))
    args = parser.parse_args()

    stopwords = set()
    for line in args.stoplist:
        stopwords.add(line.strip())

    txt_file_paths = [f for f in listdir(args.tweets_txt_dir) if isfile(join(args.tweets_txt_dir, f))]
    vocab = {}
    for p in txt_file_paths:
        with open(join(args.tweets_txt_dir, p)) as f:
            for line in f:
                extid, txt = line.split('\t')
                txt.replace('\'', ' ')
                tokens = twokenizer.tokenize(txt)
                for token in tokens:
                    token = token.strip()

                    if '@' not in token and not token.isalnum():
                        continue
                    if token == "@":
                        continue
                    if token.isdigit():
                        continue
                    if '@' not in token:
                        token = token.lower()
                    if token in stopwords:
                        continue
                    if token in vocab:
                        vocab[token] += 1
                    else:
                        vocab[token] = 1

    n = 0
    for tf, token in sorted([(tf, token) for token, tf in vocab.items()], reverse=True):
        print token, tf
        if tf < args.threshold:
            break
        args.output_vocab_file.write("{0}\t{1}\t{2}\n".format(n, token, tf))
        n += 1

    args.output_vocab_file.close()


