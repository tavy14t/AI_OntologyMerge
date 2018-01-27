import os
from owlready2 import *

cwd = os.getcwd()
onto1 = get_ontology("file://"+cwd+"//onto/1.owl")
onto2 = get_ontology("file://"+cwd+"//onto/2.owl")

with onto1:
    class Miscatoare(Thing):
        pass
    class Inghetata(Miscatoare):
        pass
    class Animal(Miscatoare):
        pass
    class Mixer(Miscatoare):
        pass
    class Caine(Animal):
        pass
    class Pisica(Animal):
        pass
    class Ocicat(Pisica):
        pass
    class Nyan(Pisica):
        pass
    class BorderCollie(Caine):
        pass
    class Shiba(Caine):
        pass

with onto2:
    class Entity(Thing):
        pass
    class Alive(Entity):
        pass
    class Dead(Entity):
        pass
    class Mammal(Alive):
        pass
    class Bird(Alive):
        pass
    class Cat(Mammal):
        pass
    class Electriccal(Dead):
        pass
    class Mechanical(Dead):
        pass

onto1.save(file="onto/1.owl")
onto2.save(file="onto/2.owl")
