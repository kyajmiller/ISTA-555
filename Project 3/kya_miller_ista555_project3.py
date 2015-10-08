# -*- coding: utf-8 -*-
"""
Created on Tue Mar 24 03:16:10 2015

@author: Kya
"""

import itertools
import pandas as pd
from utilities import *
from sklearn.linear_model import LogisticRegression

print "Relation Extraction: Per: Spouse"
ps_train = open('per_spouse.train', 'r')
ps_test = open('per_spouse.test', 'r')

ps_train = make_data_set(ps_train, 'per:spouse')
ps_test = make_data_set(ps_test, 'per:spouse')

ps_frame = pd.DataFrame(columns=['entity', 'filler', 'label', 'features'])

for i, v in enumerate(ps_test):
    ps_frame.loc[i] = [v['entity'], v['filler'], v['label'], v['features']]

ps_features = pd.Series(list(itertools.chain(*[t['features'] for t in ps_train])))
ps_features = ps_features.value_counts()

print "Number of Features: %i" % ps_features.size

# Feature Vectors
print "Building Features Vectors..."
ps_X_train = make_feature_vector([t['features'] for t in ps_train], ps_features.index)
ps_X_test = make_feature_vector([t['features'] for t in ps_test], ps_features.index)


# Question 4
threshold = 3  # Ignore all features that are repeated less than this number

# We don't need to recompute the vectors because the components are ordered!!
nfeat = ps_features[ps_features >= threshold]
ps_X2_train = ps_X_train[:, :nfeat.shape[0]]
ps_X2_test = ps_X_test[:, :nfeat.shape[0]]


# Logistic Regression
print "Training Logistic Regression..."
ps_lr = LogisticRegression()
ps_lr.fit(ps_X2_train, [t['label'] for t in ps_train])

# Getting Results of Logistic Regression
ps_frame['lr'] = ps_lr.predict(ps_X2_test)

print "Results for Logistic Regression - per:spouse vs nil:"
print "Results for per:spouse:"
print_metrics(*compute_metrics(*compute_stats(ps_frame['label'], ps_frame['lr'], _class='per:spouse')))
print '\n'
print "Results for nil:"
print_metrics(*compute_metrics(*compute_stats(ps_frame['label'], ps_frame['lr'], _class='nil')))
print '\n'

# below are the other relation extractions for the other three types
# I don't recommend trying to run all at once because it will make your computer's memory very sad

# ================================================================================================

print "Relation Extraction: Org: Country of Headquarters"
ocoh_train = open('org_country_of_headquarters.train', 'r')
ocoh_test = open('org_country_of_headquarters.test', 'r')

ocoh_train = make_data_set(ocoh_train, 'org:country of headquarters')
ocoh_test = make_data_set(ocoh_test, 'org:country of headquarters')

ocoh_frame = pd.DataFrame(columns=['entity', 'filler', 'label', 'features'])

for i, v in enumerate(ocoh_test):
    ocoh_frame.loc[i] = [v['entity'], v['filler'], v['label'], v['features']]

ocoh_features = pd.Series(list(itertools.chain(*[t['features'] for t in ocoh_train])))
ocoh_features = ocoh_features.value_counts()

print "Number of Features: %i" % ocoh_features.size

# Feature Vectors
print "Building Features Vectors..."
ocoh_X_train = make_feature_vector([t['features'] for t in ocoh_train], ocoh_features.index)
ocoh_X_test = make_feature_vector([t['features'] for t in ocoh_test], ocoh_features.index)

# Logistic Regression
print "Training Logistic Regression..."
ocoh_lr = LogisticRegression()
ocoh_lr.fit(ocoh_X_train, [t['label'] for t in ocoh_train])

# Getting Results of Logistic Regression
ocoh_frame['lr'] = ocoh_lr.predict(ocoh_X_test)

print "Results for Logistic Regression - org:country of headquarters vs nil:"
print "Results for org:country of headquarters:"
print_metrics(
    *compute_metrics(*compute_stats(ocoh_frame['label'], ocoh_frame['lr'], _class='org:country of headquarters')))
print '\n'
print "Results for nil:"
print_metrics(*compute_metrics(*compute_stats(ocoh_frame['label'], ocoh_frame['lr'], _class='nil')))
print '\n'

# ================================================================================================

print "Relation Extraction: Org: Top Members/Employees"
otme_train = open('half_org_top_membersSLASHemployees.train', 'r')
otme_test = open('org_top_membersSLASHemployees.test', 'r')

otme_train = make_data_set(otme_train, 'org top members/employees')
otme_test = make_data_set(otme_test, 'org top members/employees')

otme_frame = pd.DataFrame(columns=['entity', 'filler', 'label', 'features'])

for i, v in enumerate(otme_test):
    otme_frame.loc[i] = [v['entity'], v['filler'], v['label'], v['features']]

otme_features = pd.Series(list(itertools.chain(*[t['features'] for t in otme_train])))
otme_features = otme_features.value_counts()

print "Number of Features: %i" % otme_features.size

# Feature Vectors
print "Building Features Vectors..."
otme_X_train = make_feature_vector([t['features'] for t in otme_train], otme_features.index)
otme_X_test = make_feature_vector([t['features'] for t in otme_test], otme_features.index)

# Logistic Regression
print "Training Logistic Regression..."
otme_lr = LogisticRegression()
otme_lr.fit(otme_X_train, [t['label'] for t in otme_train])

# Getting Results of Logistic Regression
otme_frame['lr'] = otme_lr.predict(otme_X_test)

print "Results for Logistic Regression - org top members/employees vs nil:"
print "Results for org top members/employees:"
print_metrics(
    *compute_metrics(*compute_stats(otme_frame['label'], otme_frame['lr'], _class='org top members/employees')))
print '\n'
print "Results for nil:"
print_metrics(*compute_metrics(*compute_stats(otme_frame['label'], otme_frame['lr'], _class='nil')))
print '\n'

# ================================================================================================

print "Relation Extraction: Per: Employee Of"
peo_train = open('per_employee_of.train', 'r')
peo_test = open('per_employee_of.test', 'r')

peo_train = make_data_set(peo_train, 'per:employee of')
peo_test = make_data_set(peo_test, 'per:employee of')

peo_frame = pd.DataFrame(columns=['entity', 'filler', 'label', 'features'])

for i, v in enumerate(peo_test):
    peo_frame.loc[i] = [v['entity'], v['filler'], v['label'], v['features']]

peo_features = pd.Series(list(itertools.chain(*[t['features'] for t in peo_train])))
peo_features = peo_features.value_counts()

print "Number of Features: %i" % peo_features.size

# Feature Vectors
print "Building Features Vectors..."
peo_X_train = make_feature_vector([t['features'] for t in peo_train], peo_features.index)
peo_X_test = make_feature_vector([t['features'] for t in peo_test], peo_features.index)

# Logistic Regression
print "Training Logistic Regression..."
peo_lr = LogisticRegression()
peo_lr.fit(peo_X_train, [t['label'] for t in peo_train])

# Getting Results of Logistic Regression
peo_frame['lr'] = peo_lr.predict(peo_X_test)

print "Results for Logistic Regression - per:employee of vs nil:"
print "Results for per:employee of:"
print_metrics(*compute_metrics(*compute_stats(peo_frame['label'], peo_frame['lr'], _class='per:employee of')))
print '\n'
print "Results for nil:"
print_metrics(*compute_metrics(*compute_stats(peo_frame['label'], peo_frame['lr'], _class='nil')))
print '\n'
