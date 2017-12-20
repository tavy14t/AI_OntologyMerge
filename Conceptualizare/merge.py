""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
"                               WORK IN PROGRESS                             "
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

import os
import json
from owlready2 import *

relations = None
resultOntology = None
ontologies = []

with open('onto.conf') as file:
    relations = json.loads(file.read())

for x in os.scandir('/home/vm/onto'):
    onto = get_ontology("file://" + x.path)
    onto.load()
    ontologies.append(onto)

resultOntology = get_ontology("file:///home/vm/onto/result.owl")

for i in ontologies[0].classes():
    if len(i.ancestors()) == 2:
        walk(i)

"""
for x in ontologies:
    for i in x.classes():
        print(i, i.subclasses())

"""


