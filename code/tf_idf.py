import typing

import numpy as np


def get_all_words(in_csv: str) -> typing.List:
    all_words = []
    with open(in_csv, encoding='utf-8') as fin:
        for line in fin:
            words = [word.strip() for word in line.split(',')[2:]]
            all_words.append(words)
    return all_words


def create_word_set(all_words: typing.List) -> typing.Set:
    word_set = set()
    for words in all_words:
        for word in words:
            word_set.add(word)
    return word_set


def get_word2int(words_set: typing.Set) -> typing.Dict[str, int]:
    word2int = {}
    for idx, word in enumerate(words_set):
        word2int[word] = idx
    return word2int


def calc_tf(all_words: typing.List, word2int: typing.Dict[str, int]):
    tf_array = np.zeros((len(all_words), len(word2int)))


def tf_idf(in_csv: str):
    all_words = get_all_words(in_csv)
    words_set = create_word_set(all_words)
    word2int = get_word2int(words_set)
    print(len(all_words), len(word2int))
