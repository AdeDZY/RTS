#!/bos/usr0/zhuyund/bin/python2.7
import argparse
from os import listdir
from os.path import isfile, join

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("txtvector_file_dir")
    parser.add_argument("hashtag_dir")
    parser.add_argument("output_dir")
    parser.add_argument("hashtag_vocab_file", type=argparse.FileType('r'))
    parser.add_argument("txt_vocab_max", type=int)
    args = parser.parse_args()

    vec_file_paths = [f for f in listdir(args.txtvector_file_dir)
                      if isfile(join(args.txtvector_file_dir, f)) and 'extid' not in f]

    hashtag_file_paths = [f for f in listdir(args.hashtag_dir)
                          if isfile(join(args.hashtag_dir, f))]

    # read vocab
    hash_vocab = {}
    for line in args.hashtag_vocab_file:
        tid, token, tf = line.split('\t')
        tid = int(tid)
        hash_vocab[token] = tid

    for p in vec_file_paths:
        name = p.replace('.txt', '')
        extid2hashtags = {}
        with open(join(args.hashtag_dir, name +'.hashtag')) as hash_f:
            for line in hash_f:
                items = line.strip().split('\t')
                extid = int(items[0])
                hs = {}
                hlen = 0
                for tag in items[1:]:
                    if tag in hash_vocab:
                        hlen += 1
                        tagid = hash_vocab[tag] + args.txt_vocab_max
                        hs[tagid] = hs.get(tagid, 0) + 1
                if hlen == 0:
                    continue
                hstr = " ".join(["{0}:{1} ".format(k, v) for k, v in hs.items()])
                extid2hashtags[extid] = (len(hs), hlen, hstr)

        with open(join(args.txtvector_file_dir, p)) as vec_f, open(join(args.txtvector_file_dir, p + '.extid')) as extid_f:
            with open(join(args.output_dir, p), 'w') as out_f:
                for line in vec_f:
                    extid = int(extid_f.readline())
                    if extid not in extid2hashtags:
                        out_f.write(line)
                        continue
                    ntags, hlen, hstr = extid2hashtags[extid]
                    items = line.strip().split(' ')
                    nterms = int(items[0]) + ntags
                    total_len = int(items[1]) + hlen
                    vstr = " ".join(items[2:])
                    out_f.write("{0} {1} {2} {3}\n".format(nterms, total_len, vstr, hstr))




