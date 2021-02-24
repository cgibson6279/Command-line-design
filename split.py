#!/usr/bin/env python
"""
    Using the argparse module, build a Python command-line tool which takes four arguments:
    input, train, dev, and test. The program should:

    1. Read all of the input data in using the above snippet.
    2. Split the data into an 80% training set, 10% development set, and 10% test set.
    3. Write the training set to the train path.
    4. Write the develoment set to the dev path.
    5. Write the testing set to the test path.
"""

import argparse
import random

from typing import Iterator, List

def read_tags(path: str) -> Iterator[List[List[str]]]:
    with open(path, "r") as source:
        lines = []
        for line in source:
            line = line.rstrip()
            if line:  # Line is contentful.
                lines.append(line.split())
            else:  # Line is blank.
                yield lines.copy()
                lines.clear()
    # Just in case someone forgets to put a blank line at the end...
    if lines:
        yield lines

def test_train_split(data):
    '''
    :param data:
          Data = set of the format list of list of list of strings
    :return:
        train, dev, test sets in the form of a list of list
    '''

    #set training data length
    train_sample = int(len(data) * 0.8)
    dev_sample = int(len(data) * 0.1)
    #shuffle data for sampling
    random.shuffle(data)
    #split data into test, train,split
    train = data[0:train_sample]
    dev = data[train_sample: train_sample + dev_sample]
    test = data[train_sample + dev_sample:]

    return train, dev, test

def write_tags(data: List[List[str]]):
    for sent in data:
        for word in sent:
            print('\t'.join(word))


def main(args: argparse.Namespace) -> None:
    #read in corpus from input
    corpus = list(read_tags(args.input))
    #split data into test,train,split sets
    train, dev, test = test_train_split(corpus)

    print(len(train))
    print(len(dev))
    print(len(test))
    print(len(test) + len(dev) + len(train))

if __name__ == "__main__":

    parser = argparse.ArgumentParser(
        description='Split some data in to train, dev split sets',
        epilog = f"length"
    )
    parser.add_argument("input", type=str, metavar='',
                        help='Read all of the input data')
    #parser.add_argument('--train', type=str, metavar='', required=True,
    #                    help='Path for writing the training set')
    #parser.add_argument('--dev', type=str, metavar='', required=True,
    #                    help='Path for writing the dev set')
    #parser.add_argument('--test', type=str, metavar='', required=True,
    #                    help='Path for writing the test set')
    namespace = parser.parse_args()
    main(namespace)
