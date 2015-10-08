# -*- coding: utf-8 -*-
"""
Created on Sun Apr 26 04:43:34 2015

@author: Kya
"""

from __future__ import division
import re
import numpy as np
import pandas as pd


def make_data_set(datafile):
    liberal = ['WA', 'OR', 'CA', 'NV', 'CO', 'NM', 'IA', 'WI', 'MI', 'IL', 'OH', 'VA', 'DC', 'MD', 'DE', 'PA', 'NJ',
               'NY', 'CT', 'RI', 'MA', 'NH', 'VT', 'ME', 'HI', 'FL']

    # conservative = ['ID', 'MT', 'WY', 'UT', 'AZ', 'ND', 'SD', 'NE', 'KS', 'OK', 'TX', 'MO', 'AR', 'LA', 'IL', 'KY', 'TN', 'MS', 'AL', 'WV', 'NC', 'SC', 'GA', 'AK']

    libfoods = ['curry', 'bistro', 'fresh', 'fruit', 'strawberry', 'crunchy', 'thin', 'coconut', 'lamb', 'gnocchi',
                'fusili', 'radiatore', 'rice', 'wine', 'beer', 'diet', 'tap', 'fusion', 'vegetarian', 'foodie',
                'organic', 'seafood', 'toast', 'bagel', 'jamba', 'sbarro', 'chipotle', 'aubonpain', 'qdoba',
                'wienerschnitzel', 'starbucks', 'wingstop', 'panera', 'tacobell', 'quiznos', 'dunkin', 'donut',
                'dunkindonuts', 'pfchangs', 'cheesecakefactory', 'cpk', 'californiapizzakitchen', 'buffalowildwings',
                'ihop', 'wholefoods', 'whole foods', 'traderjoes', 'trader', "joe's", "trader joe's", 'safeway', 'frys',
                'fredmeyer', 'fred meyer', 'albertsons', 'osco', 'target', 'supertarget', 'macaroni', 'acme', 'blimpie',
                'ontheborder', 'asian']
    libfoodshash = ['#' + l for l in libfoods]

    confoods = ['meatloaf', 'potato', 'bean', 'gravy', 'soda', 'mcdonalds', 'steak', 'cooked', 'grape', 'soft',
                'deep dish', 'burger', 'grill', 'tuna', 'casserole', 'meatloaf', 'linguine', 'rotini', 'spaghetti',
                'juice', 'chinese', 'cheeseburger', 'bacon', 'applebees', 'schlotzskys', 'chickfila', 'arbys', 'sonic',
                'checkers', 'hardees', 'dominos', 'mcdonalds', 'wendys', 'kfc', 'subway', 'panda', 'express',
                'pandaexpress', 'olivegarden', 'olive', 'garden', 'redlobster', 'goldencorral', 'buffet', 'hooters',
                'papamurphys', "murphy's", 'dennys', "denny's", 'krystal', 'dairy queen', 'dairyqueen', 'churchs',
                "church's", 'papajohns', "john's", 'krispykreme', 'krispy kreme', 'walmart', 'foodlion', 'food lion',
                'kroger', 'harristeeter', 'harris', 'teeter', 'publix']
    confoodshash = ['#' + c for c in confoods]

    dataset = []

    for line in datafile:
        s1 = line.split('\t')
        state = s1[0]
        tweet = s1[1]
        label = ''
        features = []

        if state in liberal:
            label = 'liberal'
        else:
            label = 'conservative'

        tokens = tweet.split()

        punct = ['.', ',', '?', '!', "'", '"', '(', ')', '&', '=', '/', '+', '-', '*']

        # filter out html, handles, and floating punctuation, RT
        tokens = [t for t in tokens if
                  not t.startswith('http://') and not t.startswith('@') and not t.startswith('RT') and t not in punct]

        # remove emojis
        noemojis = []
        for t in tokens:
            if t.startswith('#'):
                tag = re.search('#([A-Za-z]|\d)+', t)
                if tag:
                    noemojis.append(tag.group().lower())
            else:
                word = re.search(r'([A-Za-z]|\d)+(\'[A-Za-z]+)*', t)
                if word:
                    noemojis.append(word.group().lower())

        tokens = noemojis

        # add bigrams
        addbigrams = tokens[:]
        for i in xrange(len(tokens) - 1):
            addbigrams.append('%s %s' % (tokens[i], tokens[i + 1]))

        features = addbigrams

        ccount = 0
        lcount = 0

        for t in tokens:
            if t in libfoods:
                lcount += 1
            if t in libfoodshash:
                lcount += 1
            if t in confoods:
                ccount += 1
            if t in confoodshash:
                ccount += 1

        # add liberal vs conservative food lexicon
        if lcount > 0:
            libcount = "Liberal Count: %i" % lcount
            features.append(libcount)
        if ccount > 0:
            concount = "Conservative Count: %i" % ccount
            features.append(concount)

        tweetinfo = {'state': state, 'label': label, 'features': features}
        dataset.append(tweetinfo)

    return dataset


def make_feature_vector(data, features):
    # borrowed from project 2a best submission

    fv = np.matrix(np.zeros((len(data), features.shape[0] + 1)))

    # Bias
    fv[:, 0] = 1

    for i, e in enumerate(data):
        # Regular Vector
        e = pd.Series(e)
        counts = e.value_counts()

        # Feature Vector
        for j, f in enumerate(features):
            if f in counts.index:
                fv[i, j + 1] = counts.ix[f]

    return fv


def compute_stats(gold, predicted, _class=''):
    tp = tn = fp = fn = 0

    for g, p in zip(gold, predicted):

        if g == p:
            if g == _class:
                tp += 1
            else:
                tn += 1

        else:
            if g == _class:
                fn += 1
            else:
                fp += 1

    return tp, tn, fp, fn


def compute_metrics(tp, tn, fp, fn):
    precision = tp / (tp + fp)
    recall = tp / (tp + fn)
    accuracy = (tp + tn) / (tp + tn + fp + fn)
    f1 = 2 * (precision * recall / (precision + recall))

    return accuracy, precision, recall, f1


def print_metrics(accuracy, precision, recall, f1):
    print 'Accuracy:\t%.3f' % accuracy
    print 'Precision:\t%.3f' % precision
    print 'Recall:\t\t%.3f' % recall
    print 'F1:\t\t%.3f' % f1
