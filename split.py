#!/usr/bin/env python
"""
split.py

    split.py splits conll2000.tag dataset into train, dev, and test sets and writes those sets to
    train.tag, dev.tag, and test.tag respectively. Data is randomly shuffled before split, and the shuffle is seeded
    at 272.

    train.tag contains 80% of the data
    dev.tag contains 10% of the data
    test.tag contains 10% of the data
"""

import argparse
import random
import logging

from typing import Iterator, List, Tuple

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

def test_train_split(data:List[List[List[str]]], seed: int) -> Tuple[List[List[List[str]]], List[List[List[str]]], List[List[List[str]]]]:
    '''
    :param data:
          Data = set of the format list of list of list of strings
    :return:
        train -> list strings representing train sample set
        dev -> list strings representing dev sample set
        test -> list strings representing test sample set
    '''

    #set training data length
    train_sample = int(len(data) * 0.8)
    dev_sample = int(len(data) * 0.1)
    #shuffle data for sampling
    random.Random(seed).shuffle(data)
    #split data into test, train,split
    train = data[0:train_sample]
    dev = data[train_sample: train_sample + dev_sample]
    test = data[train_sample + dev_sample:]

    return train, dev, test

def get_metadata(data: List[List[List[str]]]) -> Tuple[int,int]:
    sents = 0
    tokens = 0

    for sent in data:
        sents += 1
        for token in sent:
            tokens += 1

    return sents, tokens

def write_tags(data: List[List[List[str]]], output_path: str) -> None:
    '''
    :param data:
        List of sent strings containing lists of words
    :param output_path:
        a path for which to write the data input
    :return:
        None
    '''

    with open(output_path, 'w', encoding = 'utf-8') as out_path:
        #get word counts and write data to file
        for sent in data:
            for token in sent:
                #convert list to string
                word = ' '.join(token)
                #write word to file
                out_path.write(f"{word}\n")


def main(args: argparse.Namespace) -> None:

    #read in corpus from input
    corpus = list(read_tags(args.input))

    #split data into test,train,split sets
    train, dev, test = test_train_split(corpus, args.seed)

    #write data to file accordingly
    write_tags(train, args.train)
    write_tags(dev, args.dev)
    write_tags(test, args.test)

    #log metadata about set
    train_sents, train_tokens = get_metadata(train)
    dev_sents, dev_tokens = get_metadata(dev)
    test_sents, test_tokens = get_metadata(test)

    logging.info(f'Train sents: {train_sents}\nTrain tokens: {train_tokens}\n')
    logging.info(f'Dev sents: {dev_sents}\nDev tokens: {dev_tokens}\n')
    logging.info(f'Test sents: {test_sents}\nDev tokens: {test_tokens}\n')

if __name__ == "__main__":

    parser = argparse.ArgumentParser(
        description='Split some data in to train, dev split sets',
    )
    parser.add_argument('--seed', type=int, metavar='', required=True, help='Seed for random shuffle generation')
    parser.add_argument("input", type=str, metavar='', help='Read all of the input data')
    parser.add_argument('train', type=str, metavar='', help='Path for writing the training set')
    parser.add_argument('dev', type=str, metavar='', help='Path for writing the dev set')
    parser.add_argument('test', type=str, metavar='', help='Path for writing the test set')
    logging.basicConfig(level=logging.INFO)
    namespace = parser.parse_args()
    main(namespace)
