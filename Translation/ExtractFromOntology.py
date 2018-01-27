from owlready import *

# daca ontologia este salvata local
onto_path.append("/path/to/your/local/ontology/repository")
# daca ontologia este pe net
onto = get_ontology("http://www.lesfleursdunormal.fr/"
                    "static/_downloads/pizza_onto.owl")
onto.load()

onto.save("Onto.xml")
