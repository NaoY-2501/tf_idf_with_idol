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


def get_int2word(words_set: typing.Set) -> typing.Dict[int, str]:
    int2word = {}
    for idx, word in enumerate(words_set):
        int2word[idx] = word
    return int2word


def calc_tf(all_words: typing.List, word2int: typing.Dict[str, int]) -> np.ndarray:
    tf_array = np.zeros((len(all_words), len(word2int)))
    for words_idx, words in enumerate(all_words):
        temp_array = np.zeros((1, len(word2int)))
        for word_idx, word in enumerate(words):
            if word in word2int:
                temp_array[0, word_idx] += 1
        tf_array[words_idx:] = temp_array / np.sum(temp_array)
    return tf_array


def calc_idf(all_words: typing.List, word2int: typing.Dict[str, int]) -> np.ndarray:
    temp_array = np.zeros((1, len(word2int)))
    all_docs = len(all_words)
    for idx, word in enumerate(word2int.keys()):
        word_count = 0
        for doc in all_words:
            if word in doc:
                word_count += 1
        temp_array[0, idx] = word_count
    idf_array = np.log2((all_docs + 1 / temp_array + 1))
    return idf_array


def tf_idf(in_csv: str):
    all_words = get_all_words(in_csv)
    words_set = create_word_set(all_words)
    word2int = get_word2int(words_set)
    int2word = get_int2word(words_set)
    tf_array = calc_tf(all_words, word2int)
    idf_array = calc_idf(all_words, word2int)
    tf_idf = tf_array * idf_array
    return tf_idf
