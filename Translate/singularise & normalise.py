# @author: Munteanu Alexandru B7 III


from __future__ import division
from pattern.text.en import singularize
import nltk, re, pprint
from nltk import word_tokenize
from nltk.classify.rte_classify import lemmatize

# string = ['fibers', 'optic nerves', 'olfactory nerves', 'fibers',  'glossopharyngeals']

with open('input.txt') as f:
    content = f.readlines()
    content = [x.strip() for x in content]

def singular(words):
    singles = [singularize(word.lower()) for word in words]
    return singles

def normal(words):
    lem = nltk.WordNetLemmatizer()
    normals = [lem.lemmatize(word.lower()).encode('ascii','ignore') for word in words] #lemmatize functioneaza mai bn pe lower,
    return normals                                                                     #apoi am convertit la loc in ascii,
                                                                                       #deoarece lemmatize le face unicode.

print "singular: " , singular(content)
print "normal: " , normal(content)