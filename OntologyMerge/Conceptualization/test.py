from merge import mergeOntologies

#from Relation_extractor import extract_relations
#from owlready2 import *

'''
ontology1 = get_ontology("file://onto/1.owl")
ontology2 = get_ontology("file://onto/2.owl")
relations = extract_relations(ontology1.classes(), ontology2.classes())
'''

relations = []
# relations.append(("Animal", "synonym", "Vie"))
# relations.append(("Pisica", "is_included", "Mamifer"))
# relations.append(("Caine",  "is_included", "Mamifer"))
# relations.append(("Mixer",  "is_included", "Electric"))
# relations.append(("Inghetata", "synonym", "Moarta"))
# relations.append(("Animal", "includes", "Pasare"))

mergeOntologies(r"E:\Tools\PyCharm Projects\OntologyMerge\Ontologies\onto\1.owl",
                r"E:\Tools\PyCharm Projects\OntologyMerge\Ontologies\onto\2.owl",
                relations,
                r"E:\Tools\PyCharm Projects\OntologyMerge\Ontologies\onto\result.owl")

