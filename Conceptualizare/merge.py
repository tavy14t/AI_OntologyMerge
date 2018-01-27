import types
from owlready2 import *

relations = None
ontology1 = None
ontology2 = None
resultOntology = None
entities = {}

solvedRelations = []
equivalentOntologies = {}


def relationsCustomSort(relation):
    val = {}
    val["synonym"] = 5
    val["is_included"] = 2.5
    val["includes"] = 2.5
    return (entities[relation[0].upper()] +
            entities[relation[2].upper()]) * 10 - val[relation[1]]
    # return min((entities[relation[0].upper()],
    #             entities[relation[2].upper()])) * val[relation[1]]


def generateRelations():
    global resultOntology

    with resultOntology:
        class echivalent(ObjectProperty):
            domain = [Thing]
            range = [Thing]


def solveParrent(ontologyClass):
    relToSolve = []
    for rel in relations:
        if rel[0].upper == ontologyClass.__name__.upper() \
                and rel not in solvedRelations:
            relToSolve.append(rel)
        if rel[2].upper == ontologyClass.__name__.upper() \
                and rel not in solvedRelations:
            relToSolve.append(rel)


def addSynonymClasses(ontology1Class, ontology2Class,
                      ontology1Score, ontology2Score):
    global resultOntology

    ontology1ResultClass = None
    ontology2ResultClass = None

    try:
        ontology1ResultClass = min(resultOntology.search(
            iri="*" + ontology1Class.__name__))
    except Exception:
        pass
    try:
        ontology2ResultClass = min(resultOntology.search(
            iri="*" + ontology2Class.__name__))
    except Exception:
        pass

    NewClass = None
    if ontology1ResultClass is None and ontology2ResultClass is None:
        ontologyParrentClasses = []
        for ontologyAncestor in ontology1Class.ancestors():
            for ontologyAncestorSubclass in ontologyAncestor.subclasses():
                if ontologyAncestorSubclass.__name__ == ontology1Class.__name__:
                    try:
                        resultOntologyParrent = min(resultOntology.search(
                            iri="*" + ontologyAncestor.__name__))
                        ontologyParrentClasses.append(resultOntologyParrent)
                    except Exception:
                        resultOntologyParrent = solveParrent(ontologyAncestor)
                        if not resultOntologyParrentClasses.append(resultOntologyParrent):
                            solveParrent(ontologyAncestor)

        for ontologyAncestor in ontology2Class.ancestors():
            for ontologyAncestorSubclass in ontologyAncestor.subclasses():
                if ontologyAncestorSubclass.__name__ == ontology2Class.__name__:
                    try:
                        resultOntologyParrent = min(resultOntology.search(
                            iri="*" + ontologyAncestor.__name__))
                        ontologyParrentClasses.append(resultOntologyParrent)
                    except Exception:
                        resultOntologyParrent = solveParrent(ontologyAncestor)
                        if resultOntologyParrent:
                            ontologyParrentClasses.append(
                                resultOntologyParrent)

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
                NewClass = types.new_class(
                    newClassName, ontologyParrentClasses, {})

        if ontology1Score >= ontology2Score:
            with resultOntology:
                PropertyDummyClass = types.new_class(
                    ontology2Class.__name__, (Thing, ), {})
                NewClass.echivalent.append(PropertyDummyClass)
                equivalentOntologies[PropertyDummyClass] = NewClass
        else:
            with resultOntology:
                PropertyDummyClass = types.new_class(
                    ontology1Class.__name__, (Thing, ), {})
                NewClass.echivalent.append(PropertyDummyClass)
                equivalentOntologies[PropertyDummyClass] = NewClass

        for ontologySubclass in ontology1Class.subclasses():
            if not ontologySubclass.__name__ == ontology1Class.__name__:
                recursiveCopyUnproblematic(ontologySubclass, NewClass)
        for ontologySubclass in ontology2Class.subclasses():
            if not ontologySubclass.__name__ == ontology2Class.__name__:
                recursiveCopyUnproblematic(ontologySubclass, NewClass)

    elif ontology1ResultClass and ontology2ResultClass:
        # Ambele clase exista
        if ontology1Score > ontology2Score:
            ontology1ResultClass.sinonim.append(ontology2ResultClass)
            for ontologySubclass in ontology2ResultClass.subclasses():
                if ontologySubclass.__name__ != ontology2ResultClass.__name__:
                    ontologySubclass.is_a.remove(ontology2ResultClass)
                    ontologySubclass.is_a.append(ontology1ResultClass)
            ontology2ResultClass.is_a.remove(Thing)
        else:
            ontology2ResultClass.sinonim.append(ontology1ResultClass)
            for ontologySubclass in ontology1ResultClass.subclasses():
                if ontologySubclass.__name__ != ontology1ResultClass.__name__:
                    ontologySubclass.is_a.remove(ontology1ResultClass)
                    ontologySubclass.is_a.append(ontology2ResultClass)
            ontology1ResultClass.is_a.remove(Thing)

    elif ontology1ResultClass:
        pass
    else:
        pass

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

    ontology1Class = min(ontology1.search(iri="*" + relation[0]))
    ontology2Class = min(ontology2.search(iri="*" + relation[2]))

    for ontologySubclass in ontology1Class.subclasses():
        for rel in relations:
            if ontologySubclass.__name__.upper() == rel[0].upper():
                ontology1Score += valScoreSource[rel[1]]

    for ontologySubclass in ontology2Class.subclasses():
        for rel in relations:
            if ontologySubclass.__name__.upper() == rel[2].upper():
                ontology2Score += valScoreDestin[rel[1]]
    addSynonymClasses(ontology1Class, ontology2Class,
                      ontology1Score, ontology2Score)
    solvedRelations.append(relation)


