#primesc 2 liste t1 si t2 si un text
#returnez relatiile dintre elementele din t1 si t2 gasite in text
import re

#returneaza 0 daca nu este definitie
def is_part_of(text, position):
    if((text[position] == 'este') or (text[position] == 'reprezinta') or (text[position] == 'defineste')):
        if((text[position+1] == 'un') or (text[position+1] == 'o')):
            if((text[position+2] == 'tip') and (text[position+3] == 'de')):
                return position+4
            else:
                return position + 2
        else:
            return position + 1
    else:
        return -1

def includes(text, position):
    if((text[position] == 'face') and (text[position + 1] == 'parte') and (text[position + 2] == 'din')):
        return position + 3
    else:
        return -1

def relatii(t1, t2, text):
    t3 = []
    t1.sort()
    t2.sort()
    splitted_text = re.sub("[^\w]", " ",  text).split()

    splitted_text.append('')
    splitted_text.append('')
    splitted_text.append('')
    splitted_text.append('')
    splitted_text.append('')

    for termen in t1:
        for i in range(len(splitted_text)):
            if(termen == splitted_text[i]):
                def_type = is_part_of(splitted_text, i + 1)
                if(def_type != -1):
                    if any(splitted_text[def_type] in s for s in t2):
                        t3.append(tuple([splitted_text[i], 'PartOf', splitted_text[def_type]]))
                includes_type = includes(splitted_text, i + 1)
                if (includes_type != -1):
                    if any(splitted_text[includes_type] in s for s in t2):
                        t3.append(tuple([splitted_text[i], 'PartOf', splitted_text[includes_type]]))

    for termen in t2:
        for i in range(len(splitted_text)):
            if(termen == splitted_text[i]):
                def_type = is_part_of(splitted_text, i + 1)
                if(def_type != -1):
                    if any(splitted_text[def_type] in s for s in t1):
                        t3.append(tuple([splitted_text[i], 'PartOf', splitted_text[def_type]]))
                includes_type = includes(splitted_text, i + 1)
                if (includes_type != -1):
                    if any(splitted_text[includes_type] in s for s in t1):
                        t3.append(tuple([splitted_text[i], 'PartOf', splitted_text[includes_type]]))


    return t3

#print(relatii(['floare', 'petala', 'copac'], ['plantă', 'floare', 'vietate'], 'floare este un tip de plantă, petala face parte din floare'))