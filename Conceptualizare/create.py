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
    class Entitate(Thing):
        pass
    class Vie(Entitate):
        pass
    class Moarta(Entitate):
        pass
    class Mamifer(Vie):
        pass
    class Pasare(Vie):
        pass
    class Pisica(Mamifer):
        pass
    class Electric(Moarta):
        pass
    class Mecanic(Moarta):
        pass

onto1.save(file="onto/1.owl")