def solveIsIncluded(relation):

    ontology1Class = None
    ontology2Class = None
    resultOntologyClass1 = None
    resultOntologyClass2 = None

    ontology1Class = min(ontology1.search(iri="*" + relation[0]))
    ontology2Class = min(ontology2.search(iri="*" + relation[2]))

    NewClass = None

    try:
        resultOntologyClass1 = min(
            resultOntology.search(iri="*" + relation[0]))
    except Exception:
        pass
    try:
        resultOntologyClass2 = min(
            resultOntology.search(iri="*" + relation[2]))
    except Exception:
        pass

    if resultOntologyClass2:
        if resultOntologyClass1:
            with resultOntology:
                resultOntologyClass1.is_a.append(resultOntologyClass2)
        else:
            with resultOntology:
                NewClass = types.new_class(
                    ontology1Class.__name__, (resultOntologyClass2, ), {})
            for ontologySubclass in ontology1Class.subclasses():
                if not ontologySubclass.__name__ == ontology1Class.__name__:
                    recursiveCopyUnproblematic(ontologySubclass, NewClass)
    else:
        resultOntologyClass2 = solveParrent(ontology2Class)
        if resultOntologyClass2:
            if resultOntologyClass1:
                with resultOntology:
                    resultOntologyClass1.is_a.append(resultOntologyClass2)
            else:
                with resultOntology:
                    NewClass = types.new_class(
                        ontology1Class.__name__, (resultOntologyClass2, ), {})
                for ontologySubclass in ontology1Class.subclasses():
                    if ontologySubclass.__name__ != ontology1Class.__name__:
                        recursiveCopyUnproblematic(ontologySubclass, NewClass)

    solvedRelations.append(relation)
    return NewClass


def solveIncludes(relation):
    ontology1Class = None
    ontology2Class = None
    resultOntologyClass1 = None
    resultOntologyClass2 = None
    ontology1Class = min(ontology1.search(iri="*" + relation[0]))
    ontology2Class = min(ontology2.search(iri="*" + relation[2]))
    try:
        resultOntologyClass1 = min(
            resultOntology.search(iri="*" + relation[0]))
    except Exception:
        pass
    try:
        resultOntologyClass2 = min(
            resultOntology.search(iri="*" + relation[2]))
    except Exception:
        pass

    if resultOntologyClass1 in equivalentOntologies:
        resultOntologyClass1 = equivalentOntologies[resultOntologyClass1]

    if resultOntologyClass1:
        if resultOntologyClass2:
            with resultOntology:
                resultOntologyClass2.is_a.append(resultOntologyClass1)
        else:
            with resultOntology:
                NewClass = types.new_class(
                    ontology2Class.__name__, (resultOntologyClass1, ), {})
            for ontologySubclass in ontology2Class.subclasses():
                if not ontologySubclass.__name__ == ontology2Class.__name__:
                    recursiveCopyUnproblematic(ontologySubclass, NewClass)
    else:
        resultOntologyClass1 = solveParrent(ontology1Class)
        if resultOntologyClass1:
            if resultOntologyClass2:
                with resultOntology:
                    resultOntologyClass1.is_a.append(resultOntologyClass1)
            else:
                with resultOntology:
                    NewClass = types.new_class(
                        ontology1Class.__name__, (resultOntologyClass1, ), {})
                for ontologySublcass in ontology2Class.subclasses():
                    if ontologySubclass.__name__ != ontology2Class.__name__:
                        recursiveCopyUnproblematic(ontologySubclass, NewClass)
    solvedRelations.append(relation)
    return NewClass


