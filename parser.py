import neologdn
import re

import Utils
import json
import csv
import glob

PATHS = [
    './projectnextnlp-chat-dialogue-corpus/json/init100/*.json',
    './projectnextnlp-chat-dialogue-corpus/json/rest1046/*.json'
]

MERGED_PATH = 'parsed-corpus.csv'

RESHAPED_PATH = 'reshaped-corpus.csv'

CLEANED_PATH = 'cleaned-corpus.csv'


def read_all_json():
    return list.__add__(*[glob.glob(PATH, recursive=True)
                          for PATH in PATHS])


def parse_files(paths):
    with open(MERGED_PATH, 'w') as w:
        writer = csv.writer(w, lineterminator='\n', quoting=csv.QUOTE_ALL)
        for path in paths:
            with open(path, 'r') as f:
                json_data = json.load(f)
                for turn in json_data['turns']:
                    res_o = res_x = 0
                    for annotate in turn['annotations']:
                        if annotate['breakdown'] == 'O':
                            res_o += 1
                        elif annotate['breakdown'] == 'X':
                            res_x += 1
                    res = [turn['utterance'], res_o, res_x]
                    writer.writerow(res)
            writer.writerow(['', 0, 0])


def reshape_corpus(path):
    with open(path, 'r') as p, open(RESHAPED_PATH, 'w') as w:
        reader = csv.reader(p, delimiter=',', doublequote=True)
        writer = csv.writer(w, lineterminator='\n', quoting=csv.QUOTE_ALL)
        ss = [[sentence, good, bad] for sentence, good, bad in reader]
        ss1 = ss[:-1]
        ss2 = ss[1:]
        for x, y in zip(ss1, ss2):
            sentence1, good1, bad1 = x
            sentence2, good2, bad2 = y
            if sentence1 != '' and sentence2 != '':
                good = int(good1) + int(good2)
                bad = int(bad1) + int(bad2)
                if good > bad:
                    writer.writerow([sentence1, sentence2, good, bad])


def cleaning_filter(sentence, max_len, min_len, rm_eng):
    if min_len < len(sentence) < max_len:
        if rm_eng is not None and re.match(rm_eng, sentence) is not None:
            return False
        else:
            return True
    else:
        return False


def cleaning_corpus(path, opt):
    if 'hiragana' == opt.split_func:
        parse_func = Utils.get_hiragana_list
    elif 'word-yomi' == opt.split_func:
        parse_func = Utils.get_word_yomi_list
    else:
        parse_func = Utils.get_word_list
    max_len = int(opt.max_sentence_length)
    min_len = int(opt.min_sentence_length)
    if opt.remove_english:
        repattern = re.compile('.*([a-zA-Z])')
    else:
        repattern = None

    with open(path, 'r') as p, open(CLEANED_PATH, 'w') as w:
        reader = csv.reader(p, delimiter=',', doublequote=True)
        writer = csv.writer(w, lineterminator='\n', quoting=csv.QUOTE_ALL)
        for sentence1, sentence2, _, _ in reader:
            if (cleaning_filter(sentence1, max_len, min_len, repattern)
                    and cleaning_filter(sentence2, max_len, min_len, repattern)):
                sentence1 = sentence1.replace('！', '!').replace('？', '?')
                sentence2 = sentence2.replace('！', '!').replace('？', '?')
                if sentence1[-1] not in ['?', '!', '。']:
                    sentence1 += '。'
                if sentence2[-1] not in ['?', '!', '。']:
                    sentence2 += '。'
                writer.writerow([
                    ' '.join(parse_func(
                            neologdn.normalize(sentence1.replace('"', ''))
                                .replace(',', '、'))),
                    ' '.join(parse_func(
                            neologdn.normalize(sentence2.replace('"', ''))
                                .replace(',', '、')))])


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('--type', type=int, choices=range(1, 5),
                        help='Chose Process Type:'
                             'Type 1: Merge all data in NTT-Japanese-Corpus.'
                             'Type 2: Reshape merged file to conversation file.'
                             'Type 3: Cleaning reshaped data with some parameter'
                             'Type 4: Type 1 -> Type 3',
                        required=True)
    parser.add_argument('--split_func', type=str, choices=['word', 'hiragana', 'word-yomi'],
                        default='word')
    parser.add_argument('--max_sentence_length', type=int, choices=range(10, 200),
                        default=45)
    parser.add_argument('--min_sentence_length', type=int, choices=range(0, 10),
                        default=1)
    parser.add_argument('--remove_english', type=bool, default=True)

    opt = parser.parse_args()

    if opt.type == 1:
        PATHLIST = read_all_json()
        parse_files(PATHLIST)

    elif opt.type == 2:
        reshape_corpus(MERGED_PATH)

    elif opt.type == 3:
        cleaning_corpus(RESHAPED_PATH, opt)

    elif opt.type == 4:
        PATHLIST = read_all_json()
        parse_files(PATHLIST)
        reshape_corpus(MERGED_PATH)
        cleaning_corpus(RESHAPED_PATH, opt)
