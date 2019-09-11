import typing

import numpy as np
import pandas as pd


def get_all_docs(in_csv: str) -> typing.List:
    all_docs = []
    with open(in_csv, encoding='utf-8') as fin:
        for line in fin:
            words = [word.strip() for word in line.split(',')[3:]]
            all_docs.append(words)
    return all_docs


def create_words_list(all_words: typing.List) -> typing.List:
    flatten_words = []
    for words in all_words:
        for word in words:
            flatten_words.append(word)
    words_list = []
    for word in flatten_words:
        if word not in words_list:
            words_list.append(word)
    return words_list


def get_word2int(words_list: typing.List) -> typing.Dict[str, int]:
    word2int = {}
    for idx, word in enumerate(words_list):
        word2int[word] = idx
    return word2int


def get_int2word(words_list: typing.List) -> typing.Dict[int, str]:
    int2word = {}
    for idx, word in enumerate(words_list):
        int2word[idx] = word
    return int2word


def calc_tf(all_docs: typing.List, word2int: typing.Dict[str, int]) -> np.ndarray:
    tf_array = np.zeros((len(all_docs), len(word2int)))
    for doc_idx, doc in enumerate(all_docs):
        temp_array = np.zeros((1, len(word2int)))
        for word_idx, word in enumerate(word2int.keys()):
            if word in doc:
                temp_array[0, word_idx] += 1
        tf_array[doc_idx:] = temp_array / np.sum(temp_array)
    return tf_array


def calc_idf(all_docs: typing.List, word2int: typing.Dict[str, int]) -> np.ndarray:
    temp_array = np.zeros((1, len(word2int)))
    all_docs = all_docs
    for idx, word in enumerate(word2int.keys()):
        word_count = 0
        for doc in all_docs:
            if word in doc:
                word_count += 1
        temp_array[0, idx] = word_count
    idf_array = np.log2((len(all_docs) + 1 / temp_array + 1))
    return idf_array


def l2_normalize(tf_idf: np.ndarray) -> np.ndarray:
    l2_norm = np.linalg.norm(tf_idf, ord=2)
    return tf_idf / l2_norm


def get_tf_idf_df(in_csv: str, int2word: typing.Dict[int, str], tf_idf_array: np.ndarray):
    with open(in_csv, encoding='utf-8') as fin:
        index = []
        for line in fin:
            rows = line.split(',')
            index.append(f'{rows[0].strip()} {rows[1].strip()}')
    columns = [int2word[i] for i in range(np.shape(tf_idf_array)[1])]
    words_tf_idf = pd.DataFrame(tf_idf_array, index=index, columns=columns)
    return words_tf_idf


def show_result(df: pd.DataFrame):
    with open('result.txt', 'w', encoding='utf-8') as f:
        for key, row in df.iterrows():
            top_15 = df.loc[key].sort_values(ascending=False)[:15]
            f.write(f'{key}\n{top_15}\n{"="*100}\n')


def tf_idf(in_csv: str):
    all_docs = get_all_docs(in_csv)
    words_list = create_words_list(all_docs)
    word2int = get_word2int(words_list)
    int2word = get_int2word(words_list)
    tf_array = calc_tf(all_docs, word2int)
    idf_array = calc_idf(all_docs, word2int)
    tf_idf = tf_array * idf_array
    normalized_tf_idf = l2_normalize(tf_idf)
    df = get_tf_idf_df(in_csv, int2word, normalized_tf_idf)
    show_result(df)