def solveRelation(relation):
    if relation[1] == "synonym":
        return solveSynonyms(relation)
    elif relation[1] == "is_included":
        return solveIsIncluded(relation)
    else:
        return solveIncludes(relation)


def browseGraphRecursion(ontologyClass, level):
    for ontologySubclass in ontologyClass.subclasses():
        if not ontologySubclass.__name__ == ontologyClass.__name__:
            if ontologySubclass.__name__ not in entities:
                entities[ontologySubclass.__name__.upper()] = level

    for ontologySubclass in ontologyClass.subclasses():
        if not ontologySubclass.__name__ == ontologyClass.__name__:
            browseGraphRecursion(ontologySubclass, level + 1)


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
        if rel[0].upper() == ontologyClass.__name__.upper() and \
                rel[1] != "includes":
            found = True
            break
        if rel[2].upper() == ontologyClass.__name__.upper() and \
                rel[1] != "is_included":
            found = True
            break
    if not found:
        with resultOntology:
            NewClass = types.new_class(
                ontologyClass.__name__, (ontologyParrent, ), {})
        for ontologySubclass in ontologyClass.subclasses():
            if not ontologySubclass.__name__ == ontologyClass.__name__:
                recursiveCopyUnproblematic(ontologySubclass, NewClass)


def resultInit():
    global ontology1, ontology2, resultOntologym, relations

    for ontologyClass in ontology1.classes():
        if len(ontologyClass.ancestors()) == 2:
            found = False
            for rel in relations:
                if rel[0].upper() == ontologyClass.__name__.upper() and \
                        rel[1] != "includes":
                    found = True
                    break
                if rel[2].upper() == ontologyClass.__name__.upper() and \
                        rel[1] != "is_included":
                    found = True
                    break
            if not found:
                with resultOntology:
                    NewClass = types.new_class(
                        ontologyClass.__name__, (Thing,), {})
                for ontologySubclass in ontologyClass.subclasses():
                    if not ontologySubclass.__name__ == ontologyClass.__name__:
                        recursiveCopyUnproblematic(ontologySubclass, NewClass)

    for ontologyClass in ontology2.classes():
        if len(ontologyClass.ancestors()) == 2:
            found = False
            for rel in relations:
                if rel[0].upper() == ontologyClass.__name__.upper() and \
                        rel[1] != "is_included":
                    found = True
                    break
                if rel[2].upper() == ontologyClass.__name__.upper() and \
                        rel[1] != "includes":
                    found = True
                    break
            if not found:
                with resultOntology:
                    NewClass = types.new_class(
                        ontologyClass.__name__, (Thing,), {})
                for ontologySubclass in ontologyClass.subclasses():
                    if not ontologySubclass.__name__ == ontologyClass.__name__:
                        recursiveCopyUnproblematic(ontologySubclass, NewClass)


def mergeOntologies(ontology1Path, ontology2Path,
                    ontologyRelations, resultPath):
    global ontology1, ontology2, resultOntology, relations

    # Incarca ontologiile global
    ontology1 = get_ontology("file://" + ontology1Path)
    ontology1.load()
    ontology2 = get_ontology("file://" + ontology2Path)
    ontology2.load()

    # Creaza fisierul de output
    open(resultPath, "w").close()
    resultOntology = get_ontology("file://" + resultPath)
    resultOntology.load()

    # Incarca relatiile obtinute de la modulul de limbaj global
    relations = ontologyRelations

    # Parcurgerea grafului pe latime si salvarea informatiei
    # Sortarea relatiilor in functie de inaltimea termenilor
    browseGraph()
    generateRelations()
    relations = list(sorted(relations, key=relationsCustomSort))
    print(relations)

    # Startul Algoritmului
    '''
       To fix:

       In cazul cautarilor in ontologia rezultat este
       nevoie de o verificare suplimentara
       in blockul de try, catch pentru a ne asigura ca
       gasim ontologia potrivita ci nu
       una gresita care sa faca match peste masca "*"+target.__name__
    '''

    # Copiem clasele neproblematice, care au relatii ce nu le afecteaza pozitia
    # Relatii ce le afecteaza pozitia(synonym si is_included)
    resultInit()

    # Incepem rezolvarea relatiilor in ordinea stabilita anterior
    for rel in relations:
        if rel not in solvedRelations:
            solveRelation(rel)

    # Salveaza ontologia rezultata
    resultOntology.save(resultPath)
