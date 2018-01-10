import os
import json
import types    
from owlready2 import *

relations = None
resultOntology = None
ontologies = []

def sortToSolve(item):
    return len(item[0].ancestors())

def addNonProblematicClassesRecursive(ontologyClass, parentClass):
    found = False
    for item in toSolve:
        if ontologyClass.__name__.upper() == item[1]["source"].upper() or ontologyClass.__name__.upper() == item[1]["destination"].upper():
            found = True
            break
    if found == False:
        NewClass = types.new_class(ontologyClass.__name__, (parentClass, ), {})
        for ontologySubclass in ontologyClass.subclasses():
            addNonProblematicClassesRecursive(ontologySubclass, NewClass)

def addClass(ontology, auxOntology):
    found = False
    parentClass = None
    for ancestor in ontology.ancestors():
        for resultOntologyClass in resultOntology.classes():
            if ancestor.__name__.upper() == resultOntologyClass.__name__.upper():
                parentClass = resultOntologyClass
    if parentClass == None:
        for ancestor in auxOntology.ancestors():
            for resultOntologyClass in resultOntology.classes():
                if ancestor.__name__.upper() == resultOntologyClass.__name__.upper():
                    parentClass = resultOntologyClass
    if parentClass == None:
        with resultOntology:
            NewClass = types.new_class(ontology.__name__, (Thing, ), {})
    else:
        with resultOntology:
            NewClass = types.new_class(ontology.__name__, (parentClass, ), {})
    
    for ontologySubclass in ontology.subclasses():
        foundItem = None
        found = False
        for item in toSolve:
            if ontologySubclass.__name__.upper() == item[1]["source"].upper() or ontologySubclass.__name__.upper() == item[1]["destination"].upper():
                found = True
                foundItem = item
                break
        if found == False:
            NewSubclassClass = types.new_class(ontologySubclass.__name__, (NewClass, ), {})
        else:
            solveItem(foundItem)


def solveItem(item):
    destOntology = ontologies[1].search( iri = "*"+ item[1]["destination"][0].upper() + item[1]["destination"][1:])
    
    if item[1]["relation"] == 1:
        sourToSolve = 0
        destToSolve = 0
        #bug aici!
        for ontologySubclass in destOntology[0].subclasses():
            for rel in relations:
                if ontologySubclass.__name__.upper() == rel["destination"].upper():
                    destToSolve += 1
        for ontologySubclass in item[0].subclasses():
            for rel in relations:
                if ontologySubclass.__name__.upper() == rel["source"].upper():
                    sourToSolve += 1
        if sourToSolve < destToSolve:
            addClass(item[0], destOntology[0])
        else:
            addClass(destOntology[0], item[0])

    if item[1]["relation"] == 2:
        with resultOntology:
            NewClass = types.new_class(item[0].__name__, (destOntology[0], ), {})
        for ontologySubclass in item[0].subclasses():
            addNonProblematicClassesRecursive(ontologySubclass, NewClass)


def walk(ontologyClass, ontologyParrent):
    found = False
    for rel in relations:
        if rel["source"].upper() == ontologyClass.__name__.upper() or rel["destination"].upper()  == ontologyClass.__name__.upper():
            found = True
            break
    if found == False:
        with resultOntology:
            NewClass = types.new_class(ontologyClass.__name__, (ontologyParrent, ), {})
        for ontologySubclass in ontologyClass.subclasses():
            if not ontologySubclass.__name__ == ontologyClass.__name__:
                walk(ontologySubclass, NewClass)

for file in os.scandir("onto"):
    if file.path[len(file.path)-3:] == "owl":
        onto = get_ontology("file://" + file.path)
        onto.load()
        ontologies.append(onto)
        if len(ontologies) > 2:
            break

with open("onto/onto.conf") as file:
    relations = json.loads(file.read())


if os.path.exists(os.getcwd()+"\\onto\\result.owl"):
    os.remove(os.getcwd()+"\\onto\\result.owl")

resultOntology = get_ontology("file://" + os.getcwd()+"/onto/result.owl")

for ontologyClass in ontologies[0].classes():
    if len(ontologyClass.ancestors()) == 2:
        found = False
        for rel in relations:
            if rel["source"].upper() == ontologyClass.__name__.upper() or rel["destination"].upper() == ontologyClass.__name__.upper():
                found = True
                break
        if found == False:
            with resultOntology:
                NewClass = types.new_class(ontologyClass.__name__, (Thing,), {})
            for ontologySubclass in ontologyClass.subclasses():
                if not ontologySubclass.__name__ == ontologyClass.__name__:
                    walk(ontologySubclass, ontologyClass)

for ontologyClass in ontologies[1].classes():
    if len(ontologyClass.ancestors()) == 2:
        found = False
        for rel in relations:
            if rel["destination"].upper() == ontologyClass.__name__.upper() or rel["source"].upper == ontologyClass.__name__.upper():
                found = True
                break
        if found == False:
            with resultOntology:
                NewClass = types.new_class(ontologyClass.__name__, (Thing, ), {})
            for ontologySubclass in ontologyClass.subclasses():
                if not ontologySubclass.__name__ == ontologyClass.__name__:
                        walk(ontologySubclass, NewClass)

toSolve = []
for ontologyClass in ontologies[0].classes():
    for rel in relations:
        if rel["source"].upper() == ontologyClass.__name__.upper() and ontologyClass.__name__ not in toSolve:
            toSolve.append([ontologyClass, rel])

toSolve = list(sorted(toSolve, key=sortToSolve))
for item in toSolve:
    found = False
    for resultOntologyClass in resultOntology.classes():
        if resultOntologyClass.__name__.upper() == item[0].__name__.upper():
            found = True
            break
    if found == False:
        solveItem(item)

resultOntology.save("onto\\result.owl")

