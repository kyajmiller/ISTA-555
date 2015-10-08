# -*- coding: utf-8 -*-
"""
Created on Sat Apr 25 02:18:13 2015

@author: Kya
"""

from __future__ import division
import pandas as pd
import itertools
from utilities import *
from sklearn.linear_model import LogisticRegression

training = open('p4train.txt', 'r')
testing = open('p4test.txt', 'r')

train = make_data_set(training)
test = make_data_set(testing)

frame = pd.DataFrame(columns=['state', 'label', 'features'])

for i, v in enumerate(test):
    frame.loc[i] = [v['state'], v['label'], v['features']]

features = pd.Series(list(itertools.chain(*[t['features'] for t in train])))
features = features.value_counts()
print "Number of Features: %i" % features.size
print "Filtering Features..."

threshold = 6
features = features[features >= threshold]
print "Number of Features after Filtering: %i" % features.size

# Feature Vectors
print "Building Features Vectors..."
X_train = make_feature_vector([t['features'] for t in train], features.index)
X_test = make_feature_vector([t['features'] for t in test], features.index)

# Logistic Regression
print "Training Logistic Regression..."
lr = LogisticRegression()
lr.fit(X_train, [t['label'] for t in train])

# Getting Results of Logistic Regression
frame['lr'] = lr.predict(X_test)

print "Results for Logistic Regression - liberal vs conservative:"
print "Results for conservative:"
print_metrics(*compute_metrics(*compute_stats(frame['label'], frame['lr'], _class='conservative')))
print '\n'
print "Results for liberal:"
print_metrics(*compute_metrics(*compute_stats(frame['label'], frame['lr'], _class='liberal')))
print '\n'
