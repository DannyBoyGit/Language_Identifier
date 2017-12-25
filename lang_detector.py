#!/usr/bin/env python

from optparse import OptionParser
import os
import logging
import re
import collections
from math import log10


def preprocess(line):
    # get rid of the stuff at the end of the line
    line = line.rstrip()
    # lower case
    line = line.lower()
    # remove everything except characters and white space
    line = re.sub("[^a-z ]", '', line)
    # splits the line up into tokens or words
    tokens = line.split()
    # adds $ to the beggining and the end of each token
    tokens = ['$' + token + '$' for token in tokens]

    return tokens


def create_model(path):
    # unigrams will return 0 if the key doesn't exist
    unigrams = collections.defaultdict(int)
    # and then you have to figure out what bigrams will return
    bigrams = collections.defaultdict(lambda: collections.defaultdict(int))

    f = open(path, 'r')
    # You shouldn't visit a token more than once
    for l in f.readlines():
        tokens = preprocess(l)
        if len(tokens) == 0:
            continue
        for token in tokens:
            # Updates the counts for unigrams and bigrams
            for c1, c2 in zip(token, token[1:]):
                unigrams[c1] += 1
                bigrams[c1][c2] += 1

    # After calculating the counts, calculates the smoothed log probabilities
    bigrams_prob = collections.defaultdict(lambda: collections.defaultdict(int))
    for prev_char, next_chars in bigrams.items():
        for next_char in next_chars:
            # smooth probability by adding .1 to a combination not seen before
            # divided by the number of unique letters in the alphabet
            bigrams_prob[prev_char][next_char] = log10((bigrams[prev_char][next_char] + .1) / (unigrams[prev_char] + 26))

    # return the actual model
    return bigrams_prob, unigrams


def calc_prob(tokens, model):
    bigram_probability = 0.0
    # the bigram probabilities and the word count is stored
    bigram_prob, unigram_count = model
    for token in tokens:
        # for i in range(0, len(token) - 1):
        for i in range(0, len(token) - 1):
            # adds the proababilities of the tokens being together
            bigram_probability += bigram_prob[token[i]][token[i + 1]]

    # returns bigram probability
    return bigram_probability


def predict(file, model_en, model_es):
    # preprocesses the file
    tokenize = []
    f = open(file, 'r')
    for lines in f.readlines():
        tokenize += preprocess(lines)

    # calculates the probabilities and stores them
    prob_en = calc_prob(tokenize, model_en)
    prob_es = calc_prob(tokenize, model_es)

    # returns the language that is more likely
    return "English" if prob_en > prob_es else "Spanish"


def main(en_tr, es_tr, folder_te):
    # STEP 1: create a model for English with en_tr
    model_en = create_model(en_tr)

    # STEP 2: create a model for Spanish with es_tr
    model_es = create_model(es_tr)

    # STEP 3: loop through all the files in folder_te and print prediction
    folder = os.path.join(folder_te, "en")
    print ("Prediction for English documents in test:")
    for f in os.listdir(folder):
        f_path = os.path.join(folder, f)
        print ("%s\t%s" % (f, predict(f_path, model_en, model_es)))

    folder = os.path.join(folder_te, "es")
    print ("\nPrediction for Spanish documents in test:")
    for f in os.listdir(folder):
        f_path = os.path.join(folder, f)
        print ("%s\t%s" % (f, predict(f_path, model_en, model_es)))


if __name__ == "__main__":
    usage = "usage: %prog [options] EN_TR ES_TR FOLDER_TE"
    parser = OptionParser(usage=usage)

    parser.add_option("-d", "--debug", action="store_true",
                      help="turn on debug mode")

    (options, args) = parser.parse_args()
    if len(args) != 3:
        parser.error("Please provide required arguments")

    if options.debug:
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.CRITICAL)

    main(args[0], args[1], args[2])
