#bag of words model implementation
import numpy as np
import csv
import sys
import pickle
from sklearn.naive_bayes import MultinomialNB 
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer, HashingVectorizer

f = open(r'/home/walter-white/Desktop/test/files_used/textualAnalysis/V1.txt','r')
corpus = []
for line in f:
    corpus.append(line)

vectorizer = CountVectorizer()
print( vectorizer.fit_transform(corpus).todense() )
print( vectorizer.vocabulary_ )
