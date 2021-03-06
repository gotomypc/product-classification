#! /usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function

import pandas as pd
import numpy as np

df = pd.read_csv('data_preprocessed.csv', header=None, error_bad_lines=False,
                 dtype=object,
                 names=['categoryid', 'categoryname', 'prodname', 'navigation',
                        'merchant', 'brand'])
df = df.dropna()
# bootstrap sampling
bag = []
grouped = df.groupby(by=['categoryid'])
for categoryid, group in grouped:
    group = group.reset_index(drop=True)
    sampled_group = np.random.choice(group.shape[0], size=400)
    bag.append(group.ix[sampled_group])
resampled_data = pd.concat(bag)

# split train and cv dataset
r = np.random.random_sample((len(resampled_data)))
train = resampled_data.ix[r >= 0.25]
cv = resampled_data.ix[r < 0.25]
train.to_csv('train.csv', index=False, encoding='utf-8')
cv.to_csv('cv.csv', index=False, encoding='utf-8')
