import os
import sys
import fileinput
from mtranslate import translate

print("Fisierul pentru traducere: \n")
fromFile = input()
print("Noul fisier tradus: \n")
toFile = input()

def mapfunc(line: str) -> str:
    if line.startswith('name: '):
        return ''.join(('name: ', translate(line.partition(' ')[2],'ro','en').replace('ă','a').replace('â','a').replace('î','i').replace('ț','t').replace('ș','s'),'\n'))
    elif line.startswith('synonym: '):
        return ''.join(('synonym: ', translate(line.partition(' ')[2],'ro','en').replace('ă','a').replace('â','a').replace('î','i').replace('ț','t').replace('ș','s'),'\n'))
    elif line.startswith('def: '):
        return ''.join(('def: ', translate(line.partition(' ')[2],'ro','en').replace('ă','a').replace('â','a').replace('î','i').replace('ț','t').replace('ș','s'),'\n'))
    else:
        return line

with open(fromFile,'r') as inf, open (toFile,'w+') as outf:
    outf.write(''.join(map(mapfunc, inf.readlines())))
