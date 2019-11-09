import csv
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


if __name__ == '__main__':
    # 1.
    dataset = csv2list("data_sets/imdb.csv")
    print(f"Number of comments: {len(dataset[COMMENT_I])}")
    print(f"Number of Positive (1) and Negative (0) comments: {[(k,v) for k,v in Counter(dataset[LABELS_I]).items()]}")

    # 2.
    tokens = tokenize(dataset[COMMENT_I])
    print(tokens[:2])