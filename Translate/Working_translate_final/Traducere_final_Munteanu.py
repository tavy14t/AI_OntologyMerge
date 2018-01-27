import sys
import fileinput
import re
from mtranslate import translate
import codecs
import unicodedata
import unidecode as unidecode
from owlready2 import *


def Get_Ontology(onto_path):
    """Functie care ia un owl si il parseaza tot intr-un owl,
    pe care se lucreaza mai usor ulterior."""

    owl_ontologie = get_ontology(onto_path).load()
    owl_ontologie.save("in.owl")


def f_traducere(rand):
    """Functie care traduce termenii din linii
    primite ca parametrii, si inlocuieste termenii cu traducerea lor"""

    # daca nu gaseste expresie o sa crape
    # cand folosim functia .gropu(0) de mai jos
    flag = bool(re.search(r'"#.*"', rand))
    if flag == 1:
        # cautam expresia in linia din fisier
        to_replace = re.search(r'"#.*"', rand).group(0).replace('_', ' ')
        translated = translate(to_replace, 'ro', 'en').replace(
            ' ', '_')  # traducerea efectiva
        translated2 = unidecode.unidecode(translated)  # scapam de diacritice
        # inlocuim in fisier cu termenul tradus
        rand = re.sub(r'"#.*"', translated2, rand)
    else:
        pass
    return rand


def scriere_fisier_output(input, output):
    """functie care scrie in fisierul
    output ontologia cu termenii tradusi"""
    with open(input, 'r') as f:
        with open(output, 'w') as w:
            lines = f.readlines()
            for i in lines:
                w_line = f_traducere(i)
                w.write(w_line)


def Translate(cale_ontologie, output):
    """
    Functia finala, singura care trebuie sa fie apelata din main sau whatever.
    Parametrii: calea ontologiei si un fisier de output pt ontologia tradusa
    """
    Get_Ontology(cale_ontologie)
    # isi creaza singur fisierul in.owl apoi il foloseste.
    scriere_fisier_output('in.owl', output)


cale_ontologie = "file://E:/2018 faculta stuff/AN 3/IA/PROIECT" \
                 " - TRANSLATE/My_work/1_ontologie.owl"
output_file = 'out.owl'
Translate(cale_ontologie, output_file)
