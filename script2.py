import csv
from math import log
from collections import Counter
import string

header = ""
COMMENT_I = 0
LABELS_I = 1


def tokenize(docs):
    """Compute the tokens for each document.
    Input: a list of strings. Each item is a document to tokenize.
    Output: a list of lists. Each item is a list containing the tokens of the
    relative document.
    """
    tokens = []
    for doc in docs:
        for punct in string.punctuation:
            doc = doc.replace(punct, " ")
        split_doc = [token.lower() for token in doc.split(" ") if token]
        tokens.append(split_doc)
    return tokens


def csv2list(path):
    with open(path, encoding="utf8") as fp:
        global header
        dataset = [[], []]
        reader = csv.reader(fp)
        header = next(reader)

        for row in reader:
            dataset[COMMENT_I].append(row[0])
            dataset[LABELS_I].append(row[1])

        return dataset


def tf(tokens):
    tf = {}

    for word in tokens:
        try:
            tf[word] += 1
        except KeyError:
            tf[word] = 1

    return tf


def tf_list(tokens_list):
    return [tf(tokens) for tokens in tokens_list]


def idf(documents_freq):
    N = len(documents_freq)
    dft = {}

    for d in documents_freq:
        words = d.keys()
        for w in words:
            try:
                dft[w] += 1
            except KeyError:
                dft[w] = 1

    return {w: log(N/t) for w, t in dft.items()}


if __name__ == '__main__':
    # 1.
    dataset = csv2list("data_sets/imdb.csv")
    print(f"Number of comments: {len(dataset[COMMENT_I])}")
    print(f"Number of Positive (1) and Negative (0) comments: {[(k,v) for k,v in Counter(dataset[LABELS_I]).items()]}")

    # 2.
    tokens = tokenize(dataset[COMMENT_I])
    # print(tokens[:2])

    # 3.
    documents_freq = tf_list(tokens)
    # print(term_freq[:5])

    # 4.
    inverse_document_freq = idf(documents_freq)
    print(inverse_document_freq)