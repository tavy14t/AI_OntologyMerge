# @author: Munteanu Alexandru B7 III


from __future__ import division
from pattern.text.en import singularize
import nltk
import re
import pprint
from nltk import word_tokenize
from nltk.classify.rte_classify import lemmatize

# string = ['fibers', 'optic nerves', 'olfactory nerves',
#           'fibers', 'glossopharyngeals']

with open('input.txt') as f:
    content = f.readlines()
    content = [x.strip() for x in content]


def singular(words):
    singles = [singularize(word.lower()) for word in words]
    return singles


def normal(words):
    lem = nltk.WordNetLemmatizer()

    # lemmatize functioneaza mai bn pe lower,
    # apoi am convertit la loc in ascii, deoarece lemmatize le face unicode.
    normals = [lem.lemmatize(word.lower()).encode('ascii', 'ignore')
               for word in words]
    return normals


print("singular: ", singular(content))
print("normal: ", normal(content))
