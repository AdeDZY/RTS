import argparse
import json
import twokenizer


class Tweet:
    def __init__(self):
        self.extid = None
        self.text = None
        self.hashtag = None


def clean_text(json_objs):
    """
    :param json_objs: the tweet's json obj
    :return: cleaned text
    """
    text = list(json_objs["text"])
    entities = json_objs["entities"]
    for name, arr in entities.items():
        for entity in arr:
            if "indices" in entity:
                start, end = entity["indices"]
                for i in range(start, end):
                    text[i] = ''

    return ''.join(text)


def get_hashtags(json_objs):
    """
    return the hashtag text in a tweet. hashtags are seperated by tab
    :param json_objs: the tweet's json obj
    :return: tab seperated string of hashtags
    """
    res = []
    for h in json_objs["entities"]["hashtags"]:
        res.append(h["text"])
    if res:
        return '\t'.join(res)
    return ''


def parse_tweet_json(tweet_line):
    """
    parse json line. remove deletions and retweets
    :param tweet_line: a line of json text
    :return: a tweet obj
    """
    objs = json.loads(tweet_line)
    if "created_at" not in objs:  # other actions such as deleting
        return None

    if objs["lang"] != "en": # only deal with english tweets first
        return None

    text = twokenizer.unicodify(objs["text"])
    if "RT @" in text:
        return None  # remove re-tweet

    tweet = Tweet()
    tweet.extid = objs["id"]
    tweet.text = clean_text(objs).encode("ascii", "ignore").strip().replace('\n', ' ').replace('\t', ' ')
    tweet.hashtag = get_hashtags(objs)
    if tweet.text or tweet.hashtag:
        return tweet
    else:
        return None

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("tweets_json_file", type=argparse.FileType('r'))
    parser.add_argument("output_text_file", type=argparse.FileType('w'))
    parser.add_argument("output_hashtag_file", type=argparse.FileType('w'))
    args = parser.parse_args()

    for line in args.tweets_json_file:
        tweet = parse_tweet_json(line)
        if not tweet:
            continue
        if tweet.text:
            args.output_text_file.write(str(tweet.extid) + '\t' + tweet.text + '\n')
        if tweet.hashtag:
            args.output_hashtag_file.write(str(tweet.extid) + '\t' + tweet.hashtag + '\n')

    args.tweets_json_file.close()
    args.output_text_file.close()
    args.output_hashtag_file.close()
