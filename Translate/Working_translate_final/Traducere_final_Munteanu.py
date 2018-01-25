import sys
import fileinput
import re
from mtranslate import translate
import codecs
import unicodedata
import unidecode as unidecode
from owlready2 import *


# functie care ia un owl si il parseaza tot intr-un owl, pe care se lucreaza mai usor ulterior.
def Get_Ontology(onto_path):
    owl_ontologie = get_ontology(onto_path).load()
    owl_ontologie.save("in.owl")


# functie care traduce termenii din linii primite ca parametrii, si inlocuieste termenii cu traducerea lor
def f_traducere(rand):
    flag = bool (re.search(r'"#.*"', rand))    #daca nu gaseste expresie o sa crape cand folosim functia .gropu(0) de mai jos
    if flag == 1 :
        to_replace = re.search(r'"#.*"', rand).group(0).replace('_',' ')     #cautam expresia in linia din fisier
        translated = translate(to_replace, 'ro', 'en').replace(' ','_')     #traducerea efectiva
        translated2 = unidecode.unidecode(translated)  #scapam de diacritice
        rand = re.sub(r'"#.*"', translated2, rand)     #inlocuim in fisier cu termenul tradus
    else:
        pass
    return rand


# functie care scrie in fisierul output ontologia cu termenii tradusi
def scriere_fisier_output(input, output):
    with open (input, 'r') as f:
        with open(output,'w') as w:
            lines = f.readlines()
            for i in lines:
                w_line = f_traducere(i)
                w.write(w_line)


# Functia finala, singura care trebuie sa fie apelata din main sau whatever.
# Parametrii: calea ontologiei si un fisier de output pt ontologia tradusa
def Translate(cale_ontologie,output):
    Get_Ontology(cale_ontologie)
    scriere_fisier_output('in.owl',output)   #isi creaza singur fisierul in.owl apoi il foloseste.


cale_ontologie = "file://E:/2018 faculta stuff/AN 3/IA/PROIECT - TRANSLATE/My_work/1_ontologie.owl"
output_file = 'out.owl'
Translate(cale_ontologie, output_file)
