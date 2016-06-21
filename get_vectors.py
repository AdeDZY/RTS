#!/bos/usr0/zhuyund/bin/python2.7
import argparse
from os import listdir, makedirs
from os.path import isfile, join, exists
import twokenizer


def gen_dv(line, vocab):
    dv = {}
    extid, txt = line.split('\t')
    txt.replace('\'', ' ')
    tokens = twokenizer.tokenize(txt)
    txt_len = 0
    for token in tokens:
        token = token.strip()
        if '@' not in token:
            token = token.lower()
        if token not in vocab:
            continue
        txt_len += 1
        tid = vocab[token]
        dv[tid] = dv.get(tid, 0) + 1
    return extid, txt_len, len(dv), dv


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("tweets_txt_dir")
    parser.add_argument("vocab_file", type=argparse.FileType('r'))
    parser.add_argument("output_dir")
    args = parser.parse_args()

    txt_file_paths = [f for f in listdir(args.tweets_txt_dir) if isfile(join(args.tweets_txt_dir, f))]

    # read vocab
    vocab = {}
    for line in args.vocab_file:
        tid, token, tf = line.split('\t')
        tid = int(tid)
        vocab[token] = tid

    if not exists(args.output_dir):
        makedirs(args.output_dir)

    for p in txt_file_paths:
        with open(join(args.tweets_txt_dir, p)) as f, open(join(args.output_dir, p), 'w') as fout, open(join(args.output_dir, p + '.extid'), 'w') as fextid:
            for line in f:
                exitd, txt_len, n_term, dv = gen_dv(line, vocab)
                if txt_len == 0:
                    continue
                fout.write("{0} {1} ".format(n_term, txt_len))
                for tid, freq in dv.items():
                    fout.write("{0}:{1} ".format(tid, freq))
                fout.write('\n')
                fextid.write(exitd + '\n')




