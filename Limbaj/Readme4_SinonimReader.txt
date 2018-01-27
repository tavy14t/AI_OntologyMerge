Pentru sinonim reader
*Scris in Python 2.7
*Are nevoie de conexiune la internet altfel returneaza lista goala
*are nevoie de urmatoarele pachete:
 import urllib2
 import BeautifulSoup
 import re
 import unicodedata

Exemple:
 print get_sinonims('stilou',2)// returneaza: [toc,rezervor]
 print get_sinonims('briceag',2) //returneaza o lista de 2 sinonime
 print get_sinonims('roca',1)//returneaza o loista de un sinonim
 print get_sinonims('roca',10)//teoretic ar returna 10 sinonime dar returneaza cat de multe gaseste

Mentiuni:
 get_sinonims(cuvant,cat_de_multe_sinonime_vrei)
 pt numere mari returneaza toate sinonimele gasite
 dar nu este recomandat, de obicei prinele 2-3 sinonime sunt cele mai bune
 restul sunt sinonime obscure sau cate odata au doar un fel de legatura cu cuvantul tau
 programul returneaza lista goala daca nu are conexiune la net sau daca pur si simplu siteul
 https://dexonline.net/sinonime-stilou nu are sinonim pt el
 daca nr de sinonime e 0 sau mai mic din nou lista goala