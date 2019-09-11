import csv

import MeCab


def analysis(in_csv: str, out_csv: str):
    tagger = MeCab.Tagger('-d /usr/lib/x86_64-linux-gnu/mecab/dic/mecab-ipadic-neologd')

    with open(out_csv, 'w', encoding='utf-8') as fout:
        with open(in_csv, encoding='utf-8') as fin:
            reader = csv.DictReader(fin)
            for row in reader:
                lemmas = []
                node = tagger.parseToNode(row['body'])
                while node:
                    result = node.feature.split(",")
                    pos = result[0]
                    lemma = result[-3]
                    if pos == '名詞':
                        lemmas.append(lemma)
                    node = node.next
                row = f"{row['date']},{row['url']},{row['title']},{','.join(lemmas)}\n"
                fout.write(row)
