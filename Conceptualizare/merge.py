import os
import types
from owlready2 import *

relations  = None
ontology1  = None
ontology2  = None
resultOntology = None
entities = {}

def addSynonymClasses(ontology1Class, ontology2Class, ontology1Score, ontology2Score):
    global resultOntology

    ontology1ResultClass = None
    ontology2ResultClass = None
  
    try:
        ontology1ResultClass = min(resultOntology.search(iri = "*" + ontology1Class.__name__))
    except Exception:
        pass
    try:
        ontology2ResultClass = min(resultOntology.search(iri = "*" + ontology2Class.__name__))
    except Exception:
        pass

    NewClass = None
    if ontology1ResultClass == None and ontology2ResultClass == None:
       
        ontologyParrentClasses = []
        for ontologyAncestor in ontology1Class.ancestors():
            for ontologyAncestorSubclass in ontologyAncestor.subclasses():
                if ontologyAncestorSubclass.__name__ == ontology1Class.__name__:
                    try:
                        resultOntologyParrent = min(resultOntology.search(iri = "*" + ontologyAncestor.__name__))
                        ontologyParrentClasses.append(resultOntologyParrent)                    
                    except Exception:
                        pass
        for ontologyAncestor in ontology2Class.ancestors():
            for ontologyAncestorSubclass in ontologyAncestor.subclasses():
                if ontologyAncestorSubclass.__name__ == ontology2Class.__name__:
                    try:
                        resultOntologyParrent = min(resultOntology.search(iri = "*" + ontologyAncestor.__name__))
                        ontologyParrentClasses.append(resultOntologyParrent)
                    except Exception:
                        pass        

        newClassName = None
        if ontology1Score >= ontology2Score:
            newClassName = ontology1Class.__name__
        else:
            newClassName = ontology2Class.__name__
        
        if len(ontologyParrentClasses) == 0:
            with resultOntology:
                NewClass = types.new_class(newClassName, (Thing, ), {})
        else:
            with resultOntology:
                NewClass = types.new_class(newClassName, ontologyParrentClasses, {})
        
        for ontologySubclass in ontology1Class.subclasses():
            if not ontologySubclass.__name__ == ontology1Class.__name__:
                recursiveCopyUnproblematic(ontologySubclass, NewClass)
        for ontologySubclass in ontology2Class.subclasses():
            if not ontologySubclass.__name__ == ontology2Class.__name__:
                recursiveCopyUnproblematic(ontologySubclass, NewClass)                      

    return NewClass

def solveSynonyms(relation):
    ontology1Score = 0
    ontology2Score = 0
    
    ontology1Class = None
    ontology2Class = None

    valScoreSource = {}
    valScoreSource["includes"] = -1
    valScoreSource["synonym"] = -2
    valScoreSource["is_included"] = -3
    valScoreDestin = {}
    valScoreDestin["includes"] = -3
    valScoreDestin["synonym"] = -2
    valScoreDestin["is_included"] = -1

    ontology1Class = min(ontology1.search(iri = "*"+relation[0]))
    ontology2Class = min(ontology2.search(iri = "*"+relation[2]))
    
    for ontologySubclass in ontology1Class.subclasses():
        for rel in relations:
            if ontologySubclass.__name__.upper() == rel[0].upper():
                ontology1Score += valScoreSource[rel[1]]

    for ontologySubclass in ontology2Class.subclasses():
        for rel in relations:
            if ontologySubclass.__name__.upper() == rel[2].upper():
                ontology2Score += valScoreDestin[rel[1]]
    addSynonymClasses(ontology1Class, ontology2Class, ontology1Score, ontology2Score)

def solveIsIncluded(relation):    

    ontology1Class = None
    ontology2Class = None
    resultOntologyClass1 = None
    resultOntologyClass2 = None   
 
    ontology1Class = min(ontology1.search(iri = "*" + relation[0]))
    ontology2Class = min(ontology2.search(iri = "*" + relation[2]))

    NewClass = None    

    try:
        resultOntologyClass1 = min(resultOntology.search(iri = "*" + relation[0]))
    except Exception:
        pass
    try:
        resultOntologyClass2 = min(resultOntology.search(iri = "*" + relation[2]))
    except Exception:  
        pass
    

    if not resultOntologyClass2 == None:
        if not resultOntologyClass1 == None:
            resultOntologyClass1.is_a.append(resultOntologyClass2)
        else:
            with resultOntology:
                NewClass = types.new_class(ontology1Class.__name__, (resultOntologyClass2, ), {})
            for ontologySubclass in ontology1Class.subclasses():
                if not ontologySubclass.__name__ == ontology1Class.__name__:
                    recursiveCopyUnproblematic(ontologySubclass, NewClass)                
    
def solveIncludes(relation):
    pass

def solveRelation(relation):
    if relation[1] == "synonym":
        return solveSynonyms(relation)
    elif relation[1] == "is_included":
        return solveIsIncluded(relation)
    elif relation[1] == "includes":
        return solveIncludes(relation)

def relationsCustomSort(relation):
    val = {}
    val["synonym"] = 5
    val["is_included"] = 2.5
    val["includes"] = 2.5
    return (entities[relation[0].upper()] + entities[relation[2].upper()]) * 10 - val[relation[1]]
    #return min((entities[relation[0].upper()], entities[relation[2].upper()]))*val[relation[1]]

def browseGraphRecursion(ontologyClass, level):
    for ontologySubclass in ontologyClass.subclasses():
        if not ontologySubclass.__name__ == ontologyClass.__name__:
            if ontologySubclass.__name__ not in entities:
                entities[ontologySubclass.__name__.upper()] = level

    for ontologySubclass in ontologyClass.subclasses():
        if not ontologySubclass.__name__ == ontologyClass.__name__:
                browseGraphRecursion(ontologySubclass, level+1)            

def browseGraph():
    for ontologyClass in ontology1.classes():
        if len(ontologyClass.ancestors()) == 2:
            entities[ontologyClass.__name__.upper()] = 0
            browseGraphRecursion(ontologyClass, 1)
    
    for ontologyClass in ontology2.classes():
        if len(ontologyClass.ancestors()) == 2:
            entities[ontologyClass.__name__.upper()] = 0
            browseGraphRecursion(ontologyClass, 1)

def recursiveCopyUnproblematic(ontologyClass, ontologyParrent):
    found = False
    for rel in relations:
        if rel[0].upper() == ontologyClass.__name__.upper() and rel[1] != "includes":
            found = True
            break
        if rel[2].upper() == ontologyClass.__name__.upper() and rel[1] != "is_included":
            found = True
            break
    if found == False:
        with resultOntology:
            NewClass = types.new_class(ontologyClass.__name__, (ontologyParrent, ), {})
        for ontologySubclass in ontologyClass.subclasses():
            if not ontologySubclass.__name__ == ontologyClass.__name__:
                recursiveCopyUnproblematic(ontologySubclass, NewClass)

def resultInit():
    global ontology1, ontology2, resultOntologym, relations
    
    for ontologyClass in ontology1.classes():
        if len(ontologyClass.ancestors()) == 2:
            found = False
            for rel in relations:
                if rel[0].upper() == ontologyClass.__name__.upper() and rel[1] != "includes":
                    found = True
                    break
                if rel[2].upper() == ontologyClass.__name__.upper() and rel[1] != "is_included":
                    found = True
                    break
            if found == False:
                with resultOntology:
                    NewClass = types.new_class(ontologyClass.__name__, (Thing,), {})
                for ontologySubclass in ontologyClass.subclasses():
                    if not ontologySubclass.__name__ == ontologyClass.__name__:
                        recursiveCopyUnproblematic(ontologySubclass, NewClass)

    for ontologyClass in ontology2.classes():
        if len(ontologyClass.ancestors()) == 2:
            found = False
            for rel in relations:
                if rel[0].upper() == ontologyClass.__name__.upper() and rel[1] != "is_included":
                    found = True
                    break
                if rel[2].upper() == ontologyClass.__name__.upper() and rel[1] != "includes":
                    found = True
                    break
            if found == False:
                with resultOntology:
                    NewClass = types.new_class(ontologyClass.__name__, (Thing,), {})
                for ontologySubclass in ontologyClass.subclasses():
                    if not ontologySubclass.__name__ == ontologyClass.__name__:
                        recursiveCopyUnproblematic(ontologySubclass, NewClass)

def mergeOntologies(ontology1Path, ontology2Path, ontologyRelations, resultPath):
    global ontology1, ontology2, resultOntology, relations

    #Incarca ontologiile global
    ontology1 = get_ontology("file://" + ontology1Path)
    ontology1.load()
    ontology2 = get_ontology("file://" + ontology2Path)
    ontology2.load()
    
    #Creaza fisierul de output
    open(resultPath, "w").close()
    resultOntology = get_ontology("file://" + resultPath)
    resultOntology.load()

    #Incarca relatiile obtinute de la modulul de limbaj global
    relations = ontologyRelations

    #Parcurgerea grafului pe latime si salvarea informatiei
    #Sortarea relatiilor in functie de inaltimea termenilor
    browseGraph()
    relations = list(sorted(relations, key=relationsCustomSort))
    print(relations)

    ### Startul Algoritmului ###

    '''
       In cazul cautarilor in ontologia rezultat este nevoie de o verificare suplimentara
       in blockul de try, catch pentru a ne asigura ca gasim ontologia potrivita ci nu 
       una gresita care sa faca match peste masca "*"+target.__name__
    '''    

    #Copiem clasele neproblematice, care au relatii relatii ce nu le afecteaza pozitia
    #Relatii ce le afecteaza pozitia(synonym si is_included)
    resultInit()

    #Incepem rezolvarea relatiilor in ordinea stabilita anterior    
    for rel in relations:
            solveRelation(rel)
       
    #Salveaza ontologia rezultata
    resultOntology.save(resultPath)
